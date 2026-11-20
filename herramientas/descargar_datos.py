"""Descarga únicamente datos de entrada; nunca trabajos o resultados de alumnos."""
import argparse
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def descargar(url, destino):
    destino = ROOT / destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        with urllib.request.urlopen(url, timeout=90) as respuesta:
            contenido = respuesta.read()
        temporal = destino.with_suffix(destino.suffix + ".part")
        temporal.write_bytes(contenido)
        temporal.replace(destino)
    contenido = destino.read_bytes()
    print(f"{destino.relative_to(ROOT)}: {len(contenido)} bytes", flush=True)
    return {"archivo":destino.relative_to(ROOT).as_posix(), "url":url,
            "sha256":hashlib.sha256(contenido).hexdigest(), "bytes":len(contenido)}


def main():
    p=argparse.ArgumentParser(); p.add_argument("--vision", action="store_true"); args=p.parse_args()
    registros=[]
    base="https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/lifesat/"
    for nombre in ["oecd_bli_2015.csv", "gdp_per_capita.csv"]:
        registros.append(descargar(base+nombre, "05-bash-pib-satisfaccion/datos/"+nombre))
    for nombre in ["train-images-idx3-ubyte.gz","train-labels-idx1-ubyte.gz","t10k-images-idx3-ubyte.gz","t10k-labels-idx1-ubyte.gz"]:
        registros.append(descargar("https://ossci-datasets.s3.amazonaws.com/mnist/"+nombre,
                                  "08-talleres/01-red-neuronal/datos/"+nombre))
    if args.vision:
        # Fotos de entrada del taller compartido; se atribuyen en REFERENCIAS.md.
        repo="cesar-upv/2430233_FUNDAMENTOS_IA_UNIDAD_1"
        ref="99c30b7430857cf2e2ca67de810895a1a75ab336"
        url=f"https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1"
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"Unidad1-reconstruccion"}), timeout=60) as f:
            tree=json.load(f)["tree"]
        prefijo="06-talleres/vision-por-computadora/assets-taller/"
        for item in tree:
            if item["type"]=="blob" and item["path"].startswith(prefijo):
                relativo=item["path"][len(prefijo):]
                remoto=f"https://raw.githubusercontent.com/{repo}/{ref}/"+urllib.parse.quote(item["path"])
                registros.append(descargar(remoto,"08-talleres/05-vision-computadora/datos/"+relativo))
    destino=ROOT/"herramientas/fuentes_datos.json"
    anteriores=json.loads(destino.read_text(encoding="utf-8"))["archivos"] if destino.exists() else []
    por_archivo={r["archivo"]:r for r in anteriores+registros}
    destino.write_text(json.dumps({"verificado_utc":datetime.now(timezone.utc).isoformat(),"archivos":list(por_archivo.values())},ensure_ascii=False,indent=2),encoding="utf-8")


if __name__=="__main__": main()
