import asyncio
import logging
from loguru import logger

from config import TELEGRAM_TOKEN
from back_end.bot import start_bot
from ai.model_loader import load_model
from ai.analytics import Analytics


async def main():

    #Логирование
    logger.add("logs/app.log", rotation="10 MB")
    logger.info("Запуск проекта...")

    #Загрузка AI-модели
    logger.info("Загрузка AI модели...")
    model, tokenizer = load_model()
    logger.success("Модель успешно загружена!")

    #Инициализация аналитики
    analytics = Analytics(data_input_path="data-input", data_output_path="data-output")
    logger.success("Аналитика инициализирована")

    #Запуск Telegram-бота
    logger.info("Запуск Telegram-бота...")
    await start_bot(token=TELEGRAM_TOKEN, model=model, tokenizer=tokenizer, analytics=analytics)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Проект остановлен.")
