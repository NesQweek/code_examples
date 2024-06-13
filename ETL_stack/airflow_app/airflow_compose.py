import os
import sys
import subprocess


path = os.path.dirname(os.path.abspath(__file__)) + '/config/'

def are_airflow_inited() -> None:
    print('Проверка на airflow-init...')
    command = "echo $(docker ps -a | grep airflow-init | cut -d ' ' -f 1)"
    result = subprocess.check_output(command, shell=True).decode('utf-8')

    assert len(result) > 0, 'init не был выполнен'

def main() -> None:
    try:
        are_airflow_inited()
    except AssertionError:
        print('\nЗапуск compose up airflow-init...')
        subprocess.run(['docker', 'compose', '--file', f'{path}docker-compose.yaml', 'up', 'airflow-init'])

    finally:
        print('\nЗапуск compose up...')
        process = subprocess.Popen(['docker', 'compose', '--file', f'{path}docker-compose.yaml', 'up'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        logs_reading = True
        print('Ожидание сборки и запуска airflow...')
        # Нахождение события запуска для airflow
        while logs_reading:
            for line in process.stdout:
                line_ = line.strip()
                if 'GET /health HTTP/1.1" 200' in line_:
                    logs_reading = False
                    break
        print('Airflow запущен')



    airflow_url = 'http://localhost:8001'
    subprocess.run(['python', '-m', 'webbrowser', '-t', f'{airflow_url}'])









if __name__ == '__main__':
    path = 'config/'
    main()