#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест обновленной системы с ИИ генерацией пуш-уведомлений
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Тестирует импорты всех модулей"""
    try:
        from ai.analytics import Analytics
        print("✅ Analytics импортирован успешно")
        
        from ai.product_analyzer import ProductAnalyzer
        print("✅ ProductAnalyzer импортирован успешно")
        
        from ai.recommendations import llm_generate_push
        print("✅ llm_generate_push импортирован успешно")
        
        from back.csvgenerator import CSVGenerator
        print("✅ CSVGenerator импортирован успешно")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_single_client():
    """Тестирует обработку одного клиента"""
    try:
        from ai.analytics import Analytics
        from ai.product_analyzer import ProductAnalyzer
        from ai.recommendations import llm_generate_push
        
        print("\n=== Тест обработки клиента 1 ===")
        
        # Анализируем клиента
        analytics = Analytics()
        client_data = analytics.analyze_client(1)
        print(f"✅ Клиент: {client_data['name']}")
        print(f"   Город: {client_data['city']}")
        print(f"   Топ категории: {list(client_data['top_categories'].keys())[:3]}")
        
        # Анализируем продукты
        product_analyzer = ProductAnalyzer()
        best_product = product_analyzer.analyze_products(client_data)
        print(f"✅ Лучший продукт: {best_product['name']}")
        print(f"   Скор: {best_product['score']:.2f}")
        
        # Генерируем пуш с помощью ИИ
        top_categories = list(client_data['top_categories'].keys())[:3]
        benefit_sum = best_product['score'] * 1000
        
        push_notification = llm_generate_push(
            name=client_data['name'],
            product=best_product['name'],
            top_categories=top_categories,
            benefit_sum=benefit_sum
        )
        
        print(f"✅ Пуш-уведомление: {push_notification}")
        print(f"   Длина: {len(push_notification)} символов")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании клиента: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование обновленной системы TJK-BCC-Project")
    print("=" * 60)
    
    # Тест импортов
    if not test_imports():
        print("\n❌ Тест импортов не прошел")
        return False
    
    # Тест обработки одного клиента
    if not test_single_client():
        print("\n❌ Тест обработки клиента не прошел")
        return False
    
    print("\n🎉 Все тесты прошли успешно!")
    print("✅ Система готова к работе с ИИ генерацией пуш-уведомлений")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
