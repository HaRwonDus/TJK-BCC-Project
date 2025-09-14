import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import csv

# Глобальные переменные для ленивой загрузки
model_name = "EleutherAI/gpt-neo-125M"
tokenizer = None
model = None

def _load_model():
    """Ленивая загрузка модели ИИ"""
    global tokenizer, model
    if tokenizer is None or model is None:
        print("🤖 Загружаем ИИ модель...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        print("✅ ИИ модель загружена!")

def llm_generate_push(name, product, top_categories, benefit_sum):
    """Генерирует пуш-уведомление с помощью ИИ"""
    # Загружаем модель при первом вызове
    _load_model()
    
    # Обрабатываем категории
    if isinstance(top_categories, str):
        top_categories = [cat.strip() for cat in top_categories.split(",")]
    elif not top_categories:
        top_categories = ["Общие траты"]
    
    # Ограничиваем количество категорий
    top_categories = top_categories[:3]

    prompt = f"""
Имя клиента: {name}
Рекомендуемый продукт: {product}
Топ категории трат: {', '.join(top_categories)}
Ожидаемая выгода: {benefit_sum:.0f} ₸

Сгенерируй персонализированное push-уведомление:
- дружелюбно, по делу
- 180–220 символов
- c CTA
- редполитика: без капса, максимум 1 восклицательный, emoji — 0–1
- Дата дд.мм.гггг (или «30 августа 2025» — где уместно)
- Соблюдай формат чисел (разряды пробелом, дроби — через запятую), валюту — через пробел перед символом (₸)
- CTA — «Открыть», «Настроить» или «Посмотреть»

Push: """
    
    try:
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        with torch.no_grad():
            generated_ids = model.generate(
                input_ids,
                max_length=input_ids.shape[1] + 50,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.8,
                pad_token_id=tokenizer.eos_token_id,
                num_return_sequences=1
            )
        output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        push = output.split("Push:")[1].strip().split("\n")[0]
        
        # Проверяем, что пуш не пустой
        if not push or len(push.strip()) < 10:
            return f"{name}, рекомендуем {product}. Оформить сейчас."
        
        return push
        
    except Exception as e:
        print(f"⚠️ Ошибка ИИ генерации: {e}")
        # Fallback уведомление
        return f"{name}, рекомендуем {product}. Оформить сейчас."
