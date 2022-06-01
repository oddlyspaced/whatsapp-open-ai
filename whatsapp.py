from distutils.command.config import config
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from config import ProjectConfig as config
import enum

class WhatsAppState(enum.Enum):
    AskingForLogin = 1

# setting up chrome instance
options = ChromeOptions()
options.add_argument("--user-data-dir=" + config.data_direc)

# launching driver
driver = webdriver.Chrome(options=options)

driver.get("https://web.whatsapp.com")

# function to wait for whatsapp to load
def check_whatsapp_state():
    try :
        driver.find_element_by_class_name("_2WuPw")
        return WhatsAppState.AskingForLogin
    except:
        pass