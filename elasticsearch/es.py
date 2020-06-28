
from elasticsearch import Elasticsearch, helpers
import os, uuid, json


elastic = Elasticsearch()
with open("lyrics.json", encoding="utf8") as objFile:
    lyrics_list= json.load(objFile)

helpers.bulk(elastic,lyrics_list,index="lyrics",doc_type="doc")
