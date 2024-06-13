import asyncio
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from generators.generate_avro import generate_serialized_avro
from generators.generate_parquet import generate_serialized_parquet
from generators.generate_orc import generate_serialized_orc


broker_for_avro = 'localhost:19092'
broker_for_parquet = 'localhost:29092'
broker_for_orc = 'localhost:39092'

avro_topic_name = 'avro-topic'
parquet_topic_name = 'parquet-topic'
orc_topic_name = 'orc-topic'

schema_registry_client = SchemaRegistryClient({
    'url': 'http://localhost:8081'
})

avro_producer = Producer({
    'bootstrap.servers': broker_for_avro,
})
parquet_producer = Producer({
    'bootstrap.servers': broker_for_parquet
})
orc_producer = Producer({
    'bootstrap.servers': broker_for_orc
})

# -------------------------------------  START PRODUCE AVRO TO KAFKA-BROKER-1 ------------------------------------------
async def produce_avro():

    while True:
        avro_uuid_key, avro_value = generate_serialized_avro(avro_topic_name, schema_registry_client)
        print(f"Сообщение: {avro_value}\n - Успешно доставлено")
        print('______________________________________________________' * 3)
        avro_producer.produce(topic=avro_topic_name, key=avro_uuid_key, value=avro_value)
        avro_producer.flush()

        await asyncio.sleep(30)

# -------------------------------------  END PRODUCE AVRO TO KAFKA-BROKER-1 --------------------------------------------
# -----------------------------------  START PRODUCE PARQUET TO KAFKA-BROKER-2 -----------------------------------------
async def produce_parquet():

    while True:
        parquet_uuid_key, parquet_value = generate_serialized_parquet()
        print(f"Сообщение: {parquet_value}\n - Успешно доставлено")
        print('______________________________________________________' * 3)
        parquet_producer.produce(topic=parquet_topic_name, key=parquet_uuid_key, value=parquet_value)
        parquet_producer.flush()

        await asyncio.sleep(30)

# ------------------------------------  END PRODUCE PARQUET TO KAFKA-BROKER-2 ------------------------------------------
# -------------------------------------  START PRODUCE ORC TO KAFKA-BROKER-2 -------------------------------------------
async def produce_orc():

    while True:
        orc_uuid_key, orc_value = generate_serialized_orc()
        print(f"Сообщение: {orc_value}\n - Успешно доставлено")
        print('______________________________________________________' * 3)
        orc_producer.produce(topic=orc_topic_name, key=orc_uuid_key, value=orc_value)
        orc_producer.flush()

        await asyncio.sleep(30)
# ----------------------------------------  END PRODUCE ORC TO KAFKA-BROKER-2 ------------------------------------------

async def main():
    # Запуск функций асинхронно
    await asyncio.gather(produce_avro(), produce_parquet(), produce_orc())

# Запустить асинхронный цикл событий
asyncio.run(main())
