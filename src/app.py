from flask import Flask, render_template, request, jsonify, Response
from flask_sock import Sock
from pysondb import db
import os
import json
import time
from datetime import datetime, date, timedelta

app = Flask(__name__)
sock = Sock(app)


jsondb=db.getDb("db.json")

# queries
queries = {}

def days_between(d1, d2):
    return abs((d2 - d1).days)

def initializeDB():#
    pass
    #jsondb.add({"internalID": 1, "articleNumber": "1337-1", "productName": "Hack-Kekse", "PaybackPerDay": 10, "PaybackMinAge": 14})
    #jsondb.add({"internalID": 2, "articleNumber": "1337-2", "productName": "Fritz-Cola", "PaybackPerDay": 10, "PaybackMinAge": 5})
    #jsondb.add({"internalID": 3, "articleNumber": "1337-3", "productName": "Clubmate", "PaybackPerDay": 10, "PaybackMinAge": 5})
    #jsondb.add({"internalID": 4, "articleNumber": "1337-4", "productName": "Computerchips", "PaybackPerDay": 10, "PaybackMinAge": 7})
    #jsondb.add({"internalID": 5, "articleNumber": "1337-5", "productName": "Schoko-RAM-Riegel Zartbitter-Nuss", "PaybackPerDay": 10, "PaybackMinAge": 4})
    #jsondb.add({"internalID": 6, "articleNumber": "1337-6", "productName": "SATA-Schnitten", "PaybackPerDay": 10, "PaybackMinAge": 14})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/getPayback', methods=['POST'])
def calculatePaybackPoints():
    # {
    #   "id": "1655801622",
    #   "userId": 1337,
    #   "mhd": "2022-06-23",
    #   "marketCode": 21,
    #   "articleNumber": 12444
    # }
    global queries
    
    articleNumber = request.json["articleNumber"]
    articleMHD = request.json["mhd"]
    
    dbSearchResult = jsondb.reSearch("articleNumber", articleNumber)
    
    if len(dbSearchResult) == 1:
        
        mhd = datetime.strptime(articleMHD, "%Y-%m-%d").date()
        MHDLeftDays = days_between(mhd, date.today())
        article = dbSearchResult[0]       

        if mhd < date.today():

            res = {
                'paybackPoints': 0,
                'productName': article['productName'],
                'imageUrl': article['imageUrl'],
                'mhd': str(mhd),
                'mhdLeftDays': 0,
                'info': 'MHD reached - no Payback'
            }
            
            return jsonify(res)

        elif MHDLeftDays <= article['PaybackMinAge']:
            returnPaybackPoints = (article['PaybackMinAge'] - MHDLeftDays) * article['PaybackPerDay']
            
            # result
            res = {
                'paybackPoints': returnPaybackPoints,
                'productName': article['productName'],
                'imageUrl': article['imageUrl'],
                'mhd': str(mhd),
                'mhdLeftDays': MHDLeftDays,
                'info': 'MHD not reached - minAge reached - get Payback'
            }

            # update queries state
            queries = res
            
            return jsonify(res)
        else:
            res = {
                'paybackPoints': 0,
                'productName': article['productName'],
                'imageUrl': article['imageUrl'],
                'mhd': str(mhd),
                'mhdLeftDays': MHDLeftDays,
                'info': 'MHD not reached - minAge not reached - no Payback'
            }

            # update queries state
            queries = res
            
            return jsonify(res)

        #return jsonify(dbSearchResult[0])
    elif len(dbSearchResult) > 1:
        return Response(
            "Multiple Articles with this ArticleNumber found - Contact your Database-Administrator :D",
            status=400,
        )
    else:
        return Response(
            "Article not found",
            status=404,
        )

    

@app.route('/api/v1/echo', methods=['POST'])
def echo2():
   return jsonify(request.json)

@app.route('/api/v1/getDB', methods=['GET'])
def getDB():
     return jsonify(jsondb.getAll())

@app.route('/api/v1/clear', methods=['GET'])
def clearQueries():
    global queries
    queries = {}
    return Response(
        "cleared",
        status=200
    )

@sock.route('/api/v1/queries')
def echo(ws):
    while True:
        ws.send(json.dumps(queries))
        time.sleep(1)
        
if __name__ == "__main__":
    # if app.run debug=True - initializeDB run twice
    date.today()
    initializeDB()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    