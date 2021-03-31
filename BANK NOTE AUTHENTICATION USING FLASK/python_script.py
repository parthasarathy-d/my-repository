# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 14:40:04 2021

@author: Designer
"""

import pandas as pd
import numpy as np
import pickle
from flask import Flask,request, render_template

app = Flask(__name__)
pickle_in = open('classifier.pkl','rb')
classifier = pickle.load(pickle_in)


@app.route('/')
def welcome():
    return "Welcome all"

@app.route('/predict', methods =["GET", "POST"])
def bank_note_authenticatoin():
    if request.method == "POST":
        variance = request.form.get('variance')
        skewness = request.form.get('skewness')
        curtosis = request.form.get('curtosis')
        entropy = request.form.get('entropy')
        prediction = classifier.predict([[variance,skewness,curtosis,entropy]])
        
        if str(prediction) == "[0]":
            return render_template("output.html")
        else:
            return render_template("outputfalse.html")

if __name__ == '__main__':
    app.run()