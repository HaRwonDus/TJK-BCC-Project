from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ClientProfile(models.Model):
    """Профиль клиента"""
    
    STATUS_CHOICES = [
        ('student', 'Студент'),
        ('salary', 'Зарплатный клиент'),
        ('premium', 'Премиальный клиент'),
        ('standard', 'Стандартный клиент'),
    ]
    
    client_code = models.CharField(max_length=50, unique=True, verbose_name="Код клиента")
    name = models.CharField(max_length=200, verbose_name="Имя клиента")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(120)],
        verbose_name="Возраст"
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    avg_monthly_balance_KZT = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="Средний месячный баланс (KZT)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профили клиентов"
        ordering = ['client_code']
    
    def __str__(self):
        return f"{self.name} ({self.client_code})"


class Transaction(models.Model):
    """Транзакции клиента за 3 месяца"""
    
    CATEGORY_CHOICES = [
        ('clothing', 'Одежда и обувь'),
        ('food', 'Продукты питания'),
        ('cafe_restaurant', 'Кафе и рестораны'),
        ('medicine', 'Медицина'),
        ('auto', 'Авто'),
        ('sport', 'Спорт'),
        ('entertainment', 'Развлечения'),
        ('gas_station', 'АЗС'),
        ('cinema', 'Кино'),
        ('pets', 'Питомцы'),
        ('books', 'Книги'),
        ('flowers', 'Цветы'),
        ('eat_home', 'Едим дома'),
        ('watch_home', 'Смотрим дома'),
        ('play_home', 'Играем дома'),
        ('cosmetics', 'Косметика и Парфюмерия'),
        ('gifts', 'Подарки'),
        ('home_repair', 'Ремонт дома'),
        ('furniture', 'Мебель'),
        ('spa_massage', 'Спа и массаж'),
        ('jewelry', 'Ювелирные украшения'),
        ('taxi', 'Такси'),
        ('hotels', 'Отели'),
        ('travel', 'Путешествия'),
    ]
    
    CURRENCY_CHOICES = [
        ('KZT', 'Казахстанский тенге'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('RUB', 'Российский рубль'),
    ]
    
    date = models.DateTimeField(verbose_name="Дата транзакции")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Валюта")
    client = models.ForeignKey(
        ClientProfile, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        verbose_name="Клиент"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['client', 'date']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.client.name} - {self.get_category_display()} - {self.amount} {self.currency}"


class Transfer(models.Model):
    """Переводы клиента за 3 месяца"""
    
    TYPE_CHOICES = [
        ('salary_in', 'Зарплата (входящая)'),
        ('stipend_in', 'Стипендия (входящая)'),
        ('family_in', 'Семейные переводы (входящие)'),
        ('cashback_in', 'Кэшбэк (входящий)'),
        ('refund_in', 'Возврат (входящий)'),
        ('card_in', 'Пополнение карты (входящее)'),
        ('p2p_out', 'P2P перевод (исходящий)'),
        ('card_out', 'Перевод на карту (исходящий)'),
        ('atm_withdrawal', 'Снятие в банкомате'),
        ('utilities_out', 'Коммунальные услуги'),
        ('loan_payment_out', 'Платеж по кредиту'),
        ('cc_repayment_out', 'Погашение кредитной карты'),
        ('installment_payment_out', 'Платеж в рассрочку'),
        ('fx_buy', 'Покупка валюты'),
        ('fx_sell', 'Продажа валюты'),
        ('invest_out', 'Инвестиции (исходящие)'),
        ('invest_in', 'Инвестиции (входящие)'),
        ('deposit_topup_out', 'Пополнение депозита'),
        ('deposit_fx_topup_out', 'Пополнение валютного депозита'),
        ('deposit_fx_withdraw_in', 'Вывод с валютного депозита'),
        ('gold_buy_out', 'Покупка золота'),
        ('gold_sell_in', 'Продажа золота'),
    ]
    
    DIRECTION_CHOICES = [
        ('in', 'Входящий'),
        ('out', 'Исходящий'),
    ]
    
    CURRENCY_CHOICES = [
        ('KZT', 'Казахстанский тенге'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('RUB', 'Российский рубль'),
    ]
    
    date = models.DateTimeField(verbose_name="Дата перевода")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="Тип перевода")
    direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES, verbose_name="Направление")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Валюта")
    client = models.ForeignKey(
        ClientProfile, 
        on_delete=models.CASCADE, 
        related_name='transfers',
        verbose_name="Клиент"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Переводы"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['client', 'date']),
            models.Index(fields=['type']),
            models.Index(fields=['direction']),
        ]
    
    def __str__(self):
        return f"{self.client.name} - {self.get_type_display()} - {self.amount} {self.currency}"
