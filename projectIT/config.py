"""
Файл конфигурации для генератора персонажей D&D
Замените YOUR_API_KEY на ваш реальный API ключ
"""

# Выберите один из вариантов:

# Вариант 1: OpenAI (платный, но мощный)
API_KEY = "YOUR_OPENAI_API_KEY_HERE"
API_TYPE = "openai"  # openai, yandex_gpt, или local

# Вариант 2: Yandex GPT (для русскоязычных лучше)
# API_KEY = "YOUR_YANDEX_API_KEY_HERE"
# API_TYPE = "yandex_gpt"

# Вариант 3: Локальная модель (бесплатно, но нужна видеокарта)
# API_TYPE = "local"
# MODEL_PATH = "путь_к_локальной_модели"

# Настройки генерации
GENERATION_SETTINGS = {
    "max_tokens": 3000,
    "temperature": 0.9,
    "model": "gpt-4"  # или "gpt-3.5-turbo" для экономии
}