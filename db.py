from tinydb import TinyDB 
import json

db = TinyDB('db.json')
count = TinyDB('count.json')

def idx_count():
    arr = count.all()
    idx=arr[0]['count']
    return idx

def all_db():
    arr1=db.all()
    return arr1

def update_count(idx):
    idx+=1
    count.update({'count':idx},doc_ids=[1])

def update_db(photo,caption):
    db.insert({'photo':photo, 'caption':caption})

