from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://Nikelmod:Swdrop35@cluster0.mibvk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['villiam']
quotes = db['quotes']
jokes = db['jokes']