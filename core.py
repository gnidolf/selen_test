import time
import json

from selenium import webdriver

session_file = 'tg_session.json'

# Сохраняем куки и localStorage
def save_session(driver):
    cookies = driver.get_cookies()
    local_storage = driver.execute_script(
        "let ls = {};"
        "for(let i = 0; i < localStorage.length; i++){"
        "   let key = localStorage.key(i);"
        "   ls[key] = localStorage.getItem(key);"
        "} return ls;"
    )
    
    with open(session_file, 'w') as f:
        json.dump({'cookies': cookies, 'localStorage': local_storage}, f)
    print('Session saved.')

def load_session(driver):
    try:
        with open(session_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Файл сессии не найден.")
        return False

    driver.get("https://web.telegram.org/k/")
    driver.delete_all_cookies()
    
    for cookie in data['cookies']:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Ошибка добавления куки: {e}")

    # Восстанавливаем localStorage
    local_storage = data.get('localStorage', {})
    driver.execute_script("window.localStorage.clear();")
    for key, value in local_storage.items():
        driver.execute_script(f"window.localStorage.setItem('{key}', {json.dumps(value)});")
    
    print("Session loaded.")
    return True

def main():
    driver = webdriver.Chrome()
    try:
        session_loaded = False
        try:
            with open(session_file, 'r'):
                session_loaded = load_session(driver)
        except FileNotFoundError:
            pass

        if not session_loaded:
            driver.get("https://web.telegram.org/k/")
            time.sleep(30)
            save_session(driver)
        else:
            driver.get("https://web.telegram.org/k/#@axaxaxaxaxaxaxaaxaxaaxaxaxaxa") # @zecurion123
            time.sleep(20)  # тут 

    finally:
        driver.quit()

main()