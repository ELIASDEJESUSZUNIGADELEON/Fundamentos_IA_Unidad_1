"""Crea cuadernos con el código completo y los ejecuta con el Python actual."""
import hashlib
import os
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT=Path(__file__).resolve().parents[1]
PRACTICAS=[
    ("01-configuracion-entorno/verificar_entorno.py","Verificación del entorno",[]),
    ("06-logica-proposicional/logica.py","Lógica proposicional e inferencia",[]),
    ("08-talleres/01-red-neuronal/red_mnist.py","MLP NumPy y MNIST",["curvas.png","predicciones.png"]),
    ("08-talleres/02-logica-difusa/propina.py","Lógica difusa y propina",["inferencia.png"]),
    ("08-talleres/03-nlp/sentimientos.py","Análisis de sentimientos",["sentimientos.png"]),
    ("08-talleres/04-algoritmos-evolutivos/laberinto.py","Algoritmo genético y laberinto",["laberinto.png"]),
    ("08-talleres/05-vision-computadora/clasificar_frutas.py","Visión por computadora",["predicciones.png"]),
]


def main():
    env=os.environ.copy(); env.update(PYTHONUTF8="1",PYTHONIOENCODING="utf-8",MPLBACKEND="Agg",OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
    for relativo,titulo,imagenes in PRACTICAS:
        archivo=ROOT/relativo; codigo=archivo.read_text(encoding="utf-8")
        intro=f"# {titulo}\n\nElias de Jesus Zuñiga de Leon · Matrícula 2430085\n\nEste cuaderno contiene una copia completa de `{archivo.name}` y sus salidas reales. Ejecuta todas las celdas en orden, desde esta carpeta. La explicación y el análisis están en [README.md](README.md). Los archivos de entrada están en `datos/` cuando corresponda.\n\nEl código fuente principal se conserva en el archivo `.py`; `herramientas/generar_cuadernos.py` regenera y ejecuta este cuaderno después de cambiarlo."
        preparacion=f'import os, sys\nfrom pathlib import Path\nos.environ["MPLBACKEND"] = "Agg"\nos.environ["OPENBLAS_NUM_THREADS"] = "1"\n# Las rutas y argumentos equivalen a ejecutar el script desde esta carpeta.\n__file__ = str(Path.cwd() / {archivo.name!r})\nsys.argv = [__file__]'
        celdas=[nbformat.v4.new_markdown_cell(intro),nbformat.v4.new_code_cell(preparacion),nbformat.v4.new_code_cell(codigo)]
        if imagenes:
            celdas.append(nbformat.v4.new_markdown_cell("## Imágenes producidas por esta ejecución"))
            celdas.append(nbformat.v4.new_code_cell("from IPython.display import display, Image\n"+"\n".join(f"display(Image(filename='resultados/{im}'))" for im in imagenes)))
        nb=nbformat.v4.new_notebook(cells=celdas,metadata={"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":sys.version.split()[0]},"reconstruccion":{"fuente":archivo.name,"sha256":hashlib.sha256(archivo.read_bytes()).hexdigest(),"ejecutado":True}})
        km=KernelManager(kernel_name="python3")
        km.kernel_spec.argv=[sys.executable,"-m","ipykernel_launcher","-f","{connection_file}"]
        cliente=NotebookClient(nb,km=km,timeout=1200,allow_errors=False,resources={"metadata":{"path":str(archivo.parent)}})
        print("Ejecutando cuaderno:",relativo,flush=True)
        try:
            cliente.execute(cwd=str(archivo.parent),env=env)
        finally:
            if km.has_kernel: km.shutdown_kernel(now=True)
        nbformat.validate(nb)
        nbformat.write(nb,archivo.parent/"actividad.ipynb")
        print("Guardado:",archivo.parent/"actividad.ipynb",flush=True)


if __name__=="__main__": main()
