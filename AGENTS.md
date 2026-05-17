# AGENTS.md — context voor AI agents

Dit bestand wordt automatisch gelezen door agentic IDE's (Google Antigravity,
Cursor, Claude Code, Windsurf, ...). Het beschrijft hoe het project in elkaar
zit zodat de agent direct productief kan zijn.

## Wat is dit project?

Een complete herwerking (2026) van **maartendriessen.be** — een Belgische
springpaarden­handel. Drie luiken:

1. **Publieke website** (`index.html`) — viertalig (NL/EN/FR/DE), met sliders,
   paarden­catalogus per geboortejaar, intake-module "What can we do 4 you?",
   referenties, news, stable-gallery.
2. **Admin-suite** (`admin.html`) — CMS (paarden, advertenties, news,
   referenties), CRM (leads, klanten, deals pipeline) en ERP (stallen,
   voorraad, transport, personeel, financieel).
3. **Backend** — Supabase (managed Postgres + auth + RLS) of lokale Postgres
   via Docker (`docker-compose.yml`) met PostgREST, plus Cloudinary voor alle
   foto's en video's.

## Tech stack

- **Frontend**: pure HTML/CSS/JS — geen build-step, geen framework. Werkt
  rechtstreeks in elke browser.
- **Fonts**: Fraunces (display, Google Fonts) + Inter (body).
- **Kleurpalet**: off-white `#FAF7F2`, warm zand `#C9B49A`, deep zand `#8B7355`,
  zwart `#0A0A0A`. Strak, neutraal, premium.
- **Backend**: Postgres 16 (Supabase of Docker), `@supabase/supabase-js` v2 via
  CDN, Cloudinary upload widget via CDN.
- **Geen build-tools** — alles via `<script src=...>` CDN-imports.

## Mappenstructuur

```
.
├── index.html              # publieke site
├── admin.html              # admin / CMS / CRM / ERP
├── config.js               # Supabase & Cloudinary keys (NIET committen met echte waarden)
├── cloudinary.js           # MDCloud module
├── supabase-schema.sql     # master SQL (idempotent)
├── docker-compose.yml      # lokale stack
├── .env.example            # env template
├── SETUP.md                # Nederlands stappenplan
├── README.md               # project overview
└── AGENTS.md               # dit bestand
```

## Belangrijke conventies

### SQL-schema

- Master SQL is **idempotent** — `create table if not exists`, `do $$ begin ... exception when duplicate_object then null; end $$;` voor enums, `drop trigger if exists ... create trigger ...`.
- Werkt **zowel op Supabase als lokale Postgres** — de RLS-policies die `auth.role()` gebruiken zitten in een `do $$ ... exception when undefined_function then notice ...` block zodat lokaal niets crasht.
- **RLS-strategie**: publiek leest enkel gepubliceerde rijen (horses.status='published', news.published=true), publiek mag een lead inserten, authenticated mag alles.
- **Naming**: snake_case, UUIDs als primary keys, `created_at` + `updated_at` met triggers.

### Cloudinary

- **Unsigned upload preset** vereist — staat in `cloudinary.js` als `uploadPreset`.
- Asset metadata (public_id, secure_url, width, height, bytes) gaat naar de `media`-tabel in Supabase. Eerste upload op een paard zonder cover → wordt automatisch cover.
- Transformatie-helpers: `MDCloud.thumb(id)`, `.card(id)`, `.hero(id)`, `.cover(id)`, `.poster(id)`.

### Frontend

- **i18n**: data-attribuut `data-i18n="key"` + `I18N[lang][key]` object in script. Geen externe lib.
- **Sliders**: pure JS — hero slider met autoplay, featured slider met arrows + progress bar. Geen Swiper/Splide.
- **Geen localStorage in iframes** — admin gebruikt het wél, dat mag want het draait standalone.

### Branding

- Naam blijft **Maarten Driessen Sporthorses** (origineel was Engels: "We find you your Quality horse").
- Telefoon: `+32 474 444 059`, e-mail `info@maartendriessen.be`.

## Veelvoorkomende taken voor de agent

### "Voeg een paard toe"
1. Open `admin.html` → Paarden → "+ Nieuw paard"
2. Of: `insert into horses (name, year, sex, pedigree, status) values (...);`

### "Voeg een nieuwe taal toe"
1. Voeg de taalkey toe aan `I18N` in `index.html` (~regel 700+).
2. Voeg de knop toe in `#langSwitch`.
3. Voeg `title_xx` en `body_xx` kolommen toe aan `news` in `supabase-schema.sql` als je per-locale content wil.

### "Voeg een sectie toe aan de publieke site"
1. Volg het bestaande sectie-patroon: `<section class="naam"><div class="container"><div class="section-head">...</div>...</div></section>`.
2. Gebruik de bestaande tokens: `--bg`, `--sand`, `--sand-soft`, `--ink`.

### "Voeg een tabel toe in de admin"
1. Voeg een nieuwe `<section class="page" id="page-xxx">` toe in `admin.html`.
2. Voeg een `<div class="nav-item" data-page="xxx">` toe in de sidebar.
3. Schrijf desgewenst een nieuwe `create table` in `supabase-schema.sql`.

### "Wijzig kleuren"
- Alle kleuren zitten in de `:root` block bovenaan elk HTML-bestand. Wijzig daar.

## Wat NIET doen

- **Geen secrets in `config.js` committen.** Voeg `config.js` toe aan `.gitignore` zodra je echte keys invult, of gebruik `config.local.js`.
- **Geen frameworks toevoegen** zonder overleg — het project is bewust dependency-vrij.
- **Geen `cover_url` overschrijven** als die al een Cloudinary-URL heeft tenzij expliciet gevraagd.
- **Geen RLS uitschakelen** — als publiek iets moet kunnen, voeg een policy toe.

## Externe afhankelijkheden (CDN-only)

- `https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2`
- `https://upload-widget.cloudinary.com/global/all.js`
- `https://fonts.googleapis.com/css2?family=Fraunces&family=Inter&family=JetBrains+Mono`

## Test-checklist voor de agent

Na elke wijziging:
- [ ] Open `index.html` lokaal — geen JS-errors in console?
- [ ] Open `admin.html` lokaal — alle pagina's bereikbaar via sidebar?
- [ ] Test taalswitch (NL/EN/FR/DE) bovenaan `index.html`.
- [ ] Test hero slider arrows + autoplay.
- [ ] Test paarden-filter chips.
- [ ] Test intake-form (open alle opt-buttons).
- [ ] Run `supabase-schema.sql` op een lege DB — geen errors?
- [ ] Test admin → Settings → Verbinden & test.

---

Veel succes — alle vragen of nieuwe features in dezelfde stijl bouwen.
