from config import *
from classes import *
from kyui import UserInterface


scribe: object = Scribe( 
    verboseEnabled = VERBOSE_LOGGING
)
requestHandler: object = RequestHandler(
    scribe_object = scribe,
    max_retry = MAX_RETRY,
    redirects_allowed = False,
    response_timeout = RESPONSE_TIMEOUT,
    request_headers = {"User-Agent": USER_AGENT},
    min_request_interval = MIN_REQUEST_INTERVAL,
    delay_on_retry = DELAY_ON_RETRY
)
webPage: object = WebPage(
    scribeObject = scribe,
    requestHandlerObject = requestHandler,
)
webPageParser: object = WebPageParser(
    scribeObject = scribe,
    webPageObject = webPage
)
imageSaver: object = ImageSaver(
    scribe_object = scribe,
    output_dir_path = "images"
)
userInput: object = UserInput(
    scribeObject = scribe
)
userInterface: object = UserInterface(
    defaultUIColor = DEFAULT_UI_COLOR,
    artEnabled = BANNER_ART_ENABLED,
    scribeObject = scribe
)

def uiLink():
    while True:
        command = userInterface.main()
        if command:
            if command == 'exit':
                return None
                
                
if __name__ == "__main__":
    uiLink()