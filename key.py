import os
from os import environ

# Mongo DB URI
_mongo_uri = environ['MONGO_URI']

_port = os.Getenv("PORT")

# Tenet Results Saves on ID
_tenet_record = "record"