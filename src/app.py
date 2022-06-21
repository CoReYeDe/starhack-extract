from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)