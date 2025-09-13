<<<<<<< HEAD
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Основной файл для запуска системы персонализированных рекомендаций
TJK-BCC-Project
"""

import sys
import os
from pathlib import Path

# Добавляем текущую папку в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from back.csvgenerator import CSVGenerator

def main():
    """Основная функция для запуска системы"""
    print("🚀 Запуск системы персонализированных рекомендаций TJK-BCC-Project")
    print("=" * 60)
    
    try:
        # Создаем генератор CSV
        generator = CSVGenerator()
        
        # Обрабатываем всех клиентов
        print("📊 Обрабатываем 60 клиентов...")
        results = generator.process_all_clients()
        
        # Сохраняем результаты
        print("\n💾 Сохраняем результаты...")
        output_file = generator.save_results(results, "personalized_recommendations.csv")
        
        print(f"\n✅ Генерация завершена!")
        print(f"📁 Файл сохранен: {output_file}")
        print(f"👥 Обработано клиентов: {len(results)}")
        
        # Показываем статистику
        products = {}
        for result in results:
            product = result['product']
            products[product] = products.get(product, 0) + 1
        
        print(f"\n📈 Статистика рекомендаций:")
        for product, count in sorted(products.items(), key=lambda x: x[1], reverse=True):
            print(f"   {product}: {count} клиентов")
        
        # Показываем примеры
        print(f"\n📝 Примеры уведомлений:")
        for i, result in enumerate(results[:3]):
            print(f"   {i+1}. Клиент {result['client_code']}: {result['push_notification']}")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
=======
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
>>>>>>> 483bc2eab05204f41fc39a4623040b09868709d7
