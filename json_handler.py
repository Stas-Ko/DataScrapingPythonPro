import json


def save_to_json(ad_info, count_obj):

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

        print(f"JSON файл {count_obj} збережено.")
