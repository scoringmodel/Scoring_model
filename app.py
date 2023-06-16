from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas as pd
import json

app = Flask('__name__')

payload = {}

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/output/', methods=['GET', 'POST'])
def output():
    #if request.method == 'POST':
    loan = request.form.get('loan')
    mortdue = request.form.get('mortdue')
    value = request.form.get('value')
    job = request.form.get('job')
    yoj = request.form.get('yoj')
    delinq = request.form.get('delinque')
    derog = request.form.get('derog')
    clage = request.form.get('clage')
    reason = request.form.get('reason')
    ninq = request.form.get('ninq')
    clno = request.form.get('clno')
    debtinc = request.form.get('debtinc')       

    payload['JOB']= job
    payload["YOJ"]= yoj
    payload["DELINQ"]= delinq
    payload["CLNO"]=  clno
    payload["REASON"]=  reason
    payload["VALUE"]= value
    payload["CLAGE"]= clage
    payload["DEBTINC"]= debtinc
    payload["MORTDUE"]= mortdue
    payload["LOAN"]= loan
    payload["NINQ"]= ninq
    payload["DEROG"]= derog
    
    response = requests.post('http://demo-ml.polymatica.ru/sroring_hse/api/v1/execute/models/', json=payload)
    df_scoring_model=pd.json_normalize(json.loads(json.dumps(response.json())))
    if df_scoring_model['BAD'][0] == 0:
        result = 'Application is approved'
    else:
        result = 'Application is not approved'
    
    return render_template('output.html', name = result)    
    #return render_template('output.html', name = payload)



if __name__== "main":
    app.run(host="0.0.0.0", port=5000)
