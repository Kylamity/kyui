# File name: classes.py
# Author: Kylamity

import requests, os, time
from bs4 import BeautifulSoup
from PIL import Image


class ProgressBar:
    def __init__(self, length, appendPercent = True):
        self.progressCharacter = "█"
        self.emptyCharacter = "░"
        self.length = length
        self.appendPercent = appendPercent
        self.divisor = None
        self.percentage = None
        self.string = None
        
    def make(self, currentNumber, totalNumber):
        percentProgress = self.calculate(currentNumber, totalNumber)
        if not percentProgress == self.percentage:
            self.percentage = percentProgress
            self.generate()
        return self.string
        
    def calculate(self, currentNumber, totalNumber):
        self.divisor = totalNumber / currentNumber
        return round(100 / self.divisor)
        
    def generate(self):
        numFilled = round(self.length / self.divisor)
        numEmpty = self.length - numFilled
        string = ""
        for _ in range(numFilled):
            string += self.progressCharacter
        for _ in range(numEmpty):
            string += self.emptyCharacter
        if self.appendPercent:
            string += f"{round(self.percentage)}%"
        self.string = string 
    

class UserInput:
    def __init__(self, scribeObject: object, prompt: str = None):
        self.scribe = scribeObject
        self.debounceTime = 0.2 # seconds
        self.prompt = "> "
        if prompt:
            self.prompt = prompt
            
    def query(self, inputType: str, message: str = None, messageColor: str = None):
        if message:
            self.scribe.write(message, 'c', messageColor)
        while True:
            try:
                userInput = inputType(input(self.prompt))
                break
            except Exception as e:
                raise e
        time.sleep(self.debounceTime)
        return userInput


class ImageSaver:
    def __init__(self, scribe_object: object, output_dir_path: str = None):
        self.scribe = scribe_object
        self.output_dir_path = None
        if self.output_dir_path:
            self.set_output_dir(output_dir_path)
                
    def set_output_dir(self, output_dir_path):
        self.output_dir_path = output_dir_path
        try:
            os.makedirs(self.output_dir_path, exist_ok = True)
        except Exception as e:
            self.scribe.write(f"[ImageSaver] Error creating output directory:\n[ImageSaver] {e}", 'cl', 'red')

    def save_image(self, image_data, file_name):
        self.tangent_save = False
        self.file_mode = None
        if self.output_dir_path:
            output_file_path = f'{os.path.join(self.output_dir_path, file_name)}'
            try:
                if image_data.mode in ['RGB', 'L', 'F', 'CMYK']:
                    self.file_mode = 'JPEG'
                elif image_data.mode in ['P', 'PA', '1']:
                    self.file_mode = 'GIF'
                    self.check_animated(image_data, file_name, output_file_path)
                elif image_data.mode in ['SVG']:
                    self.file_mode = 'SVG'
                else:
                    self.file_mode = 'PNG'
            except Exception as e:
                self.scribe.write(f"[ImageSaver] Image mode not discovered:\n[ImageSaver] {e}", 'cl', 'red')
                return None
            if not self.tangent_save:
                try:
                    image_data.save(f"{output_file_path}.{self.file_mode}", self.file_mode)
                except Exception as e:
                    self.scribe.write(f"[ImageSaver] Error saving {self.file_mode}:\n[ImageSaver] {e}", 'cl', 'red')
                    return None
                self.scribe.write(f"[ImageSaver] Image saved as {file_name}.{self.file_mode}", 'l', 'green')
        else:
            self.scribe.write("[ImageSaver] Warning: Output path not defined", 'cl', 'yellow')

    def check_animated(self, image_data, file_name, output_file_path):
        frames = []
        try:
            while True:
                frames.append(image_data.copy())
                image_data.seek(len(frames))
        except EOFError:
            pass
        except Exception as e:
            self.scribe.write(f"[ImageSaver] Error processing {self.file_mode}:\n[ImageSaver] {e}", 'cl', 'red')
        if len(frames) > 1:
            self.tangent_save = True
            try:
                frames[0].save(f"{output_file_path}.{self.file_mode}", self.file_mode, save_all = True, append_images = frames[1:])
                self.scribe.write(f"[ImageSaver] Image saved as {file_name}.{self.file_mode}", 'cl', 'green')
            except Exception as e:
                self.scribe.write(f"[ImageSaver] Error saving {self.file_mode}:\n[ImageSaver] {e}", 'cl', 'red')
        else:
            self.tangent_save = False


class Scribe:
    def __init__(self, defaultLogDir: str = None, defaultLogName: str = None, verboseEnabled: bool = False):
        self.logDir = None
        self.logName = defaultLogName
        self.verbose = verboseEnabled
        self.outputModifiers = 'c'
        self.color = 'default'
        self.colorDict = {
            'purple':   '\033[95m',
            'cyan':     '\033[96m',
            'darkcyan': '\033[36m',
            'blue':     '\033[94m',
            'green':    '\033[92m',
            'yellow':   '\033[93m',
            'red':      '\033[91m',
            'default':  '\033[0m',
        }
        if defaultLogDir:
            self.setLogDir(defaultLogDir)
    
    # Verbose mode outputs all to console and log
    # Output Modifiers:
    #  d: verbose mode enabled only "debug"
    #  c: console
    #  l: log
    # -v: ignore verbose mode
    def write(self, outputString: str, outputModifiers: str = None , color: str = None):
        outputModifiers = outputModifiers or self.outputModifiers
        color = color or self.color
        if self.verbose and not '-v' in outputModifiers:
            self.writeConsole(outputString, color)
            self.writeLog(outputString)
        else:
            if 'c' in outputModifiers:
                self.writeConsole(outputString, color)
            if 'l' in outputModifiers:
                self.writeLog(outputString)
    
    def writeConsole(self, string: str, color: str):
        colorCode = self.colorDict[color]
        defaultColorCode = self.colorDict['default']
        print(colorCode + string + defaultColorCode)
    
    def writeLog(self, string):
        if self.logDir and self.logName:
            logFilePath = f"{os.path.join(self.logDir, self.logName)}.txt"
            try:
                with open(logFilePath, 'a') as logFile:
                    logFile.write(f"{string}\n")
            except Exception as e:
                self.write(f"[Scribe] Error writing to log file:\n[Scribe] {e}", 'c-v', 'red')
        else:
            self.write("[Scribe] Warning: Log directory or file name not set!", 'c-v', 'yellow')
            
    def setLogDir(self, logDirPath: str):
        try:
            os.makedirs(logDirPath, exist_ok = True)
            self.logDir = logDirPath
        except Exception as e:
            self.write(f"[Scribe] Error creating log directory:\n[Scribe] {e}", 'c-v' 'red')


