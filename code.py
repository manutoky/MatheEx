# Mathe Exercises for Adafruit Macroboard

import os
import random
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad


# CONFIGURABLES ------------------------
ANZ_AUFGABEN = 10
STATEMACHINE = {'MENU': 0,
    'RUN': 1,
    'FINISHED_FAIL': 2,
    'FINISHED_SUCCESS': 3,
    }
KEY_START = 9
KEY_ENTER = 11
KEY_CORRECT = 9

# CLASSES AND FUNCTIONS ----------------www.adafruit.com
class Aufgabe:
    def __init__(self, type) -> None:
        self.type_ = type
        if type == 0: # plus
            self.typestr_ = 'Addiere!'
            self.val1_ = random.randrange(0,99)
            self.val2_ = random.randrange(0,min(100-self.val1_,10))
            self.result_ = self.val1_ + self.val2_
        elif type == 1:# minus
            self.typestr_ = 'Ziehe ab!'
            self.val1_ = random.randrange(0,10)
            self.val2_ = random.randrange(0,10)
            self.result_ = self.val1_ + self.val2_
        elif type == 2: # multiplizieren
            self.typestr_ = 'Multipliziere!'
            self.val1_ = random.randrange(0,10)
            self.val2_ = random.randrange(0,10)
            self.result_ = self.val1_ + self.val2_
        elif type == 3: # dividieren
            self.typestr_ = 'Dividiere!'
            self.val1_ = random.randrange(0,10)
            self.val2_ = random.randrange(0,10)
            self.result_ = self.val1_ + self.val2_
        else:
            pass

class Menu:
    def __init__(self, macropad):
        self.macropad_ = macropad
        self.menugroup_ = displayio.Group()
        self.menugroup_.append(Rect(0, 0, self.macropad_.display.width, 12, fill=0xFFFFFF))
        self.menugroup_.append(label.Label(terminalio.FONT, text='Mathe für Sam', color=0x000000,
                            anchored_position=(self.macropad_.display.width//2, -2),
                            anchor_point=(0.5, 0.0)))
        self.menugroup_.append(Rect(0, self.macropad_.display.height-12, 40, 12, fill=0xFFFFFF))  
        self.menugroup_.append(label.Label(terminalio.FONT, text='Start', color=0x000000,
                            anchored_position=(5, self.macropad_.display.height),
                            anchor_point=(0.0, 1.0))) 

    def showMenu(self):
        self.macropad_.display.show(self.menugroup_)

class Run:
    def __init__(self, macropad) -> None:
        self.rungroup_ = displayio.Group()
        self.macropad_ = macropad
        self.rungroup_.append(Rect(0, 0, self.macropad_.display.width, 12, fill=0xFFFFFF))
        self.runlabel_ = label.Label(terminalio.FONT, text='Los geht\'s!', color=0x000000,
                                anchored_position=(self.macropad_.display.width//2, -2),
                                anchor_point=(0.5, 0.0))
        self.rungroup_.append(self.runlabel_)
        self.countdown_ = label.Label(terminalio.FONT, text=' '*3, color=0xFFFFFF,
            anchored_position=(self.macropad_.display.width//2, self.macropad_.display.height//2),
            anchor_point=(0.5, 1.0))
        self.rungroup_.append(self.countdown_)
        self.rungroup_.append(Rect(self.macropad_.display.width-45, self.macropad_.display.height-12, 40, 12, fill=0xFFFFFF))  
        self.rungroup_.append(label.Label(terminalio.FONT, text='Fertig', color=0x000000,
                                anchored_position=(self.macropad_.display.width-5, self.macropad_.display.height),
                                anchor_point=(1.0, 1.0)))      
      

    def startRunCountdown(self):    
        self.runstate_ = 'COUNTDOWN'
        self.starttime_ = time.time()
        self.cdtime_ = 3
        self.macropad_.display.show(self.rungroup_)
    
    def erstelleAufgabe(self):
        self.aufgabentyp = 0 #random.randrange(0,3)
        self.aufgabe = Aufgabe(self.aufgabentyp)
        self.runlabel_.text = self.aufgabe.typestr_
        self.countdown_.text = str(self.aufgabe.val1_)+'+'+str(self.aufgabe.val2_)+'='
        self.inputval_ = []
        self.runstate_ = 'INPUT'

    
    def StateMachine(self, keyev):
        if self.runstate_ == 'COUNTDOWN':
            self.cdtime_ = 3 -(time.time() - self.starttime_)
            if self.cdtime_ >= 0:
                self.countdown_.text = str(self.cdtime_)
            else:
                self.countdown_.text = ' '*3
                self.erstelleAufgabe()
        if self.runstate_ == 'CORRECT':
            self.countdown_.text = 'RICHTIG!'
            self.macropad_.display.show(self.rungroup_)
            time.sleep(3.0)
            self.countdown_.text = ' '*3
            self.erstelleAufgabe()
            self.macropad_.display.show(self.rungroup_)
        if self.runstate_ == 'WRONG':
            self.countdown_.text = 'FALSCH!'
            self.macropad_.display.show(self.rungroup_)
            time.sleep(3.0)
            self.countdown_.text = ' '*3
            self.erstelleAufgabe()
            self.macropad_.display.show(self.rungroup_)
        if self.runstate_ == 'INPUT':
            if keyev and keyev.pressed:
                #print(self.runstate_)
                knum = keyev.key_number
                if knum in range(9): # Zahlen 1-9
                    if not self.inputval_:
                        self.inputval_ = knum + 1
                    else:
                        self.inputval_ = self.inputval_*10 + knum + 1
                elif knum == 10: # null
                    if self.inputval_:
                        self.inputval_ = self.inputval_*10
                elif knum == KEY_CORRECT:
                    self.inputval_ = ''
                self.countdown_.text = str(self.aufgabe.val1_)+'+'+str(self.aufgabe.val2_)+'='+str(self.inputval_)
                if knum == KEY_ENTER:
                    #print(str(self.inputval_)+'|'+str(self.aufgabe.result_))
                    if self.inputval_ == self.aufgabe.result_:
                        self.runstate_ = 'CORRECT'
                        #print(' ->'+self.runstate_)
                    else:
                        self.runstate_ = 'WRONG'
                        #print(' ->'+self.runstate_)
        self.macropad_.display.show(self.rungroup_)

        
        

# INITIALIZATION -----------------------

macropad = MacroPad()
menuinst = Menu(macropad)
runinst = Run(macropad)

#macropad.display.auto_refresh = False
#macropad.pixels.auto_write = False

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
state_ = 'MENU'

# MAIN LOOP ----------------------------
menuinst.showMenu()
while True:
    key_event = macropad.keys.events.get()
    if state_ == 'MENU':
        if key_event and key_event.pressed:
            if key_event.key_number == KEY_START:
                runinst.startRunCountdown()
                state_ = 'RUN'
    elif state_ == 'RUN':
        runinst.StateMachine(key_event)
    elif state_ == 'FINISHED_FAIL':
        pass
    elif state_ == 'FINISHED_PASS':
        pass
