# Vibe Frontend Agent

> Мульти-модельный AI-агент для Claude Code: дизайн в код за минуты

![Status](https://img.shields.io/badge/status-v2-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Claude Code](https://img.shields.io/badge/Claude_Code-skill-blueviolet)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-orange)

## Что это

Скилл для [Claude Code](https://claude.ai/code), который конвертирует скриншот или URL сайта в готовый адаптивный HTML/CSS/JS с live preview.

Вдохновлён [Kombai](https://kombai.com). Захотел свой инструмент и навайбкодил за пару часов.

## Архитектура: 3 модели, 3 роли

```
┌─────────────────────────────────────────────┐
│              Claude Opus 4.6                │
│           (оркестратор в Claude Code)        │
│                                             │
│  - Получает задачу от пользователя          │
│  - Формирует промты для других моделей      │
│  - Ревьюит весь сгенерированный код         │
│  - Управляет итерациями                     │
└──────────┬──────────────────┬───────────────┘
           │                  │
           ▼                  ▼
┌──────────────────┐ ┌──────────────────┐
│  Gemini 3.1 Pro  │ │  Nano Banana 2   │
│  (через OpenRouter) │  (через OpenRouter) │
│                  │ │                  │
│ - Анализ дизайна │ │ - Иконки         │
│ - Генерация кода │ │ - Hero-фоны      │
│ - Патчинг файлов │ │ - Иллюстрации    │
│ - 1M контекст    │ │ - Favicon        │
└──────────────────┘ └──────────────────┘
```

| Модель | Роль | Зачем |
|--------|------|-------|
| **Claude Opus 4.6** | Оркестратор | Ставит задачи, ревьюит результат, общается с пользователем |
| **Gemini 3.1 Pro** | Кодогенерация | Анализ дизайна, генерация HTML/CSS/JS (1M контекст) |
| **Nano Banana 2** | Изображения | Генерация иконок, иллюстраций, фонов |

## Возможности

- **Скриншот/URL в код** - полная HTML-страница из изображения или живого сайта
- **Анализ дизайна** - извлечение цветов, шрифтов, сетки, компонентов
- **GSAP-анимации** - 4 уровня: от статики до максимума (ScrollTrigger, SplitText, Flip)
- **Live preview** - мгновенный просмотр через Playwright (desktop + mobile)
- **Анти-галлюцинационный протокол** - Content Manifest разделяет контент и инструкции
- **Патч без перегенерации** - точечные правки существующих файлов
- **Mobile-first** - адаптивная верстка по умолчанию
- **Мульти-стек** - HTML/CSS/JS, React+Tailwind, shadcn/ui, Astro, Svelte (v2)
- **Accessibility** - WCAG 2.1 AA: ARIA, alt-тексты, focus-стили, skip-link (v2)
- **Security Check** - XSS, CDN integrity, mixed content, localStorage audit (v2)
- **JS Quality** - early returns, const arrows, handle* prefix, JSDoc (v2)

## Быстрый старт

### Требования

- [Claude Code](https://claude.ai/code) (CLI)
- [OpenRouter](https://openrouter.ai/) API-ключ (для Gemini + Nano Banana)
- Python 3.10+ с `requests`, `python-dotenv`, `Pillow`

### Установка

```bash
# 1. Клонировать
git clone https://github.com/artemsharkUfa/vibe-frontend-agent.git

# 2. Скопировать в директорию скиллов Claude Code
cp -r vibe-frontend-agent ~/.claude/skills/frontend-agent

# 3. Настроить API-ключ
cp .env.example ~/.env
# Вписать свой OpenRouter ключ в ~/.env

# 4. Установить Python-зависимости
pip install requests python-dotenv Pillow
```

### Использование

В Claude Code просто пишите естественным языком:

```
# Из скриншота
Сверстай сайт как на скриншоте /path/to/design.png

# Из URL
Скопируй дизайн https://example.com

# Из описания
Сделай лендинг для AI-стартапа с hero, услугами и контактами

# Патч
Измени цвет кнопок на синий и добавь анимацию при скролле
```

## Промты для Gemini

Ключевой system prompt для кодогенерации содержит **CRITICAL CONTENT RULES**:

```
You are an expert frontend developer. Generate clean, production-ready code.
Use semantic HTML, CSS custom properties, mobile-first responsive design.
Use BEM naming for CSS classes.

CRITICAL CONTENT RULES:
1. Content text is SACRED - reproduce ALL text from the content manifest EXACTLY
2. NEVER invent, rephrase, summarize, or replace any text content
3. NEVER add placeholder text like 'Lorem ipsum'
4. If content manifest is provided, use ONLY data from it
5. Keep all numbers, names, titles, descriptions EXACTLY as given
6. Your job is LAYOUT and STYLING only. Content comes from the manifest.
```

Это решает главную проблему LLM-кодогенерации: модель не выдумывает и не перефразирует тексты.

## Анти-галлюцинационный протокол

**Проблема:** при генерации кода LLM заменяет реальные тексты generic-описаниями, перефразирует заголовки, выдумывает числа.

**Решение:** Content Manifest - JSON-файл со всеми текстами, числами и ссылками. Передаётся отдельно от инструкций по верстке через флаг `--content`.

```bash
# Генерация с манифестом
python3 scripts/openrouter_client.py code \
  --prompt "Responsive landing, bento-grid services, glassmorphism cards" \
  --content content.json \
  --image reference.png \
  --output index.html
```

Пример манифеста: [`examples/content-manifest.json`](examples/content-manifest.json)

Подробности: [`references/content-protocol.md`](references/content-protocol.md)

## Workflow

```
1. Вход               2. Анализ              3. План
   (скриншот/URL/       (цвета, шрифты,       (файлы, секции,
    описание)            сетка, компоненты)     стек, палитра)
       │                      │                      │
       ▼                      ▼                      ▼
4. Content Manifest    5. Генерация           6. Live Preview
   (JSON с текстами,     (HTML/CSS/JS           (Playwright:
    числами, ссылками)    через Gemini)          desktop+mobile)
                                                     │
                                                     ▼
                                              7. Итерации
                                                 (патч, ревью,
                                                  повтор превью)
```

1. **Определить вход** - скриншот, URL или текстовое описание
2. **Анализ дизайна** - Gemini извлекает структуру, палитру, типографику
3. **План** - Opus формирует план и показывает для одобрения
4. **Content Manifest** - JSON с точными текстами для анти-галлюцинации
5. **Генерация** - Gemini создаёт код, Opus ревьюит качество
6. **Preview + итерации** - Playwright показывает результат, правки по фидбеку

## Команды API-клиента

```bash
# Анализ дизайна
python3 scripts/openrouter_client.py analyze \
  --image screenshot.png --output analysis.md

# Генерация кода
python3 scripts/openrouter_client.py code \
  --prompt "Create responsive landing page" \
  --content content.json --image ref.png --output index.html

# Патч существующего файла
python3 scripts/openrouter_client.py patch \
  --file index.html --prompt "Center the hero section" --output index.html

# Генерация изображений
python3 scripts/openrouter_client.py image \
  --prompt "Flat icon of a gear, blue #3B82F6" \
  --aspect-ratio 1:1 --quality 2k --output icon.png
```

### Параметры изображений
- `--aspect-ratio`: `1:1` | `16:9` | `9:16` | `4:3` | `3:4`
- `--quality`: `1k` (1024px) | `2k` (2048px, default) | `4k` (4096px)

## GSAP-анимации

4 уровня анимации на выбор:

| Уровень | Что включает | GSAP-плагины |
|---------|-------------|-------------|
| Без анимации | Статичная страница | - |
| Минимальный | Fade/slide при скролле, hover на карточках | gsap + ScrollTrigger |
| Средний | + Text reveal, parallax, counters | + SplitText |
| Максимальный | + Horizontal scroll, SVG draw, Flip | + все плагины |

Каталог эффектов с готовым кодом: [`references/gsap-animations.md`](references/gsap-animations.md)

## Статус

**Работает:**
- Мульти-модельная архитектура (Opus + Gemini + Nano Banana)
- Анализ дизайна из скриншота/URL
- Генерация HTML/CSS/JS
- Content Manifest (анти-галлюцинация)
- GSAP-анимации
- Live preview через Playwright
- Патч существующих файлов

**Новое в v2:**
- Выбор стека перед генерацией (7+ вариантов)
- Accessibility (WCAG 2.1 AA) - ARIA, focus-стили, skip-link
- Security Check - проверка XSS, CDN integrity, localStorage
- JS Quality Rules - early returns, const arrows, JSDoc
- Image optimization - lazy loading, width/height, WebP

**В планах:**
- Поддержка многостраничных сайтов
- Экспорт в Figma-совместимый формат
- Автоматическое A/B тестирование вариантов

## Инструменты

- [Claude Code](https://claude.ai/code) + Claude Opus 4.6
- [OpenRouter API](https://openrouter.ai/)
- [Gemini 3.1 Pro](https://deepmind.google/technologies/gemini/) (1M контекст)
- Nano Banana 2 (генерация изображений)
- [Playwright](https://playwright.dev/) (live preview)
- [GSAP](https://gsap.com/) (анимации)

## Telegram

Пишу про AI, автоматизацию и vibe coding: [@Neironka_live](https://t.me/Neironka_live). Подписывайтесь.

## Лицензия

[MIT](LICENSE)
