import subprocess
import os
import sys
import pexpect


def main():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cur_dir)

    subprocess.run(['docker-compose', 'run', '--rm', 'web-app', 'sh', '-c', 'python manage.py'])

    print('Применение миграций...')

    subprocess.run(['docker-compose', 'run', '--rm', 'web-app', 'sh', '-c', 'python manage.py migrate'])

    print('Создание суперпользователя')

    # Создание суперпользователя Django
    command = 'docker-compose run --rm web-app sh -c "python manage.py createsuperuser --username admin --email ml_engineer@vk.com"'
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    child = pexpect.spawn(command)
    child.logfile = sys.stdout.buffer
    child.expect(r'Password: ')
    child.sendline(r'openfukingweb')
    child.sendline(r'openfukingweb')

    child.expect(pexpect.EOF)
    #
    print('Запуск compose up...')
    subprocess.run(['docker', 'compose', 'up', '-d'])

    web_url = 'http://localhost:8000/info'
    subprocess.run(['python', '-m', 'webbrowser', '-t', f'{web_url}'])

if __name__=='__main__':
    main()