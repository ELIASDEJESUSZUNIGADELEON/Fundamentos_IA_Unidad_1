# Referencias y alcance de la reconstrucción

Reconstrucción realizada el 20 de noviembre de 2026. El código de las prácticas se escribió para esta carpeta. No se copiaron los PDF personales, informes, salidas de cuadernos ni capturas de los compañeros. Los nombres y temas se identificaron consultando sus repositorios:

- [César: Unidad 1](https://github.com/cesar-upv/2430233_FUNDAMENTOS_IA_UNIDAD_1/tree/99c30b7430857cf2e2ca67de810895a1a75ab336), revisión `99c30b7430857cf2e2ca67de810895a1a75ab336`.
- [ZapataFrame: Unidad 1](https://github.com/ZapataFrame/FIA-Actividades-Unidad-1/tree/1f6c6eb29d80264aa76a3cbf5243927e860eb93b), revisión `1f6c6eb29d80264aa76a3cbf5243927e860eb93b`.

El orden sigue el desglose de ocho secciones de ZapataFrame y agrega visión por computadora, que aparece en el de César. Los repositorios no sustituyen las instrucciones originales del profesor: se trata de una reconstrucción de los temas, con implementaciones propias de sus ejercicios.

| Bloque | Referencia / datos usados | Adaptación |
| --- | --- | --- |
| Entorno | Los dos repositorios verifican Python y sus librerías | Verificación de seis librerías y una regresión mínima |
| Historia y mapa | Documentos e imagen proporcionados por Elias | Reporte PDF y LaTeX, evidencia del cuaderno y mapa mental |
| Clientes | [CSV de ejemplo de ZapataFrame](https://github.com/ZapataFrame/FIA-Actividades-Unidad-1/blob/1f6c6eb29d80264aa76a3cbf5243927e860eb93b/04-bash-limpieza-clientes/clientes_sucio.csv) y reto de departamentos/ventas | Se reutilizó solo el pequeño dataset de entrada; script nuevo |
| PIB y satisfacción | [Datos originales de Hands-On Machine Learning, Aurélien Géron](https://github.com/ageron/handson-ml/tree/master/datasets/lifesat), recopilados de OCDE y FMI | Descarga de los dos CSV originales, script Bash nuevo y unión verificada independientemente con Python |
| Lógica | Operadores e interpretación de la política de acceso en la sección de ZapataFrame | Enumeración exhaustiva, equivalencia real y contraejemplos de inferencia |
| CrewAI | Práctica de investigador/redactor con modelos locales | Dos agentes con un mismo Qwen2.5 local; tres fuentes oficiales curadas en lugar de Serper |
| Red neuronal | [TallerSaid](https://github.com/DiegoRIbarra/TallerSaid) y guía de NumPy/MNIST incluida por César | MLP 784-100-10 con SSE y dropout; implementación por mini lotes con sesgos y derivadas completas |
| MNIST | [Fuente y sumas MD5 en torchvision](https://docs.pytorch.org/vision/main/_modules/torchvision/datasets/mnist.html); archivos del espejo `ossci-datasets.s3.amazonaws.com/mnist/` | Lectura IDX sin TensorFlow; 1000 imágenes de entrenamiento y 10 000 de prueba |
| Lógica difusa | Ejercicio de propina en ambos repositorios; [ejemplo oficial de scikit-fuzzy](https://scikit-fuzzy.readthedocs.io/en/latest/auto_examples/plot_tipping_problem_newapi.html) | Mismas funciones triangulares y reglas del taller; script nuevo, casos y gráfica |
| NLP | Analizador de sentimientos por palabras en el cuaderno de ZapataFrame | Léxico, normalización de acentos, ventana sencilla de negación y contraste; se documenta el fallo de sarcasmo |
| Evolutivos | Taller de laberinto de ambos repositorios | Laberinto nuevo, población 240, selección por torneo, cruce, mutación y elitismo; BFS solo evalúa distancias |
| Visión | [Fotos de entrada compartidas en el taller de César](https://github.com/cesar-upv/2430233_FUNDAMENTOS_IA_UNIDAD_1/tree/99c30b7430857cf2e2ca67de810895a1a75ab336/06-talleres/vision-por-computadora/assets-taller) | Clasificador propio con histogramas HSV y regresión logística; se excluyen de la métrica dos fotos repetidas |

## Documentación técnica

- [CrewAI: agentes](https://docs.crewai.com/en/concepts/agents), [equipos](https://docs.crewai.com/en/concepts/crews) y [modelos/Ollama](https://docs.crewai.com/en/concepts/llms).
- [Ollama: versión portátil oficial 0.40.16](https://github.com/ollama/ollama/releases/tag/v0.40.16).
- [Modelo Qwen2.5 1.5B para Ollama](https://ollama.com/library/qwen2.5:1.5b).

Los archivos de resultados contienen las salidas de las prácticas. Las capturas de consola muestran sus registros TXT en una ventana de texto; las gráficas se guardan directamente desde cada programa. Las vistas previas de los documentos se renderizan desde los PDF proporcionados por Elias. Los datos de entrada conservan su procedencia.
