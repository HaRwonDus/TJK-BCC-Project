#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ai.analytics import Analytics
from ai.product_analyzer import ProductAnalyzer
from ai.push_generator import PushGenerator

def test_system():
    """Тестирует систему на клиенте 1"""
    print("=== Тестирование системы персонализированных рекомендаций ===\n")
    
    # Инициализируем компоненты
    analytics = Analytics()
    product_analyzer = ProductAnalyzer()
    push_generator = PushGenerator()
    
    try:
        # Тестируем на клиенте 1
        print("1. Анализируем клиента 1...")
        client_data = analytics.analyze_client(1)
        print(f"   Имя: {client_data['name']}")
        print(f"   Город: {client_data['city']}")
        print(f"   Статус: {client_data['status']}")
        print(f"   Средний баланс: {client_data['avg_monthly_balance_KZT']:,.0f} ₸")
        print(f"   Общие траты: {client_data['transaction_sum']:,.0f} ₸")
        print(f"   Топ категории: {client_data['top_categories']}")
        
        print("\n2. Анализируем продукты...")
        best_product = product_analyzer.analyze_products(client_data)
        print(f"   Лучший продукт: {best_product['name']}")
        print(f"   Скор: {best_product['score']:.2f}")
        print(f"   Описание: {best_product['description']}")
        
        print("\n3. Генерируем пуш-уведомление...")
        push_notification = push_generator.generate_push(client_data, best_product)
        print(f"   Уведомление: {push_notification}")
        print(f"   Длина: {len(push_notification)} символов")
        
        print("\n✅ Тест прошел успешно!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_system()
