En CrewAI, dos agentes cooperan para realizar tareas utilizando un modelo local. El proceso se divide en tres etapas: configuración del agente, definición de tareas y ejecución local.

1. Configuración del agente: Cada agente se configura con un rol, una meta y un contexto. Por ejemplo, un agente puede ser un "agente de investigación" con la meta de "descubrir información relevante" y un contexto específico de un proyecto. 

2. Definición de tareas: Una tarea en CrewAI se define con una descripción y un resultado esperado. Por ejemplo, una tarea podría ser "buscar información sobre el clima en una ciudad específica" con el resultado esperado de "información detallada sobre el clima de la ciudad".

3. Ejecución local: Una tarea puede usar como contexto la salida de una tarea anterior. Por ejemplo, una tarea de "buscar información sobre el clima" podría usar la salida de una tarea anterior de "descubrir información relevante" para proporcionar contexto sobre la relevancia de la información encontrada.

En este proceso, la integración de Ollama se realiza utilizando el modelo local. CrewAI permite configurar un LLM mediante un identificador de modelo y una URL base. La integración de Ollama utiliza LiteLLM y requiere la dependencia crewai[litellm]. Ollama debe estar ejecutándose con el modelo descargado.

Las tres fuentes mencionadas proporcionan una comprensión completa del proceso de cooperación entre agentes en CrewAI. La configuración del agente, la definición de tareas y la ejecución local son fundamentales para el correcto funcionamiento del sistema. Además, la integración de Ollama y el uso de modelos locales son características clave que permiten la colaboración efectiva entre agentes.