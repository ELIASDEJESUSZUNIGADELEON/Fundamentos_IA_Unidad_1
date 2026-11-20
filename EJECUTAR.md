# Cómo ejecutar la unidad 1

Abre PowerShell en `C:\Users\elias\Downloads\Said - github`.

## Entorno que quedó preparado en este equipo

Las prácticas usan Python 3.14 en `.venv-u1/`. CrewAI usa Python 3.12 en `.venv-crewai/`, por sus requisitos de compatibilidad. Ambos entornos están junto a la carpeta de la unidad y no se deben subir a GitHub.

```powershell
# Todas las prácticas salvo CrewAI
.\.venv-u1\Scripts\python.exe .\Fundamentos_IA_Unidad_1\reproducir.py

# Solo una actividad (ejemplo)
.\.venv-u1\Scripts\python.exe .\Fundamentos_IA_Unidad_1\reproducir.py --solo 06-logica

# Abrir los cuadernos
.\.venv-u1\Scripts\python.exe -m notebook .\Fundamentos_IA_Unidad_1

# Actualizar las capturas después de ejecutar
.\.venv-u1\Scripts\python.exe .\Fundamentos_IA_Unidad_1\herramientas\capturar_reportes.py
```

Los dos scripts `.sh` necesitan Git Bash y GNU Awk 5.3 o posterior (`gawk --csv`), además de `sort`, `join` e `iconv`. Este equipo tiene GNU Awk 5.4.1.

## CrewAI local

Ollama portátil está en `.herramientas-u1/ollama/` y los pesos del modelo en `.herramientas-u1/modelos/`, junto a la carpeta de la unidad. No se agregó Ollama al PATH del sistema. Usa el puerto local `127.0.0.1:11435`.

```powershell
& .\Fundamentos_IA_Unidad_1\herramientas\iniciar_ollama.ps1
.\.venv-u1\Scripts\python.exe .\Fundamentos_IA_Unidad_1\reproducir.py --solo 07-crewai --incluir-crewai
```

La primera vez en otro equipo se debe descargar el modelo con `herramientas/preparar_modelo.py`. El programa guarda el análisis y el informe de dos agentes; usa fuentes oficiales seleccionadas previamente. El resultado de un modelo de lenguaje puede variar entre ejecuciones y requiere lectura antes de entregarlo.

## Preparar otro equipo

Con Python y Git Bash instalados, desde la carpeta que contiene la unidad:

```powershell
python -m venv .venv-u1
.\.venv-u1\Scripts\python.exe -m pip install -r .\Fundamentos_IA_Unidad_1\requirements.txt

# Para CrewAI, usa un Python 3.12 instalado y sustituye la ruta si hace falta.
py -3.12 -m venv .venv-crewai
.\.venv-crewai\Scripts\python.exe -m pip install -r .\Fundamentos_IA_Unidad_1\07-crewai\requirements.txt
```

Los datos necesarios ya están incluidos en la unidad. Si se pierden, `herramientas/descargar_datos.py --vision` los descarga de sus fuentes. `herramientas/fuentes_datos.json` registra las URL y SHA-256 de los datos utilizados.

Las versiones exactas de las bibliotecas usadas se guardan en `herramientas/requirements-ejecucion.txt` y `07-crewai/requirements-ejecucion.txt`. Las capturas requieren Chrome o Edge. No hacen falta TensorFlow, GPU, claves de API ni un servicio de búsqueda de pago.

## Validar la entrega

```powershell
.\.venv-u1\Scripts\python.exe .\Fundamentos_IA_Unidad_1\herramientas\validar_entregables.py
```

Esta comprobación se ejecuta después de generar resultados, cuadernos y capturas. Para regenerar los siete cuadernos, usa `herramientas/generar_cuadernos.py` con el mismo Python de `.venv-u1`.
