## Problem Statement
Using real time audio stream collected over a microphone, we aim to classify sound as cough or not cough. 

### Getting Started
#### Prerequisites
XXX
#### Installation
XXX

### Datasets
* [ESC-50](https://github.com/karolpiczak/ESC-50)
* [Freesound](www.freesound.org)
* [Soundsnap](www.soundsnap.com)

### Pre-Processing
`Librosa` is a Python package for music and audio processing which allows us to load audio as a numpy array for analysis and manipulation. For much of the preprocessing we use Librosa’s `load` function, which converts the sampling rate to 22.05 KHz, normalizes the data so the bit-depth values range between -1 and 1 and flattens the audio channels into mono.

### Feature Extraction
For each audio file in the dataset, we extract Mel-Frequency Cepstral Coefficients or MFCCs (so we have an image representation for each audio sample) and store it in a Pandas Dataframe along with it’s classification label. For this we use Librosa’s `mfcc` function which generates an MFCC from time series audio data. MFCCs use a quasi-logarithmic spaced frequency scale, which is similar to how the human auditory system processes sounds.

### Model
A Convolutional Neural Network (CNN) model was built and trained using the datasets listed. CNNs make good classifiers and perform particularly well with image classification tasks due to their feature extraction and classification parts. We use a `Sequential` model, starting with a simple model architecture, consisting of `Conv2D` convolution layers, with the final output layer being a `Dense` layer. The output layer has n nodes `num_labels` which matches the number of possible classifications.

##### The Web Application is deployed on Microsoft Azure, and can be accessed via 
<a href="https://pnuemosenseai.azurewebsites.net/" target="_blank">https://pnuemosenseai.azurewebsites.net/</a>
Edit : We have stopped hosting the website as of now.

### Deployment
To run the model on your <b>local machine</b>, you can download this repository as a zip file, clone or pull it by using the command
```
$ git pull https://github.com/mitali3112/Cough-Detector.git
```
or
```
$ git clone https://github.com/mitali3112/Cough-Detector.git
```
Requirements can be installed using the command (from the command-line)
```
$ pip install -r requirements.txt
```

Then, navigate to the project folder and execute the command
```
$ python app.py
```

to deploy the app locally. 

On your web browser go to <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

#### Built With
* Flask
* Librosa
* Keras
* Tensorflow
* Media Recorder API
* Bootstrap 4

### Contributers
* **Mitali Sheth**
* **Aparna Ranjith**
* **Mansi Parashar**
* **Gunveen Batra**
* **Sruti Dammalapati**

### Acknowledgements 
We thank B-Aegis Life Sciences for the opportunity of collaboration.
