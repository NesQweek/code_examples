#!/usr/bin/python3

import pandas as pd
import io
import sys

# Чтение байт-строки из stdin
input_data = sys.stdin.buffer.read()
# преобразование в JSON
json_file = pd.read_orc(io.BytesIO(input_data)).to_json(orient='records', lines=True)
# Запись JSON в stdout
sys.stdout.buffer.write(json_file.encode())






