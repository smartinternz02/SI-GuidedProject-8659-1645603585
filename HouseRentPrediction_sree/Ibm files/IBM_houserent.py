# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:51:32 2021

@author: HP
"""
from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import os
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "94Sb4mTPK3QgBVQl-QFNydq33hoivC3SUYR9H4Z_8bhX"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app=Flask(__name__,template_folder="templates")


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')
@app.route('/pred',methods=['GET'])
def page():
    return render_template('upload.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    input_feature = [float(x) for x in request.form.values()]
    
   
    feature_name=["city","BHKS","sqft_per_inch","build_up_area","Type_of_property","deposit"]
    
    payload_scoring = {"input_data":[{"fields":feature_name,"values":[input_feature]}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/21a2ec16-011e-4754-8228-cb02cfaaeb6d/predictions?version=2021-12-15', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    
    pred= response_scoring.json()
    print(pred)
    
    output = pred['predictions'][0]['values'][0][0]
    print(output)

    output=output[0]    #np.exp(predictions)
    output = np.exp(output)
    output = np.round(output)
    print(output)
    return render_template('upload.html', prediction_text= 'House Rent is Rs {} '.format((output)))

    
if __name__ == '__main__':
      app.run(debug=False)










# NOTE: manually define and pass the array(s) of values to be scored in the next line

payload_scoring = {"input_data": [{"fields": ["city","BHKS","sqft_per_inch","build_up_area","Type_of_property","deposit"], "values": [[5,1.0,470.0,1,2,11.225257]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/21a2ec16-011e-4754-8228-cb02cfaaeb6d/predictions?version=2021-12-15', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())