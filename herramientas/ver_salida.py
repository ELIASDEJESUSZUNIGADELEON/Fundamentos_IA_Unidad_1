"""Muestra los registros de salida en una ventana de texto sencilla.

No ejecuta órdenes ni simula una sesión de PowerShell. Lee los TXT guardados
por reproducir.py. Se puede hacer una captura de esta ventana con el sistema.
"""
import argparse
import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--actividad",default="01-entorno")
    p.add_argument("--lineas",type=int,help="Mostrar solo el inicio de una salida extensa.")
    p.add_argument("--seleccion",type=Path)
    args=p.parse_args()
    registros=json.loads((ROOT/"evidencias/registro_ejecuciones.json").read_text(encoding="utf-8"))
    mapa={r["id"]:r for r in registros}
    ventana=tk.Tk(); ventana.title("Salida de ejecución")
    ventana.configure(bg="#0c0c0c")
    marco=ttk.Frame(ventana); marco.pack(fill="both",expand=True)
    texto=tk.Text(marco,bg="#0c0c0c",fg="#eeeeee",insertbackground="white",font=("Consolas",12),wrap="word",borderwidth=0,highlightthickness=0,padx=14,pady=12)
    barra=ttk.Scrollbar(marco,orient="vertical",command=texto.yview)
    texto.configure(yscrollcommand=barra.set)
    barra.pack(side="right",fill="y"); texto.pack(side="left",fill="both",expand=True)
    actual=None

    def cargar(slug):
        nonlocal actual
        if slug not in mapa or slug==actual: return
        registro=mapa[slug]
        salida=(ROOT/"evidencias"/f"{slug}.txt").read_text(encoding="utf-8")
        if args.lineas:
            salida="\n".join(salida.splitlines()[:args.lineas])
        contenido=registro["comando_legible"]+"\n\n"+salida
        lineas=sum(max(1,(len(linea)+119)//120) for linea in contenido.splitlines())
        alto=min(ventana.winfo_screenheight()-100,max(300,lineas*21+66))
        ventana.geometry(f"1220x{alto}+35+35")
        ventana.title("Salida de ejecución - "+Path(registro["script"]).name+(" (resumen)" if args.lineas else ""))
        texto.configure(state="normal"); texto.delete("1.0","end"); texto.insert("1.0",contenido)
        texto.configure(state="disabled"); texto.yview_moveto(0)
        actual=slug

    def revisar():
        slug=args.actividad
        if args.seleccion and args.seleccion.exists():
            slug=args.seleccion.read_text(encoding="utf-8").strip()
        cargar(slug)
        ventana.after(200,revisar)

    revisar(); ventana.mainloop()


if __name__=="__main__": main()
