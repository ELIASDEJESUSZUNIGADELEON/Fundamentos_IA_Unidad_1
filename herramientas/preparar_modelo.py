"""Descarga el modelo en el servidor Ollama local ya iniciado."""
import json
import urllib.request


def main():
    req=urllib.request.Request("http://127.0.0.1:11435/api/pull",data=json.dumps({"model":"qwen2.5:1.5b","stream":True}).encode(),headers={"Content-Type":"application/json"})
    ultimo=-1
    with urllib.request.urlopen(req,timeout=1800) as f:
        for linea in f:
            r=json.loads(linea)
            if "error" in r: raise RuntimeError(r["error"])
            total=r.get("total",0)
            if total:
                avance=int(100*r.get("completed",0)/total)//10*10
                if avance!=ultimo: print(f"{r['status']}: {avance}%",flush=True); ultimo=avance
            else: print(r["status"],flush=True)


if __name__=="__main__": main()
