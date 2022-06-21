from flask import Flask, render_template, request, jsonify
from pysondb import db
import os

app = Flask(__name__)
jsondb=db.getDb("db.json")

def initializeDB():
    jsondb.add({"internalID": 1, "articleNumber": 1337-1, "productName": "Hack-Kekse", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 2, "articleNumber": 1337-2, "productName": "Fritz-Cola", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 3, "articleNumber": 1337-3, "productName": "Clubmate", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 4, "articleNumber": 1337-4, "productName": "Computerchips", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 5, "articleNumber": 1337-5, "productName": "Schoko-RAM-Riegel Zartbitter-Nuss", "PaybackPerDay": 10, "PaybackMinAge": 7})
    jsondb.add({"internalID": 6, "articleNumber": 1337-6, "productName": "SATA-Schnitten", "PaybackPerDay": 10, "PaybackMinAge": 7})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/getPayback', methods=['POST'])
def calculatePaybackPoints():
    return jsonify(
       id= 1655801622,
       dbId="DBID",
       userId=1337,
       mhd="23-06-2022",
       days=2,
       paybackpoints=6,
       productName="Hack-Kekse"
    )

@app.route('/api/v1/echo', methods=['POST'])
def echo():
   return jsonify(request.json)

@app.route('/api/v1/getDB', methods=['GET'])
def getDB():
     return jsonify(jsondb.getAll())

if __name__ == "__main__":
    # if app.run debug=True - initializeDB run twice
    initializeDB()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    