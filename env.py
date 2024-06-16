import os

os.environ["HADOOP_HOME"] = os.path.join('/usr', 'local', 'hadoop')
os.environ["CONF_DIR"] = os.path.join('/usr', 'local', 'hadoop', 'etc', 'hadoop')
os.environ["WORK_DIR"] = os.path.join('/home', 'jovyan', 'work')
os.environ["MAPPER"] = os.path.join('/home', 'jovyan', 'work', 'mapper.py')
os.environ["REDUCER"] = os.path.join('/home', 'jovyan', 'work', 'reducer.py')