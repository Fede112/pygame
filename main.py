import numpy as np
import cv2
import time
import pyautogui
import win32gui
from directkeys import PressKey, ReleaseKey, MoveCursor, LeftClick
from directkeys import W, A, S, D, U, P, UP, DOWN, LEFT, RIGHT, CTRL, ENTER
from grabscreen import grab_screen, window_pos
from getkeys import key_check

import matplotlib.pyplot as plt


# Posicion en pixeles
INVENTARIO = (800, 190)
INV1 = (760, 240) # rojas
INV2 = (800, 240) # comida
INV3 = (840, 240) # bebida
INV4 = (880, 240)

# stats (y,x)
VIDA = (600, 815)
MANA =  (560, 815)
HAMBRE = (600, 940)
SED = (630, 942)

# VIDA = [815, 600]
# MANA =  [815, 560]
# HAMBRE = [940, 600]
# SED = [942, 630]


dt = 0.01
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

def usar():
    PressKey(U)
    ReleaseKey(UP)
    ReleaseKey(DOWN)
    ReleaseKey(LEFT)
    ReleaseKey(RIGHT)
    time.sleep(dt)
    ReleaseKey(U)


def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # vida, mana, hambre, sed
    print(processed_img.shape)
    # processed_img[VIDA[0], VIDA[1]]
    # stats = [[],[],[],[]]
    stats = {'vida':processed_img[VIDA], 'mana':processed_img[MANA], 'hambre': processed_img[HAMBRE], 'sed': processed_img[SED]}
    # print(stats)
    # exit()
    # edge detection
    # processed_img =  cv2.Canny(original_image, threshold1 = 50, threshold2=300)
    # processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
        
    mask = np.zeros(processed_img.shape,np.uint8)
    

    coord = processed_img[728,870:950]

    mask[720:740,870:950] = processed_img[720:740,870:950]

    print(coord.shape)
    mask_expand = np.array([coord,]*100)

    print(coord)
    plt.imshow(mask_expand)
    plt.show()
    # plt.plot(np.arange(coord.size), coord, marker='.')
    # print(np.where(coord>70,1,0))
    time.sleep(1)
    # plt.show()
    # input()
    
    # screen without inventory & borders
    # mask[188:711,10:692] = processed_img[188:711,10:692]
    
    # text = pytesseract.image_to_string(processed_img, config='--psm 6')
    # print(text)

    # try:
        # l1, l2, m1,m2 = draw_lanes(original_image,lines)
        # cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        # cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    # except Exception as e:
        # print(str(e))
        # pass

    return mask, stats



def move_pescador(prev_screen, screen):
    diff = np.sum(prev_screen-screen)
    print (f'diff: {diff}')
    if diff !=0:
        left()
        time.sleep(.2)
        return True
    return False

# def check_vida(val):
#     print(f'val: {val}')
#     if val < 10:
        # consume
def check_hambre(val):
    print(f'hambre: {val}')
    if val < 10:
        MoveCursor(*INVENTARIO, bbox[0], bbox[1])
        LeftClick()
        MoveCursor(*INV1, bbox[0], bbox[1])
        LeftClick()
        usar()
        usar()
        usar()





        # LeftClick()
        # time.sleep(0.01)
        # LeftClick()


def check_sed(val):
    print(f'sed: {val}')
    if val < 10:
        MoveCursor(*INVENTARIO, bbox[0], bbox[1])
        LeftClick()
        MoveCursor(*INV2, bbox[0], bbox[1])
        LeftClick()
        usar()
        usar()
        usar()




if __name__ == '__main__':
        
    for i in list(range(3))[::-1]:
        print(i+1)
        time.sleep(1)

    bbox = window_pos('fénixao')
    print(bbox)
    last_time = time.time()

    screen = grab_screen(bbox)
    processed_screen, stats = process_img(screen)
    prev_screen = processed_screen
    
    paused = False
    while True:
        if not paused:
            screen = grab_screen(bbox)
            print('Frame took {} seconds'.format(time.time()-last_time))
            last_time = time.time()    
            processed_screen, stats = process_img(screen) 


            # check_vida(stats['vida'])
            # check_hambre(stats['hambre'])
            # check_sed(stats['sed'])

            #--------------------------------------------------------------
            # pescador
            # if move_pescador(prev_screen, processed_screen):
            #     screen = grab_screen(bbox)
            #     processed_screen, stats = process_img(screen)
            
            # prev_screen = processed_screen
            #--------------------------------------------------------------


            cv2.imshow('window2', processed_screen)
            # cv2.imshow('window2',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            

            # mouse movement
            # print(bbox)
            # time.sleep(2)
            # # MoveCursor(20, 50, bbox[0], bbox[1])
            # MoveCursor(*INVENTARIO, bbox[0], bbox[1])
            # LeftClick()
            # MoveCursor(*INV1, bbox[0], bbox[1])
            # LeftClick()
            # time.sleep(0.01)
            # LeftClick()
            
            #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        keys = key_check()
        if 'P' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
