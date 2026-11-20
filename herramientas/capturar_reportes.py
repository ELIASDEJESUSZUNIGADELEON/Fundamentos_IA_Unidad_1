"""Capturas PNG reales de los reportes HTML mediante Chrome en modo headless."""
import argparse
import subprocess
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(); p.add_argument("--solo",nargs="*"); args=p.parse_args()
    chrome=next((x for x in [Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")] if x.exists()),None)
    if not chrome: raise RuntimeError("Se necesita Chrome o Edge para generar capturas.")
    perfil=ROOT.parent/".herramientas-u1/perfil-chrome"
    for html in sorted((ROOT/"evidencias").glob("*.html")):
        if args.solo and html.stem not in args.solo: continue
        texto=html.read_text(encoding="utf-8")
        altura=1300 if html.stem=="00-indice" else min(4200,1100+texto.count("<figure>")*620+(1200 if html.stem=="07-crewai" else 0))
        png=html.with_suffix(".png")
        comando=[str(chrome),"--headless=new","--disable-gpu","--no-first-run","--no-default-browser-check","--hide-scrollbars",f"--user-data-dir={perfil}",f"--window-size=1400,{altura}","--force-device-scale-factor=1",f"--screenshot={png}",html.as_uri()]
        proceso=subprocess.run(comando,capture_output=True,timeout=60)
        if proceso.returncode or not png.exists(): raise RuntimeError(proceso.stderr.decode(errors="replace"))
        # Se conserva la captura completa del navegador, sin modificar la imagen.
        with Image.open(png) as img:
            assert img.width==1400 and img.height>=1000
        print(png.relative_to(ROOT),flush=True)


if __name__=="__main__": main()
