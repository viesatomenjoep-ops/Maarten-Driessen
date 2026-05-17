# Maarten Driessen Sporthorses — Setup gids

Stappenplan om de volledige stack te koppelen. Je hebt twee routes — kies wat je wil:

- **Route A — Supabase (aanbevolen, gehost)** → snelst, geen server-onderhoud.
- **Route B — Docker (lokaal)** → zelfde Postgres-schema, draait op je eigen machine.

Beide routes gebruiken **dezelfde** `supabase-schema.sql` en **dezelfde** Cloudinary-configuratie.

---

## 0. Wat zit er in deze map?

| Bestand | Wat doet het |
|---|---|
| `index.html` | Publieke website (2026-design, NL/EN/FR/DE, sliders, intake) |
| `admin.html` | CMS + CRM + ERP dashboard |
| `supabase-schema.sql` | **Master SQL** — schema, RLS, triggers, views, seed data |
| `cloudinary.js` | Cloudinary upload widget + transformaties + Supabase persist |
| `config.js` | Eén centraal config-bestand (Supabase URL/key, Cloudinary cloud/preset) |
| `docker-compose.yml` | Lokale stack: Postgres 16 + PgAdmin + PostgREST |
| `.env.example` | Template voor environment variables |

---

## Route A — Supabase (aanbevolen)

### 1. Maak een Supabase-project

1. Ga naar https://supabase.com → **New project**.
2. Geef het een naam (bv. `md-horses`), kies een regio (Frankfurt voor laagste latency in Europa), zet een database password.
3. Wacht tot het project provisioned is (~2 minuten).

### 2. Run het master SQL

1. Open je project → **SQL Editor** → **New query**.
2. Open `supabase-schema.sql` uit deze map → kopieer alles → plak in de editor.
3. Klik **Run**.
4. Je krijgt: `Success. No rows returned.` — check via **Table editor**: je ziet nu `horses`, `leads`, `customers`, `deals`, `ads`, `news`, `references`, `media`, `stables`, `inventory_items`, `transports`, `transport_horses`, `staff`, `jobs`, `invoices`, `site_settings`.

> Het script is **idempotent** — je kan het meerdere keren draaien zonder fouten.

### 3. Haal je API keys op

1. **Settings → API**.
2. Kopieer:
   - **Project URL** → `https://xxxxxxxxxxxx.supabase.co`
   - **anon public key** → `eyJhbGciOi...` (mag in frontend)
   - **service_role key** → NIET in frontend gebruiken (alleen server-side)

### 4. Plak ze in `config.js`

```js
window.MD_CONFIG = {
  supabase: {
    url:     'https://xxxxxxxxxxxx.supabase.co',
    anonKey: 'eyJhbGciOi...',
    schema:  'public'
  },
  cloudinary: { ... }
};
```

### 5. Test in Admin

1. Open `admin.html` in de browser.
2. **Systeem → Supabase & Cloudinary**.
3. Vul Project URL + anon key in → **Verbinden & test**.
4. Statuspill rechtsboven wordt groen: *"Supabase: verbonden"*.
5. Klik **"Laad demo-paarden in Supabase"** om de gescraped paarden in te schieten (alleen als de tabel nog leeg is).

---

## Route B — Docker (lokaal)

### 1. Vereisten

