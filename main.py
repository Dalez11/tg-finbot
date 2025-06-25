import os
import requests
import random
import asyncio
from telegram import Bot

# === БЕРЁМ КЛЮЧИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHANNEL = "@fin_geniuss"

bot = Bot(token=TG_BOT_TOKEN)

IMAGES = [
    "https://picsum.photos/800/600?random=1",
    "https://picsum.photos/800/600?random=2",
    "https://picsum.photos/800/600?random=3",
    "https://picsum.photos/800/600?random=4",
    "https://picsum.photos/800/600?random=5"
]

def generate_title():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "TG Bot"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo-16k",
        "messages": [
            {"role": "system", "content": "Ты эксперт в маркетинге и копирайтинге."},
            {"role": "user", "content": "Придумай уникальный и интересный заголовок для короткой статьи на тему личных финансов, инвестиций или мышления богатых. Не повторяйся. Коротко и цепляюще."}
        ],
        "temperature": 0.9
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip().strip('"')
    except Exception as e:
        print("❌ Ошибка генерации заголовка:", e)
        return "Финансовая грамотность: с чего начать"

def generate_article(title):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "TG Bot"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo-16k",
        "messages": [
            {"role": "system", "content": "Ты профессиональный копирайтер по финансовой тематике."},
            {"role": "user", "content": f"Напиши короткую статью на тему: {title}. Максимум 900 символов. Без повторов и клише."}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Ошибка генерации статьи:", e)
        return "Не удалось сгенерировать статью 😢"

async def post_to_telegram(title, text, image_url):
    try:
        if len(text) > 900:
            text = text[:900].rsplit('.', 1)[0] + "..."

        caption = f"<b>{title}</b>\n\n{text}"

        await bot.send_photo(
            chat_id=TG_CHANNEL,
            photo=image_url,
            caption=caption,
            parse_mode='HTML'
        )
        print(f"✅ Пост отправлен: {title}")
    except Exception as e:
        print("❌ Ошибка Telegram:", e)

async def post_article():
    title = generate_title()
    image = random.choice(IMAGES)
    print(f"📝 Генерация статьи: {title}")
    article = generate_article(title)
    await post_to_telegram(title, article, image)

async def main():
    await post_article()  # 🔥 Первый пост сразу
    while True:
        await asyncio.sleep(10 * 60)  # 10 минут
        await post_article()

if __name__ == "__main__":
    asyncio.run(main())


