import pandas as pd
import io
from uuid import uuid4
from confluent_kafka.serialization import StringSerializer

try:
    from .generate_dict import generate_random_data_dict
except:
    from generate_dict import generate_random_data_dict

def generate_serialized_parquet():
    generated_dict = generate_random_data_dict()

    # Создание DataFrame из JSON-объекта
    df = pd.DataFrame([generated_dict])

    string_serializer = StringSerializer('utf-8')
    # DataFrame > ORC > байт-строка (без сохранения на диск)
    parquet_bytes = df.to_parquet(index=False)

    key = string_serializer(str(uuid4()))
    value = io.BytesIO(parquet_bytes).read()

    print("Parquet файл преобразован в байт-строку")



    return key, value

if __name__=='__main__':
    generate_serialized_parquet()