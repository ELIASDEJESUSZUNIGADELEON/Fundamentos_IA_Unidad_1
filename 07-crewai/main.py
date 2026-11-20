"""Dos agentes reales con Ollama: análisis de fuentes curadas y redacción."""
import hashlib
import importlib.metadata
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# La práctica usa solo un modelo local y no necesita telemetría ni credenciales.
os.environ["OTEL_SDK_DISABLED"]="true"
os.environ["CREWAI_TELEMETRY_DISABLED"]="true"
os.environ["CREWAI_TRACING_ENABLED"]="false"
os.environ["LITELLM_LOCAL_MODEL_COST_MAP"]="true"
from crewai import Agent, Crew, LLM, Process, Task

HERE=Path(__file__).parent.resolve()


def main():
    from dotenv import load_dotenv
    load_dotenv(HERE/".env",override=False)
    base=os.getenv("OLLAMA_BASE_URL","http://127.0.0.1:11435")
    modelo=os.getenv("OLLAMA_MODEL","qwen2.5:1.5b")
    with urllib.request.urlopen(base+"/api/tags",timeout=10) as f: disponibles=json.load(f)
    if modelo not in [m["name"] for m in disponibles["models"]]:
        raise RuntimeError(f"Falta el modelo {modelo}. Ejecuta herramientas/preparar_modelo.py.")
    out=HERE/"resultados"; out.mkdir(exist_ok=True)
    fuentes=json.loads((HERE/"fuentes.json").read_text(encoding="utf-8"))
    dossier="\n".join(f"[{i}] {s['titulo']} — {s['url']}\n{s['nota']}" for i,s in enumerate(fuentes,1))
    llm=LLM(model="ollama/"+modelo,base_url=base,temperature=.1,max_tokens=1000,timeout=900,seed=2430085,context_window_size=8192)
    investigador=Agent(role="Analista de fuentes de IA",goal="Explicar con precisión cómo cooperan dos agentes con un modelo local.",
        backstory="Trabajas únicamente con el dossier de documentación oficial que recibes. Distingues hechos y límites.",llm=llm,allow_delegation=False,verbose=False,max_iter=2)
    redactor=Agent(role="Redactor académico",goal="Redactar un informe breve en español a partir del análisis y las fuentes.",
        backstory="Escribes para una práctica de Fundamentos de IA. No inventas resultados experimentales, citas ni prestaciones.",llm=llm,allow_delegation=False,verbose=False,max_iter=2)
    analisis=Task(description="Analiza estas fuentes curadas. Explica rol, tarea, proceso secuencial, contexto y ejecución local. No hagas búsquedas ni inventes fuentes. Cita [1], [2] y [3]. Máximo 220 palabras, todo en español.\n"+dossier,
        expected_output="Un análisis en español con hechos respaldados por las tres fuentes, y dos limitaciones.",agent=investigador,output_file=str(out/"analisis.md"))
    redaccion=Task(description="Redacta el informe 'Agentes colaborativos con CrewAI y Ollama'. Usa el análisis previo. Incluye objetivo, funcionamiento de dos agentes en secuencia, ventajas, límites y conclusión. Máximo 320 palabras en español; conserva las referencias [1], [2], [3]. No afirmes haber hecho búsquedas web: las fuentes fueron seleccionadas previamente. No inventes benchmarks.\nFuentes:\n"+dossier,
        expected_output="Informe académico breve en Markdown y en español con referencias a las tres fuentes proporcionadas.",agent=redactor,context=[analisis],output_file=str(out/"informe.md"))
    equipo=Crew(agents=[investigador,redactor],tasks=[analisis,redaccion],process=Process.sequential,verbose=False,memory=False)
    print(f"CrewAI {importlib.metadata.version('crewai')} | Ollama {modelo} | {base}",flush=True)
    print("Dos agentes, dos tareas reales, proceso secuencial, tres fuentes oficiales curadas.",flush=True)
    comienzo=time.perf_counter(); resultado=equipo.kickoff()
    tareas=[]
    for t in resultado.tasks_output:
        tareas.append({"agente":t.agent,"descripcion":t.description,"salida":t.raw})
    if len(tareas)!=2 or any(not t["salida"].strip() for t in tareas): raise RuntimeError("No se completaron ambas tareas.")
    # La bibliografía se conserva como dato de entrada, sin alterar las respuestas.
    bibliografia="\n\n## Fuentes proporcionadas\n"+"\n".join(f"{i}. [{s['titulo']}]({s['url']})" for i,s in enumerate(fuentes,1))
    (out/"informe.md").write_text(resultado.raw+bibliografia+"\n",encoding="utf-8")
    tokens=resultado.token_usage.model_dump() if resultado.token_usage else {}
    meta={"fecha_utc":datetime.now(timezone.utc).isoformat(),"modelo":modelo,"crewai":importlib.metadata.version("crewai"),"segundos":time.perf_counter()-comienzo,"proceso":"sequential","fuentes":"curadas, sin búsqueda automática","sha256_fuentes":hashlib.sha256((HERE/"fuentes.json").read_bytes()).hexdigest(),"tokens":tokens,"tareas":tareas}
    (out/"ejecucion.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
    print(f"Tareas completadas: {len(tareas)}; duración: {meta['segundos']:.1f} s",flush=True)
    print(f"Tokens registrados por CrewAI: {tokens}",flush=True)
    print("Informe: resultados/informe.md",flush=True)
    print(resultado.raw,flush=True)


if __name__=="__main__": main()
