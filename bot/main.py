import logging
import os

from aiogram import Bot, Dispatcher, types
from aiohttp import web
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

if not API_TOKEN:
    raise ValueError("Токен бота не найден. Убедитесь, что файл .env содержит TELEGRAM_API_TOKEN.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def notify(request):
    try:
        data = await request.json()
        logger.info(f"Получены данные: {data}")  # Логируем данные запроса

        telegram_id = data.get('telegram_id')
        order_id = data.get('order_id')
        new_status = data.get('new_status')

        if not telegram_id or not order_id or not new_status:
            logger.error("Отсутствуют обязательные поля")
            return web.json_response({'error': 'Missing required fields'}, status=400)

        # Проверяем, что telegram_id является числом
        try:
            telegram_id = int(telegram_id)
        except ValueError:
            logger.error(f"Некорректный telegram_id: {telegram_id}")
            return web.json_response({'error': 'Invalid telegram_id'}, status=400)

        # Пытаемся отправить сообщение
        try:
            message = f'Ваш заказ #{order_id} изменил статус на: {new_status}'
            await bot.send_message(chat_id=telegram_id, text=message)
            return web.json_response({'status': 'success'})
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            return web.json_response({'error': str(e)}, status=500)

    except Exception as e:
        logger.error(f'Ошибка при обработке запроса: {e}', exc_info=True)
        return web.json_response({'error': str(e)}, status=500)

app = web.Application()
app.router.add_post('/notify/', notify)

async def on_startup(app):
    try:
        # Проверяем, что бот может отправлять сообщения
        await bot.send_message(chat_id=1507961620, text="Бот запущен и готов к работе!")  # Замените на ваш ID
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

app.on_startup.append(on_startup)

if __name__ == '__main__':
    try:
        web.run_app(app, host='127.0.0.1', port=8081)
    except Exception as e:
        logger.error(f"Ошибка при запуске сервера: {e}")