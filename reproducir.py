"""Ejecuta las prácticas y conserva logs, estado, huellas de código y reportes HTML."""
import argparse
import hashlib
import html
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).parent.resolve()
EVIDENCIAS=ROOT/"evidencias"
ACTIVIDADES=[
    ("01-entorno","Configuración del entorno","01-configuracion-entorno/verificar_entorno.py",[]),
    ("04-clientes","Bash: limpieza de clientes","04-bash-limpieza-clientes/limpiar.sh",[]),
    ("05-pib","Bash: PIB y satisfacción","05-bash-pib-satisfaccion/preparar.sh",[]),
    ("06-logica","Lógica proposicional e inferencia","06-logica-proposicional/logica.py",[]),
    ("08-1-red-neuronal","Red neuronal NumPy y MNIST","08-talleres/01-red-neuronal/red_mnist.py",["curvas.png","predicciones.png"]),
    ("08-2-difusa","Lógica difusa: propina","08-talleres/02-logica-difusa/propina.py",["inferencia.png"]),
    ("08-3-nlp","Procesamiento de lenguaje natural","08-talleres/03-nlp/sentimientos.py",["sentimientos.png"]),
    ("08-4-evolutivos","Algoritmo genético: laberinto","08-talleres/04-algoritmos-evolutivos/laberinto.py",["laberinto.png"]),
    ("08-5-vision","Visión por computadora","08-talleres/05-vision-computadora/clasificar_frutas.py",["predicciones.png"]),
    ("07-crewai","CrewAI con modelo local","07-crewai/main.py",[]),
]
CSS="""*{box-sizing:border-box}body{margin:0;padding:44px;background:#f2f5f9;color:#182638;font:18px 'Segoe UI',sans-serif}main{max-width:1280px;margin:auto}h1{font-size:34px;margin:10px 0}h2{font-size:22px}header{border-left:7px solid #297568;padding-left:24px;margin-bottom:24px}p{line-height:1.5}.meta{color:#526171;font-size:15px}pre{background:#172638;color:#e5edf6;padding:24px;border-radius:9px;white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.5 Consolas,monospace}figure{margin:22px 0;padding:16px;background:white;border:1px solid #dbe2e9;border-radius:9px}img{display:block;width:100%;max-height:570px;object-fit:contain}figcaption{padding:10px;font-size:15px;color:#526171}table{width:100%;border-collapse:collapse;background:white;font-size:17px}td,th{text-align:left;padding:13px;border-bottom:1px solid #dce4ed}th{background:#172638;color:white}.ok{color:#15664b}.pending{color:#885c12}a{color:#135ea2}.tag{font-size:15px;letter-spacing:2px;color:#297568;font-weight:bold}"""


def guardar_reporte(registro,imagenes):
    slug=registro["id"]; estado="EJECUTADO" if registro["codigo_salida"]==0 else "ERROR"
    log=registro["salida"]
    # El log completo siempre se conserva; la captura resume ejecuciones verbosas.
    lineas=log.splitlines()
    muestra="\n".join(lineas if len(lineas)<=35 else lineas[:12]+["... salida intermedia en el archivo TXT ..."]+lineas[-20:])
    partes=[f'<span class="tag">UNIDAD 1 / EVIDENCIA DE EJECUCIÓN</span><header><h1>{html.escape(registro["titulo"])}</h1><p>Elias de Jesus Zuñiga de Leon · Matrícula 2430085</p></header>',
            f'<p class="meta">{html.escape(registro["inicio"])} · {registro["segundos"]:.2f} s · {estado} · código de salida {registro["codigo_salida"]}</p>',
            f'<p><b>Comando ejecutado</b></p><pre>{html.escape(registro["comando_legible"])}</pre>',
            f'<h2>Salida de la ejecución</h2><pre>{html.escape(muestra)}</pre>',
            f'<p class="meta">Salida completa: <a href="{slug}.txt">{slug}.txt</a> · SHA-256 del código: {registro["sha256_codigo"][:20]}…</p>']
    for archivo in imagenes:
        rel=os.path.relpath(archivo,EVIDENCIAS).replace("\\","/")
        partes.append(f'<figure><img src="{html.escape(rel)}"><figcaption>{html.escape(archivo.name)} · archivo generado por la práctica</figcaption></figure>')
    if slug=="07-crewai":
        informe=ROOT/"07-crewai/resultados/informe.md"
        if informe.exists(): partes.append('<p><a href="../07-crewai/resultados/informe.md">Abrir el informe Markdown con su bibliografía</a></p>')
    partes.append('<p class="meta">Captura del reporte HTML construido a partir de la ejecución real. Consulta el código, el TXT y registro_ejecuciones.json para reproducirla.</p>')
    documento=f'<!doctype html><html lang="es"><meta charset="utf-8"><title>{html.escape(registro["titulo"])}</title><style>{CSS}</style><main>'+"".join(partes)+"</main></html>"
    (EVIDENCIAS/f"{slug}.html").write_text(documento,encoding="utf-8")


