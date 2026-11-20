"""Operadores, equivalencia e inferencia por enumeración exhaustiva."""
import csv
import inspect
import itertools
import json
from pathlib import Path


def neg(p): return not p
def conj(p, q): return bool(p and q)
def disy(p, q): return bool(p or q)
def xor(p, q): return bool(p) != bool(q)
def implica(p, q): return (not p) or bool(q)
def ssi(p, q): return bool(p) == bool(q)
def nand(p, q): return not conj(p, q)
def nor(p, q): return not disy(p, q)


def casos(n):
    return list(itertools.product([False, True], repeat=n))


def equivalentes(f, g):
    n = len(inspect.signature(f).parameters)
    if n != len(inspect.signature(g).parameters):
        raise ValueError("Las fórmulas deben tener la misma aridad.")
    return all(f(*v) == g(*v) for v in casos(n))


def contraejemplos(premisas, conclusion, n):
    """La inferencia es válida si no hay premisas verdaderas y conclusión falsa."""
    return [v for v in casos(n) if all(p(*v) for p in premisas) and not conclusion(*v)]


def main():
    salida = Path(__file__).parent / "resultados"
    salida.mkdir(exist_ok=True)
    with (salida / "operadores.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["p", "q", "NOT_p", "AND", "OR", "XOR", "IMPLICA", "SSI", "NAND", "NOR"])
        for p, q in casos(2):
            w.writerow([p, q, neg(p), conj(p,q), disy(p,q), xor(p,q), implica(p,q), ssi(p,q), nand(p,q), nor(p,q)])
    distributiva = equivalentes(lambda p,q,r: p or (q and r), lambda p,q,r: (p or q) and (p or r))
    de_morgan = equivalentes(lambda p,q: not (p and q), lambda p,q: (not p) or (not q))
    mp = contraejemplos([lambda p,q: p, lambda p,q: implica(p,q)], lambda p,q: q, 2)
    afirmacion_consecuente = contraejemplos([lambda p,q: implica(p,q), lambda p,q: q], lambda p,q: p, 2)
    ambigua = lambda p,q,r: p or (q and not r)
    estructurada = lambda p,q,r: (p or q) and not r
    tabla = [{"admin":p,"clave":q,"suspendida":r,"ambigua":ambigua(p,q,r),"estructurada":estructurada(p,q,r)} for p,q,r in casos(3)]
    with (salida / "acceso.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=tabla[0]); w.writeheader(); w.writerows(tabla)
    resultados = {"ley_distributiva":distributiva, "de_morgan":de_morgan, "modus_ponens_valido":not mp,
                  "contraejemplo_afirmacion_consecuente":afirmacion_consecuente,
                  "politicas_equivalentes":equivalentes(ambigua, estructurada)}
    assert distributiva and de_morgan and not mp
    assert afirmacion_consecuente == [(False, True)]
    assert ambigua(True,False,True) and not estructurada(True,False,True)
    (salida / "resultados.json").write_text(json.dumps(resultados, indent=2), encoding="utf-8")
    print("Tablas: 4 combinaciones de dos variables y 8 de tres variables.")
    print(json.dumps(resultados, ensure_ascii=False, indent=2))
    print("Caso admin=True, clave=False, suspendida=True:")
    print("Política ambigua: permite acceso. Política estructurada: deniega acceso.")


if __name__ == "__main__":
    main()
