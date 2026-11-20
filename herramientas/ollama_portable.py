"""Extrae la versión oficial para CPU sin descargar las bibliotecas de GPU.

Se usa acceso HTTP por rangos al ZIP oficial. No modifica PATH ni instala servicios.
"""
import argparse
import io
import json
import urllib.request
import zipfile
from pathlib import Path

URL = "https://github.com/ollama/ollama/releases/download/v0.40.16/ollama-windows-amd64.zip"
SIZE = 1618244995
ROOT = Path(__file__).resolve().parents[2] / ".herramientas-u1" / "ollama"


class ArchivoHTTP(io.RawIOBase):
    def __init__(self):
        self.pos = 0
        self.url = URL

    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence==0 else self.pos+offset if whence==1 else SIZE+offset
        return self.pos

    def read(self, n=-1):
        if self.pos >= SIZE: return b""
        end=SIZE-1 if n<0 else min(SIZE-1,self.pos+n-1)
        if end<self.pos: return b""
        req=urllib.request.Request(self.url, headers={"Range":f"bytes={self.pos}-{end}","User-Agent":"Unidad1-Ollama-portable"})
        with urllib.request.urlopen(req,timeout=120) as r:
            if r.status!=206:
                raise RuntimeError("El servidor no admite rangos; se evitó descargar el ZIP completo.")
            self.url=r.url
            data=r.read()
        if len(data)!=end-self.pos+1: raise RuntimeError("Rango incompleto")
        self.pos+=len(data)
        return data


def main():
    p=argparse.ArgumentParser(); p.add_argument("--extraer", action="store_true"); args=p.parse_args()
    with zipfile.ZipFile(ArchivoHTTP()) as z:
        for item in z.infolist(): print(f"{item.filename} ({item.file_size})", flush=True)
        if not args.extraer: return
        ROOT.mkdir(parents=True,exist_ok=True)
        registros=[]
        for item in z.infolist():
            name=item.filename.replace("\\","/")
            # El paquete principal tiene CPU en lib/ollama y GPU en subdirectorios.
            incluir=name=="ollama.exe" or (name.startswith("lib/ollama/") and name.count("/")==2 and name.endswith((".dll",".exe")))
            if not incluir or item.is_dir(): continue
            dest=(ROOT/name).resolve()
            if not dest.is_relative_to(ROOT.resolve()): raise ValueError("Ruta fuera del destino")
            dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():
                dest.write_bytes(z.read(item))
            print("Extraído:",name,flush=True)
            registros.append(name)
        (ROOT/"origen.json").write_text(json.dumps({"url":URL,"version":"0.40.16","archivos":registros},indent=2),encoding="utf-8")


if __name__=="__main__": main()
