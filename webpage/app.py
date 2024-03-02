import flask
from flask import Flask, render_template, request, jsonify, Response
import numpy as np
import mediapipe as mp
import cv2 as cv
import matplotlib.pyplot as pyplot
import matplotlib.image as mping
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

app = Flask(__name__)

class FlaskPublisher(Node):

    def __init__(self):
        super().__init__('FlaskPublisher')
        self.publisher_ = self.create_publisher(Twist, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        self.publisher_.publish(msg)
        print(msg)


@app.route('/')
def index():
    return render_template('index.html')

def main(args=None):
    rclpy.init(args=args)

    flask_publisher= FlaskPublisher()

    rclpy.spin(flask_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    flask_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    app.run(debug=True)
    main()