- [Docker Desktop](https://www.docker.com/products/docker-desktop) geïnstalleerd.
- De bestanden uit deze map in één folder.

### 2. Env file maken

```bash
cp .env.example .env
# pas wachtwoorden aan
```

### 3. Stack starten

```bash
docker compose up -d
```

Dit start:

- **Postgres 16** op `localhost:5432` (user/password uit `.env`) — schema wordt automatisch ingeladen vanuit `supabase-schema.sql`.
- **PgAdmin 4** op http://localhost:5050 (login met `PGADMIN_EMAIL` / `PGADMIN_PASSWORD`).
- **PostgREST** op http://localhost:3000 — een gratis Supabase-compatible REST API bovenop diezelfde Postgres.

### 4. Controleer

```bash
# Containers draaien?
docker compose ps

# Connect met psql:
docker exec -it md_db psql -U md -d md_horses -c "select count(*) from horses;"
# → moet 10 (seed-paarden) teruggeven
```

### 5. Koppel admin.html aan de lokale Postgres

Open `config.js`:

```js
window.MD_CONFIG = {
  supabase: {
    url:     'http://localhost:3000',   // PostgREST endpoint
    anonKey: '',                         // leeg laten (lokale, geen auth)
    schema:  'public'
  }
};
```

Open `admin.html` — de admin praat nu met je lokale Postgres alsof het Supabase is.

---

## Cloudinary — voor alle foto's en video's

### 1. Maak een account

https://cloudinary.com → free tier (25 GB / maand gratis). Noteer **Cloud name**.

### 2. Maak een **unsigned upload preset**

Dit is wat de upload widget gebruikt om bestanden direct vanuit de browser te uploaden zonder dat je API-secret in de frontend hoeft.

1. **Settings → Upload → Add upload preset**.
2. **Signing mode → Unsigned**.
3. **Folder** → `horses`.
4. (Aanbevolen) Eager transformations:
   - `w_800,h_1000,c_fill,g_auto,q_auto,f_auto` — card
   - `w_1600,h_900,c_fill,g_auto,q_auto,f_auto` — hero
5. **Save** — noteer de preset-naam (bv. `md_horses`).

### 3. Plak ze in `config.js`

```js
cloudinary: {
  cloudName:    'maartendriessen',
  uploadPreset: 'md_horses',
  folder:       'horses'
}
```

### 4. Upload testen

- Open `admin.html` → **Paarden** → **+ Nieuw paard** → **Upload foto's & video**.
- De Cloudinary widget opent. Drag&drop een paar foto's.
- Ze verschijnen in je Cloudinary Media Library onder de folder `horses/`.
- Als je Supabase aan hebt staan, schrijft `cloudinary.js` automatisch een rij naar de `media`-tabel én zet de eerste foto als cover op je paard.

### 5. Bestaande foto's importeren

Wil je de oorspronkelijke foto's van maartendriessen.be in één keer overnemen naar Cloudinary?

Open een DevTools console op `admin.html` en run:

```js
const photos = [
  'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/rubel-44-high-zm7mao.jpg',
  'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/coup-de-foudre-high-sdm922.png',
  // ...
];
MDCloud.init();
for (const u of photos) console.log(await MDCloud.importUrl(u));
```

`MDCloud.importUrl()` laat Cloudinary de remote URL fetchen en in je library zetten.

---

## Hoe de drie samenwerken

```
┌─────────────────────────────────────────────────────────────┐
│                      index.html (publiek)                    │
│                                                              │
│   • leest paarden uit  →  v_public_horses (Supabase view)    │
│   • toont foto's via    →  res.cloudinary.com/.../horses/.. │
│   • POST intake form    →  insert into leads (RLS staat       │
│                              dat publiek toe)                 │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                       admin.html (login)                     │
│                                                              │
│   • CMS-CRUD          →  Supabase tabellen (RLS: authenticated)│
│   • Upload foto/video →  Cloudinary widget → asset            │
│                          → wordt geschreven naar media        │
│                          → cover_url op horses                │
│   • CRM (leads)       →  realtime stream uit leads-tabel       │
│   • ERP (transport)   →  CRUD op transports + horses          │
└──────────────────────────────────────────────────────────────┘
```

---

## Veelgemaakte fouten

| Symptoom | Oplossing |
|---|---|
| `auth.role() does not exist` bij lokale Postgres | Geen probleem — `supabase-schema.sql` vangt dit op en slaat auth-policies over (`raise notice`). |
| Cloudinary widget opent niet | `<script src="https://upload-widget.cloudinary.com/global/all.js"></script>` ontbreekt. |
| "Upload preset must be whitelisted for unsigned" | Preset staat nog op *Signed*. Zet op **Unsigned**. |
| Lege paarden-tabel op de site | Status van de paarden staat op `draft`. Verander naar `published`. |
| CORS-error vanuit Supabase | Voeg je domein toe onder **Authentication → URL Configuration → Site URL**. |

---

## Volgende stappen

- **Authenticatie voor admin**: Supabase **Authentication → Providers** aanzetten (Email + Google werkt prima). De RLS-policies staan al klaar.
- **Realtime updates**: in `admin.html` wordt `supa.channel('horses').on('postgres_changes', ...)` werkt out-of-the-box dankzij de view.
- **Backup**: Supabase doet dagelijkse backups (Pro plan). Lokaal: `docker exec md_db pg_dump -U md md_horses > backup-$(date +%F).sql`.
- **Domeinkoppeling**: hostprovider (Vercel/Netlify/Cloudflare Pages) — upload `index.html`, `admin.html`, `cloudinary.js`, `config.js`. Klaar.

---

Heb je hulp nodig met de hosting of een eerste auth-flow? Vraag het gerust.
