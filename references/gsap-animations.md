# GSAP Animations — Справочник для Frontend Agent

Каталог анимаций на основе https://demos.gsap.com/
Все плагины бесплатны (включая бывшие Club-only, с 2025).

## CDN-подключение (v3.13.0)

### Минимальный набор (для большинства сайтов)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
```

### Расширенный набор (для продвинутых анимаций)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollSmoother.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/SplitText.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/Flip.min.js"></script>
```

### Все плагины
```html
<!-- Core -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
<!-- Scroll -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollSmoother.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/Observer.min.js"></script>
<!-- Text -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/SplitText.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/TextPlugin.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrambleTextPlugin.min.js"></script>
<!-- SVG -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/MorphSVGPlugin.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/DrawSVGPlugin.min.js"></script>
<!-- Layout & Interaction -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/Flip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/Draggable.min.js"></script>
```

## Регистрация плагинов

```javascript
gsap.registerPlugin(ScrollTrigger, SplitText, Flip);
```

## Каталог эффектов по категориям

### 1. Появление при скролле (ScrollTrigger)

**Fade Up** — элементы плавно появляются снизу при скролле
```javascript
gsap.from(".section", {
  y: 60,
  opacity: 0,
  duration: 1,
  stagger: 0.2,
  scrollTrigger: {
    trigger: ".section",
    start: "top 80%",
    end: "top 50%",
    toggleActions: "play none none reverse"
  }
});
```

**Slide In** — элементы выезжают сбоку
```javascript
gsap.from(".card", {
  x: -100,
  opacity: 0,
  duration: 0.8,
  stagger: 0.15,
  scrollTrigger: { trigger: ".cards-container", start: "top 75%" }
});
```

**Scale Reveal** — элементы увеличиваются из точки
```javascript
gsap.from(".feature", {
  scale: 0.5,
  opacity: 0,
  duration: 0.6,
  stagger: 0.1,
  ease: "back.out(1.7)",
  scrollTrigger: { trigger: ".features", start: "top 70%" }
});
```

### 2. Hero-секция (загрузка страницы)

**Staggered Hero** — заголовок, подзаголовок и кнопка появляются последовательно
```javascript
const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
tl.from(".hero__title", { y: 40, opacity: 0, duration: 1 })
  .from(".hero__subtitle", { y: 30, opacity: 0, duration: 0.8 }, "-=0.5")
  .from(".hero__cta", { y: 20, opacity: 0, duration: 0.6 }, "-=0.4")
  .from(".hero__image", { scale: 0.9, opacity: 0, duration: 1 }, "-=0.6");
```

**Text Reveal** — побуквенное появление заголовка
```javascript
const split = new SplitText(".hero__title", { type: "chars" });
gsap.from(split.chars, {
  y: 50,
  opacity: 0,
  rotateX: -90,
  stagger: 0.03,
  duration: 0.8,
  ease: "back.out(1.7)"
});
```

### 3. Навигация

**Navbar Hide/Show on Scroll** — навбар прячется при скролле вниз
```javascript
let lastScroll = 0;
ScrollTrigger.create({
  onUpdate: (self) => {
    const scrollY = self.scroll();
    if (scrollY > lastScroll && scrollY > 80) {
      gsap.to(".navbar", { y: -100, duration: 0.3 });
    } else {
      gsap.to(".navbar", { y: 0, duration: 0.3 });
    }
    lastScroll = scrollY;
  }
});
```

### 4. Параллакс

**Background Parallax** — фон двигается медленнее контента
```javascript
gsap.to(".parallax-bg", {
  yPercent: -30,
  ease: "none",
  scrollTrigger: {
    trigger: ".parallax-section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

**Multi-layer Parallax** — несколько слоёв с разной скоростью
```javascript
gsap.utils.toArray(".parallax-layer").forEach((layer, i) => {
  gsap.to(layer, {
    yPercent: -20 * (i + 1),
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-container",
      start: "top bottom",
      end: "bottom top",
      scrub: true
    }
  });
});
```

### 5. Карточки и галереи

**Card Hover Lift** — карточка поднимается при наведении
```javascript
document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("mouseenter", () => {
    gsap.to(card, { y: -10, scale: 1.02, boxShadow: "0 20px 40px rgba(0,0,0,0.15)", duration: 0.3 });
  });
  card.addEventListener("mouseleave", () => {
    gsap.to(card, { y: 0, scale: 1, boxShadow: "0 4px 6px rgba(0,0,0,0.1)", duration: 0.3 });
  });
});
```

**Staggered Grid** — карточки в сетке появляются волной
```javascript
gsap.from(".grid-item", {
  y: 40,
  opacity: 0,
  duration: 0.6,
  stagger: { amount: 0.8, grid: "auto", from: "start" },
  scrollTrigger: { trigger: ".grid", start: "top 75%" }
});
```

### 6. Горизонтальный скролл

**Horizontal Scroll Section** — секция скроллится горизонтально
```javascript
const sections = gsap.utils.toArray(".h-panel");
gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".h-scroll-container",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".h-scroll-container").offsetWidth
  }
});
```

### 7. Счётчики и числа

**Number Counter** — числа анимированно увеличиваются
```javascript
gsap.from(".stat-number", {
  textContent: 0,
  duration: 2,
  ease: "power1.inOut",
  snap: { textContent: 1 },
  scrollTrigger: { trigger: ".stats", start: "top 80%" }
});
```

### 8. SVG-анимации

**SVG Path Draw** — линия рисуется
```javascript
gsap.from(".svg-path", {
  drawSVG: "0%",
  duration: 2,
  ease: "power2.inOut",
  scrollTrigger: { trigger: ".svg-container", start: "top 70%" }
});
```

## Рекомендуемые комбинации по типу сайта

### Лендинг / Промо-страница
- Hero: Staggered Hero + Text Reveal
- Секции: Fade Up при скролле
- Карточки: Staggered Grid
- CTA: Scale Reveal
- Фон: Background Parallax
- Плагины: `gsap + ScrollTrigger + SplitText`

### Корпоративный сайт
- Hero: Staggered Hero (без эффектных текстовых анимаций)
- Секции: Fade Up при скролле
- Числа: Number Counter для статистики
- Навигация: Navbar Hide/Show
- Плагины: `gsap + ScrollTrigger`

### Портфолио / Креативный сайт
- Hero: Text Reveal + Parallax
- Галерея: Horizontal Scroll или Flip transitions
- Карточки: Card Hover Lift
- SVG: Path Draw для декора
- Плагины: `gsap + ScrollTrigger + SplitText + Flip`

### Интернет-магазин
- Секции: Fade Up (минимально)
- Карточки: Card Hover Lift
- Фильтры: Flip для анимации перестроения сетки
- Плагины: `gsap + ScrollTrigger + Flip`

## Уровни анимации

При планировании спросить у пользователя:

| Уровень | Описание | Плагины |
|---------|----------|---------|
| Минимальный | Fade/slide при скролле, hover на карточках | gsap + ScrollTrigger |
| Средний | + Text reveal, parallax, counters, navbar effects | + SplitText |
| Максимальный | + Horizontal scroll, SVG draw, Flip, smooth scroll | + все плагины |
