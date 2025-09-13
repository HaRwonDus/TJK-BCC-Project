import random
from datetime import datetime

class PushGenerator:
    def __init__(self):
        self.month_names = {
            1: "январе", 2: "феврале", 3: "марте", 4: "апреле",
            5: "мае", 6: "июне", 7: "июле", 8: "августе",
            9: "сентябре", 10: "октябре", 11: "ноябре", 12: "декабре"
        }
        
        self.templates = {
            "Карта для путешествий": [
                "{name}, в {month} у вас много поездок на такси на {amount} ₸. С картой для путешествий вернули бы ≈{cashback} ₸. Откройте карту в приложении.",
                "{name}, вы часто путешествуете и пользуетесь такси. Карта для путешествий даёт 4% кешбэк на все поездки. Оформить карту.",
                "{name}, в {month} потратили {amount} ₸ на поездки. С тревел-картой часть расходов вернулась бы кешбэком. Хотите оформить?"
            ],
            "Премиальная карта": [
                "{name}, у вас стабильно крупный остаток и траты в ресторанах. Премиальная карта даст повышенный кешбэк и бесплатные снятия. Оформить сейчас.",
                "{name}, ваш баланс {balance} ₸ позволяет получить максимум от премиальной карты — до 4% кешбэка. Подключить карту.",
                "{name}, с вашими тратами премиальная карта сэкономит {savings} ₸ в месяц. Оформить карту."
            ],
            "Кредитная карта": [
                "{name}, ваши топ-категории — {cat1}, {cat2}, {cat3}. Кредитная карта даёт до 10% в любимых категориях и на онлайн-сервисы. Оформить карту.",
                "{name}, вы тратите много на {top_category}. Кредитная карта вернёт до 10% с этих покупок. Получить карту.",
                "{name}, с вашими тратами кредитная карта сэкономит {savings} ₸ в месяц. Оформить сейчас."
            ],
            "Обмен валют": [
                "{name}, вы часто платите в {currency}. В приложении выгодный обмен и авто-покупка по целевому курсу. Настроить обмен.",
                "{name}, обмен валют в приложении без комиссии и с выгодным курсом. Настроить уведомления о курсе.",
                "{name}, можете выставить целевой курс для автоматической покупки валюты. Настроить обмен."
            ],
            "Кредит наличными": [
                "{name}, если нужен запас на крупные траты — можно оформить кредит наличными с гибкими выплатами. Узнать доступный лимит.",
                "{name}, кредит наличными от 12% годовых без залога и справок. Рассчитать условия.",
                "{name}, нужны деньги? Кредит наличными с гибким погашением. Узнать лимит."
            ],
            "Депозит Мультивалютный": [
                "{name}, у вас остаются свободные средства. Мультивалютный депозит под 14,5% с доступом к деньгам. Открыть вклад.",
                "{name}, разместите свободные средства на мультивалютном депозите под 14,5%. Открыть вклад.",
                "{name}, мультивалютный депозит под 14,5% — удобно хранить разные валюты. Открыть вклад."
            ],
            "Депозит Сберегательный": [
                "{name}, у вас есть свободные средства. Сберегательный депозит под 16,5% с максимальной защитой. Открыть вклад.",
                "{name}, максимальный доход 16,5% годовых на сберегательном депозите. Открыть вклад.",
                "{name}, сберегательный депозит под 16,5% — максимальная доходность при защите KDIF. Открыть вклад."
            ],
            "Депозит Накопительный": [
                "{name}, у вас остаются свободные средства. Накопительный депозит под 15,5% — удобно копить и получать вознаграждение. Открыть вклад.",
                "{name}, накопительный депозит под 15,5% с возможностью пополнения. Открыть вклад.",
                "{name}, планомерно откладывайте под 15,5% годовых. Открыть накопительный вклад."
            ],
            "Инвестиции": [
                "{name}, попробуйте инвестиции с низким порогом входа и без комиссий на старт. Открыть счёт.",
                "{name}, инвестиции от 6 ₸ без комиссий в первый год. Начать инвестировать.",
                "{name}, начните инвестировать с малых сумм без издержек. Открыть счёт."
            ],
            "Золотые слитки": [
                "{name}, диверсифицируйте сбережения золотыми слитками 999,9 пробы. Посмотреть ассортимент.",
                "{name}, золотые слитки для долгосрочного сохранения стоимости. Заказать в приложении.",
                "{name}, храните золото в сейфовых ячейках банка. Посмотреть условия."
            ]
        }
    
    def generate_push(self, client_data, product_info):
        """Генерирует персонализированное пуш-уведомление"""
        product_name = product_info["name"]
        client_name = client_data.get("name", "Клиент")
        
        # Выбираем случайный шаблон для продукта
        templates = self.templates.get(product_name, ["{name}, рассмотрите {product}."])
        template = random.choice(templates)
        
        # Получаем текущий месяц
        current_month = self.month_names.get(datetime.now().month, "августе")
        
        # Форматируем данные для шаблона
        template_data = {
            "name": client_name,
            "month": current_month,
            "product": product_name
        }
        
        # Добавляем специфичные данные в зависимости от продукта
        if product_name == "Карта для путешествий":
            template_data.update(self._get_travel_data(client_data))
        elif product_name == "Премиальная карта":
            template_data.update(self._get_premium_data(client_data))
        elif product_name == "Кредитная карта":
            template_data.update(self._get_credit_card_data(client_data))
        elif product_name == "Обмен валют":
            template_data.update(self._get_fx_data(client_data))
        elif product_name in ["Депозит Мультивалютный", "Депозит Сберегательный", "Депозит Накопительный"]:
            template_data.update(self._get_deposit_data(client_data))
        elif product_name == "Кредит наличными":
            template_data.update(self._get_loan_data(client_data))
        elif product_name == "Инвестиции":
            template_data.update(self._get_investment_data(client_data))
        elif product_name == "Золотые слитки":
            template_data.update(self._get_gold_data(client_data))
        
        # Форматируем шаблон
        try:
            push_text = template.format(**template_data)
        except KeyError as e:
            # Если не хватает данных, используем базовый шаблон
            push_text = f"{client_name}, рассмотрите {product_name}."
        
        # Ограничиваем длину (180-220 символов)
        if len(push_text) > 220:
            push_text = push_text[:217] + "..."
        
        return push_text
    
    def _get_travel_data(self, client_data):
        """Данные для карты путешествий"""
        top_categories = client_data.get("top_categories", {})
        
        # Считаем траты на поездки
        travel_amount = 0
        for category in ["Путешествия", "Такси", "Отели"]:
            travel_amount += top_categories.get(category, 0)
        
        # Вычисляем потенциальный кешбэк (4%)
        cashback = int(travel_amount * 0.04)
        
        return {
            "amount": self._format_currency(travel_amount),
            "cashback": self._format_currency(cashback)
        }
    
    def _get_premium_data(self, client_data):
        """Данные для премиальной карты"""
        balance = client_data.get("avg_monthly_balance_KZT", 0)
        total_spending = client_data.get("transaction_sum", 0)
        
        # Вычисляем потенциальную экономию (2-4% кешбэк)
        savings = int(total_spending * 0.03)  # 3% средний кешбэк
        
        return {
            "balance": self._format_currency(balance),
            "savings": self._format_currency(savings)
        }
    
    def _get_credit_card_data(self, client_data):
        """Данные для кредитной карты"""
        top_categories = client_data.get("top_categories", {})
        
        # Берем топ-3 категории
        sorted_categories = sorted(top_categories.items(), key=lambda x: x[1], reverse=True)
        categories = [cat[0] for cat in sorted_categories[:3]]
        
        # Если категорий меньше 3, добавляем общие
        while len(categories) < 3:
            categories.append("покупки")
        
        total_spending = client_data.get("transaction_sum", 0)
        savings = int(total_spending * 0.05)  # 5% средний кешбэк
        
        return {
            "cat1": categories[0],
            "cat2": categories[1],
            "cat3": categories[2],
            "top_category": categories[0],
            "savings": self._format_currency(savings)
        }
    
    def _get_fx_data(self, client_data):
        """Данные для обмена валют"""
        # Определяем основную валюту по переводам
        currencies = ["USD", "EUR", "RUB"]
        return {
            "currency": random.choice(currencies)
        }
    
    def _get_deposit_data(self, client_data):
        """Данные для депозитов"""
        balance = client_data.get("avg_monthly_balance_KZT", 0)
        return {
            "balance": self._format_currency(balance)
        }
    
    def _get_loan_data(self, client_data):
        """Данные для кредита наличными"""
        return {}
    
    def _get_investment_data(self, client_data):
        """Данные для инвестиций"""
        return {}
    
    def _get_gold_data(self, client_data):
        """Данные для золотых слитков"""
        return {}
    
    def _format_currency(self, amount):
        """Форматирует сумму в тенге"""
        if amount >= 1000000:
            return f"{amount // 1000000} млн ₸"
        elif amount >= 1000:
            return f"{amount // 1000} тыс ₸"
        else:
            return f"{int(amount)} ₸"
