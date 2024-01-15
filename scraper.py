import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from utils import get_image_links


# функція призначена для отримання даних зі сторінки.
def get_page_data(url, current_date, driver):

    # Встановлення заголовків, щоб емулювати браузер
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    }

    # Відправлення GET-запиту і отримання відповіді
    response = requests.get(url, headers=headers)

    # Перевірка на правильність отримання сторінки
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Знаходження опису оголошення, перевірка чи елемент існує
        description_elem = soup.find("div", itemprop="description")
        if description_elem:
            description = description_elem.text.strip()

        else:
            description = "Опис не знайдено"

        # Знаходження та збереження заголовка (title)
        title_elem = soup.find("span", {"data-id": "PageTitle"})
        title = title_elem.text.strip() if title_elem else "Заголовок не знайдено"

        # Знаходження та збереження регіону (region)
        region_elem = soup.find("h2", itemprop="address")
        region = region_elem.text.strip() if region_elem else "Регіон не знайдено"
        region = ', '.join(region.split(',')[1:]).strip()

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
            "region": region,
            "price": price,
            "date": current_date,
            "rooms": rooms[0],
            "real estate area": area,
            "address": address,
            "url": response.url,
            # виклик функції для збереження посилань на кожне фото одного оголошення
            "array links images": get_image_links(driver)
        }

        return ad_info


# функція призначена для отримання всіх посилань на фотографії в оголошенні.
def get_image_links(driver):

    # Знаходження елементу на сторінці
    button = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="thumbnail last-child first-child"]'))
    )
    time.sleep(0.5)

    # Натискання на кнопку
    button.click()
    time.sleep(1)

    # Знаходження елементу на сторінці
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='description']"))
    )

    # кількість фото в альбомі на сторінці
    if "/" in element.text:
        number_of_photos = int(element.text.split("/")[1])
    else:
        number_of_photos = 0  # или другое значение по умолчанию, если текст не содержит "/"

    # створення списку для зберігання посилання на фото
    list_img = []

    for i in range(number_of_photos):
        # Знаходження елемента за id "fullImg"
        img_element = driver.find_element(By.ID, 'fullImg')

        # Отримання значення атрибута src
        src_value = img_element.get_attribute('src')

        # Додавання значення атрибута src до списку
        list_img.append(src_value)

        # створення прапора для управління циклом, реакція на винятки
        check_errors = True

        while check_errors:

            try:
                # Знаходження елемента
                next_img = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, 'fullImg'))
                )
                next_img.click()

                # прапора False  якщо не виникло винятків
                check_errors = False
            except Exception as e:
                time.sleep(2)

    # повернення на попередню сторінку
    driver.back()

    # список посилань на фото з одного оголошення
    return list_img
