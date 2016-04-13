from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image as PILImage
import zbarlight
import cv2
import time

def DecodeQRImage(CVImage):
    #start = datetime.datetime.utcnow()
    codes = None
    print "inside QR read"
    if not CVImage == None :
        image = PILImage.fromarray(CVImage)
        codes = zbarlight.scan_codes('qrcode', image)
        #print('QR codes: %s' % codes)
    return codes



camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera,size=(640,480,))

time.sleep(0.2)
font = cv2.FONT_HERSHEY_SIMPLEX
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array # CV Image in BGR format
    print "img convert"
    qrimage = PILImage.fromarray(image)
    print "img zbar check"
    codes = zbarlight.scan_codes('qrcode', qrimage)
    print "img shape check"
    print(image.shape)
    #code = DecodeQRImage(image)
    cv2.putText(image,codes, (100, 200), font, 2, (0, 0, 255), 2)
    cv2.imshow("Pi Camera Feed", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
