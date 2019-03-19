import cv2
import numpy as np

def nothing(x):
    pass
    
cap=cv2.VideoCapture(0)
cv2.ocl.setUseOpenCL(False)
cv2.namedWindow('test1')

cv2.createTrackbar('RL','test1',0,255,nothing)
cv2.createTrackbar('GL','test1',0,255,nothing)
cv2.createTrackbar('BL','test1',0,255,nothing)
switch = '0:OFF \n 1 : ON' 
cv2.createTrackbar(switch,'test1',0,1,nothing)

fgbg=cv2.createBackgroundSubtractorMOG2()

global rl
global gl
global bl
global rlp
global glp
global blp
global flag
global empty
global block

first_block_l=[70,30]
first_block_r=[190,150]
second_block_l=[260,30]
second_block_r=[380,150]
third_block_l=[450,30]
third_block_r=[570,150]
fourth_block_l=[70,180]
fourth_block_r=[190,300]
fifth_block_l=[260,180]
fifth_block_r=[380,300]
sixth_block_l=[450,180]
sixth_block_r=[570,300]
seventh_block_l=[70,330]
seventh_block_r=[190,450]
eighth_block_l=[260,330]
eighth_block_r=[380,450]
ninth_block_l=[450,330]
ninth_block_r=[570,450]

main_gesture=[]
gesture=[0]

empty=[]
empty1=[0]

while cv2.waitKey(1) != 103 and cap.isOpened():
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    rl=cv2.getTrackbarPos('RL','test1')
    gl=cv2.getTrackbarPos('GL','test1')
    bl=cv2.getTrackbarPos('BL','test1')
    s=cv2.getTrackbarPos(switch,'test1')
    
    lower_blue=np.array([bl,gl,rl])
    upper_value=np.array([255,255,255])
    
    mask_blue=cv2.inRange(hsv,lower_blue,upper_value)
    
    res_blue=cv2.bitwise_and(frame,frame,mask=mask_blue)
    cv2.imshow('test1',res_blue)
    
