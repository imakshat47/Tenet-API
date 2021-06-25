try:    
    from flask import Flask, json, request, make_response    
    from pymongo import MongoClient
    from bson import json_util    
    from src.Mts import MTS
    import key
    import os
    from os import environ
    import random
except ModuleNotFoundError:
    exit("Missing Lib: " + str(e))

# app
app = Flask(__name__)

# Mongo Object
__client = MongoClient(key._mongo_uri)
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


# scatterchart
@app.route('/scatterchart/<limit>/<skip>', methods=['GET', 'POST'])
def scatterchart(limit = 100, skip = 300):        
    collection = db.find({"$expr": {"$ne": ["$polarity", "$trans_polarity"]}, 'polarity': {"$ne" : "0.0"}},{"polarity": 1, "trans_polarity": 1}).skip(int(skip)).limit(int(limit))
    data = []
    for _collection in collection:        
        data.append(_collection)    
    return response({"count":limit, "offset": skip, "data": data})


@app.route('/fetch/<limit>/<skip>', methods=['GET', 'POST'])
def fetch(limit, skip = 0):
    collection = db.find().skip(skip).limit(limit).sort("_id",-1)
    data = []
    for _collection in collection:
        data.append(_collection)
    return response({"data": data})


@app.route('/mts', methods=['GET', 'POST'])
def mts():
    # data = request.get_json()
    if request.method == 'POST':
        _text = request.form['text']
        _lang = request.form['lang']
    else:
        _text = request.args.get("text", "")
        _lang = request.args.get("lang", "")
    mts = MTS()
    _text = mts._translator(_text, _lang)
    _code = 200
    if _text == None:
        _code = 100
        _text = "No Text Found!!"
    # return data
    return response({"text": _text, "lang": _lang}, _code)


@app.route('/record', methods=['GET', 'POST'])
def record():
    _very_good = db.find({"polarity": {"$gte": 0.5}}).count()
    _good = db.find({"polarity": {"$gt": 0.0}}).count()

    _neutral = db.find({"polarity": {"$eq": 0.0}}).count()

    _bad = db.find({"polarity": {"$lt": 0.0}}).count()
    _very_bad = db.find({"polarity": {"$lt": -0.5}}).count()

    _total = db.find().count()
    _left_processed = db.find({"polarity": {"$exists": False}}).count()
    _processed = db.find({"polarity": {"$exists": True}}).count()

    _differ_polarity = db.find({"$expr": {"$ne": ["$polarity", "$trans_polarity"]}}).count()
    # return data
    return response({"Total Record": _total, "Total Record Processed": _processed, "Total Record Not Processed": _left_processed,  "Total Record Imporved by MTS": _differ_polarity, "ordinals": {"Netural": _neutral, "Good": _good, "Very Good": _very_good, "Bad": _bad, "Very Bad": _very_bad}})


# Error handing
@app.errorhandler(404)
def page_not_found(error):
    return response({}, 404)


# Driver Method
if __name__ == '__main__':
    app.run(port=5000, debug=True)    