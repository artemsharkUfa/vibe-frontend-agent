# Шаблон плана разработки

Заполнить перед генерацией кода. Показать пользователю для одобрения.

## Проект

- **Название:** [project-name] (латиница, kebab-case)
- **Описание:** [что это за страница/сайт]
- **Язык контента:** [ru / en]

## Технологический стек

- **Основной:** [HTML/CSS/JS | React+Tailwind | Vue | Next.js]
- **CSS-подход:** [Custom CSS | Tailwind | CSS Modules]
- **Шрифты:** [Google Fonts: Font1, Font2]
- **Иконки:** [Lucide / Heroicons / Font Awesome / нет]
- **Библиотеки:** [если нужны: Swiper, AOS, GSAP]

## Структура файлов

```
<project-name>/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
└── images/
```

## CSS Custom Properties

```css
:root {
  /* Цвета */
  --color-primary: #XXXXXX;
  --color-accent: #XXXXXX;
  --color-bg: #XXXXXX;
  --color-surface: #XXXXXX;
  --color-text: #XXXXXX;
  --color-text-secondary: #XXXXXX;

  /* Типографика */
  --font-heading: 'Font Name', sans-serif;
  --font-body: 'Font Name', sans-serif;

  /* Размеры */
  --container-width: 1200px;
  --border-radius: 8px;
  --spacing-unit: 8px;
}
```

## Секции страницы

| # | Секция | Содержимое | Компоненты |
|---|--------|-----------|------------|
| 1 | Header | Лого + навигация + CTA | nav, burger menu |
| 2 | Hero | Заголовок + подзаголовок + кнопка | background image/gradient |
| ... | ... | ... | ... |
| N | Footer | Контакты + ссылки + копирайт | grid layout |

## Breakpoints

- Mobile: default (< 768px)
- Tablet: @media (min-width: 768px)
- Desktop: @media (min-width: 1024px)
- Wide: @media (min-width: 1440px) — если нужен

## Заметки

[Особые требования, edge cases, TODO]
