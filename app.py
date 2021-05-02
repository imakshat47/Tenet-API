from flask import Flask, json, request, make_response
from bson import json_util
import Mongodb as mongo

# app
app = Flask(__name__)
# Mongo Object
db = mongo.MongoDB("tenet", "result")

# Json Dump


def jd(obj):
    return json.dumps(obj, default=json_util.default)

#
# Response
#


def response(data={}, code=200):
    resp = {
        "code": code,
        "data": data
    }
    response = make_response(jd(resp))
    response.headers['Status-Code'] = resp['code']
    response.headers['Content-Type'] = "application/json"
    return response

# routes


@app.route('/', methods=['GET', 'POST'])
def result():
    polarity = []
    pos_polarity = []
    neg_polarity = []
    for row in db._find():
        polarity[row['_id']] = row['polarity']
        pos_polarity[row['_id']] = row['pos_polarity']
        neg_polarity[row['_id']] = row['neg_polarity']

    # return data
    return response({"polarity": polarity, "pos_polarity": pos_polarity, "neg_polarity": neg_polarity})


@app.route('/record', methods=['GET', 'POST'])
def record():
    res = db._find({"_id": key._tenet_record})
    # return data
    return response({"ordinals": res[0]['ordinals']})


# Error handing
@app.errorhandler(404)
def page_not_found(error):
    return response({}, 404)


if __name__ == '__main__':
    app.run(port=os.Getenv("PORT"), debug=True)
