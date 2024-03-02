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
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.msg=Twist()
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.publisher_.publish(self.msg)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buttons', methods=['GET', 'POST'])
def buttons():
    if 'forward' in request.form:
        flask_publisher.msg.linear.x=1.0
        flask_publisher.msg.angular.z=0.0
        flask_publisher.publisher_.publish(flask_publisher.msg)
    elif 'backward' in request.form:
        flask_publisher.msg.linear.x=-1.0
        flask_publisher.msg.angular.z=0.0
        flask_publisher.publisher_.publish(flask_publisher.msg)
    elif 'right' in request.form:
        flask_publisher.msg.linear.x=1.0
        flask_publisher.msg.angular.z=-0.5
        flask_publisher.publisher_.publish(flask_publisher.msg)
    elif 'left' in request.form:
        flask_publisher.msg.linear.x=1.0
        flask_publisher.msg.angular.z=0.5
        flask_publisher.publisher_.publish(flask_publisher.msg)
    elif 'stop' in request.form:
        flask_publisher.msg.linear.x=0.0
        flask_publisher.msg.angular.z=0.0
        flask_publisher.publisher_.publish(flask_publisher.msg)
    return render_template('buttons.html')

@app.route('/signal')
def signal():
    return render_template('signal.html')

@app.route('/path')
def path():
    return render_template('path.html')


def main(args=None):
    pass

    #rclpy.spin(flask_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    #flask_publisher.destroy_node()
    #rclpy.shutdown()


if __name__ == '__main__':
    rclpy.init(args=None)
    flask_publisher=FlaskPublisher()
    app.run(debug=True)
    flask_publisher.destroy_node()
    rclpy.shutdown()

