# Content Protocol - Anti-Hallucination System

Протокол разделения контента и инструкций для предотвращения фабрикации данных при генерации кода.

## Проблема

При генерации кода LLM (Gemini) может:
- Заменить реальные тексты generic-описаниями
- Перефразировать заголовки и описания
- Заменить имена, числа, бренды выдуманными
- Добавить несуществующий контент
- Удалить секции или карточки

## Решение: Content Manifest

JSON-файл с **всеми** текстами, числами, ссылками и alt-текстами. Передаётся в Gemini через `--content`, отделяя данные от инструкций по верстке.

## JSON-схема манифеста

```json
{
  "meta": {
    "title": "Page Title",
    "description": "Meta description",
    "lang": ["en", "ru"],
    "favicon": "images/favicon.png"
  },
  "sections": [
    {
      "id": "hero",
      "type": "hero",
      "heading": { "en": "English Title", "ru": "Русский заголовок" },
      "subheading": { "en": "Subtitle text", "ru": "Подзаголовок" },
      "cta": [
        { "text": { "en": "Get Started", "ru": "Начать" }, "href": "#contact", "style": "primary" }
      ]
    },
    {
      "id": "about",
      "type": "about",
      "heading": { "en": "About", "ru": "О нас" },
      "content": { "en": "Full text paragraph...", "ru": "Полный текст параграфа..." },
      "person": {
        "name": "Alex Johnson",
        "role": { "en": "Founder & CEO", "ru": "Основатель и CEO" },
        "photo": "images/photo.webp"
      }
    },
    {
      "id": "services",
      "type": "cards",
      "heading": { "en": "Services", "ru": "Услуги" },
      "items": [
        {
          "title": { "en": "Service Name", "ru": "Название услуги" },
          "description": { "en": "Description", "ru": "Описание" },
          "icon": "chart-line"
        }
      ]
    },
    {
      "id": "stats",
      "type": "stats",
      "items": [
        { "value": "150+", "label": { "en": "Projects", "ru": "Проектов" } }
      ]
    }
  ],
  "images": [
    { "id": "logo", "src": "images/logo.png", "alt": { "en": "Company logo", "ru": "Логотип компании" } },
    { "id": "photo", "src": "images/photo.webp", "alt": { "en": "Alex Johnson", "ru": "Алекс Джонсон" } }
  ],
  "navigation": [
    { "text": { "en": "About", "ru": "О нас" }, "href": "#about" },
    { "text": { "en": "Services", "ru": "Услуги" }, "href": "#services" }
  ],
  "footer": {
    "copyright": "2025 TechCorp",
    "links": [
      { "text": "Telegram", "href": "https://t.me/channel" }
    ]
  }
}
```

## Правила для Opus (создатель манифеста)

1. Извлечь **все** тексты из анализа дизайна или скриншота
2. Для каждого текста указать точное значение, без перефразирования
3. Для билингвальных сайтов указать обе версии (en/ru)
4. Включить все числа, статистику, бейджи
5. Включить все ссылки (href) и alt-тексты
6. Включить навигацию и footer
7. Показать манифест пользователю для проверки перед генерацией кода

## Правила для Gemini (потребитель манифеста)

1. Использовать ТОЛЬКО тексты из манифеста
2. НЕ перефразировать, НЕ сокращать, НЕ дополнять
3. НЕ добавлять тексты, которых нет в манифесте
4. НЕ удалять секции или карточки из манифеста
5. Сохранять порядок секций как в манифесте
6. Для билингвальных сайтов использовать data-атрибуты (data-en, data-ru)
7. Числа и статистика воспроизводятся символ-в-символ

## Использование

```bash
# Генерация с манифестом
python3 openrouter_client.py code \
  --prompt "Create responsive landing page with bento-grid services, glassmorphism cards" \
  --content "content.json" \
  --image "reference.png" \
  --output "index.html"

# Патч с манифестом
python3 openrouter_client.py patch \
  --file "index.html" \
  --prompt "Add new testimonials section after services" \
  --content "content.json" \
  --output "index.html"
```
