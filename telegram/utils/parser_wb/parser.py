from loguru import logger
import requests
from bs4 import BeautifulSoup as BS
import lxml

from main.models import *


def get_categories():
    """Возвращает список категорий"""
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'if-modified-since': 'Wed, 02 Oct 2024 13:01:16 GMT',
        'origin': 'https://www.wildberries.ru',
        'priority': 'u=1, i',
        'referer': 'https://www.wildberries.ru/catalog/zhenshchinam',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    response = requests.get('https://static-basket-01.wbbasket.ru/vol0/data/main-menu-kz-ru-v3.json')

    return response


def get_card_data(url, shard, cat_id):
    """Запрос данных по карточки товара"""
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': f'https://www.wildberries.ru{url}?sort=popular&page=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'ab_testing': 'false',
        'appType': '1',
        'cat': cat_id,
        'curr': 'rub',
        'dest': '134',
        'page': '1',
        'sort': 'rate',
        'spp': '30',
    }

    response = requests.get(f'https://catalog.wb.ru/catalog/{shard}/v2/catalog', params=params, headers=headers)

    return response


def get_images(id, vol, part, pics):
    """сбор ссылок на изображения товара"""
    image_list = []
    short_id = int(vol)
    if 0 <= short_id <= 143:
        basket = "01"
    elif 144 <= short_id <= 287:
        basket = "02"
    elif 288 <= short_id <= 431:
        basket = "03"
    elif 432 <= short_id <= 719:
        basket = "04"
    elif 720 <= short_id <= 1007:
        basket = "05"
    elif 1008 <= short_id <= 1061:
        basket = "06"
    elif 1062 <= short_id <= 1115:
        basket = "07"
    elif 1116 <= short_id <= 1169:
        basket = "08"
    elif 1170 <= short_id <= 1313:
        basket = "09"
    elif 1314 <= short_id <= 1601:
        basket = "10"
    elif 1602 <= short_id <= 1655:
        basket = "11"
    elif 1656 <= short_id <= 1919:
        basket = "12"
    elif 1920 <= short_id <= 2045:
        basket = "13"
    elif 2046 <= short_id <= 2189:
        basket = "14"
    elif 2190 <= short_id <= 2405:
        basket = "15"
    elif 2406 <= short_id <= 2621:
        basket = "16"
    elif 2622 <= short_id <= 2837:
        basket = "17"
    elif 2838 <= short_id <= 3053:
        basket = "18"
    else:
        basket = "19"

    urls = []
    for i in range(1, pics):
        urls.append(
            f"https://basket-{basket}.wbbasket.ru/vol{str(vol)}/part{str(part)}/{str(id)}/images/big/{i}.webp"
        )
    return urls


def run_parser_wb():
    categories = get_categories()
    category_data = {}
    for item in categories.json():
        if item.get("name") == "Женщинам":
            category_data = {
                "url": item.get("url"),
                "childs": [{
                    "url": child.get("url"),
                    "shard": child.get("shard"),
                    "cat_id": child.get("id")
                } for child in item.get("childs") if
                           child.get("name") != "Спецодежда и СИЗы" and child.get("name") != "Подарки женщинам"]
            }
            break

    cards = []
    for category in category_data.get("childs"):
        try:
            data = get_card_data(url=category.get("url"), shard=category.get("shard"), cat_id=category.get("cat_id")).json()

            for item in data.get("data").get("products")[:16]:
                try:
                    product_data = {
                            "name": item.get("name"),
                            "product_category": category.get("shard"),
                            "article": item.get("id"),
                            "review": item.get("reviewRating"),
                            "entity": item.get("entity"),
                            "price": f'{str(item.get("sizes")[0]["price"]["total"])[:-2]} ₽',
                            "feedbacks": item.get("feedbacks"),
                            "url": f"https://www.wildberries.ru/catalog/{item.get('id')}/detail.aspx?targetUrl=EX",
                            "pics": item.get("pics"),
                            "part": f"{int(item.get('id')) // 1000}",
                            "vol": f"{int(item.get('id')) // 100000}",
                            "images": get_images(
                                id=item.get("id"),
                                vol=f"{int(item.get('id')) // 100000}",
                                part=f"{int(item.get('id')) // 1000}",
                                pics=item.get("pics")
                            ),
                            "posted": False
                        }

                    if Post.objects.filter(article=str(product_data.get("article"))).exists():
                        logger.error("Такой товар уже присутсвует")
                    else:
                        post = Post.objects.create(
                            article=product_data.get("article"),
                            product_category=product_data.get("product_category"),
                            text=f"""{product_data['name']}\n
        Цена: {product_data['price']}\n
        <a href="{product_data['url']}">Артикул ссылка: {product_data['article']}</a>\n
        ⭐️ {product_data['review']} Отзывы: {product_data['feedbacks']}\n
        {("#"+product_data['entity'].lower()) if product_data.get('entity') else ''}\n
        ♥️ - нравится\n🤔 - ищем дальше
                        """
                        )

                    # Добавляем медиафайлы
                    for image_url in product_data["images"][:5]:
                        Media.objects.create(
                            file_url=image_url,  # Сохраните URL для загрузки файла
                            post=post  # Связываем медиа с постом
                        )
                except Exception as ex:
                    pass
        except Exception as ex:
            pass
    logger.debug("Парсинг закончен")


def run_parser_tg():
    """Запуск пасера tg контента"""
    logger.debug("TG Parser is run")
    # for i in range(1, 10):
    with open(f"/mnt/638AED35134656EE/Desktop_linux/Telegram/content/psih/messages.html") as file:
        src = file.read()

        soup = BS(src, "lxml")

        all_messages = soup.find_all(class_="message default clearfix")
        logger.debug(f"Total messages found: {len(all_messages)}")
        for index, item in enumerate(all_messages):
            text_element = item.find(class_='text')
            if text_element:
                post = Post.objects.create(
                    text=text_element.get_text().strip()
                )
                image_tag = item.find('a', class_='photo_wrap')
                if image_tag:
                    logger.debug(f"/mnt/638AED35134656EE/Desktop_linux/Telegram/content/psih/{image_tag.get('href')}")
                    filename = f"/mnt/638AED35134656EE/Desktop_linux/Telegram/content/psih/{image_tag.get('href')}"
                    with open(filename, 'rb') as f:
                        django_file = File(f)
                        media = Media(post=post)  # Создаем объект медиа
                        media.file.save(os.path.basename(filename), django_file)  # Сохраняем файл
                        media.save()  # Сохраняем объект медиа
            else:
                logger.debug(f"{index} - No text found")


    logger.debug("Parsing completed")