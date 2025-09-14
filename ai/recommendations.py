import pandas as pd
import random
from ai.templates_dict import get_random_template


def llm_generate_push(name, product, top_categories, benefit_sum):
    """
    Генерация push-уведомления на основе словаря шаблонов.
    При необходимости fallback на дефолтный вариант.
    """

    # Обработка категорий
    if isinstance(top_categories, str):
        categories = [cat.strip() for cat in top_categories.split(",")]
    elif not top_categories:
        categories = ["общие траты"]
    else:
        categories = top_categories[:3]

    categories_str = ", ".join(categories)

    # Выбираем тип шаблона по продукту или категориям
    product_lower = product.lower()
    categories_lower = categories_str.lower()

    if "преми" in product_lower:
        template_type = "premium"
    elif "путеше" in product_lower or "travel" in product_lower:
        template_type = "travel"
    elif "шоп" in categories_lower or "магаз" in categories_lower:
        template_type = "shopping"
    else:
        template_type = "default"

    try:
        # Берём случайный шаблон из словаря
        template = get_random_template(template_type)

        push = template.format(
            name=name,
            product=product,
            categories=categories_str,
            benefit_sum=benefit_sum,
            cta=random.choice(["Открыть", "Посмотреть", "Настроить"])
        )

        # Проверка длины и fallback
        if len(push) < 50:
            return f"{name}, рекомендуем {product}. Оформить сейчас."

        return push

    except Exception as e:
        print(f"⚠️ Ошибка генерации push: {e}")
        return f"{name}, рекомендуем {product}. Оформить сейчас."
