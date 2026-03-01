# Превью через Playwright — Инструкция

## Для HTML/CSS/JS проектов

### 1. Запустить HTTP-сервер

```bash
cd outputs/<project-name> && python3 -m http.server 8080 &
```

Запустить в фоне (run_in_background: true). Запомнить task ID для остановки.

### 2. Открыть в Playwright

```
browser_navigate -> http://localhost:8080
```

### 3. Desktop-скриншот

```
browser_resize -> width: 1440, height: 900
browser_take_screenshot -> type: png, filename: preview-desktop.png
```

### 4. Mobile-скриншот

```
browser_resize -> width: 375, height: 812
browser_take_screenshot -> type: png, filename: preview-mobile.png
```

### 5. Проверка консоли

```
browser_console_messages -> level: error
```

Если есть ошибки — исправить и повторить.

### 6. Показать пользователю

Прочитать оба скриншота через Read tool, чтобы показать пользователю.

### 7. Остановить сервер

```bash
kill $(lsof -t -i:8080) 2>/dev/null
```

## Для React/Vite проектов

### 1. Установить зависимости и запустить

```bash
cd outputs/<project-name>
npm install
npm run dev -- --port 8080 &
```

Подождать 5 секунд для запуска.

### 2-7. Аналогично HTML-проекту

Адрес: `http://localhost:8080` (или `http://localhost:5173` по умолчанию для Vite)

## Извлечение данных с живого сайта (режим URL)

### Скриншот

```
browser_navigate -> <URL>
browser_take_screenshot -> type: png, fullPage: true, filename: reference-full.png
browser_resize -> width: 375, height: 812
browser_take_screenshot -> type: png, fullPage: true, filename: reference-mobile.png
```

### Извлечение метаданных

```javascript
browser_evaluate -> function: () => {
  const styles = getComputedStyle(document.documentElement);
  const body = getComputedStyle(document.body);

  // Цвета из CSS custom properties
  const cssVars = {};
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.selectorText === ':root') {
          for (const prop of rule.style) {
            if (prop.startsWith('--')) {
              cssVars[prop] = rule.style.getPropertyValue(prop).trim();
            }
          }
        }
      }
    } catch(e) {}
  }

  return {
    title: document.title,
    description: document.querySelector('meta[name="description"]')?.content,
    bodyFont: body.fontFamily,
    bodyColor: body.color,
    bodyBg: body.backgroundColor,
    h1Font: document.querySelector('h1') ?
      getComputedStyle(document.querySelector('h1')).fontFamily : null,
    cssVars: cssVars,
    links: [...document.querySelectorAll('link[rel="stylesheet"]')]
      .map(l => l.href).slice(0, 10),
    googleFonts: [...document.querySelectorAll('link[href*="fonts.googleapis"]')]
      .map(l => l.href)
  };
}
```

### Структура страницы

```
browser_snapshot -> (получить accessibility tree)
```

Это даст полную структуру элементов страницы.