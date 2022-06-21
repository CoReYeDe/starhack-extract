from flask import Flask, render_template, request, jsonify, Response
from pysondb import db
import os
from datetime import datetime, date, timedelta

app = Flask(__name__)
jsondb=db.getDb("db.json")

def days_between(d1, d2):
    #d1 = datetime.strptime(d1, "%Y-%m-%d")
    #d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def initializeDB():
    jsondb.add({"internalID": 1, "articleNumber": "1337-1", "productName": "Hack-Kekse", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 2, "articleNumber": "1337-2", "productName": "Fritz-Cola", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 3, "articleNumber": "1337-3", "productName": "Clubmate", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 4, "articleNumber": "1337-4", "productName": "Computerchips", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 5, "articleNumber": "1337-5", "productName": "Schoko-RAM-Riegel Zartbitter-Nuss", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 6, "articleNumber": "1337-6", "productName": "SATA-Schnitten", "PaybackPerDay": 10, "PaybackMinAge": 7})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/getPayback', methods=['POST'])
def calculatePaybackPoints():
    # {
    #   "id": "1655801622",
    #   "userId": 1337,
    #   "mhd": "23-06-2022",
    #   "marketCode": 21,
    #   "articleNumber": 12444
    # }
    
    articleNumber = request.json["articleNumber"]
    articleMHD = request.json["mhd"]
    
    dbSearchResult = jsondb.reSearch("articleNumber", articleNumber)
    
    if len(dbSearchResult) == 1:
        
        mhd = datetime.strptime(articleMHD, "%Y-%m-%d").date()
        MHDLeftDays = days_between(mhd, date.today())
        article = dbSearchResult[0]       

        if mhd < date.today():

            return Response(
                "MHD reached",
                status=400,
            )

        elif MHDLeftDays <= article['PaybackMinAge']:
            returnPaybackPoints = (article['PaybackMinAge'] - MHDLeftDays) * article['PaybackPerDay']
                
            res = {
                'paybackPoints': returnPaybackPoints,
                'productName': article['productName'],
                'mhd': str(mhd),
                'mhdLeftDays': MHDLeftDays
            }
            
            return jsonify(res)
        else:
            return Response(
                "Earntime not reached",
                status=400,
            )

        #return jsonify(dbSearchResult[0])
    elif len(dbSearchResult) > 1:
        return Response(
            "Multiple Articles with this ArticleNumber found - Contact your Database-Administrator :D",
            status=400,
        )
    else:
        return Response(
            "Article not found",
            status=400,
        )

    

@app.route('/api/v1/echo', methods=['POST'])
def echo():
   return jsonify(request.json)

@app.route('/api/v1/getDB', methods=['GET'])
def getDB():
     return jsonify(jsondb.getAll())





if __name__ == "__main__":
    # if app.run debug=True - initializeDB run twice
    date.today()
    initializeDB()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    