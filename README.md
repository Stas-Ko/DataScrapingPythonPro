# DataScrapingPythonPro

# Завдання

Парсинг інформації з сайту realtylink.org

Є сайт з оголошеннями по нерухомості realtylink.org у якого є серп з оголошеннями: Residental: For Rent

Потрібно написати .py скрипт, який сформує JSON, який буде містити: 
1. 60 оголошень з цього серпа. Кожне оголошення - окремий об'єкт в JSON файлі. 
2. Кожен об'єкт має містити наступні ключі: 
- лінк на оголошення
- тайтл оголошення (https://prnt.sc/6UfLi4VqTb6S) 
- регіон (https://prnt.sc/hYHrPfPAHG6v) 
- адресу (https://prnt.sc/tYIR1d7th1cw) 
- опис (https://prnt.sc/J_2_jonm6tgc) 
- масив зображень з оголошення (масив лінків на зображення)
- дату публікації/оновлення оголошення
- ціна 
- к-сть кімнат
- площа нерухомості  

Приклад JSON:

[
  {
    "title": "House for sale",
    "region": " Downtown PG, Prince George ",
     "address" :  "207 1499 6 Avenue, Downtown PG"
    ...
  },
  ...
]


# Опис проекту

Цей проект містить скрипт для парсингу даних із веб-сторінки та збереження їх у форматі JSON.

## Структура проекту

- `main.py`: Основний скрипт для запуску парсера.
- `scraper.py`: Модуль із функціями для парсингу даних.
- `json_handler.py`: Модуль з функціями для обробки та збереження даних у JSON.
- `realtylink_info.json` : Це файл, в якому зберігаються дані, отримані з веб-сайту RealtyLink за допомогою main.py. 
Формат цього файлу - JSON.
- `README.md`: Цей файл містить опис проекту.


# Встановіть залежності:

Залежності включають:

pip install requests
pip install beautifulsoup4
pip install selenium

Завантажте та встановіть chromedriver для сумісності з вашою версією браузера Chrome.

Запустіть `main.py` для виконання скрипта:
