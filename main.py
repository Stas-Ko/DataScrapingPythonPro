import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

# Отримати поточну дату в форматі "місяць/день/рік"
current_date = datetime.now().strftime("%m/%d/%Y")

# Створити пустий список для зберігання даних про оголошення
ad_info_list = []

# функція призначена для отримання всіх посилань на фотографії в оголошенні.
def img_save_to_json_data(url):
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    #chrome_options.add_argument('--headless')  # Додаємо параметр для фонового режиму
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    time.sleep(1)

    button = driver.find_element(By.XPATH, '//div[@class="thumbnail last-child first-child"]')
    time.sleep(1)

    # Натискання на кнопку
    button.click()
    time.sleep(1)

    # Знаходження елементу на сторінці
    element = driver.find_element(By.XPATH, "//div[@class='description']")

    # Отримання тексту елемента
    element_text = int(element.text.split("/")[1])

    list_img = []

    for i in range(element_text):
        # Знаходження елемента за id "fullImg"
        img_element = driver.find_element(By.ID, 'fullImg')

        # Отримання значення атрибута src
        src_value = img_element.get_attribute('src')

        list_img.append(src_value)

        # Знаходження елемента
        next_img = driver.find_element(By.ID, 'fullImg')
        time.sleep(1)
        # Натискання на елемент
        next_img.click()
        time.sleep(1)

    # Завершення сеансу
    driver.quit()

    return list_img



#Запуск скрипта

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
#chrome_options.add_argument('--headless')  # Додаємо параметр для фонового режиму
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://realtylink.org/en/properties~for-rent')

for next_page in range(3):

    # Знаходження всіх елементів зображень за атрибутом src
    img_elements = driver.find_elements(By.XPATH, '//img[@itemprop="image"]')

    # Проходження по кожному елементу та натискання на нього
    for i in range(len(img_elements)):
        img_element = driver.find_elements(By.XPATH, '//img[@itemprop="image"]')[i]
        img_element.click()

        # Отримання поточного URL після натискання на зображення
        url = driver.current_url
        time.sleep(1)

        # Встановлення заголовків, щоб емулювати браузер
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        # Перевірка на правильність отримання сторінки
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Знаходження опису оголошення, перевірка чи елемент існує
            description_elem = soup.find("div", itemprop="description")
            if description_elem:
                description = description_elem.text.strip()
                print("Опис:", description)
            else:
                description = "Опис не знайдено"


            # Знаходження та збереження заголовка (title)
            title_elem = soup.find("span", {"data-id": "PageTitle"})
            title = title_elem.text.strip() if title_elem else "Заголовок не знайдено"


            # Знаходження та збереження регіону (region)
            region_elem = soup.find("h2", itemprop="address")
            region = region_elem.text.strip() if region_elem else "Регіон не знайдено"
            print("Регіон:", ', '.join(region.split(',')[1:]).strip())

            # Знаходження та збереження адреси (address)
            address_elem = soup.find("h2", itemprop="address")
            address = region_elem.text.strip() if region_elem else "Адреса не знайдена"

            # Знаходження та збереження Ціни (price)
            price_elem = soup.find("div", class_="price text-right")
            price_currency = price_elem.find("meta", itemprop="priceCurrency")["content"]
            price_value = price_elem.find("meta", itemprop="price")["content"]
            price = f"{price_currency} {price_value}"

            # Знаходження та збереження кількості кімнат (rooms)
            rooms_elem = soup.find("div", class_="col-lg-3 col-sm-6 cac")
            rooms_text = rooms_elem.text.strip() if rooms_elem else "Кількість кімнат не знайдена"

            # Перевірка чи повертається числове значення
            rooms_number = rooms_text[0] if rooms_text and rooms_text[0].isdigit() else None

            # Збереження інформації у випадку відсутності даних
            rooms = rooms_number if rooms_number is not None else "Кількість кімнат не знайдена"


            # Знаходження та збереження площі (real estate area)
            area_elem = soup.find("div", class_="carac-value")
            area = area_elem.text.strip() if area_elem else "Площа не знайдена"

            # Збереження інформації у вигляді JSON
            ad_info = {
                "title": title,
                "description": description,
                "region": ', '.join(region.split(',')[1:]).strip(),
                "price": price,
                "date": current_date,
                "rooms": rooms[0],
                "real estate area": area,
                "address": address,
                "url": response.url,
                "array links images": img_save_to_json_data(url)
            }

            try:
                with open("realtylink_info.json", "r+", encoding="utf-8") as json_file:
                    # Читання існуючих даних з файлу
                    ad_info_list = json.load(json_file)
            except FileNotFoundError:
                # Якщо файл не існує, створення нового списку
                ad_info_list = []

            # Додавання нового об'єкта до списку
            ad_info_list.append(ad_info)

            # Збереження всіх оголошень у файл
            with open("realtylink_info.json", "w", encoding="utf-8") as json_file:
                json.dump(ad_info_list, json_file, ensure_ascii=False, indent=2)

            print("JSON файл збережено.")

        driver.back()
        time.sleep(1)

    # Знаходження елементу за класом "next"
    next_button = driver.find_element(By.CLASS_NAME, 'next')

    # Натискання на елемент
    next_button.click()
    time.sleep(1)

driver.quit()
