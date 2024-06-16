#  Для локального запуска

import os
import env
import csv
import subprocess
import pandas as pd
from docker_init import run_init

container_id = run_init(local=True)


os.system(f'docker exec {container_id} hadoop fs -mkdir /tmp')

# Загрузить данные в HDFS
os.system(f'docker exec {container_id} hadoop fs -put {os.path.join(os.getenv("WORK_DIR"), "spotify/log_mini.csv")} /tmp/spotify_data.csv')

# Установка прав
os.system(f'docker exec {container_id} chmod +x {os.path.join(os.getenv("WORK_DIR"), "mapper.py")}')
os.system(f'docker exec {container_id} chmod +x {os.path.join(os.getenv("WORK_DIR"), "reducer.py")}')


os.system(f'docker exec {container_id} hadoop fs -rm -r /tmp/spotify_results')

# Стрим-вычисление прослушиваний с использованием Hadoop Streaming
os.system(f'docker exec {container_id} hadoop jar {os.path.join(os.getenv("HADOOP_HOME"), \
  "share", "hadoop", "tools", "lib", "hadoop-streaming-3.3.4.jar")} \
  -input /tmp/spotify_data.csv \
  -output /tmp/spotify_results \
  -mapper {os.getenv("MAPPER")} \
  -reducer {os.getenv("REDUCER")}')


result_csv = "mapreduce_results.csv"
if os.path.exists(result_csv):
    os.remove(result_csv)

# Создать пустой .csv

with open(result_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([])

# Добавить названия столбцов 
os.system(f'echo "track_id,count" > {result_csv}') # Добавляем заголовки

# Загрузить файл с результатами из HDFS
os.system(f"docker exec {container_id} "                      + \
          "hadoop fs -cat /tmp/spotify_results/part-00000 | " + \
          "awk '{print $1 \",\" $2}' | "                      + \
          "sort -t, -k2 -nr >> mapreduce_results.csv")

df = pd.read_csv(result_csv)
print(df.head())