#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ai.analytics import Analytics
    print("✅ Analytics импортирован успешно")
    
    from ai.product_analyzer import ProductAnalyzer
    print("✅ ProductAnalyzer импортирован успешно")
    
    from ai.push_generator import PushGenerator
    print("✅ PushGenerator импортирован успешно")
    
    # Тестируем аналитику
    analytics = Analytics()
    print("✅ Analytics инициализирован")
    
    # Тестируем на клиенте 1
    client_data = analytics.analyze_client(1)
    print(f"✅ Данные клиента получены: {client_data['name']}")
    
    # Тестируем анализ продуктов
    product_analyzer = ProductAnalyzer()
    best_product = product_analyzer.analyze_products(client_data)
    print(f"✅ Лучший продукт: {best_product['name']}")
    
    # Тестируем генератор пушей
    push_generator = PushGenerator()
    push_notification = push_generator.generate_push(client_data, best_product)
    print(f"✅ Пуш сгенерирован: {push_notification[:50]}...")
    
    print("\n🎉 Все тесты прошли успешно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
