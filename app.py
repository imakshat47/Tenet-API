from flask import Flask, json, request, make_response
from bson import json_util
import key
import pymongo
import os
from os import environ
from src.Mts import MTS

# app
app = Flask(__name__)

# Mongo Object
__client = pymongo.MongoClient(key._mongo_uri)
__db = __client["tenet"]
db = __db["tweets"]

# Json Dump
def jd(obj):
    return json.dumps(obj, default=json_util.default)

# Response


def response(data={}, code=200):
    resp = {
        "code": code,
        "data": data
    }
    response = make_response(jd(resp))
    response.headers['Status-Code'] = resp['code']
    response.headers['Content-Type'] = "application/json"
    # response.headers['Access-Control-Allow-Origin'] = "*"
    return response

# routes


# @app.route('/', methods=['GET', 'POST'])
# def result():
#     polarity = []
#     pos_polarity = []
#     neg_polarity = []
#     for row in db._find():
#         polarity[row['_id']] = row['polarity']
#         pos_polarity[row['_id']] = row['pos_polarity']
#         neg_polarity[row['_id']] = row['neg_polarity']
#     # return data
#     return response({"polarity": polarity, "pos_polarity": pos_polarity, "neg_polarity": neg_polarity})


@app.route('/mts', methods=['GET', 'POST'])
def mts():

    _text = request.form.get("text")
    _lang = request.form.get("lang")
    mts = MTS()
    _text = mts._translator(_text, _lang)
    # return data
    return response({"text": _text, "lang": _lang})


@app.route('/record', methods=['GET', 'POST'])
def record():   
    _very_good = db.find({"polarity": {"$gte": 0.5}})
    _good = db.find({"polarity": {"$gt": 0.0}})

    _neutral = db.find({"polarity": {"$eq": 0.0}})

    _bad = db.find({"polarity": {"$lt": 0.0}})
    _very_bad = db.find({"polarity": {"$lt": -0.5}})

    _left_processed = db.find({"polarity": None}).count()
    _total = db.find().count()
    _processed = int(int(_total) - int(_left_processed))
    
    # return data
    return response({"Total Record": _total, "Total Record Processed": _processed, "Total Record Not Processed": _left_processed,  "Total Record Imporved by MTS": _differ_polarity, "ordinals": {"Netural": _neutral, "Good": _good, "Very Good": _very_good, "Bad": _bad, "Very Bad": _very_bad}})


# Error handing
@app.errorhandler(404)
def page_not_found(error):
    return response({}, 404)


# Driver Method
if __name__ == '__main__':
    app.run(port=5000, debug=True)
