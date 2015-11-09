import ctypes
from flask import Flask, request, render_template
import gevent
import numpy as np
import cv2
import os, sys, inspect, time
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import base64
import struct
import array


app = Flask(__name__)

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_IMAGES)

@app.route('/')
def index():
    #return render_template('ShowImage.html')
    #return render_template('camera.html')
    return render_template('client.html')

@app.route('/websocket')
def handle_websocket():
    count = 0
    #wsock = request.environ['wsgi.websocket']
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        count += 1
        if(controller.is_connected):
            images = controller.images
            left_image = images[0]
            if(left_image.height != 0):
                image_buffer_ptr = left_image.data_pointer
                ctype_array_def = \
                    ctypes.c_ubyte*left_image.width*left_image.height
                as_ctype_array = \
                    ctype_array_def.from_address(int(image_buffer_ptr))
                as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
                viewImage = as_numpy_array[:,240:480]
                smallImage = cv2.resize(viewImage, (0,0), fx=0.25, fy=0.25)
                [height, width] = smallImage.shape
                sendImage = smallImage.reshape(1, height * width)
                b = buffer(sendImage.tostring())
                #barray = array.array('b', test)
                #packer = struct.Struct(test)

                wsock.send(b, binary=True)
        gevent.sleep(0.1)  # change delay to alter update speed

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
if __name__=="__main__":
    server = WSGIServer(("127.0.0.1", 8080), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()
