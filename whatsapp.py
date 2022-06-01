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
    ChatPage = 3
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
    
    def open_chat(self, contact: str) -> None:
        searchbox = self.driver.find_element(By.CLASS_NAME, "_16C8p")
        searchbox.click()
        self.driver.find_element(By.XPATH, "//*[@id='side']/div[1]/div/div/div[2]/div/div[2]").send_keys(contact)
        results = self.driver.find_elements(By.CLASS_NAME, "zoWT4")
        print(len(results))
        for user in results:
            if contact == str(user.text):
                user.click()
                break

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
                try:
                    self.driver.find_element(By.CLASS_NAME, "_2vbn4")
                    return WhatsAppState.ChatPage
                except:
                    return WhatsAppState.Undefined
                return WhatsAppState.Undefined
            return WhatsAppState.Undefined
            pass

handler = WhatsAppHandler()
handler.load_driver()
handler.launch_whatsapp()

# wait for login page
while handler.check_whatsapp_state() not in [WhatsAppState.AskingForLogin, WhatsAppState.MainPage]:
    pass

print("Loaded WhatsApp Web!")
handler.open_chat("Me Airtel")