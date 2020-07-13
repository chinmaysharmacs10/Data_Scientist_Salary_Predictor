import requests
from input_data import data_in

# api-endpoint
URL = 'http://127.0.0.1:5000/predict'

# make a dictionary of parameters to be sent to API
headers = {"Content-Type": "application/json"}
# data is the input data to the API
data = {"input": data_in}

# Run the server in another terminal by executing the wgsi.py file; then get response for the request

# send a get request and save response as response object
r = requests.get(URL,headers=headers,json=data)

# extract data in json format
predicted_value = r.json()
print(predicted_value)    # this is the predicted value for our input data
