# Maarten Driessen Sporthorses — 2026 platform

Een volledige, moderne herwerking van **maartendriessen.be**: publieke site,
admin-suite (CMS / CRM / ERP) en backend-koppeling met Supabase + Cloudinary +
optioneel Docker.

## Project op één pagina

| Map / bestand | Wat het is |
|---|---|
| `index.html` | Publieke website (NL · EN · FR · DE, sliders, intake module, paarden-catalogus) |
| `admin.html` | Admin-suite — Dashboard, Paarden (CMS), Leads (CRM), Voorraad/Transport/Personeel (ERP), Advertenties, News, Settings |
| `config.js` | Eén centraal config-bestand — vul Supabase & Cloudinary keys in |
| `cloudinary.js` | Upload widget + transformaties, schrijft assets door naar Supabase `media`-tabel |
| `supabase-schema.sql` | **Master SQL** — schema, RLS, triggers, views, seed (werkt op Supabase én lokale Postgres) |
| `docker-compose.yml` | Lokale dev-stack: Postgres 16 + PgAdmin + PostgREST |
| `.env.example` | Template voor alle environment variables |
| `SETUP.md` | Volledig stappenplan in het Nederlands |
| `AGENTS.md` | Context-bestand voor AI agents (Antigravity, Cursor, Claude Code, …) |

## Snel starten

1. Open `config.js` en vul je Supabase URL + anon key en Cloudinary cloud name + upload preset in.
2. Open `supabase-schema.sql` in de Supabase SQL editor en run het.
3. Open `index.html` in je browser — klaar.
4. Voor lokaal ontwikkelen: `docker compose up -d`.

Lees `SETUP.md` voor de volledige uitleg.

## Hosting

Pure statische HTML/JS — werkt op Vercel, Netlify, Cloudflare Pages, GitHub Pages
of zelfs een gewone S3-bucket. Geen build-step nodig.

---

© 2026 Maarten Driessen Sporthorses
