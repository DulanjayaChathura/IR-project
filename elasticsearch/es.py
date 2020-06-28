
from elasticsearch import Elasticsearch, helpers
import os, uuid
elastic = Elasticsearch()

def script_path():
    path = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'posix': 
        path = path + "/"
    else:
        path = path + chr(92) 
    return path

def get_data_from_file(file_name):
    if "/" in file_name or chr(92) in file_name:
        file = open(file_name, encoding="utf8", errors='ignore')
    else:
        
        file = open(script_path() + str(file_name), encoding="utf8", errors='ignore')
    data = [line.strip() for line in file]
    file.close()
    return data

def bulk_json_data(json_file, _index, doc_type):
    json_list = get_data_from_file(json_file)
    for doc in json_list:
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }

try:
    response = helpers.bulk(elastic, bulk_json_data("lyrics.json", "lyrics", "doc"))

    print ("\nRESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)