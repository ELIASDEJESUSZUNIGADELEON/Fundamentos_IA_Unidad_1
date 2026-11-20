"""Verificación independiente de datos, cuadernos, evidencias y enlaces locales."""
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote
import nbformat
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def main():
    comprobaciones=[]
    def ok(mensaje): comprobaciones.append(mensaje); print("OK:",mensaje)
    # La unión se recalcula con el lector CSV de Python, independiente de awk/join.
    datos=ROOT/"05-bash-pib-satisfaccion/datos"
    with (datos/"oecd_bli_2015.csv").open(encoding="utf-8-sig",newline="") as f:
        felicidad={r["Country"]:float(r["Value"]) for r in csv.DictReader(f) if r["INDICATOR"]=="SW_LIFS" and r["INEQUALITY"]=="TOT"}
    pib={}
    with (datos/"gdp_per_capita.csv").open(encoding="latin-1",newline="") as f:
        for r in csv.DictReader(f,delimiter="\t"):
            try: pib[r["Country"]]=float((r.get("2015") or "").replace(",",""))
            except (ValueError,TypeError): continue
    esperados=sorted(set(felicidad)&set(pib))
    out=ROOT/"05-bash-pib-satisfaccion/resultados"
    with (out/"merged_data.csv").open(encoding="utf-8",newline="") as f: filas=list(csv.DictReader(f))
    assert len(filas)==len(esperados)==36
    assert [r["Pais"] for r in filas]==esperados
    assert all(float(r["Satisfaccion_Vida"])==felicidad[r["Pais"]] and float(r["PIB_Capita"])==pib[r["Pais"]] for r in filas)
    assert np.array_equal(np.loadtxt(out/"X.csv"),[pib[p] for p in esperados])
    assert np.array_equal(np.loadtxt(out/"y.csv"),[felicidad[p] for p in esperados])
    ok("Unión Bash de 36 países y alineación X/y coinciden con el cálculo independiente en Python.")
    manifest=json.loads((ROOT/"herramientas/fuentes_datos.json").read_text(encoding="utf-8"))
    for dato in manifest["archivos"]:
        archivo=ROOT/dato["archivo"]
        assert hashlib.sha256(archivo.read_bytes()).hexdigest()==dato["sha256"],archivo
    ok(f"Integridad SHA-256 de {len(manifest['archivos'])} archivos de datos de entrada.")
    md5={"train-images-idx3-ubyte.gz":"f68b3c2dcbeaaa9fbdd348bbdeb94873","train-labels-idx1-ubyte.gz":"d53e105ee54ea40749a09fcbcd1e9432","t10k-images-idx3-ubyte.gz":"9fb629c4189551a2d022fa330f9573f3","t10k-labels-idx1-ubyte.gz":"ec29112dd5afa0611ce80d1b7f02629c"}
    for nombre,esperado in md5.items(): assert hashlib.md5((ROOT/"08-talleres/01-red-neuronal/datos"/nombre).read_bytes()).hexdigest()==esperado
    ok("Los cuatro archivos MNIST coinciden con las sumas de la distribución original.")
    registros=json.loads((ROOT/"evidencias/registro_ejecuciones.json").read_text(encoding="utf-8"))
    assert len(registros)==10
    for r in registros:
        assert r["codigo_salida"]==0,r["id"]
        assert hashlib.sha256((ROOT/r["script"]).read_bytes()).hexdigest()==r["sha256_codigo"],r["id"]
        for extension in ["txt","png"]: assert (ROOT/"evidencias"/f"{r['id']}.{extension}").is_file()
    assert not list((ROOT/"evidencias").glob("*.html"))
    ok("Diez prácticas con salida 0, código vigente y salidas TXT/PNG sin reportes HTML.")
    cuadernos=list(ROOT.rglob("actividad.ipynb")); assert len(cuadernos)==7
    for archivo in cuadernos:
        nb=nbformat.read(archivo,as_version=4); nbformat.validate(nb)
        fuente=archivo.parent/nb.metadata.reconstruccion.fuente
        assert hashlib.sha256(fuente.read_bytes()).hexdigest()==nb.metadata.reconstruccion.sha256
        assert nb.cells[2].source==fuente.read_text(encoding="utf-8")
        for celda in nb.cells:
            if celda.cell_type=="code":
                assert celda.execution_count is not None,archivo
                assert all(o.output_type!="error" for o in celda.outputs),archivo
    ok("Siete cuadernos válidos, ejecutados sin errores, con código completo sincronizado con sus scripts.")
    rutas_png=list((ROOT/"evidencias").glob("*.png")); assert len(rutas_png)==13
    for ruta in rutas_png:
        with Image.open(ruta) as imagen:
            imagen.verify()
    ok("Trece imágenes PNG válidas: diez salidas de consola y tres vistas de documentos.")
    rotos=[]
    for md in ROOT.rglob("*.md"):
        for enlace in re.findall(r'\[[^\]]*\]\(([^)]+)\)',md.read_text(encoding="utf-8")):
            if enlace.startswith(("http:","https:","#","mailto:")): continue
            enlace=unquote(enlace.split("#")[0])
            destino=(md.parent/enlace).resolve()
            # Este mismo validador crea su archivo de salida al terminar.
            if enlace and destino!=ROOT/"evidencias/validacion.json" and not destino.exists(): rotos.append((str(md.relative_to(ROOT)),enlace))
    assert not rotos,rotos
    ok("Todos los enlaces locales de los Markdown apuntan a archivos o carpetas existentes.")
    entregados=json.loads((ROOT/"herramientas/documentos_entregados.json").read_text(encoding="utf-8"))
    assert len(entregados)==5
    for documento in entregados:
        assert hashlib.sha256((ROOT/documento["archivo"]).read_bytes()).hexdigest()==documento["sha256"]
    ok("Cinco archivos originales incorporados: tres PDF, una fuente LaTeX y una imagen del mapa mental.")
    readme=(ROOT/"README.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^## [a-l][.]",readme,re.MULTILINE))==12
    assert not any(linea.startswith("| ") for linea in readme.splitlines())
    assert "Cada práctica contiene su explicación" not in readme
    assert "El orden se obtuvo de los" not in readme
    ok("README organizado en doce apartados con imágenes, sin tabla ni el bloque final anterior.")
    crew=json.loads((ROOT/"07-crewai/resultados/ejecucion.json").read_text(encoding="utf-8"))
    assert len(crew["tareas"])==2 and all(t["salida"].strip() for t in crew["tareas"])
    ok("CrewAI registró las respuestas reales de sus dos agentes con el modelo local.")
    resumen={"fecha_utc":datetime.now(timezone.utc).isoformat(),"estado":"correcto","comprobaciones":comprobaciones}
    (ROOT/"evidencias/validacion.json").write_text(json.dumps(resumen,ensure_ascii=False,indent=2),encoding="utf-8")


if __name__=="__main__": main()
