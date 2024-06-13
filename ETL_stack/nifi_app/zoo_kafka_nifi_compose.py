import os
import time
import subprocess
import requests
import pandas as pd


path = os.path.dirname(os.path.abspath(__file__)) + '/config/'

KAFKA_CONTAINERS = 3


def are_brokers_created() -> None:
    command = """docker ps -a --format 'table "{{.Names}}","{{.Image}}","{{.Ports}}","{{.Status}}"' > status.csv"""
    subprocess.check_output(command, shell=True)

    df = pd.read_csv('status.csv')
    os.remove('status.csv')

    created_brokers = df.loc[df['NAMES'].str.contains('kafka-broker'), 'NAMES']
    assert len(created_brokers) == KAFKA_CONTAINERS, 'Проверка: брокеры не были созданы'


def are_topics_created() -> None:
    active_topics = subprocess.check_output(['docker', 'exec', 'kafka-broker-1', 'kafka-topics', '--bootstrap-server',
                                             'kafka-broker-1:9092', '--list']).decode('utf-8')

    state = all(topic in active_topics for topic in ['avro-topic', 'parquet-topic', 'orc-topic'])
    assert state == True, 'Проверка: топики не были созданы'


def create_topics() -> None:
    'Создать топики под разные типы файлов'
    subprocess.run(['docker', 'compose', '--file', f'{path}docker-compose.yml', 'exec', 'kafka-broker-1',
                    'kafka-topics', '--bootstrap-server', 'kafka-broker-1:9092', '--create', '--topic', 'avro-topic',
                    '--partitions', '3', '--replication-factor', '3'])
    subprocess.run(['docker', 'compose', '--file', f'{path}docker-compose.yml', 'exec', 'kafka-broker-2',
                    'kafka-topics', '--bootstrap-server', 'kafka-broker-2:9092', '--create', '--topic', 'parquet-topic',
                    '--partitions', '3', '--replication-factor', '3'])
    subprocess.run(['docker', 'compose', '--file', f'{path}docker-compose.yml', 'exec', 'kafka-broker-3',
                    'kafka-topics', '--bootstrap-server', 'kafka-broker-3:9092', '--create', '--topic', 'orc-topic',
                    '--partitions', '3', '--replication-factor', '3'])


def main() -> None:
    'Полноценный запуск кластера после init-nifi'

    try:
        are_brokers_created()
    except AssertionError:
        # print('Запуск compose build...\n')
        # subprocess.run(['docker', 'compose', '--file', f'{path}docker-compose.yml', 'build'])
        print('\nЗапуск compose up...')
        kafka_brokers_started = 0
        # Чтение логов после запуска docker compose up
        process = subprocess.Popen(['docker', 'compose', '--file', f'{path}docker-compose.yml', 'up'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        logs_reading = True
        print('Ожидание запуска zookeeper клиентов и kafka брокеров...')
        # Нахождение события запуска для каждого kafka брокера
        while logs_reading:
            for line in process.stdout:
                line_ = line.strip()
                if 'Starting (kafka.controller.RequestSendThread)' in line_:
                    kafka_brokers_started += 1
                    if kafka_brokers_started == KAFKA_CONTAINERS:
                        logs_reading = False
                        break
        create_topics()

    print('Ожидание запуска nifi...')
    nifi_url = 'http://localhost:8080/nifi'
    url_is_open = False
    while not url_is_open:
        try:
            result = requests.get(nifi_url)
            if result.status_code == 200:
                url_is_open = True
                break
        except:
            print(f'{nifi_url} ещё не доступен, ожидайте...')

        finally:
            time.sleep(3)

    subprocess.run(['python', '-m', 'webbrowser', '-t', f'{nifi_url}'])


if __name__ == '__main__':
    path = 'config/'
    main()