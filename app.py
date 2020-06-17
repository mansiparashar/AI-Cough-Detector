from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import librosa.display
import librosa
import base64
#from keras.models import model_from_json
from tensorflow.keras.models import model_from_json



os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from flask import jsonify

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Define a flask app
app = Flask(__name__)

#Saving filenames
count = "0"

# load json and create model
json_file = open(os.path.join(os.getcwd(),"model_6\model_sd_6.json"), 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(r".\model_6\model_sd_6.h5")
print("Loaded model from disk")

print('Model loaded. Check http://127.0.0.1:5000/')


def extract_features(file_name):
    
    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
    print("Audio File Loaded")
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs = mfccs[:40,:216]
         
    return mfccs

def print_prediction(model,file_name):

    prediction_feature = extract_features(file_name) 
    print("Features Extracted")
    prediction_feature = librosa.util.fix_length(prediction_feature, 216)
    prediction_feature = prediction_feature.reshape(1, 40, 216, 1)
    predicted_vector = model.predict_classes(prediction_feature)

    return predicted_vector


def getLabel(labelid):

    labelname = ""
    labels = {'airplane': 0, 'breathing': 1, 'car_horn': 2, 'cat': 3, 'chainsaw': 4, 'chirping_birds': 5,
 'church_bells': 6, 'clapping': 7, 'clock_alarm': 8, 'coughing': 9, 'cow': 10, 'crow': 11, 'crying_baby': 12,
 'dog': 13, 'door_wood_knock': 14, 'engine': 15, 'fireworks': 16, 'helicopter': 17, 'laughing': 18,
 'laughter': 19, 'rain': 20, 'siren': 21, 'speech': 22, 'thunderstorm': 23, 'train': 24, 'wind': 25}

    for name,i in labels.items():
        if i == labelid:
            labelname = name
    return labelname

@app.route('/', methods=['GET'])

def index():
    # Main page
    return render_template('index1.html')


@app.route('/index1', methods=['POST'])

def api_message():
    global count
    filename = count + ".wav"
    if request.method == "POST":
        content = request.json
        
        try:

            bstring = content["message"]
            data = base64.b64decode(bstring)
            f = open('./audios/'+filename, 'wb')
            f.write(data)
            f.close()
        except:
            pass
        
        count = str(int(count)+1)

        fname = "audios"+"\\" + filename
        filepath = os.path.abspath(fname)
        #print("Check for this:",filepath)
        #print(os.path.isfile(filepath))

        if int(count) > 10:
            count = "0"

        if (os.path.isfile(filepath)):
            print(filepath)
            v = print_prediction(loaded_model,filepath)
            
            print("The predicted class number is:", v[0], '\n')
            labelid = np.int16(v[0]).item()
            labelname = getLabel(labelid) 
            print("Label predicted: ",labelname)
            os.remove(filepath)
            return jsonify({"label":labelname})
            
        else:
            print("filepath ERROR")

          
        return jsonify({"label":"Message received"})
    


if __name__ == '__main__':
    
    
    app.run(debug=True)
    

