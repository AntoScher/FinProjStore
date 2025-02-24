import requests

# Ваш токен бота
token = '6712048539:AAGREql6w2v47fLYsL0o7eUZgb6fQmW-H3A'

# URL для получения информации о боте
url = f'https://api.telegram.org/bot{token}/getMe'

# Запрос к API
response = requests.get(url)
data = response.json()

# Проверка, успешно ли выполнен запрос
if data['ok']:
    bot_id = data['result']['id']
    bot_username = data['result']['username']
    print(f"Bot ID: {bot_id}")
    print(f"Bot Username: {bot_username}")
else:
    print("Ошибка при получении данных о боте")



