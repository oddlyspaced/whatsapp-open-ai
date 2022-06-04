from distutils.command.config import config
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from config import ProjectConfig as config
import enum
import time
import openai

openai.api_key = config.api_key

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
    
    def send_message(self, text: str) -> None:
        if self.check_whatsapp_state() != WhatsAppState.ChatPage:
            raise Exception("Chat Page not open!")
        chat_text_box = self.driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]")
        chat_text_box.click()
        chat_text_box.send_keys(text)
        self.driver.find_element(By.CLASS_NAME, "_1Ae7k").click()
    
    def get_contact_name_chat(self) -> str:
        if self.check_whatsapp_state() != WhatsAppState.ChatPage:
            raise Exception("Chat Page not open!")
        time.sleep(2)
        return self.driver.find_element(By.CLASS_NAME, "_21nHd").text
    
    def get_latest_text(self, contact: str) -> str:
        if self.check_whatsapp_state() != WhatsAppState.ChatPage:
            raise Exception("Chat Page not open!")
        time.sleep(2)
        messages = self.driver.find_elements(By.CLASS_NAME, "_22Msk")
        latest = None
        for message in messages:
            parent_temp = message.find_element(By.XPATH, "..")
            aria_label = parent_temp.find_element(By.TAG_NAME, "span")
            if contact in str(aria_label.get_attribute("aria-label")):
                latest = message
        msg = str(latest.text)
        try:
            return (msg[0:msg.rindex('\n')])
        except:
            return msg

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

class GPT3Handler:
    def __init__(self) -> None:
        pass

    def get_response(self, prompt: str) -> str:
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, temperature=0, max_tokens=6)
        return response.choices[0].text

handler = WhatsAppHandler()
handler.load_driver()
handler.launch_whatsapp()

# wait for login page
while handler.check_whatsapp_state() not in [WhatsAppState.AskingForLogin, WhatsAppState.MainPage]:
    pass

print("Loaded WhatsApp Web!")
handler.open_chat(config.contact_name)

latest = handler.get_latest_text(config.contact_name)
while True:
    time.sleep(5)
    temp = handler.get_latest_text(config.contact_name)
    if temp != latest:
        print(temp)
        handler.send_message(GPT3Handler().get_response(temp))
        latest = temp