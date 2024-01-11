# DataScrapingPythonPro

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




# Встановіть залежності:

Залежності включають:

requests
beautifulsoup4
selenium
datetime
Завантажте та встановіть chromedriver для сумісності з вашою версією браузера Chrome.

Запустіть скрипт:
