"""Ejecuta las prácticas y conserva sus salidas de consola y registros."""
import argparse
import hashlib
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
        ruta.write_text(json.dumps(list(registros.values()),ensure_ascii=False,indent=2),encoding="utf-8")
        print(log,flush=True)
        print(f"Código de salida: {proceso.returncode}",flush=True)
    if any(r["codigo_salida"]!=0 for r in registros.values()): raise SystemExit(1)


if __name__=="__main__": main()
