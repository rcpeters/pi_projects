from flask import Flask
from flask import send_file
import io
import picamera
import threading
import time
from time import sleep

last_stream = io.BytesIO()
camera =  picamera.PiCamera()
camera.resolution =  (800, 600)
camera_running = True

def record_loop():
    global camera_running
    global last_stream
    try:
        while camera_running:
            print 'start capture ' + str(time.time())
            tmp_stream = io.BytesIO()
            camera.start_recording(tmp_stream, format='h264', quality=25)
            camera.wait_recording(8)
            camera.stop_recording()
            tmp_stream.seek(0)
            old_stream = last_stream
            last_stream = tmp_stream
            old_stream.close()
            io.open('/tmp/test.h264', 'wb').write(last_stream.read())
            print 'end capture ' + str(time.time())
            time.sleep(0.0001)
    finally:
        camera.close()

cam_thread = threading.Thread(target=record_loop)
cam_thread.start()

def camera_exit():
    global camera_running
    print 'Shutting down camera'
    camera_running = False

app = Flask(__name__)

@app.route('/')
def hello_world():
        return 'Hello World!'

@app.route('/loop.h264')
def loop():
     global lastStream
     last_stream.seek(0)
     return send_file(last_stream,
          attachment_filename='loop.h264',
          mimetype='video/h264')

if __name__ == '__main__':
     app.run(host='0.0.0.0')
     camera_exit()
     print "exiting"


