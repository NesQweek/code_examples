import env
import os
import subprocess


def run_init(local=True):

    container_id = None

    if local == True:

        print('Проверка на наличие контейнера...')
        command = "echo $(docker ps -a | grep sindq/sb-m8:latest | cut -d ' ' -f 1)"
        container_id = subprocess.check_output(command, shell=True).decode('utf-8').strip()
        if len(container_id) > 1:
            print(f'\n {container_id} Уже запущен')
        else:
            print('\nЗапуск контейнера...')
            # Выполнить команду
            process = subprocess.Popen(['docker', 'run', '-d', '-p', '80:80', '-p', '8888:8888', 'sindq/sb-m8:latest'], \
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Получить вывод
            stdout, stderr = process.communicate()
            container_id = stdout.decode('utf-8').strip()

        try:
            for file in ['code.ipynb', 'mapper.py', 'reducer.py', 'env.py']:
                subprocess.run(["docker", "cp", file, f"{container_id}:{os.getenv('WORK_DIR')}"], check=True)
        except Exception:
            pass

    # Экспорт конфигов

    try:
        for file in ['resource-types.xml', 'mapred-site.xml', 'yarn-site.xml']:
            subprocess.run(["docker", "cp", f'./conf/{file}', f"{container_id}:{os.getenv('CONF_DIR')}/{file}" ], check=True)
    except Exception as e:
        pass 



    return container_id

if __name__ == "__main__":
    run_init()