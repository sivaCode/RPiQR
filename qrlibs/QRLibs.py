
__author__ = 'siva'

from PIL import Image as PILImage
import FileHandle
import datetime
import zbarlight
import cv2


def QRReader(file_path = './out.png'):
    start = datetime.datetime.utcnow()
    with open(file_path, 'rb') as image_file:
        image = PILImage.open(image_file)
        image.load()
    codes = zbarlight.scan_codes('qrcode', image)
    print('QR codes: %s' % codes)
    print(datetime.datetime.utcnow()-start)


def DecodeQRImage(CVImage):
    #start = datetime.datetime.utcnow()
    codes = None
    if not CVImage == None :
        image = PILImage.fromarray(CVImage)
        codes = zbarlight.scan_codes('qrcode', image)
        #print('QR codes: %s' % codes)
    #print(datetime.datetime.utcnow()-start)
    return codes

def readQRFromCamera():
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0)
    if cam.isOpened(): # try to get the first frame
        fps = cam.get(cv2.cv.CV_CAP_PROP_FPS)
        rval, frame = cam.read()
    else:
        rval = False
    #FileHandle.writetoFile("./results/QRdata.csv","FrameNumber,Time(Seconds)")
    while rval:
        qrData = DecodeQRImage(frame)
        if qrData is None :
            print "No QR Code identified"
        else:
            print('QR codes: %s, Type %s' %(qrData,type(qrData)))
            if not qrData[0] == '' :
                qrvals = qrData[0].split(",")
                #cv2.putText(frame,'Video Frame identified # : {0} , Current video Duration # : {1} , playing : {2}'.format(qrvals[0],qrvals[0],qrvals[0]),(10,500), font, 0.5,(255,0,0),2)
                cv2.putText(frame,'Video Data # : {0} '.format(qrData[0]),(100,850), font, 2,(0,0,255),2)
                FileHandle.writetoFile("./results/QRdata.csv","{0}\n".format(qrData[0]))
        cv2.imshow("VIPER Video Test Automation", frame)
        # read teh next frame
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyAllWindows()
