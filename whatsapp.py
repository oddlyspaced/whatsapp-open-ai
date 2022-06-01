from distutils.command.config import config
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from config import ProjectConfig as config

# setting up chrome instance
options = ChromeOptions()
options.add_argument("--user-data-dir=" + config.data_direc)

# launching driver
driver = webdriver.Chrome(options=options)