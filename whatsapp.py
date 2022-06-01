from distutils.command.config import config
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from config import ProjectConfig as config
import enum

# enum to hold whatsapp web page states
class WhatsAppState(enum.Enum):
    AskingForLogin = 1
    MainPage = 2
    Undefined = 99

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
    # TODO: Improve multi check handling
    def check_whatsapp_state(self) -> WhatsAppState:
        try:
            self.driver.find_element(By.CLASS_NAME, "_2WuPw")
            return WhatsAppState.AskingForLogin
        except:
            try:
                self.driver.find_element(By.CLASS_NAME, "_1y6Yk")
                return WhatsAppState.MainPage
            except:
                return WhatsAppState.Undefined
            return WhatsAppState.Undefined
            pass

handler = WhatsAppHandler()
handler.load_driver()
handler.launch_whatsapp()

# wait for login page
while handler.check_whatsapp_state() not in [WhatsAppState.AskingForLogin, WhatsAppState.MainPage]:
    print(handler.check_whatsapp_state())
    pass

print("Loaded WhatsApp Web!")