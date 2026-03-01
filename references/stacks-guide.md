# Справочник стеков и UI-библиотек

## Стеки генерации

### 1. HTML/CSS/JS (Vanilla)

**Когда:** Простые лендинги, промо-страницы, статичные сайты
**Плюсы:** Нулевые зависимости, мгновенная загрузка, простой деплой
**Минусы:** Нет компонентной системы, ручное управление состоянием
**Анимации:** GSAP (через CDN)
**Файлы:** index.html, css/style.css, js/main.js

---

### 2. React + Tailwind CSS

**Когда:** SPA, интерактивные интерфейсы, дашборды, многостраничные приложения
**Плюсы:** Компонентный подход, огромная экосистема, переиспользование
**Минусы:** Нужна сборка (Vite), тяжелее для простых страниц
**Анимации:** Framer Motion / GSAP
**Файлы:** Vite + React проект

---

### 3. React + shadcn/ui

**Когда:** Продуктовые интерфейсы, дашборды, админки, SaaS
**Стек:** React 19 + Tailwind CSS v4 + Radix UI (accessibility) + Lucide Icons
**Плюсы:** Красивые accessible-компоненты, полный контроль над кодом (copy-paste, не npm), TypeScript, тёмная тема из коробки
**Минусы:** Только React, нужен Vite/Next.js
**Компоненты:** Button, Card, Dialog, Drawer, Table, Form, Tabs, Toast, Sidebar, Calendar, Chart, Combobox, Data Table, Date Picker и 50+ других
**Сайт:** https://ui.shadcn.com
**Особенность:** Код компонентов копируется в проект, а не устанавливается как зависимость. Полный контроль и кастомизация.

---

### 4. React + Aceternity UI

**Когда:** Лендинги с wow-эффектом, маркетинговые страницы, портфолио
**Стек:** React/Next.js + Tailwind CSS + Framer Motion
**Плюсы:** 200+ анимированных компонентов, spotlight-эффекты, parallax, 3D-карточки, mask reveal
**Минусы:** Тяжёлые анимации, не для контентных сайтов
**Сайт:** https://ui.aceternity.com
**Особенность:** Copy-paste компоненты с красивыми анимациями. Идеально для впечатляющих лендингов.

---

### 5. React + Magic UI

**Когда:** Лендинги для стартапов, маркетинговые страницы, product-страницы
**Стек:** React + Tailwind CSS + Motion (Framer Motion)
**Плюсы:** 150+ анимированных компонентов, микро-интеракции, блоки для лендингов
**Минусы:** Заточен под лендинги, не для сложных приложений
**Сайт:** https://magicui.design
**Особенность:** Компаньон shadcn/ui. Фокус на анимациях и лендинг-блоках. 15k+ GitHub stars.

---

### 6. Astro (Static-first)

**Когда:** Контентные сайты, блоги, документация, высококонверсионные лендинги
**Плюсы:** Zero JS по умолчанию, islands architecture, работает с любым UI-фреймворком (React, Vue, Svelte)
**Минусы:** Не для SPA с тяжёлой интерактивностью
**Сайт:** https://astro.build
**Особенность:** Максимальная производительность. JS подключается только там, где нужна интерактивность.

---

### 7. Svelte + SvelteKit

**Когда:** Высокопроизводительные приложения, лёгкие SPA, мобильные веб-приложения
**Плюсы:** Компиляция в чистый JS (нет runtime), маленький бандл, нативные transitions
**Минусы:** Меньше экосистема чем React, меньше UI-библиотек
**Сайт:** https://svelte.dev

---

### 8. Vue.js + Nuxt

**Когда:** Средние и большие приложения, корпоративные порталы
**Плюсы:** Простой синтаксис, Composition API, хорошая документация
**Минусы:** Меньше компонентных библиотек чем React
**UI-библиотеки:** Vuetify, PrimeVue, Naive UI, Radix Vue

---

## Design-системы крупных компаний (для референса)

| Система | Компания | Стек | Сайт |
|---------|----------|------|------|
| Material Design 3 | Google | Web Components | m3.material.io |
| Fluent UI | Microsoft | React, Web Components | developer.microsoft.com/fluentui |
| Carbon | IBM | React, Vue, Svelte, Angular | carbondesignsystem.com |
| Spectrum | Adobe | React, Web Components | spectrum.adobe.com |
| Polaris | Shopify | React | polaris.shopify.com |
| Ant Design | Ant Financial | React | ant.design |
| Chakra UI | Community | React | chakra-ui.com |
| Flowbite | Themesberg | Tailwind CSS | flowbite.com |
| HeroUI | HeroUI Inc. | React + Tailwind | heroui.com |
| Blueprint | Palantir | React | blueprintjs.com |
| Base Web | Uber | React | baseweb.design |
| Headless UI | Tailwind Labs | React, Vue | headlessui.com |
| Porsche DS | Porsche | Web Components, React, Vue | designsystem.porsche.com |
| GOV.UK | UK Government | Nunjucks | design-system.service.gov.uk |

## Матрица выбора стека

| Задача | Рекомендуемый стек |
|--------|-------------------|
| Простой лендинг, промо | HTML/CSS/JS + GSAP |
| Лендинг с wow-анимациями | Aceternity UI или Magic UI |
| Продуктовый лендинг для SaaS | shadcn/ui или Magic UI |
| Дашборд, админка | shadcn/ui |
| Интернет-магазин | React + Tailwind или Next.js + shadcn/ui |
| Корпоративный портал | Vue + Nuxt или React + shadcn/ui |
| Блог, документация | Astro |
| Высокая производительность | Svelte + SvelteKit |
| Портфолио дизайнера | Aceternity UI |
| MVP стартапа | Next.js + shadcn/ui |