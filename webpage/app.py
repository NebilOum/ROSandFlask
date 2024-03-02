import flask
from flask import Flask, render_template, request, jsonify, Response
from roslibpy import Header, Message, Ros, Time, Topic
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


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutons.holistic
mp_pose = mp.solutions.pose

class FlaskPublisher(Node):

    def __init__(self):
        super().__init__('FlaskPublisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.msg=Twist()
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.publisher_.publish(self.msg)

def topic_pubsub():
    context = dict(wait=threading.Event(),counter=0)

    ros = Ros("127.0.0.1",9090) ##local host
    ros.run()

    listener = Topic(ros, "/webChatter", "std_msgs/String")
    publisher =Topic(ros, "/webChater", "std_msgs/String")

    def receive_message(message):
        context["counter"] += 1
        assert message["data"] == "hello world","Unexpected message content"

        if context["counter"] ==3:
            listener.unsubscrive()
            context["wait"].set()
    def start_sending():
        while True:
            if context["counter"] >= 3:
                break
            publisher.publish(Message({"data": "hello world"}))
            time.sleep(0.1)
        publisher.unadvertise()

    def start_receiving():
        listener.subscribe(receive_message)

    t1 = threading.Thread(target=start_receiving)
    t2 = threading.Thread(target=start_sending)

    t1.start()
    t2.start()

    if not context["wait"].wait(10):
        raise Exception

    t1.join()
    t2.join()

    assert context["counter"] >= 3, "Expected at least 3 messages but got " + str(context["counter"])
    ros.close()
def detect_pose():
    camera= cv.VideoCapture(0)
    with mp_holistic.Holistic(min_detection_confidence= 0.5, min_tracking_condifence=0.5) as holistic:
        while camera.isOpened():
            ret, frame = cap.read()

            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = holistic.process(image)
            image =cv.cbtColor(frame, cv.COLOR_BGR2RGB)

            mp_drawing.draw_landmarks(frame,results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            cv.imshow('Raw Webcam Feed', image)

            if(cv.waitKey(10)) & (0xFF == ord('q')):
                break
    camera.release()
    cv.destroyAllWindows()

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

@app.route("/vidoeo_feed")
def video_feed():
    return Response(detect_pose(),miimetype = 'multipart/x-mixed-replace; boundary=frame')

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

