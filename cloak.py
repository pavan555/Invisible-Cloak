import cv2
import time
import datetime as d
import numpy as np
import argparse
import imutils

ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",help="Path to Video(optional)")
args=vars(ap.parse_args())

if not args.get("video",False):
	camera=cv2.VideoCapture(0)
else:
	camera=cv2.VideoCapture(args["video"])

time.sleep(3)

#FOUR CHRACTER CODE (FOURCC) define codec for video
fourcc=cv2.VideoWriter_fourcc('m','p','4','v')
#recording the video
out=cv2.VideoWriter("~/Desktop/Cloak1.mov",fourcc,15,(720,480))

bg=0
count=0

red_lower1 = np.array([0,120,70])
red_upper1 = np.array([10,255,255])
red_lower2 = np.array([170,120,70])
red_upper2 = np.array([180,255,255])

lower_blue=np.array([86,31,4])
upper_blue=np.array([220,88,50])

#For capturing the Background

def backg():
    for i in range(20):
        (grabbed,BackGround)=camera.read()
    bg=BackGround
    return bg
    
#reading background in range of 20
bg=np.flip(backg(),axis=1)
while True:
    (grabbed,frame)=camera.read()
    count+=1
    
    if args.get("video") and not grabbed:
        break
    
    frame=np.flip(frame,axis=1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    #maskb= cv2.inRange(gray,lower_blue,upper_blue) + cv2.inRange(gray,np.array([110,50,50]),np.array([130,255,255]))
    mask=cv2.inRange(gray,red_lower1,red_upper1)+cv2.inRange(gray,red_lower2,red_upper2)
    
    #mask=cv2.bitwise_or(maskb,maskr)
    mask=cv2.erode(mask,np.ones((9,9),dtype=np.uint8),iterations=2)
    mask=cv2.dilate(mask,np.ones((9,9),dtype=np.uint8),iterations=1)
    
    #mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)
    #mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=1)
    
    maskNegate=cv2.bitwise_not(mask)
    
    
    result1=cv2.bitwise_and(frame,frame,mask=maskNegate)
    result2=cv2.bitwise_and(bg,bg,mask=mask)
    final=cv2.addWeighted(result2,1,result1,1,0)#imageBlending
    final=cv2.resize(final,(720,480))
    cv2.putText(final,d.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
    cv2.imshow("Harry Potter Invisible Cloak",final)
    
    out.write(final)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    if count%500==0:
        bg=np.flip(backg(),axis=1)
camera.release()
out.release()
cv2.destroyAllWindows()
