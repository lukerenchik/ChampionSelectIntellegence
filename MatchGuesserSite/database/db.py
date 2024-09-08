from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://lukerenchik:8Fjyypj8zZCdb3pz@championselectintellige.vegpc.mongodb.net/?retryWrites=true&w=majority&appName=ChampionSelectIntelligence"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)