from flask import FLask, render_template, request, jsonify, Response
import numppy as np
import mediapipe as mp
import cv2 as cv
import matplotlib.pyplot as pyplot
import matplotlib.image as mping
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
