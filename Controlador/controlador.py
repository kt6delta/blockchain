from flask import Flask, jsonify
# Building a Flask based Web App for interacting with the blockchain
app = Flask(__name__)


# Creating a blockchain based on architecture defined
blockchain = Blockchain()


# Welcome page
@app.route('/', methods=['GET'])

def welcome():
    return wl


# Mining the blockchain
@app.route('/mineblock', methods=['GET'])

def mineblock():
    return jsonify(response), 200


# Gwtting the full blockchain displayed in Postman
@app.route('/getchain', methods=['GET'])

def getchain():
    response = {'chain': blockchain.chain,
                'len': len(blockchain.chain)}
    return jsonify(response), 200


# Validating the Blockchain
@app.route('/validate', methods=['GET'])

def validate():
    return jsonify(response), 200


# Running the Web App
app.run(host='0.0.0.0', port=5000)