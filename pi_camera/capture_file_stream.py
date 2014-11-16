import time
import picamera
import io

camera = picamera.PiCamera()
#camera.resolution = (1296,972)
camera.resolution = (640, 480)
camera.start_preview()
# Camera warm-up time
time.sleep(2)
try:
    while True:
        print time.time()
        stream = io.BytesIO()
        camera.capture(stream, 'jpeg')
        time.sleep(1.0/5.0)
finally:
        camera.close()
