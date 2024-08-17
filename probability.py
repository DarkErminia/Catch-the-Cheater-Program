from pytesseract import pytesseract
from math import comb
from PIL import ImageGrab
from time import sleep
from pyautogui import (press,scroll,typewrite,hotkey,
                       keyDown,keyUp,click,moveTo,dragTo,mouseDown,mouseUp)
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

'''
table = {
        "0,0": "roll",
        "0,1": "roll",
        "0,2": "fair",
        "1,0": "roll",
        "1,1": "roll",
        "1,2": "roll",
        "1,3": "fair",
        "2,0": "cheat",
        "2,1": "roll",
        "2,2": "roll",
        "2,3": "fair",
        "3,1": "cheat",
        "3,2": "roll",
        "3,3": "roll",
        "3,4": "fair",
        "4,1": "cheat",
        "4,2": "roll",
        "4,3": "roll",
        "4,4": "fair",
        "5,2": "cheat",
        "5,3": "roll",
        "5,4": "roll",
        "5,5": "fair",
        "6,2": "cheat",
        "6,3": "roll",
        "6,4": "roll",
        "6,5": "fair",
        "7,3": "cheat",
        "7,4": "roll",
        "7,5": "fair",
        "8,4": "cheat",
    }
'''

table = {
        "0,6": "fair",
        "1,5": "fair",
        "2,4": "fair",
        "3,3": "fair",
        "4,2": "cheat",
        "5,1": "cheat",
        "6,0": "cheat",
    }

def ch_exval(heads, tails):
    c_chance=binom_prob(heads,tails,0.75)
    f_chance=binom_prob(heads,tails,0.5)
    c_percent=c_chance/(c_chance+f_chance)
    c_exval=c_percent*(15-heads-tails)+(1-c_percent)*(-30-heads-tails)
    return c_exval

def fa_exval(heads, tails):
    c_chance=binom_prob(heads,tails,0.75)
    f_chance=binom_prob(heads,tails,0.5)
    f_percent=f_chance/(c_chance+f_chance)
    f_exval=f_percent*(15-heads-tails)+(1-f_percent)*(-30-heads-tails)
    return f_exval

def binom_prob(heads,tails,p): #p is heads probability
    return comb(heads+tails,heads)*p**(heads)*(1-p)**(tails)

def get_flips():
    image = ImageGrab.grab(bbox=(1036,832,1183,862))
    text = pytesseract.image_to_string(image)
    temp = text[:-1].split()
    nums=[]
    for i in temp:
        if i.isnumeric():
            nums+=[int(i)]
    try:
        flips=nums[0]
        return flips
    except BaseException:
        print("Error with flips")
        return -1
    
print(get_flips())
input(">")
exp_score=100

while True:
    image = ImageGrab.grab(bbox=(920,525,1050,600))
    text = pytesseract.image_to_string(image)
    temp = text[:-1].split()
    nums=[]
    for i in temp:
        if i.isnumeric():
            nums+=[int(i)]
    try:
        heads=nums[0]
        tails=nums[1]
        heads=int(heads)
        tails=int(tails)
        
        c_chance=binom_prob(heads,tails,0.75)
        f_chance=binom_prob(heads,tails,0.5)
        c_percent=c_chance/(c_chance+f_chance)
        c_exval=c_percent*(15-heads-tails)+(1-c_percent)*(-30-heads-tails)
        f_percent=f_chance/(c_chance+f_chance)
        f_exval=f_percent*(15-heads-tails)+(1-f_percent)*(-30-heads-tails)
        
        if heads+tails>=12:
            if c_exval>f_exval:
                click(1000,1000) #Label as Cheater
                print("["+str(round(heads,2))+
                      ","+str(round(tails,2))+
                      "], Cheat %: "+str(round(c_percent,2))+
                      ", Exp. Value: "+str(round(c_exval,2)))
                exp_score+=round(c_exval,2)
                flips=get_flips()
                print("Expected Score: "+str(round(exp_score,2))+
                      ", Actual Score: "+str(flips)+
                      ", (Difference "+round(flips-exp_score,2))
            else:
                click(842,1003)  #Label as Fair
                print("["+str(round(heads,2))+
                      ","+str(round(tails,2))+
                      "], Fair %: "+str(round(f_percent,2))+
                      ", Exp. Value: "+str(round(f_exval,2)))
                exp_score+=round(f_exval,2)
                flips=get_flips()
                print("Expected Score: "+str(round(exp_score,2))+
                      ", Actual Score: "+str(flips)+
                      ", (Difference "+round(flips-exp_score,2))
        elif c_exval>0:
            click(1000,1000) #Label as Cheater
            print("["+str(round(heads,2))+
                  ","+str(round(tails,2))+
                  "], Cheat %: "+str(round(c_percent,2))+
                  ", Exp. Value: "+str(round(c_exval,2)))
            exp_score+=round(c_exval,2)
            flips=get_flips()
            print("Expected Score: "+str(round(exp_score,2))+
                  ", Actual Score: "+str(flips)+
                  ", (Difference "+round(flips-exp_score,2))
        elif f_exval>0:
            click(842,1003) #Label as Fair
            print("["+str(round(heads,2))+
                  ","+str(round(tails,2))+
                  "], Fair %: "+str(round(f_percent,2))+
                  ", Exp. Value: "+str(round(f_exval,2)))
            exp_score+=round(f_exval,2)
            flips=get_flips()
            print("Expected Score: "+str(round(exp_score,2))+
                  ", Actual Score: "+str(flips)+
                  ", (Difference "+round(flips-exp_score,2))
        else:
            click(832,901) #Flip 1 Coin
        '''
        if heads>=4:
            click(1000,1000)
        elif tails>=3:
            click(842,1003)
        else:
            click(832,901)
        '''
        '''
        lookup=heads+","+tails
        if lookup in table:
            if table[lookup]=="fair":
                click(842,1003)
            if table[lookup]=="cheat":
                click(1000,1000)
        else:
            click(832,901)
        '''
    except BaseException:
        click(832,901)
    
    
