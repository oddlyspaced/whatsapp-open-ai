from distutils.command.config import config
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from config import ProjectConfig as config
import enum

# enum to hold whatsapp web page states
class WhatsAppState(enum.Enum):
    AskingForLogin = 1

class WhatsAppHandler():
    def __init__(self) -> None:
        driver = None
    
    # loads up chrome driver and launches window
    def load_driver(self) -> None:
        # setting up chrome instance
        options = ChromeOptions()
        options.add_argument("--user-data-dir=" + config.data_direc)
        self.driver = webdriver.Chrome(options=options)

    # launches whatsapp web page
    def launch_whatsapp(self) -> None:
        self.driver.get("https://web.whatsapp.com")

    # function to wait for whatsapp to load
    def check_whatsapp_state(self) -> WhatsAppState:
        try :
            self.driver.find_element_by_class_name("_2WuPw")
            return WhatsAppState.AskingForLogin
        except:
            pass