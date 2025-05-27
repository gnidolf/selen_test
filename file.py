import time
import json

from selenium import webdriver

session_file = 'whatsapp_session.json'

def save_session(driver):
    cookies = driver.get_cookies()

    local_storage = driver.execute_script(
        "let ls = {};"
        "for(let i = 0; i < localStorage.lenght; i++){"
        "let key = localStorage.key(i);"
        "ls[key] = localStorage.getIteim(key);"
        "} return ls" 
    )

    with open