while cv2.waitKey(1) != 27 and cap.isOpened():
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    first=cv2.rectangle(frame,(first_block_l[0],first_block_l[1]),(first_block_r[0],first_block_r[1]),(0,0,255),1)
    second=cv2.rectangle(frame,(second_block_l[0],second_block_l[1]),(second_block_r[0],second_block_r[1]),(0,0,255),1)
    third=cv2.rectangle(frame,(third_block_l[0],third_block_l[1]),(third_block_r[0],third_block_r[1]),(0,0,255),1)
    fourth=cv2.rectangle(frame,(fourth_block_l[0],fourth_block_l[1]),(fourth_block_r[0],fourth_block_r[1]),(0,0,255),1)
    fifth=cv2.rectangle(frame,(fifth_block_l[0],fifth_block_l[1]),(fifth_block_r[0],fifth_block_r[1]),(0,0,255),1)
    sixth=cv2.rectangle(frame,(sixth_block_l[0],sixth_block_l[1]),(sixth_block_r[0],sixth_block_r[1]),(0,0,255),1)
    seventh=cv2.rectangle(frame,(seventh_block_l[0],seventh_block_l[1]),(seventh_block_r[0],seventh_block_r[1]),(0,0,255),1)
    eighth=cv2.rectangle(frame,(eighth_block_l[0],eighth_block_l[1]),(eighth_block_r[0],eighth_block_r[1]),(0,0,255),1)
    ninth=cv2.rectangle(frame,(ninth_block_l[0],ninth_block_l[1]),(ninth_block_r[0],ninth_block_r[1]),(0,0,255),1)
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    lower_blue=np.array([bl,gl,rl])
    upper_value=np.array([255,255,255])
    
    mask_blue=cv2.inRange(hsv,lower_blue,upper_value)
    
    res_blue=cv2.bitwise_and(frame,frame,mask=mask_blue)
    
    bnw_blue=cv2.cvtColor(res_blue,cv2.COLOR_BGR2GRAY)
    
    ret,thresh_blue=cv2.threshold(bnw_blue,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    fgmask_blue=fgbg.apply(thresh_blue)
    
    blur_blue=cv2.GaussianBlur(fgmask_blue,(5,5),0)
    
    contimage,contours_blue,hierarchy=cv2.findContours(blur_blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    for i in range(len(contours_blue)):
        cnt1=np.array(contours_blue[i])
    nothing

    hull_blue=cv2.convexHull(cnt1,returnPoints=False)
    defects_blue=cv2.convexityDefects(cnt1,hull_blue)
    (x,y),radius_blue=cv2.minEnclosingCircle(cnt1)
    center_blue=(int(x),int(y))
    radius_blue=int(radius_blue)
    rect_blue=cv2.minAreaRect(cnt1)
    box_blue=cv2.boxPoints(rect_blue)
    box_blue=np.int0(box_blue)
    final_blue=cv2.circle(frame,center_blue,radius_blue,(0,255,0),2)
    final2_blue=cv2.circle(frame,center_blue,10,(255,0,0),2)
    final3_blue=cv2.drawContours(frame,[box_blue],0,(0,0,255),2)

    if contours_blue==empty:
        if gesture==empty1:
            pass
        else:
            main_gesture.append(gesture)
        gesture=[0]
    else:
        if first_block_l[0]<center_blue[0]<first_block_r[0] and first_block_l[1]<center_blue[1]<first_block_r[1]:
            block=1
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif second_block_l[0]<center_blue[0]<second_block_r[0] and second_block_l[1]<center_blue[1]<second_block_r[1]:
            block=2
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif third_block_l[0]<center_blue[0]<third_block_r[0] and third_block_l[1]<center_blue[1]<third_block_r[1]:
            block=3
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif fourth_block_l[0]<center_blue[0]<fourth_block_r[0] and fourth_block_l[1]<center_blue[1]<fourth_block_r[1]:
            block=4
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif fifth_block_l[0]<center_blue[0]<fifth_block_r[0] and fifth_block_l[1]<center_blue[1]<fifth_block_r[1]:
            block=5
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif sixth_block_l[0]<center_blue[0]<sixth_block_r[0] and sixth_block_l[1]<center_blue[1]<sixth_block_r[1]:
            block=6
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif seventh_block_l[0]<center_blue[0]<seventh_block_r[0] and seventh_block_l[1]<center_blue[1]<seventh_block_r[1]:
            block=7
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif eighth_block_l[0]<center_blue[0]<eighth_block_r[0] and eighth_block_l[1]<center_blue[1]<eighth_block_r[1]:
            block=8
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        elif ninth_block_l[0]<center_blue[0]<ninth_block_r[0] and ninth_block_l[1]<center_blue[1]<ninth_block_r[1]:
            block=9
            if gesture[len(gesture)-1] != block:
                gesture.append(block)
        else:
            pass
    
    print(gesture)
    #print(main_gesture)
    if gesture==[0,5,3,2,1,4,7,8,9]:
        img=cv2.imread('c.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    elif gesture==[0,5,1,4,7,8,9]:
        img=cv2.imread('l.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    elif gesture==[0,5,3,2,1,4,7,8,9,6,5]:
        img=cv2.imread('g.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    elif gesture==[0,5,2,5,8]:
        img=cv2.imread('i.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    elif gesture==[0,5,1,2,5,8,7]:
        img=cv2.imread('j.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    elif gesture==[0,5,1,2,3,6,9,8,7,4,1]:
        img=cv2.imread('o.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    elif gesture==[0,5,7,4,1,2,3,6,5]:
        img=cv2.imread('p.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    elif gesture==[0,5,3,2,1,4,5,6,9,8,7]:
        img=cv2.imread('s.jpg')
        cv2.imshow('result',img)
        cv2.waitKey()
        break
    cv2.imshow('test1',res_blue)
    cv2.imshow('final',final_blue)
    cv2.imshow('final',final2_blue)
    cv2.imshow('final',final3_blue)
    cv2.imshow('final',first)
    cv2.imshow('final',second)
    cv2.imshow('final',third)
    cv2.imshow('final',fourth)
    cv2.imshow('final',fifth)
    cv2.imshow('final',sixth)
    cv2.imshow('final',seventh)
    cv2.imshow('final',eighth)
    cv2.imshow('final',ninth)
    cv2.resizeWindow('final',640,480)

cap.release()
cv2.destroyAllWindows()
