# conda env export > environment.yml 


Окружение conda с работающим CUDA: весит много, поэтому устанавливать его самостоятельно (буквально парой строк ниже)


# открыть терминал от имени администратора (обязательно)

Для инициализации окружения запустить эту команду
conda env create --prefix conda_env --file environment.yml

conda init # перезапустить терминал
conda activate ./conda_env 

# закрыть терминал