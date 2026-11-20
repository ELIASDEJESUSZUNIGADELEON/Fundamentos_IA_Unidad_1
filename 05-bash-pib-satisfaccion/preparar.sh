#!/usr/bin/env bash
# Unión OCDE/FMI mediante herramientas de Bash y GNU Awk.
set -euo pipefail
export LC_ALL=C
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p resultados
printf 'Líneas de los archivos fuente:\n'
wc -l datos/oecd_bli_2015.csv datos/gdp_per_capita.csv
# GNU Awk >=5.3 conserva los campos CSV con comas internas entrecomilladas.
gawk --csv 'BEGIN { OFS="," }
NR>1 && $3=="SW_LIFS" && $7=="TOT" {
    print $2,$15
}' datos/oecd_bli_2015.csv | sort -t, -k1,1 > resultados/satisfaccion.csv
iconv -f ISO-8859-1 -t UTF-8 datos/gdp_per_capita.csv |
    awk -F '\t' 'BEGIN {OFS=","} NR>1 {
        gsub(/,/,"",$6); gsub(/\r/,"",$6)
        if($6 ~ /^[0-9]+([.][0-9]+)?$/) print $1,$6
    }' | sort -t, -k1,1 > resultados/pib.csv
printf 'Pais,Satisfaccion_Vida,PIB_Capita\n' > resultados/merged_data.csv
join --check-order -t, -o '1.1 1.2 2.2' resultados/satisfaccion.csv resultados/pib.csv >> resultados/merged_data.csv
awk -F, 'NR>1 {print $3}' resultados/merged_data.csv > resultados/X.csv
awk -F, 'NR>1 {print $2}' resultados/merged_data.csv > resultados/y.csv
test -s resultados/X.csv
test "$(wc -l < resultados/X.csv)" -eq "$(wc -l < resultados/y.csv)"
printf '\nPaíses unidos: %s\n' "$(wc -l < resultados/X.csv)"
head -n 9 resultados/merged_data.csv
printf '\nX.csv e y.csv conservan el mismo orden de países.\n'
