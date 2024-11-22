import requests


def get_request_config(category_id: str, page_number: str) -> tuple[dict[str, str], dict[str, str]]:
    # Параметры запроса
    params = {
        'categoryId': category_id,
        'cityId': '9ae64229-9f7b-4149-b27a-d1f6ec74b5ce',
        'pageNumber': page_number,
        'z': '14-46'
    }

    # Заголовки запроса
    headers = {
        'sec-ch-ua-platform': '"Linux"',
        'Referer': '',
        'x-gast': '37068833.637526624,37068833.637526624',
        'sec-ch-ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'traceparent': '00-e03db3c5320b40913569f8c588ecf10a-e5c3a03f41eef85e-01',
        'x-app-version': '1.60.0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*'
    }
    # Возвращение params и headers
    return params, headers


def request_product_page(page_number: str, category_id: str):
    # URL для запроса
    url = 'https://goldapple.ru/front/api/catalog/products'
    params, headers = get_request_config(category_id=category_id, page_number=page_number)
    # Выполнение GET-запроса
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка:", response.status_code)

