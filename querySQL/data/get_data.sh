#!/bin/sh

curl "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv" > TotalPopulation.csv

gzip -k TotalPopulation.csv

python3 <<EOF
import pandas
pandas.read_csv('TotalPopulation.csv').to_parquet('TotalPopulation.parquet')
EOF

mkdir sql-example && mv TotalPopulation* sql-example
mc mb minio-minimal/shared/blair-drummond/
mc cp -r sql-example minio-minimal/shared/blair-drummond/