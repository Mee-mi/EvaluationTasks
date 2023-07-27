#Python Practice Problem - LOAD BLANCER

 

#Assume you have a flask API, that deals different ML models, but due to GPU/CPU/RAM restrictions, it can load only 2 ML model at once. This flask API has two following routes.

#1. '/get_loaded_models' This will return the two loaded models info at that time (code is already provided below)

#2. '/process_request' This will process the request, using the required model, specified in request against key 'model'. If that model is already loaded, the API will process that request using loaded model. Otherwise the API will load this model at the place of the one model which is previously loaded and has less frequently requested.

#You are required to write its load balancer. Your load balancer should be able to record the number of requests processed by all models, so that it can intelligently load new model on the place of less frequent model.  Sample code with dummy processing is provided below. You have to write its load balancer function. You may also also re structure the code, or change in code according to your need. But those changes should not change any previous functionality.

 
import traceback
from flask import Flask, request, render_template, redirect, url_for

class ML:
    def __init__(self):
        self.available_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }
        self.model_frequency = {
           "shoe_detection": 1, "car_detection": 1, "face_detection": 0, "cloth_detection": 0,
           "signal_detection": 0, "water_level_detection": 0, "missile_detection": 0
        }
        self.loaded_models_limit = 2
        self.loaded_models = {
            model: self.load_weights(model)
            for model in list(self.available_models)[:self.loaded_models_limit]
        }

    def load_weights(self, model):
        return self.available_models.get(model, None)

    def load_balancer(self, new_model):
        if new_model in self.loaded_models:
            self.model_frequency[new_model] += 1
        else:
            if len(self.loaded_models) < self.loaded_models_limit:
                self.loaded_models[new_model] = self.load_weights(new_model)
            else:
                least_freq_model = min(self.model_frequency, key=self.model_frequency.get)
                if self.model_frequency[new_model] > self.model_frequency[least_freq_model]:
                    del self.loaded_models[least_freq_model]
                    self.loaded_models[new_model] = self.load_weights(new_model)
        self.model_frequency[new_model] += 1

app = Flask(__name__)
ml = ML()

@app.route('/get_loaded_models', methods=['GET', 'POST'])
def get_loaded_models():
    return render_template('index.html', models=ml.loaded_models)

@app.route('/request_model')
def get_request_model():
    return render_template('index.html')

@app.route('/process_request', methods=['GET', 'POST'])
def process_request():
    try:
        if request.method == 'POST':
            model = request.form['model']
            if model not in ml.loaded_models:
                ml.load_balancer(model)
                return "processed , " + ml.loaded_models[model]
            else:
                return redirect(url_for('get_loaded_models'))
    except:
        return str(traceback.format_exc())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