def indice(registros):
    mapa={r["id"]:r for r in registros}
    filas=[]
    orden=[("01","Configuración del entorno","01-entorno"),("02","Historia y fundamentos de la IA",None),("03","Mapa mental de agentes inteligentes",None),("04","Bash: limpieza de clientes","04-clientes"),("05","Bash: PIB y satisfacción","05-pib"),("06","Lógica proposicional","06-logica"),("07","CrewAI: investigación y redacción","07-crewai"),("08.1","Red neuronal MNIST","08-1-red-neuronal"),("08.2","Lógica difusa","08-2-difusa"),("08.3","Procesamiento de lenguaje natural","08-3-nlp"),("08.4","Algoritmos evolutivos","08-4-evolutivos"),("08.5","Visión por computadora","08-5-vision")]
    for numero,nombre,slug in orden:
        r=mapa.get(slug); estado="PDF pendiente" if slug is None else "Ejecutado" if r and r["codigo_salida"]==0 else "Pendiente de ejecución" if r is None else "Revisar error"
        enlace=f'<a href="{slug}.html">Ver reporte</a>' if r else "Agregar documento" if slug is None else "—"
        filas.append(f'<tr><td>{numero}</td><td>{nombre}</td><td class="{"ok" if estado=="Ejecutado" else "pending"}">{estado}</td><td>{enlace}</td></tr>')
    n=sum(r["codigo_salida"]==0 for r in registros)
    doc=f'<!doctype html><html lang="es"><meta charset="utf-8"><title>Índice de actividades · Unidad 1</title><style>{CSS}</style><main><span class="tag">FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL</span><header><h1>Unidad 1 · Orden de actividades</h1><p>Elias de Jesus Zuñiga de Leon · Matrícula 2430085</p></header><p>{n} prácticas ejecutadas · 2 secciones documentales para completar con tus PDF</p><table><thead><tr><th>Orden</th><th>Actividad</th><th>Estado</th><th>Evidencia</th></tr></thead><tbody>'+"".join(filas)+'</tbody></table><p class="meta">Orden de reconstrucción basado en los dos repositorios de referencia. No equivale a una rúbrica oficial del profesor. Las imágenes son capturas de reportes de ejecución propios.</p></main></html>'
    (EVIDENCIAS/"00-indice.html").write_text(doc,encoding="utf-8")


def main():
    p=argparse.ArgumentParser(); p.add_argument("--solo",nargs="*"); p.add_argument("--incluir-crewai",action="store_true"); args=p.parse_args()
    EVIDENCIAS.mkdir(exist_ok=True)
    ruta=EVIDENCIAS/"registro_ejecuciones.json"
    previos=json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else []
    registros={r["id"]:r for r in previos}
    env=os.environ.copy(); env.update(PYTHONUTF8="1",PYTHONIOENCODING="utf-8",MPLBACKEND="Agg",OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
    for slug,titulo,script,figuras in ACTIVIDADES:
        if args.solo and slug not in args.solo: continue
        if slug=="07-crewai" and not args.incluir_crewai: continue
        archivo=ROOT/script
        if script.endswith(".sh"):
            bash=shutil.which("bash") or r"C:\Program Files\Git\bin\bash.exe"
            comando=[bash,archivo.name]
        else:
            python=ROOT.parent/".venv-crewai/Scripts/python.exe" if slug=="07-crewai" else Path(sys.executable)
            comando=[str(python),archivo.name]
        inicio=datetime.now(ZoneInfo("America/Mexico_City")); print(f"Ejecutando {slug}...",flush=True)
        proceso=subprocess.run(comando,cwd=archivo.parent,env=env,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1800)
        log=proceso.stdout+("\nSTDERR:\n"+proceso.stderr if proceso.stderr else "")
        registro={"id":slug,"titulo":titulo,"script":script,"inicio":inicio.isoformat(),"segundos":(datetime.now(ZoneInfo("America/Mexico_City"))-inicio).total_seconds(),"codigo_salida":proceso.returncode,"comando_legible":("bash " if script.endswith(".sh") else "python ")+script,"comando_real":comando,"sha256_codigo":hashlib.sha256(archivo.read_bytes()).hexdigest(),"salida":log}
        registros[slug]=registro
        (EVIDENCIAS/f"{slug}.txt").write_text(log,encoding="utf-8")
        guardar_reporte(registro,[archivo.parent/"resultados"/f for f in figuras if (archivo.parent/"resultados"/f).exists()])
        ruta.write_text(json.dumps(list(registros.values()),ensure_ascii=False,indent=2),encoding="utf-8")
        print(log,flush=True)
        print(f"Código de salida: {proceso.returncode}",flush=True)
    indice(list(registros.values()))
    if any(r["codigo_salida"]!=0 for r in registros.values()): raise SystemExit(1)


if __name__=="__main__": main()
