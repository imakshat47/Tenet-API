from flask import Flask, json, request, make_response
from bson import json_util
import key
import pymongo
import os
from os import environ

# app
app = Flask(__name__)

# Mongo Object
__client = pymongo.MongoClient(key._mongo_uri)
__db = __client["tenet"]
db = __db["tweets"]
_db = __db["result"]


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
    response.headers['Access-Control-Allow-Origin'] = "*"
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


@app.route('/record', methods=['GET', 'POST'])
def record():
    res = _db.find({"_id": key._tenet_record})
    if res != None:
        _ordinal = res[0]['ordinals']
    _differ_polarity = db.find({"$expr": {"$ne": ["$polarity", "$trans_polarity"]}}).count()
    _polarity = db.find({"$expr": {"$ne": ["$polarity", None]}}).count()
    # return data
    return response({"left_processed": _polarity,  "differ_polarity": _differ_polarity, "ordinals": {"Netural": _ordinal[0], "Good": _ordinal[1], "Very Good": _ordinal[2], "Bad": _ordinal[3], "Very Bad": _ordinal[4]}})


# Error handing
@app.errorhandler(404)
def page_not_found(error):
    return response({}, 404)


# Driver Method
if __name__ == '__main__':
    app.run(port=os.Getenv("PORT"), debug=True)
