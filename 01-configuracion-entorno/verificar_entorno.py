"""Verifica los imports y ejecuta una operación real de ciencia de datos."""
import importlib
import json
import platform
import sys
from pathlib import Path


def main():
    versiones = {"python": platform.python_version(), "sistema": platform.system()}
    for nombre in ["IPython", "notebook", "numpy", "matplotlib", "scipy", "sklearn"]:
        modulo = importlib.import_module(nombre)
        versiones[nombre] = modulo.__version__
        print(f"{nombre:15} {modulo.__version__}")
    import numpy as np
    from sklearn.linear_model import LinearRegression
    x = np.array([[1.0], [2.0], [3.0]])
    modelo = LinearRegression().fit(x, [2.0, 4.0, 6.0])
    prediccion = float(modelo.predict([[4.0]])[0])
    assert np.isclose(prediccion, 8.0)
    print(f"Python: {versiones['python']} | Ejecutable: {sys.executable}")
    print(f"Prueba de regresión y=2x: para x=4 se obtuvo {prediccion:.2f}")
    salida = Path(__file__).parent / "resultados"
    salida.mkdir(exist_ok=True)
    (salida / "versiones.json").write_text(json.dumps(versiones, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
