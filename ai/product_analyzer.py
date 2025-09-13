import pandas as pd
from datetime import datetime

class ProductAnalyzer:
    def __init__(self):
        self.products = {
            "Карта для путешествий": {
                "cashback_categories": ["Путешествия", "Такси"],
                "cashback_rate": 0.04,
                "description": "4% кешбэк на поездки и такси"
            },
            "Премиальная карта": {
                "base_cashback": 0.02,
                "premium_cashback": 0.04,
                "premium_categories": ["Ювелирные украшения", "Косметика и Парфюмерия", "Кафе и рестораны"],
                "balance_threshold_1": 1000000,  # 1 млн тенге
                "balance_threshold_2": 6000000,  # 6 млн тенге
                "free_withdrawals": True,
                "description": "Повышенный кешбэк и бесплатные снятия"
            },
            "Кредитная карта": {
                "credit_limit": 2000000,
                "max_cashback": 0.10,
                "online_cashback": 0.10,
                "online_categories": ["Играем дома", "Смотрим дома", "Кино"],
                "installment": True,
                "description": "До 10% кешбэк в любимых категориях"
            },
            "Обмен валют": {
                "fx_operations": ["fx_buy", "fx_sell"],
                "description": "Выгодный обмен валют без комиссии"
            },
            "Кредит наличными": {
                "rate_1_year": 0.12,
                "rate_over_1_year": 0.21,
                "description": "Кредит без залога и справок"
            },
            "Депозит Мультивалютный": {
                "rate": 0.145,
                "currencies": ["KZT", "USD", "RUB", "EUR"],
                "flexible": True,
                "description": "14,5% годовых, мультивалютный"
            },
            "Депозит Сберегательный": {
                "rate": 0.165,
                "flexible": False,
                "description": "16,5% годовых, без снятия"
            },
            "Депозит Накопительный": {
                "rate": 0.155,
                "topup": True,
                "withdrawal": False,
                "description": "15,5% годовых, можно пополнять"
            },
            "Инвестиции": {
                "min_amount": 6,
                "commission": 0.0,
                "description": "Инвестиции без комиссий"
            },
            "Золотые слитки": {
                "gold_operations": ["gold_buy_out", "gold_sell_in"],
                "description": "Покупка и продажа золота"
            }
        }
    
    def analyze_products(self, client_data):
        """Анализирует все продукты и выбирает лучший для клиента"""
        scores = {}
        
        for product_name, product_info in self.products.items():
            score = self._calculate_product_score(client_data, product_name, product_info)
            scores[product_name] = score
        
        # Сортируем по убыванию скора
        best_product_name = max(scores, key=scores.get)
        best_score = scores[best_product_name]
        
        return {
            "name": best_product_name,
            "score": best_score,
            "description": self.products[best_product_name]["description"],
            "all_scores": scores
        }
    
    def _calculate_product_score(self, client_data, product_name, product_info):
        """Вычисляет скор для конкретного продукта"""
        score = 0
        
        # Анализируем транзакции
        if "top_categories" in client_data:
            top_categories = client_data["top_categories"]
            
            # Карта для путешествий
            if product_name == "Карта для путешествий":
                travel_score = 0
                for category, amount in top_categories.items():
                    if category in product_info["cashback_categories"]:
                        travel_score += amount * product_info["cashback_rate"]
                score += travel_score / 1000  # Нормализуем
        
            # Премиальная карта
            elif product_name == "Премиальная карта":
                # Базовый кешбэк
                total_spending = client_data.get("transaction_sum", 0)
                base_cashback = total_spending * product_info["base_cashback"]
                
                # Премиальный кешбэк на специальные категории
                premium_cashback = 0
                for category, amount in top_categories.items():
                    if category in product_info["premium_categories"]:
                        premium_cashback += amount * product_info["premium_cashback"]
                
                # Бонус за высокий баланс
                balance = client_data.get("avg_monthly_balance_KZT", 0)
                if balance >= product_info["balance_threshold_2"]:
                    score += 1000
                elif balance >= product_info["balance_threshold_1"]:
                    score += 500
                
                score += (base_cashback + premium_cashback) / 1000
            
            # Кредитная карта
            elif product_name == "Кредитная карта":
                # Анализируем разнообразие категорий
                category_count = len(top_categories)
                if category_count >= 3:
                    score += 500
                
                # Бонус за онлайн-категории
                online_score = 0
                for category, amount in top_categories.items():
                    if category in product_info["online_categories"]:
                        online_score += amount * product_info["online_cashback"]
                score += online_score / 1000
        
        # Анализируем переводы
        if "total_transfer_in" in client_data and "total_transfer_out" in client_data:
            transfer_in = client_data["total_transfer_in"]
            transfer_out = client_data["total_transfer_out"]
            
            # Обмен валют
            if product_name == "Обмен валют":
                # Ищем операции с валютой в данных клиента
                # Это упрощенная логика - в реальности нужно анализировать типы переводов
                if transfer_in > 0 or transfer_out > 0:
                    score += 100
            
            # Депозиты
            elif product_name in ["Депозит Мультивалютный", "Депозит Сберегательный", "Депозит Накопительный"]:
                # Бонус за стабильные поступления
                if transfer_in > 100000:  # 100k тенге
                    score += 200
                
                # Бонус за высокий баланс
                balance = client_data.get("avg_monthly_balance_KZT", 0)
                if balance > 500000:  # 500k тенге
                    score += 300
            
            # Инвестиции
            elif product_name == "Инвестиции":
                # Бонус за молодой возраст (студенты)
                age = client_data.get("age", 30)
                if age < 25:
                    score += 200
                
                # Бонус за стабильные поступления
                if transfer_in > 50000:
                    score += 100
            
            # Золотые слитки
            elif product_name == "Золотые слитки":
                # Бонус за высокий доход
                if transfer_in > 200000:
                    score += 150
        
        # Кредит наличными (только при необходимости)
        if product_name == "Кредит наличными":
            # Анализируем, нужен ли кредит
            balance = client_data.get("avg_monthly_balance_KZT", 0)
            monthly_out = client_data.get("total_transfer_out", 0)
            
            # Если расходы превышают баланс
            if monthly_out > balance * 1.2:
                score += 500
            else:
                score = 0  # Не рекомендуем если не нужен
        
        return max(0, score)  # Не возвращаем отрицательные скоры
