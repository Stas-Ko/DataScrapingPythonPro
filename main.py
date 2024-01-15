import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper import get_page_data, get_image_links
from json_handler import save_to_json



# Запуск скрипту
def main():
    # Отримати поточну дату в форматі "місяць/день/рік"
    current_date = datetime.now().strftime("%m/%d/%Y")

    # лічильник збережених об'єктів в JSON файл
    count_obj = 1

    # Налаштування опцій для браузера Chrome
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    # Створення об'єкту веб-драйвера для браузера Chrome з заданими опціями
    driver = webdriver.Chrome(options=chrome_options)

    # Перехід на вказану веб-сторінку
    driver.get('https://realtylink.org/en/properties~for-rent')

    # Цикл для переходу на наступні сторінки (три сторінки в цьому прикладі)
    for next_page in range(3):

        # Очікування, доки всі елементи знайдуться на сторінці
        img_elements = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, '//img[@itemprop="image"]'))
        )

        # Проходження по кожному елементу оголошення на сторінці та натискання на нього
        for i, img_element in enumerate(img_elements):

            # Отримання поточного URL
            current_url = driver.current_url

            # Перевірка, чи поточний URL є 'data:,'
            if 'data:,' == current_url:
                # Якщо так, то переходимо вперед
                driver.forward()
                
            # Очікування видимості елемента зображення
            img_element = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, f'(//img[@itemprop="image"])[{i + 1}]'))
            )

            img_element.click()
            time.sleep(1)

            # Отримання поточного URL після натискання на зображення
            url = driver.current_url

            # Виклик функції для отримання словника з даними з одного оголошення
            ad_info = get_page_data(url, current_date, driver)

            # Виклик функції для збереження даних у json файл
            save_to_json(ad_info, count_obj)

            # лічильник об'єктів
            count_obj += 1

            # повернення на попередню сторінку
            driver.back()
            time.sleep(1)

        # створення прапора для управління циклом, реакція на винятки
        check_next_button = True

        while check_next_button:

            current_url = driver.current_url

            # Перевірка, чи поточний URL є 'data:,'
            if 'data:,' == current_url:
                # Якщо так, то переходимо вперед
                driver.forward()

            try:
                # Знаходження елементу за класом "next"
                wait = WebDriverWait(driver, 60)
                # Очікування, доки елемент стане клікабельним (в даному випадку - кнопка "next")
                next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))

                # Натискання на елемент
                next_button.click()
                time.sleep(1)

                # прапора False якщо не виникло винятків
                check_next_button = False

            except Exception as e:
                time.sleep(2)

    # закриття браузера після завершення всіх операцій
    driver.quit()


if __name__ == "__main__":
    main()

