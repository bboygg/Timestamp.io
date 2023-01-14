from flask import Flask
from flask_pymongo import pymongo

client = pymongo.MongoClient("mongodb+srv://bboygg:<1234qwer>@primary.n6fr9mr.mongodb.net/?retryWrites=true&w=majority")
db = client.test


