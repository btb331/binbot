from flask import Flask, render_template, Response, request
import requests

baseUrl = "http://192.168.1.233/"

app = Flask(__name__)

@app.route("/control", methods=["GET", "POST"])
def gen():
    return render_template('control.html')


@app.route("/controlforward", methods=["GET", "POST"])
def fwd():
    url_params = request.args 
    try: 
        step = url_params['step'] 
    except KeyError: 
        step = str(0)
    requests.get(baseUrl + "forward?step=" + step)
    return "OK"

@app.route("/controlbackward", methods=["GET", "POST"])
def bwd():
    url_params = request.args 
    try: 
        step = url_params['step'] 
    except KeyError: 
        step = str(0)
    requests.get(baseUrl + "backward?step=" + step)
    return "OK"

@app.route("/controlleft", methods=["GET", "POST"])
def left():
    url_params = request.args 
    try: 
        step = url_params['step'] 
    except KeyError: 
        step = str(0)
    try:
        pivot = url_params['pivot'] 
    except KeyError: 
        pivot = 'false'
    requests.get(baseUrl + "left?step=" + step + "&pivot=" + pivot)
    return "OK"

@app.route("/controlright", methods=["GET", "POST"])
def right():
    url_params = request.args 
    try: 
        step = url_params['step'] 
    except KeyError: 
        step = str(0)
    try: 
        pivot = url_params['pivot'] 
    except KeyError: 
        pivot = 'false'
    requests.get(baseUrl + "/right?step=" + step + "&pivot=" + pivot)
    return "OK"

@app.route("/controlstop", methods=["GET", "POST"])
def stop():
    requests.get(baseUrl + "stop")
    return "OK"
