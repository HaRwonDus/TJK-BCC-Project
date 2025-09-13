from pathlib import Path
import django
import pandas as pd
import sys
import os

# Добавляем корневую папку проекта в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.analytics import Analytics
from ai.product_analyzer import ProductAnalyzer
from ai.push_generator import PushGenerator

class CSVGenerator:
    def __init__(self, data_input_path="data_intput", data_output_path="data_output"):
        self.analytics = Analytics(data_input_path, data_output_path)
        self.product_analyzer = ProductAnalyzer()
        self.push_generator = PushGenerator()
        
    def process_all_clients(self):
        """Обрабатывает всех клиентов и генерирует CSV с рекомендациями"""
        results = []
        
        # Получаем список всех клиентов (1-60)
        client_codes = list(range(1, 61))
        
        for client_code in client_codes:
            try:
                print(f"Обрабатываем клиента {client_code}...")
                
                # Анализируем клиента
                client_data = self.analytics.analyze_client(client_code)
                
                # Анализируем продукты и выбираем лучший
                best_product = self.product_analyzer.analyze_products(client_data)
                
                # Генерируем пуш-уведомление
                push_notification = self.push_generator.generate_push(
                    client_data, best_product
                )
                
                # Добавляем результат
                results.append({
                    'client_code': client_code,
                    'product': best_product['name'],
                    'push_notification': push_notification
                })
                
                print(f"Клиент {client_code}: {best_product['name']}")
                
            except Exception as e:
                print(f"Ошибка при обработке клиента {client_code}: {e}")
                # Добавляем пустой результат для клиента с ошибкой
                results.append({
                    'client_code': client_code,
                    'product': 'Ошибка обработки',
                    'push_notification': 'Не удалось сгенерировать уведомление'
                })
        
        return results
    
    def save_results(self, results, filename="recommendations.csv"):
        """Сохраняет результаты в CSV файл"""
        df = pd.DataFrame(results)
        
        # Создаем папку data_output если её нет
        output_path = Path("data_output")
        output_path.mkdir(exist_ok=True)
        
        # Сохраняем файл
        file_path = output_path / filename
        df.to_csv(file_path, index=False, encoding='utf-8')
        
        print(f"Результаты сохранены в файл: {file_path}")
        print(f"Обработано клиентов: {len(results)}")
        
        return file_path

def main():
    """Основная функция для запуска генератора"""
    print("Запуск генератора CSV...")
    
    generator = CSVGenerator()
    
    # Обрабатываем всех клиентов
    results = generator.process_all_clients()
    
    # Сохраняем результаты
    output_file = generator.save_results(results)
    
    print(f"Генерация завершена! Файл: {output_file}")
    
    # Показываем первые несколько результатов
    print("\nПервые 5 результатов:")
    for i, result in enumerate(results[:5]):
        print(f"{i+1}. Клиент {result['client_code']}: {result['product']}")

if __name__ == "__main__":
    main()
    