from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import time

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera,size=(640,480,))

time.sleep(0.2)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array # CV Image in BGR format
	#print(image.shape)
	cv2.imshow("Pi Camer Feed", image)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord("q"):
		break

cv2.destroyAllWindows()
