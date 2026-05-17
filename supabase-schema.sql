-- =========================================================================
--  MAARTEN DRIESSEN SPORTHORSES — MASTER SQL
--  Werkt op Supabase (managed Postgres) én op lokale Postgres via Docker.
--  Idempotent: kan je meerdere keren draaien.
--
--  Hoe gebruiken:
--   - Supabase  → SQL Editor → New query → plak dit hele bestand → Run
--   - Docker    → docker compose up -d   (zie docker-compose.yml)
--                 daarna automatisch ingeladen vanuit /docker-entrypoint-initdb.d/
--                 of handmatig:  psql $DATABASE_URL -f supabase-schema.sql
-- =========================================================================

begin;

-- ---------- EXTENSIONS -------------------------------------------------
create extension if not exists "pgcrypto";
create extension if not exists "uuid-ossp";
create extension if not exists "citext";
create extension if not exists "unaccent";
create extension if not exists "pg_trgm";

-- ---------- HELPERS ----------------------------------------------------
create or replace function set_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end;
$$;

create or replace function slugify(txt text)
returns text language sql immutable as $$
  select trim(both '-' from
           regexp_replace(
             lower(unaccent(coalesce(txt,''))),
             '[^a-z0-9]+', '-', 'g'))
$$;

-- ---------- ENUMS ------------------------------------------------------
do $$ begin
  create type sex_t as enum ('Stallion','Mare','Gelding');
exception when duplicate_object then null; end $$;

do $$ begin
  create type horse_status_t as enum ('draft','published','reserved','sold','archived');
exception when duplicate_object then null; end $$;

do $$ begin
  create type lead_stage_t as enum ('new','qualified','viewing','vet','negotiation','won','lost');
exception when duplicate_object then null; end $$;

do $$ begin
  create type customer_type_t as enum ('pro_rider','amateur','owner','stable','trader','breeder','other');
exception when duplicate_object then null; end $$;

do $$ begin
  create type transport_status_t as enum ('planned','in_progress','delivered','cancelled');
exception when duplicate_object then null; end $$;

do $$ begin
  create type ad_status_t as enum ('draft','live','paused','expired');
exception when duplicate_object then null; end $$;