class RequestHandler:
    def __init__(self, scribe_object, max_retry = 3, redirects_allowed = False, response_timeout = 30, request_headers = None , min_request_interval = None, delay_on_retry = None):
        self.scribe = scribe_object
        self.max_retry = max_retry
        self.redirects_allowed = redirects_allowed
        self.response_timeout = response_timeout
        self.request_headers = request_headers
        self.min_request_interval = min_request_interval
        self.delay_on_retry = delay_on_retry
        self.last_request_timestamp = 0
        self.response_duration = 0
        self.response_size_kb = 0

    def request(self, url):
        next_allowed_request = self.last_request_timestamp + self.min_request_interval
        current_time = time.time()
        response_content = None
        response_recieved_timestamp = None
        self.retry_count = 0
        while True:
            if current_time < next_allowed_request:
                waitTime = next_allowed_request - current_time
                self.scribe.write(f"[RequestHandler] Minimum request interval not met, waiting {round(waitTime, 2)} sec...", 'd')
                time.sleep(waitTime)
            self.scribe.write(f"[RequestHandler] Request sent: {url}", 'd')
            try:
                self.last_request_timestamp = time.time()
                response_content = requests.get(url, allow_redirects = self.redirects_allowed, timeout = self.response_timeout, headers = self.request_headers)
                response_recieved_timestamp = time.time()
                break
            except Exception as e:
                if not self.retry():
                    self.scribe.write(f"[RequestHandler] Error retrieving response:\n[RequestHandler] {e}", 'cl', 'red')
                    raise e
        if response_content:
            self.response_duration = round(response_recieved_timestamp - self.last_request_timestamp, 2)
            self.response_size_kb = len(response_content.content) / 1024
            self.scribe.write(f"[RequestHandler] Response recieved in {self.response_duration} sec", 'd')
            return response_content
        self.response_duration = 0
        self.response_size_kb = 0
        return None

    def retry(self):
        self.retry_count = self.retry_count + 1
        if self.retry_count > self.max_retry:
            return False
        self.scribe.write(f"[RequestHandler] Warning: Could not retrieve response from URL, retrying: {self.retry_count}", 'cl', 'yellow')
        time.sleep(self.delay_on_retry)
        return True

    def dynamic_interval(self):
        #FUTURE: use response_duration and or response size to decrease request rate for picky servers
        pass


class WebPage:
    def __init__(self, scribeObject: object, requestHandlerObject: object):
        self.scribe = scribeObject
        self.requestHandler = requestHandlerObject
        self.url = ""
        self.pageResponse = None
        self.htmlSoup = None
        
    def setURL(self, url: str):
        self.url = url
        self.pageResponse = self.requestHandler.request(url)
        try:
            self.htmlSoup = BeautifulSoup(self.pageResponse.content, 'html.parser')
        except Exception as e:
            self.scribe.write(f"[WebPage] Error extracting HTML from page response content:\n[Webpage] {e}", 'cl', 'red')
        self.scribe.write("[WebPage] Retrieved HTML from URL", 'd')


class WebPageParser:
    def __init__(self, scribeObject: object, webPageObject: object):
        self.scribe = scribeObject
        self.webpage = webPageObject
        self.elements = []
        self.childElements = []
        
    def getElements(self, idAttType: str, idAttValue: str, quantity: int = None):
        self.elements = []
        idAttributeType = idAttType
#        if idAttType == 'class':
#            idAttributeType = 'class_'
        try:
            self.elements = self.webpage.htmlSoup.find_all(attrs = {idAttributeType: idAttValue}, limit = quantity)
            self.scribe.write(f"[WebPageParser] Captured {len(self.elements)} web page element(s)", 'd')
        except Exception as e:
            self.scribe.write(f"[WebPageParser] Error capturing element(s):\n[WebPageParser] {e}", 'cl')
        if not self.elements:
            self.scribe.write(f"[WebPageParser] Warning: Element indentifier attribute type / value combination not found.", 'cl', 'yellow')
            
    def getElementAttValue(self, element, attName: str):
        return element.get(attName)
        
    def getAttValueFromChildElement(self, parentElement, attName: str, occuranceNum: int):
        self.childElements = []
        self.childElements = parentElement.find_all(attrs = {attName: True})
        if self.childElements:
            self.scribe.write(f"[WebPageParser] Captured {len(self.childElements)} child element(s) containing: {attName}", 'd')
            return self.childElements[occuranceNum - 1].get(attName)
        else:
            self.scribe.write(f"[WebPageParser] Warning: Child element(s) containing {attName} not found", 'cl', 'yellow')
            
