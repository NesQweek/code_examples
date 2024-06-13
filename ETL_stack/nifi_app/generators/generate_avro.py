try:
    from .generate_dict import generate_random_data_dict
except:
    from generate_dict import generate_random_data_dict

import os
from uuid import uuid4
from confluent_kafka.serialization import SerializationContext, StringSerializer, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer



# Определение схемы данных
schema = """{
"type": "record", 
"name": "application", 
"namespace": "avro.schema",
"fields": [
    {"name": "Loan_ID", "type": "string"},
    {"name": "Gender", "type": "string"},
    {"name": "Married", "type": "string"},
    {"name": "Dependents", "type": "int"},
    {"name": "Education", "type": "string"},
    {"name": "Self_Employed", "type": "string"},
    {"name": "ApplicantIncome", "type": "int"},
    {"name": "CoapplicantIncome", "type": "float"},
    {"name": "LoanAmount", "type": "float"},
    {"name": "Loan_Amount_Term", "type": "float"},
    {"name": "Credit_History", "type": "float"},
    {"name": "Property_Area", "type": "string"},
    {"name": "Loan_Status", "type": "string"}
    ]
}"""

def process_record_confluent(record: bytes, src: SchemaRegistryClient, schema: str):
    deserializer = AvroDeserializer(schema_str=schema, schema_registry_client=src)
    return deserializer(record, None) # returns dict

def generate_serialized_avro(topic_name: str, schema_registry_client: SchemaRegistryClient):

    generated_data_dict = generate_random_data_dict()
    avro_serializer = AvroSerializer(schema_registry_client, schema)
    string_serializer = StringSerializer('utf-8')
    key = string_serializer(str(uuid4()))
    value = avro_serializer(generated_data_dict, SerializationContext(topic_name, MessageField.VALUE))
    # print('key:', key)
    # print('value:', value)


    deserialized_value = process_record_confluent(value,schema_registry_client,schema)
    assert deserialized_value==generated_data_dict, 'Несоответствие схемы и данных в JSON'

    print("Avro файл преобразован в байт-строку")

    return key, value


if __name__=='__main__':
    test_topic_name = 'topic_test'
    schema_registry_client = SchemaRegistryClient({
    'url': 'http://localhost:8081'})
    serialized_value = generate_serialized_avro(test_topic_name, schema_registry_client)




