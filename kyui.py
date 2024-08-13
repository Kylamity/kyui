# File name: kyui.py
# Author: Kylamity

import os, time
from config import *

bannerArt = """\
 __  __ ___ ___ _ _______ _______ _________________________________________________________________
|  |/  |   |   | |   |   |_     _| 
|     < \     /  |   |   |_|   |_ 
|__|\__|_|___|___|_______|_______|TM_______________________________________________________________"""


class UserInterface:
    def __init__(self, defaultUIColor: str, artEnabled: bool, scribeObject: object):
        self.uiColor = defaultUIColor
        self.artEnabled = artEnabled
        self.scribe = scribeObject
        self.navPath = ['main']
        self.scribe.color = defaultUIColor
        self.subPage = None
        
    def navPathUpdate(self, menuID: str):
        self.navPath.append(menuID)
           
    def navBack(self):
        self.navPath.pop()
        
    def navExit(self):
        os.system('clear')
        self.scribe.write("Exiting...", 'c')
                    
    def main(self):
        self.scribe.setLogDir("logs")
        self.scribe.logName = "kyui"
        while True:
            self.printInterface()
            if self.subPage:
                self.scribe.write(self.subPage, 'c')
                self.subPage = None
            command = None
            try:
                command = self.menuLogic(self.getUserInput('int'))
            except KeyboardInterrupt:
                pass
            if command:
                return command
                
    def menuLogic(self, userInput):
        uIn = userInput
        menu = self.navPath[-1]
        if uIn == 0:
            if menu == 'main':
                self.navExit()
                return 'exit'
            else:
                self.navBack()
                return None
        #-------------------------------------------------------------------main
        elif menu == 'main':
            if uIn == 1:
                return None
            elif uIn == 2:
                return None
            
    def getUserInput(self, inputType: str, message: str = None, messageColor: str = None):
        debounceTime = 0.2 # sec
        prompt = "> "
        if message:
            if messageColor:
                self.scribe.write(message, 'c', messageColor)
            else:
                self.scribe.write(message, 'c')
        while True:
            try:
                if inputType == 'int':
                    usrInput = int(input(prompt))
                elif inputType == 'str':
                    usrInput = str(input(prompt))
                break
            except ValueError:
                self.printInterface()
                self.scribe.write("Invalid character", 'c', 'red')
        time.sleep(debounceTime)
        return usrInput
        
    def printInterface(self):
        os.system('clear')
        if self.artEnabled:
            self.scribe.write(bannerArt, 'c')
        self.printMenuPath()
        self.printMenuBody()
        
    def printMenuPath(self):
        pathDisplay = " > ".join(self.navPath)
        self.scribe.write("- " + pathDisplay, 'c')
        
    def printMenuBody(self):
        menu = self.navPath[-1]
        self.scribe.write(menuDisplays[menu], 'c')


menuDisplays = {
    'main': """
0  <Exit)
""",
}