import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import csv

model_name = "EleutherAI/gpt-neo-125M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def llm_generate_push(name, product, top_categories, benefit_sum):
    if isinstance(top_categories, str):
        top_categories = [cat.strip() for cat in top_categories.split(",")]

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
    return push


input_csv = "input_clients.csv" # Файл от Айбара
df = pd.read_csv(input_csv)

pushes = []
for _, row in df.iterrows():
    push = llm_generate_push(
        name=row["name"],
        product=row["product"],
        top_categories=row["top_categories"],
        benefit_sum=row["benefit_sum"]
    )
    pushes.append(push)

df["push_notification"] = pushes

final_df = df[["client_code", "product", "push_notification"]]
final_df.to_csv("final_push_notifications.csv", index=False, encoding="utf-8")

print("Файл сохранён")