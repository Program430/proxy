import requests


def get_data_about_word_through_proxy(message=None):
    url_proxy = 'https://tim.pythonanywhere.com/proxy'
    url = 'https://api.groq.com/openai/v1/chat/completions'

    headers = {
        "Authorization": "Bearer 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",
        'Content-Type': 'application/json',

    }

    main_data = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "model": "llama3-8b-8192"
    }

    json = {
        'url': url,
        'headers': headers,
        'data': main_data,
    }

    data = requests.post(url_proxy, json=json)
    if data.status_code != 200:  
        raise ValueError('Server returned error!')
    return data.json()

try:
    print(get_data_about_word_through_proxy('Привет'))
except ValueError as ve:
    print(ve)
