import random

TEMPLATES = {
    "default": [
        "{name}, для вас спецпредложение: {product}. Экономия {benefit_sum:,.0f} ₸ на {categories}. {cta}",
        "{name}, обратите внимание на {product} — выгода {benefit_sum:,.0f} ₸ в {categories}. {cta}",
        "{name}, мы подготовили для вас {product}. Сэкономьте {benefit_sum:,.0f} ₸ на {categories}. {cta}",
    ],
    "premium": [
        "✨ {name}, премиальный уровень: {product}. Ваша выгода {benefit_sum:,.0f} ₸ на {categories}. {cta}",
        "{name}, только для вас премиальное предложение — {product}. Экономия {benefit_sum:,.0f} ₸. {cta}",
        "🎯 {name}, {product} открывает новые возможности. Сбережёте {benefit_sum:,.0f} ₸ на {categories}. {cta}",
    ],
    "travel": [
        "✈️ {name}, с {product} ваши путешествия выгоднее — {benefit_sum:,.0f} ₸ экономии на {categories}. {cta}",
        "{name}, {product} для поездок: возвращаем {benefit_sum:,.0f} ₸ на {categories}. {cta}",
        "🌍 {name}, {product} создана для путешествий. Ваша выгода {benefit_sum:,.0f} ₸. {cta}",
    ],
    "shopping": [
        "🛍️ {name}, с {product} покупки в {categories} выгоднее на {benefit_sum:,.0f} ₸. {cta}",
        "{name}, используйте {product} и экономьте {benefit_sum:,.0f} ₸ на {categories}. {cta}",
        "🔥 {name}, {product} для шопинга. Экономия {benefit_sum:,.0f} ₸ в {categories}. {cta}",
    ]
}


def get_random_template(template_type="default"):
    """Возвращает случайный шаблон по типу"""
    templates = TEMPLATES.get(template_type, TEMPLATES["default"])
    return random.choice(templates)
