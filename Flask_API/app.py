import flask
from flask import Flask, jsonify, request
import json
import pickle
import numpy as np


# function to load our pickled model
def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

app = Flask(__name__)
@app.route('/predict', methods=['GET'])    # route is like pages on website; when /predict requested then respond by an html page
def predict():
    # parse input features from the request
    request_json = request.get_json()
    x = request_json['input']

    # reshape data to input it to model for prediction
    # this is just one data point with all necessary parameters for prediction
    x_input = np.array(x).reshape(1,-1)

    # load the pickled prediction model
    model = load_models()
    prediction = model.predict(x_input)[0]

    response = json.dumps({'response': prediction})    # gives the prediction made by the model as response
    return response, 200

if __name__ == '__main__':
    application.run(debug=True)