-- ---------- HORSES -----------------------------------------------------
create table if not exists horses (
  id              uuid primary key default gen_random_uuid(),
  slug            text unique,
  name            text not null,
  year            int  not null check (year between 1990 and extract(year from now())::int + 1),
  sex             sex_t not null,
  color           text,
  height_cm       int check (height_cm between 100 and 200),
  level           text,
  pedigree        text,
  damline         text,
  approval        text,                         -- bv BWP approved
  description_nl  text,
  description_en  text,
  description_fr  text,
  description_de  text,
  price_eur       numeric(12,2),
  price_label     text,                         -- 'On request'
  status          horse_status_t not null default 'draft',
  cover_url       text,                         -- Cloudinary secure_url
  cover_public_id text,                         -- Cloudinary public_id
  video_url       text,
  featured        boolean not null default false,
  views           int not null default 0,
  meta            jsonb not null default '{}'::jsonb,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
create index if not exists ix_horses_status on horses(status);
create index if not exists ix_horses_year on horses(year);
create index if not exists ix_horses_featured on horses(featured) where featured = true;
create index if not exists ix_horses_search on horses using gin (to_tsvector('simple', coalesce(name,'') || ' ' || coalesce(pedigree,'')));

-- auto slug + updated_at
create or replace function horses_before_write()
returns trigger language plpgsql as $$
begin
  if new.slug is null or new.slug = '' then
    new.slug := slugify(new.name) || '-' || new.year;
  end if;
  new.updated_at := now();
  return new;
end $$;
drop trigger if exists trg_horses_before on horses;
create trigger trg_horses_before
  before insert or update on horses
  for each row execute procedure horses_before_write();

-- ---------- MEDIA (Cloudinary assets) ----------------------------------
create table if not exists media (
  id            uuid primary key default gen_random_uuid(),
  horse_id      uuid references horses(id) on delete cascade,
  news_id       uuid,                          -- gevuld via app
  reference_id  uuid,
  public_id     text not null,                 -- Cloudinary public_id
  secure_url    text not null,
  resource_type text not null default 'image', -- image | video | raw
  format        text,
  width         int,
  height        int,
  bytes         bigint,
  duration_sec  numeric,
  position      int not null default 0,
  alt           text,
  is_cover      boolean not null default false,
  created_at    timestamptz not null default now()
);
create index if not exists ix_media_horse on media(horse_id);
create index if not exists ix_media_position on media(horse_id, position);

-- ---------- CUSTOMERS --------------------------------------------------
create table if not exists customers (
  id           uuid primary key default gen_random_uuid(),
  full_name    text not null,
  email        citext,
  phone        text,
  country      text,
  language     text,
  type         customer_type_t default 'other',
  notes        text,
  lifetime_value_eur numeric(14,2) default 0,
  tags         text[] default '{}'::text[],
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
create unique index if not exists ux_customers_email on customers(email) where email is not null;
drop trigger if exists trg_customers_upd on customers;
create trigger trg_customers_upd before update on customers
  for each row execute procedure set_updated_at();

-- ---------- LEADS (intake-formulier) -----------------------------------
create table if not exists leads (
  id                  uuid primary key default gen_random_uuid(),
  full_name           text,
  email               citext,
  phone               text,
  country             text,
  sex_preferences     text[],
  age_range           text,
  experience_level    text,
  preferred_colors    text[],
  budget_range        text,
  remarks             text,
  stage               lead_stage_t not null default 'new',
  owner               text,
  source              text default 'website',  -- website | whatsapp | phone | manual
  customer_id         uuid references customers(id) on delete set null,
  related_horse_id    uuid references horses(id) on delete set null,
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now()
);
create index if not exists ix_leads_stage on leads(stage);
create index if not exists ix_leads_created on leads(created_at desc);
drop trigger if exists trg_leads_upd on leads;
create trigger trg_leads_upd before update on leads
  for each row execute procedure set_updated_at();

-- ---------- DEALS ------------------------------------------------------
create table if not exists deals (
  id              uuid primary key default gen_random_uuid(),
  horse_id        uuid references horses(id) on delete set null,
  customer_id     uuid references customers(id) on delete set null,
  lead_id         uuid references leads(id) on delete set null,
  stage           lead_stage_t not null default 'qualified',
  amount_eur      numeric(14,2),
  commission_eur  numeric(14,2),
  currency        text default 'EUR',
  expected_close  date,
  closed_at       timestamptz,
  notes           text,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
create index if not exists ix_deals_stage on deals(stage);
drop trigger if exists trg_deals_upd on deals;
create trigger trg_deals_upd before update on deals
  for each row execute procedure set_updated_at();

-- ---------- ADS --------------------------------------------------------
create table if not exists ads (
  id          uuid primary key default gen_random_uuid(),
  horse_id    uuid references horses(id) on delete cascade,
  platform    text not null,
  region      text,
  status      ad_status_t not null default 'draft',
  views       int not null default 0,
  leads       int not null default 0,
  starts_on   date,
  ends_on     date,
  budget_eur  numeric(10,2),
  url         text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index if not exists ix_ads_horse on ads(horse_id);
create index if not exists ix_ads_status on ads(status);
drop trigger if exists trg_ads_upd on ads;
create trigger trg_ads_upd before update on ads
  for each row execute procedure set_updated_at();

-- ---------- NEWS -------------------------------------------------------
create table if not exists news (
  id            uuid primary key default gen_random_uuid(),
  slug          text unique,
  title_nl text, title_en text, title_fr text, title_de text,
  body_nl  text, body_en  text, body_fr  text, body_de  text,
  cover_url     text,
  cover_public_id text,
  category      text,
  published     boolean not null default false,
  published_at  timestamptz,
  meta          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create or replace function news_before_write()
returns trigger language plpgsql as $$
begin
  if new.slug is null or new.slug = '' then
    new.slug := slugify(coalesce(new.title_nl,new.title_en,'post')) || '-' || to_char(now(),'YYYYMM');
  end if;
  if new.published and new.published_at is null then
    new.published_at := now();
  end if;
  new.updated_at := now();
  return new;
end $$;
drop trigger if exists trg_news_before on news;
create trigger trg_news_before before insert or update on news
  for each row execute procedure news_before_write();

-- ---------- REFERENCES (verkochte paarden + resultaten) ----------------
create table if not exists "references" (
  id           uuid primary key default gen_random_uuid(),
  horse_name   text not null,
  horse_id     uuid references horses(id) on delete set null,
  result       text,
  location     text,
  rider        text,
  country      text,
  event_date   date,
  cover_url    text,
  cover_public_id text,
  video_url    text,
  created_at   timestamptz not null default now()
);
create index if not exists ix_references_date on "references"(event_date desc);

-- ---------- STABLES / INVENTORY (ERP) ---------------------------------
create table if not exists stables (
  id         uuid primary key default gen_random_uuid(),
  name       text not null,
  capacity   int not null default 0,
  occupied   int not null default 0,
  notes      text,
  created_at timestamptz default now()
);
create table if not exists inventory_items (
  id         uuid primary key default gen_random_uuid(),
  name       text not null,
  category   text,                              -- voer | hooi | stro | veterinair | hardware
  unit       text,                              -- kg | balen | doses | stuks
  stock      numeric not null default 0,
  min_level  numeric not null default 0,
  supplier   text,
  updated_at timestamptz not null default now()
);
drop trigger if exists trg_inv_upd on inventory_items;
create trigger trg_inv_upd before update on inventory_items
  for each row execute procedure set_updated_at();

-- ---------- TRANSPORTS -------------------------------------------------
create table if not exists transports (
  id             uuid primary key default gen_random_uuid(),
  departure_date date not null,
  arrival_date   date,
  origin         text default 'Maaseik, BE',
  destination    text,
  charter        text,
  documents_ok   boolean not null default false,
  status         transport_status_t not null default 'planned',
  cost_eur       numeric(10,2),
  notes          text,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);
create table if not exists transport_horses (
  transport_id uuid references transports(id) on delete cascade,
  horse_id     uuid references horses(id) on delete cascade,
  primary key (transport_id, horse_id)
);
drop trigger if exists trg_transports_upd on transports;
create trigger trg_transports_upd before update on transports
  for each row execute procedure set_updated_at();

-- ---------- STAFF & JOBS ----------------------------------------------
create table if not exists staff (
  id         uuid primary key default gen_random_uuid(),
  full_name  text not null,
  role       text,
  email      citext,
  phone      text,
  since      date,
  status     text default 'active',
  notes      text
);
create table if not exists jobs (
  id          uuid primary key default gen_random_uuid(),
  title       text not null,
  description text,
  active      boolean not null default true,
  created_at  timestamptz not null default now()
);

-- ---------- FINANCE (read-only weergave) ------------------------------
create table if not exists invoices (
  id              uuid primary key default gen_random_uuid(),
  number          text unique,
  customer_id     uuid references customers(id) on delete set null,
  deal_id         uuid references deals(id)     on delete set null,
  amount_eur      numeric(14,2) not null,
  vat_eur         numeric(14,2) default 0,
  status          text default 'open',           -- open | paid | overdue | cancelled
  issued_at       date default current_date,
  paid_at         timestamptz,
  pdf_url         text,
  created_at      timestamptz not null default now()
);

-- ---------- SITE-SETTINGS (key/value voor CMS) ------------------------
create table if not exists site_settings (
  key        text primary key,
  value      jsonb not null,
  updated_at timestamptz not null default now()
);
drop trigger if exists trg_site_upd on site_settings;
create trigger trg_site_upd before update on site_settings
  for each row execute procedure set_updated_at();

-- =========================================================================
--  ROW LEVEL SECURITY (alleen actief op Supabase / met auth-rol)
-- =========================================================================
alter table horses        enable row level security;
alter table leads         enable row level security;
alter table customers     enable row level security;
alter table deals         enable row level security;
alter table ads           enable row level security;
alter table news          enable row level security;
alter table "references"  enable row level security;
alter table media         enable row level security;
alter table site_settings enable row level security;

-- Publiek (anon-rol) leest enkel gepubliceerde content
drop policy if exists "horses_public_read" on horses;
create policy "horses_public_read" on horses
  for select using (status = 'published');

drop policy if exists "news_public_read" on news;
create policy "news_public_read" on news
  for select using (published = true);

drop policy if exists "references_public_read" on "references";
create policy "references_public_read" on "references"
  for select using (true);

drop policy if exists "media_public_read" on media;
create policy "media_public_read" on media
  for select using (true);

drop policy if exists "site_settings_public_read" on site_settings;
create policy "site_settings_public_read" on site_settings
  for select using (true);

-- Publiek mag enkel een lead inschieten (geen lezen / updaten)
drop policy if exists "leads_public_insert" on leads;
create policy "leads_public_insert" on leads
  for insert with check (true);

-- Authenticated users (admin login) mogen alles
do $$
declare t text;
begin
  foreach t in array array['horses','leads','customers','deals','ads','news','references','media','site_settings'] loop
    execute format($f$
      drop policy if exists "auth_all_%I" on %I;
      create policy "auth_all_%I" on %I
        for all using (auth.role() = 'authenticated')
        with check (auth.role() = 'authenticated');
    $f$, t, t, t, t);
  end loop;
exception when undefined_function then
  -- Lokaal (geen Supabase auth schema) → policies overslaan
  raise notice 'auth.role() niet beschikbaar — auth-policies overgeslagen (lokale Postgres).';
end $$;

-- =========================================================================
--  VIEWS (handig voor frontend)
-- =========================================================================
create or replace view v_public_horses as
  select
    h.id, h.slug, h.name, h.year, h.sex, h.level,
    h.pedigree, h.color, h.height_cm,
    h.cover_url, h.video_url,
    coalesce(h.description_nl, h.description_en) as description,
    h.price_label, h.price_eur, h.featured
  from horses h
  where h.status = 'published'
  order by h.featured desc, h.year desc;

create or replace view v_dashboard_kpis as
  select
    (select count(*) from horses where status='published')                          as horses_live,
    (select count(*) from leads  where stage='new')                                 as leads_new,
    (select count(*) from deals  where stage='won' and extract(year from coalesce(closed_at,now())) = extract(year from now())) as deals_won_ytd,
    (select coalesce(sum(amount_eur),0) from invoices where status='paid' and extract(year from coalesce(paid_at,issued_at)) = extract(year from now())) as revenue_ytd;

create or replace view v_horses_with_media as
  select h.*,
         (select json_agg(json_build_object('url', m.secure_url, 'public_id', m.public_id, 'is_cover', m.is_cover) order by m.position)
            from media m where m.horse_id = h.id) as gallery
  from horses h;

-- =========================================================================
--  STORAGE BUCKET (Supabase Storage — optioneel naast Cloudinary)
-- =========================================================================
do $$
begin
  insert into storage.buckets (id, name, public)
    values ('horses-fallback','horses-fallback', true)
    on conflict (id) do nothing;
exception when undefined_table then
  raise notice 'storage.buckets niet aanwezig (lokale Postgres) — bucket-aanmaak overgeslagen.';
end $$;

-- =========================================================================
--  SEED DATA — gescraped uit maartendriessen.be
-- =========================================================================

-- Stables
insert into stables (name, capacity, occupied) values
  ('Indoor A', 12, 12),
  ('Indoor B', 14, 9),
  ('Foal stal', 8, 6),
  ('Quarantaine', 4, 2)
on conflict do nothing;

-- Inventory
insert into inventory_items (name, category, unit, stock, min_level, supplier) values
  ('Krachtvoer Cavalor', 'voer', 'kg', 1240, 500, 'Cavalor BE'),
  ('Hooi (balen)',       'hooi', 'balen', 180, 120, 'Lokale boer'),
  ('Stro (balen)',       'stro', 'balen', 96, 100, 'Lokale boer'),
  ('Mineralen mix',      'voer', 'kg', 42, 30, 'Cavalor BE'),
  ('Wormkuur',           'veterinair', 'doses', 8, 20, 'Dierenarts X')
on conflict do nothing;

-- Staff
insert into staff (full_name, role, since, status) values
  ('Maarten Driessen', 'Eigenaar',    '1995-01-01', 'active'),
  ('Morinne Donnay',   'Head rider',  '2021-01-01', 'active'),
  ('L. Vermeulen',     'Groom',       '2023-01-01', 'active'),
  ('S. Janssens',      'Flat rider',  '2024-01-01', 'active')
on conflict do nothing;

-- Jobs
insert into jobs (title, description, active) values
  ('Student',                'Flexibel, 2-4 dagen/week', true),
  ('Fulltime Groom',         'Onmiddellijke start', true),
  ('Flat Rider',             'Ervaring jonge paarden', true),
  ('Mucking Stable Expert',  'Fulltime', true),
  ('Fulltime Rider',         'Topsport ervaring vereist', true)
on conflict do nothing;

-- Customers (uit referenties scrape)
insert into customers (full_name, country, type, notes) values
  ('Ward McClain',         'USA', 'pro_rider', 'Rides Snapchat — WEC Ocala'),
  ('Ibrahim Barazi',       'JOR', 'owner',     'Joie de Vigo — NC Wellington'),
  ('Johnny Pals',          'NL',  'pro_rider', 'Maastricht 4*'),
  ('SencerHorsan Stables', 'TR',  'stable',    'Cerenke / Agalove'),
  ('Erynn Ballard',        'CAN', 'pro_rider', 'Wellington FL'),
  ('Eurohorse',            'BE',  'trader',    'Long-term partner'),
  ('Mariano Bastida',      'ES',  'pro_rider', 'Sunshine tour')
on conflict do nothing;

-- Horses (selectie uit scrape)
insert into horses (name, year, sex, pedigree, level, status, price_eur, price_label, cover_url, featured) values
  ('Rubel',                       2017, 'Mare',     'Quint vh Maarlo × Nevado vd Rostal × Grand Amour', '1.60m', 'published', 490000, 'On request',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/rubel-44-high-zm7mao.jpg?enable-io=true&fit=bounds&width=800', true),
  ('Charisma vd Broekkant Z',     2017, 'Mare',     'Cicero van Paemel Z × Cornet Obolensky',           '1.50m', 'published',  85000, '€ 85.000',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/image-standard-gllnhb.png?enable-io=true&fit=bounds&width=800', true),
  ('Coup de Foudre',              2019, 'Gelding',  'CWD Ambassador horse',                              '1.45m', 'published',  null,  'On request',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/coup-de-foudre-high-sdm922.png?enable-io=true&fit=bounds&width=800', true),
  ('Picasso JMS Z',               2022, 'Stallion', 'Pegase van ''t Ruytershof × Cancara Z',             'Young', 'published',  62000, '€ 62.000',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/picasso-11b-high.jpg?enable-io=true&fit=bounds&width=800', false),
  ('Cognac van ''t Breezerhof Z', 2024, 'Stallion', 'Comme il Faut × Indian Gold vd Castershoeve',       'Foal',  'draft',      null,  'On request',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/cognac-1-high-xdte85.jpg?enable-io=true&fit=bounds&width=800', false),
  ('Bamina',                      2020, 'Mare',     'Bamako de Muze × Kannan',                           '5yo',   'published',  48000, '€ 48.000',
   null, false),
  ('Uricane Hero',                2019, 'Gelding',  'Uricas × _ _ (Linotte/Femke P)',                    '6yo',   'published',  95000, '€ 95.000',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/uricane-13-high.jpg?enable-io=true&fit=bounds&width=800', false),
  ('Catobelleau DBH Z',           2023, 'Stallion', 'Catoki × Clearway (Capitol I)',                     'Young', 'draft',      null,  'On request',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/catobelleau-12-high-ii8wh8.jpg?enable-io=true&fit=bounds&width=800', false),
  ('Joie de Vigo',                2014, 'Gelding',  '5* CSI tour horse',                                 '1.55m', 'sold',       null,  'Sold',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/joi21-high-bm5mex.jpg?enable-io=true&fit=bounds&width=800', false),
  ('Kay Blue',                    2025, 'Mare',     'Cero Blue × Ustinov × Concorde',                    'Foal',  'draft',      null,  'On request',
   null, false)
on conflict do nothing;

-- References
insert into "references" (horse_name, result, location, rider, country, event_date, cover_url) values
  ('Curiosa PS',                   'NEHC Junior 1° & MHC Medal 2°', 'Fieldsone Spring',  null,           'USA', '2026-05-01',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/image-high-3nx7o9.png?enable-io=true&fit=bounds&width=900'),
  ('Peyton',                       'CSI 2*',                         'Peelbergen',        null,           'NL',  '2026-04-01',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/peyton-ref-high.jpg'),
  ('Snapchat van de Broekkant',    '2° FEI WEC 2*',                  'Ocala FL',          'Ward McClain', 'USA', '2026-02-01',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/snapshat-high.jpg'),
  ('Quickly vh Ijzeren Lindenhof', 'Winner 6-Bars',                  'Doha',              null,           'UAE', '2026-02-01',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/quickly-doha-high.jpg'),
  ('Emely van de Pluimert Z',      '4° Kentucky Classic',            'Kentucky',          null,           'USA', '2025-12-01',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/emely-11-high-goiqos.jpg'),
  ('Zarkava Hero Z',               'CSI 4*',                         'Maastricht',        'Johnny Pals',  'NL',  '2025-11-01',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/pals-13-high.jpg')
on conflict do nothing;

-- News
insert into news (title_nl, title_en, body_nl, body_en, category, published, published_at, cover_url) values
  ('Rubel & Morinne 5° @ 3* Lier',
   'Rubel & Morinne 5th @ 3* Lier',
   'Double clear en een 5e plaats in de ranking class met 95 deelnemers.',
   'Double clear and 5th place in the ranking class out of 95 starters.',
   'Resultaten', true, '2026-05-10',
   'https://primary.jwwb.nl/public/x/u/l/temp-exgfvmevdfqypkiyhati/news-260510-high.jpg?enable-io=true&fit=bounds&width=1100'),
  ('Coup de Foudre — CWD Ambassador',
   'Coup de Foudre — CWD Ambassador',
   'Coup de Foudre wordt nieuwe ambassador van CWD Sellier.',
   'Coup de Foudre joins CWD Sellier as new ambassador.',
   'Partnerships', true, '2025-06-30',
   null)
on conflict do nothing;

-- Site settings (CMS toggles)
insert into site_settings (key, value) values
  ('hero',  jsonb_build_object('autoplay', true, 'interval_ms', 5500)),
  ('contact', jsonb_build_object('phone','+32 474 444 059','email','info@maartendriessen.be','whatsapp','+32474444059')),
  ('locales', jsonb_build_array('nl','en','fr','de'))
on conflict (key) do nothing;

-- ---------- Voorbeeld ads ----------------------------------------------
insert into ads (horse_id, platform, region, status, views, leads, ends_on, budget_eur)
select h.id, 'Horsetelex', 'Internationaal', 'live', 4210, 18, current_date + 30, 120
  from horses h where h.name = 'Rubel'
  and not exists (select 1 from ads a where a.horse_id = h.id and a.platform='Horsetelex');

insert into ads (horse_id, platform, region, status, views, leads, ends_on, budget_eur)
select h.id, 'EHorses', 'DACH', 'live', 2180, 9, current_date + 14, 80
  from horses h where h.name = 'Charisma vd Broekkant Z'
  and not exists (select 1 from ads a where a.horse_id = h.id and a.platform='EHorses');

insert into ads (horse_id, platform, region, status, views, leads, ends_on, budget_eur)
select h.id, 'Facebook Ads', 'USA · Europe', 'live', 12640, 24, current_date + 30, 350
  from horses h where h.name = 'Coup de Foudre'
  and not exists (select 1 from ads a where a.horse_id = h.id and a.platform='Facebook Ads');

commit;

-- =========================================================================
--  HET IS KLAAR.
--   - Test:    select * from v_public_horses;
--   - KPI's:   select * from v_dashboard_kpis;
--   - Galerij: select * from v_horses_with_media where slug = 'rubel-2017';
-- =========================================================================
