import time
import json
from selenium import webdriver

session_file = 'tg_session.json'

def save_session(driver):
    # Сохраняем куки и localStorage
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

    # Загружаем куки ПЕРЕД открытием страницы
    driver.get("https://web.telegram.org/k/")  # Сначала открываем домен
    driver.delete_all_cookies()
    
    for cookie in data['cookies']:
        # Удаляем 'expiry', если он есть (может вызвать ошибку)
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])  # Преобразуем в int
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


driver = webdriver.Chrome()
try:
    # Пытаемся загрузить сессию
    session_loaded = False
    try:
        with open(session_file, 'r'):
            session_loaded = load_session(driver)
    except FileNotFoundError:
        pass

    if not session_loaded:
        print("Отсканируйте QR-код для входа в tg Web...")
        driver.get("https://web.telegram.org/k/")
        time.sleep(15)
        save_session(driver)
    else:
        driver.get("https://web.telegram.org/k/")  # Перезагружаем страницу с куками
        time.sleep(5)  

    print("Проверка сессии...")
    time.sleep(10)
finally:
    driver.quit()