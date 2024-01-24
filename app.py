from flask import Flask, render_template, request, jsonify
from pyln.client import LightningRpc
import os
import random

app = Flask(__name__)

# Replace 'rpc_user', 'rpc_password', and 'rpc_path' with your LND node's actual details.
rpc_interface = LightningRpc("rpc_user:rpc_password@localhost:10009")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        bet_amount = int(request.form['bet_amount'])
        invoice = rpc_interface.invoice(bet_amount, 'Paiement pour le jeu de pile ou face')
        return render_template('play.html', invoice=invoice, bet_amount=bet_amount)
    return render_template('play.html')

@app.route('/result', methods=['POST'])
def result():
    user_choice = request.form['choice']
    server_choice = random.choice(['pile', 'face'])
    bet_amount = int(request.form['bet_amount'])
    
    if user_choice == server_choice:
        result = "Vous avez de la chance ! Vous avez gagné."
    else:
        result = "Dommage, vous avez perdu."

    return render_template('result.html', user_choice=user_choice, server_choice=server_choice, result=result, bet_amount=bet_amount)

if __name__ == '__main__':
    app.run(debug=True)
