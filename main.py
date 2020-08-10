import numpy as np
import cv2
import time
import pyautogui
from directkeys import PressKey, ReleaseKey, MoveCursor, LeftClick
from directkeys import W, A, S, D, UP, DOWN, LEFT, RIGHT, CTRL, ENTER
# from draw_lanes import draw_lanes
from grabscreen import grab_screen, window_size
import win32gui

import pytesseract
# from pytesseract import image_to_string

HECHIZOS = [0,0]
H1 = [0,0]
H2 = [0,0]
INVENTARIO = [800, 190]
INV1 = [760, 240]
INV2 = [800, 240]
INV3 = [840, 240]
INV4 = [880, 240]


def roi(img, vertices):
    
    #blank mask:
    mask = np.zeros_like(img)   
    
    #filling pixels inside the polygon defined by "vertices" with the fill color    

    #returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked



def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    # processed_img =  cv2.Canny(original_image, threshold1 = 50, threshold2=300)
    # processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    
    # (0, -1, 1000, 749)
    # print(f'hambre: {processed_img[600,940]}')
    
    mask = np.zeros(processed_img.shape,np.uint8)
    # stats
    # mask[bbox[1]+500:bbox[3],bbox[0]+700:bbox[2]] = processed_img[bbox[1]+500:bbox[3],bbox[0]+700:bbox[2]]
    
    # screen
    mask[bbox[1]+188:bbox[3]-40,bbox[0]+10:bbox[2]-305] = processed_img[bbox[1]+188:bbox[3]-40,bbox[0]+10:bbox[2]-305]
    
    # text = pytesseract.image_to_string(processed_img, config='--psm 6')
    # print(text)

    # try:
        # l1, l2, m1,m2 = draw_lanes(original_image,lines)
        # cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        # cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    # except Exception as e:
        # print(str(e))
        # pass

    return mask #,original_image


dt = 0.05
def up():
    PressKey(UP)
    ReleaseKey(DOWN)
    ReleaseKey(LEFT)
    ReleaseKey(RIGHT)
    time.sleep(dt)
    ReleaseKey(UP)

def down():
    PressKey(DOWN)
    ReleaseKey(UP)
    ReleaseKey(LEFT)
    ReleaseKey(RIGHT)
    time.sleep(dt)
    ReleaseKey(DOWN)

def left():
    PressKey(LEFT)
    ReleaseKey(UP)
    ReleaseKey(DOWN)
    ReleaseKey(RIGHT)
    time.sleep(dt)
    ReleaseKey(LEFT)

def right():
    PressKey(RIGHT)
    ReleaseKey(UP)
    ReleaseKey(DOWN)
    ReleaseKey(LEFT)
    time.sleep(dt)
    ReleaseKey(RIGHT)



# for i in list(range(3))[::-1]:
    # print(i+1)
    # time.sleep(1)

def move_pescador(prev_screen, screen):
    diff = np.sum(prev_screen-screen)
    print (f'diff: {diff}')
    if diff !=0:
        left()
        time.sleep(.2)
        return True
    return False
        # exit()



if __name__ == '__main__':
        
    bbox = window_size('notepad')

    last_time = time.time()

    screen = grab_screen(bbox)
    processed_screen = process_img(screen)
    prev_screen = processed_screen
    while True:

        # # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # screen = grab_screen(bbox)
        # print('Frame took {} seconds'.format(time.time()-last_time))
        # last_time = time.time()

        
        # processed_screen = process_img(screen)
            
        # if move_pescador(prev_screen, processed_screen):
        #     screen = grab_screen(bbox)
        #     processed_screen = process_img(screen)
        
        # prev_screen = processed_screen
        # # print(new_screen.shape)
        # cv2.imshow('window2', processed_screen)
        # # cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        

        # mouse movement
        print(bbox)
        time.sleep(2)
        # MoveCursor(20, 50, bbox[0], bbox[1])
        MoveCursor(*INVENTARIO, bbox[0], bbox[1])
        LeftClick()
        MoveCursor(*INV1, bbox[0], bbox[1])
        LeftClick()
        time.sleep(0.01)
        LeftClick()
        # straight()
        # time.sleep(0.5)
        # if m1 < 0 and m2 < 0:
        #     right()
        # elif m1 > 0  and m2 > 0:
        #     left()
        # else:
        #     straight()
        
        #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break