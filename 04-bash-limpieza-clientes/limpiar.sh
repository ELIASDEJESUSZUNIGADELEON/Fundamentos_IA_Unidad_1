#!/usr/bin/env bash
# Limpieza del CSV sencillo del ejercicio (sus campos no tienen comas internas).
set -euo pipefail
export LC_ALL=C
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p resultados
awk -F, '
function trim(s) { gsub(/^[[:space:]]+|[[:space:]]+$/, "", s); return s }
BEGIN { OFS=","; print "id,nombre,edad,salario,departamento" }
NR > 1 {
    for(i=1;i<=NF;i++) $i=trim($i)
    if($1 !~ /^[0-9]+$/ || seen[$1]++) next
    # Se descartan registros sin edad o salario; no se inventan esos valores.
    if($3 !~ /^[0-9]+$/ || $4 !~ /^[0-9]+([.][0-9]+)?$/) next
    $5=toupper($5)
    print $1,$2,$3,$4,$5
}' datos/clientes_sucio.csv > resultados/clientes_limpios.csv
tail -n +2 resultados/clientes_limpios.csv | cut -d, -f5 | sort -u > resultados/departamentos.txt
awk -F, 'NR==1 || $5=="VENTAS"' resultados/clientes_limpios.csv > resultados/ventas.csv
printf 'Filas originales: %s\n' "$(awk 'END {print NR-1}' datos/clientes_sucio.csv)"
printf 'Filas limpias: %s\n' "$(awk 'END {print NR-1}' resultados/clientes_limpios.csv)"
cat resultados/clientes_limpios.csv
printf '\nDepartamentos únicos ordenados:\n'
cat resultados/departamentos.txt
printf '\nPersonas de ventas:\n'
cat resultados/ventas.csv
