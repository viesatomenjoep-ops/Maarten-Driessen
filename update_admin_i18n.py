import re

with open('admin.html', 'r') as f:
    html = f.read()

# Add langSwitch to topnav
if 'id="langSwitchAdmin"' not in html:
    html = html.replace('<div class="actions">', '<div class="actions">\n        <div id="langSwitchAdmin" style="display:flex;gap:4px;margin-right:12px"><button data-lang="nl" class="active">NL</button><button data-lang="en">EN</button><button data-lang="fr">FR</button><button data-lang="de">DE</button></div>')

replacements = {
    '<span>Admin Suite</span>': '<span data-i18n="ad.suite">Admin Suite</span>',
    '<h6>CMS</h6>': '<h6 data-i18n="ad.cms">CMS</h6>',
    '<div class="nav-item active" data-page="dashboard"><span class="ic">◆</span>Dashboard</div>': '<div class="nav-item active" data-page="dashboard"><span class="ic">◆</span><span data-i18n="ad.nav.dash">Dashboard</span></div>',
    '<div class="nav-item" data-page="horses"><span class="ic">♞</span>Paarden</div>': '<div class="nav-item" data-page="horses"><span class="ic">♞</span><span data-i18n="ad.nav.horses">Paarden</span></div>',
    '<div class="nav-item" data-page="ads"><span class="ic">⬡</span>Advertenties</div>': '<div class="nav-item" data-page="ads"><span class="ic">⬡</span><span data-i18n="ad.nav.ads">Advertenties</span></div>',
    '<div class="nav-item" data-page="news"><span class="ic">▤</span>News &amp; updates</div>': '<div class="nav-item" data-page="news"><span class="ic">▤</span><span data-i18n="ad.nav.news">News &amp; updates</span></div>',
    '<div class="nav-item" data-page="references"><span class="ic">★</span>Referenties</div>': '<div class="nav-item" data-page="references"><span class="ic">★</span><span data-i18n="ad.nav.refs">Referenties</span></div>',
    
    '<h6>CRM</h6>': '<h6 data-i18n="ad.crm">CRM</h6>',
    '<div class="nav-item" data-page="leads"><span class="ic">✎</span>Leads &amp; intakes</div>': '<div class="nav-item" data-page="leads"><span class="ic">✎</span><span data-i18n="ad.nav.leads">Leads &amp; intakes</span></div>',
    '<div class="nav-item" data-page="customers"><span class="ic">☺</span>Klanten</div>': '<div class="nav-item" data-page="customers"><span class="ic">☺</span><span data-i18n="ad.nav.cust">Klanten</span></div>',
    '<div class="nav-item" data-page="deals"><span class="ic">▣</span>Deals pipeline</div>': '<div class="nav-item" data-page="deals"><span class="ic">▣</span><span data-i18n="ad.nav.deals">Deals pipeline</span></div>',

    '<h6>ERP</h6>': '<h6 data-i18n="ad.erp">ERP</h6>',
    '<div class="nav-item" data-page="inventory"><span class="ic">⌂</span>Stallen &amp; voorraad</div>': '<div class="nav-item" data-page="inventory"><span class="ic">⌂</span><span data-i18n="ad.nav.inv">Stallen &amp; voorraad</span></div>',
    '<div class="nav-item" data-page="transport"><span class="ic">⇆</span>Transport &amp; export</div>': '<div class="nav-item" data-page="transport"><span class="ic">⇆</span><span data-i18n="ad.nav.trans">Transport &amp; export</span></div>',
    '<div class="nav-item" data-page="staff"><span class="ic">👤</span>Personeel &amp; jobs</div>': '<div class="nav-item" data-page="staff"><span class="ic">👤</span><span data-i18n="ad.nav.staff">Personeel &amp; jobs</span></div>',
    '<div class="nav-item" data-page="finance"><span class="ic">€</span>Financieel</div>': '<div class="nav-item" data-page="finance"><span class="ic">€</span><span data-i18n="ad.nav.fin">Financieel</span></div>',

    '<h6>Systeem</h6>': '<h6 data-i18n="ad.sys">Systeem</h6>',
    '<div class="nav-item" data-page="settings"><span class="ic">⚙</span>Supabase &amp; Cloudinary</div>': '<div class="nav-item" data-page="settings"><span class="ic">⚙</span><span data-i18n="ad.nav.set">Supabase &amp; Cloudinary</span></div>',
    '<div class="nav-item" data-page="sql"><span class="ic">{}</span>SQL schema</div>': '<div class="nav-item" data-page="sql"><span class="ic">{}</span><span data-i18n="ad.nav.sql">SQL schema</span></div>',

    '<small>Eigenaar · admin@md.be</small>': '<small data-i18n="ad.owner">Eigenaar · admin@md.be</small>',
    
    '<div class="crumbs">MD Admin / <strong id="crumb">Dashboard</strong></div>': '<div class="crumbs"><span data-i18n="ad.admin">MD Admin</span> / <strong id="crumb" data-i18n="ad.nav.dash">Dashboard</strong></div>',
    '<input placeholder="Zoek paard, klant, lead…">': '<input placeholder="Zoek paard, klant, lead…" data-i18n-placeholder="ad.search">',
    
    '<span id="statusText">Supabase: niet verbonden</span>': '<span id="statusText" data-i18n="ad.status.no">Supabase: niet verbonden</span>',
    
    '<button class="btn btn-p" id="primaryAction">+ Nieuw paard</button>': '<button class="btn btn-p" id="primaryAction" data-i18n="ad.newhorse">+ Nieuw paard</button>',
    
    '<h1>Welcome back, Maarten.</h1>': '<h1 data-i18n="ad.h1">Welcome back, Maarten.</h1>',
    '<div class="sub">Een overzicht van de stal — vandaag, deze week en deze maand.</div>': '<div class="sub" data-i18n="ad.sub">Een overzicht van de stal — vandaag, deze week en deze maand.</div>',
    
    '<div class="l">Paarden in stal</div>': '<div class="l" data-i18n="ad.kpi.horses">Paarden in stal</div>',
    '<div class="delta">+3 deze week</div>': '<div class="delta" data-i18n="ad.kpi.h.delta">+3 deze week</div>',
    
    '<div class="l">Open leads</div>': '<div class="l" data-i18n="ad.kpi.leads">Open leads</div>',
    '<div class="delta">+5 vandaag</div>': '<div class="delta" data-i18n="ad.kpi.l.delta">+5 vandaag</div>',

    '<div class="l">Sold YTD</div>': '<div class="l" data-i18n="ad.kpi.sold">Sold YTD</div>',
    '<div class="delta">+18% YoY</div>': '<div class="delta" data-i18n="ad.kpi.s.delta">+18% YoY</div>',

    '<div class="l">Omzet (€)</div>': '<div class="l" data-i18n="ad.kpi.rev">Omzet (€)</div>',
    '<div class="delta down">-3% vs vorige maand</div>': '<div class="delta down" data-i18n="ad.kpi.r.delta">-3% vs vorige maand</div>',
    
    '<h3>Verkoop per maand</h3>': '<h3 data-i18n="ad.sales">Verkoop per maand</h3>',
    '<span style="color:var(--muted);font-size:12px;font-weight:400">2026 — € in duizenden</span>': '<span style="color:var(--muted);font-size:12px;font-weight:400" data-i18n="ad.sales.sub">2026 — € in duizenden</span>',
    '<button class="btn btn-g" style="padding:6px 12px;font-size:12px">Export CSV</button>': '<button class="btn btn-g" style="padding:6px 12px;font-size:12px" data-i18n="ad.export">Export CSV</button>',

    '<h3>Recente activiteit</h3>': '<h3 data-i18n="ad.recent">Recente activiteit</h3>',
    '<small>Vandaag in de stal</small>': '<small data-i18n="ad.recent.sub">Vandaag in de stal</small>',

    '<h6>Nieuwe lead — Sophia Martens (BE)</h6>': '<h6><span data-i18n="ad.act.1.t">Nieuwe lead</span> — Sophia Martens (BE)</h6>',
    '<small>Zoekt 8-9 jaar merrie, ervaring 140cm · 12 min geleden</small>': '<small data-i18n="ad.act.1.d">Zoekt 8-9 jaar merrie, ervaring 140cm · 12 min geleden</small>',

    '<h6>Sold — Snapchat vd Broekkant</h6>': '<h6><span data-i18n="ad.act.2.t">Sold</span> — Snapchat vd Broekkant</h6>',
    '<small>USA · Ward McClain · vandaag</small>': '<small data-i18n="ad.act.2.d">USA · Ward McClain · vandaag</small>',

    '<h6>Transport gepland — Oliva Nova</h6>': '<h6><span data-i18n="ad.act.3.t">Transport gepland</span> — Oliva Nova</h6>',
    '<small>3 paarden · vertrek 18 mei · charter "Sky Cargo"</small>': '<small data-i18n="ad.act.3.d">3 paarden · vertrek 18 mei · charter "Sky Cargo"</small>',

    '<h6>Embryo geïmplanteerd</h6>': '<h6 data-i18n="ad.act.4.t">Embryo geïmplanteerd</h6>',
    '<small>Kashmir van \'t Schuttershof × Vaberlina</small>': '<small data-i18n="ad.act.4.d">Kashmir van \'t Schuttershof × Vaberlina</small>',

    '<h6>News post gepubliceerd</h6>': '<h6 data-i18n="ad.act.5.t">News post gepubliceerd</h6>',
    '<small>Rubel &amp; Morinne 5° in Lier 3* · 1u geleden</small>': '<small data-i18n="ad.act.5.d">Rubel &amp; Morinne 5° in Lier 3* · 1u geleden</small>',

    '<h3>Top paarden (views)</h3>': '<h3 data-i18n="ad.top">Top paarden (views)</h3>',
    '<small>Deze week</small>': '<small data-i18n="ad.top.sub">Deze week</small>',
    
    '<h3>Pipeline</h3>': '<h3 data-i18n="ad.pipe">Pipeline</h3>',
    '<small>Open deals</small>': '<small data-i18n="ad.pipe.sub">Open deals</small>',
    
    '<td style="color:var(--muted)">Qualified</td>': '<td style="color:var(--muted)" data-i18n="ad.pipe.1">Qualified</td>',
    '<td style="color:var(--muted)">Bezichtiging</td>': '<td style="color:var(--muted)" data-i18n="ad.pipe.2">Bezichtiging</td>',
    '<td style="color:var(--muted)">Veterinair check</td>': '<td style="color:var(--muted)" data-i18n="ad.pipe.3">Veterinair check</td>',
    '<td style="color:var(--muted)">Onderhandeling</td>': '<td style="color:var(--muted)" data-i18n="ad.pipe.4">Onderhandeling</td>',
    '<td style="color:var(--ok)">Won</td>': '<td style="color:var(--ok)" data-i18n="ad.pipe.5">Won</td>',
    '<td style="color:var(--danger)">Lost</td>': '<td style="color:var(--danger)" data-i18n="ad.pipe.6">Lost</td>',

    '<h3>Stallen</h3>': '<h3 data-i18n="ad.stables">Stallen</h3>',
    '<small>Bezetting</small>': '<small data-i18n="ad.stables.sub">Bezetting</small>',
    
    '<td>Indoor Stal A</td>': '<td data-i18n="ad.st.1">Indoor Stal A</td>',
    '<span class="pill muted">12/12 vol</span>': '<span class="pill muted" data-i18n="ad.st.1.s">12/12 vol</span>',
    '<td>Outdoor Stal B</td>': '<td data-i18n="ad.st.2">Outdoor Stal B</td>',
    '<span class="pill ok">9/14 5 vrij</span>': '<span class="pill ok" data-i18n="ad.st.2.s">9/14 5 vrij</span>',
    '<td>Foal Stal</td>': '<td data-i18n="ad.st.3">Foal Stal</td>',
    '<span class="pill ok">6/8 2 vrij</span>': '<span class="pill ok" data-i18n="ad.st.3.s">6/8 2 vrij</span>',
    '<td>Quarantaine</td>': '<td data-i18n="ad.st.4">Quarantaine</td>',
    '<span class="pill ok">2/4 2 vrij</span>': '<span class="pill ok" data-i18n="ad.st.4.s">2/4 2 vrij</span>',
    '<td>Walker capacity</td>': '<td data-i18n="ad.st.5">Walker capacity</td>',
    '<span class="pill ok">OK</span>': '<span class="pill ok" data-i18n="ad.st.5.s">OK</span>',
}

for k, v in replacements.items():
    html = html.replace(k, v)

# Inject JS for I18N and langSwitch handler just before closing body
script_injection = """
<style>
#langSwitchAdmin button {
  background: transparent; border: 1px solid var(--line); border-radius: 6px;
  padding: 4px 8px; font-size: 11px; cursor: pointer; color: var(--muted);
}
#langSwitchAdmin button.active {
  background: var(--ink); color: #fff; border-color: var(--ink);
}
</style>
<script>
const I18N_ADMIN = {
  nl: {
    "ad.suite": "Admin Suite", "ad.cms": "CMS", "ad.crm": "CRM", "ad.erp": "ERP", "ad.sys": "Systeem",
    "ad.nav.dash": "Dashboard", "ad.nav.horses": "Paarden", "ad.nav.ads": "Advertenties", "ad.nav.news": "News & updates", "ad.nav.refs": "Referenties",
    "ad.nav.leads": "Leads & intakes", "ad.nav.cust": "Klanten", "ad.nav.deals": "Deals pipeline",
    "ad.nav.inv": "Stallen & voorraad", "ad.nav.trans": "Transport & export", "ad.nav.staff": "Personeel & jobs", "ad.nav.fin": "Financieel",
    "ad.nav.set": "Supabase & Cloudinary", "ad.nav.sql": "SQL schema",
    "ad.owner": "Eigenaar · admin@md.be", "ad.admin": "MD Admin",
    "ad.search": "Zoek paard, klant, lead…", "ad.newhorse": "+ Nieuw paard",
    "ad.status.no": "Supabase: niet verbonden",
    "ad.h1": "Welcome back, Maarten.", "ad.sub": "Een overzicht van de stal — vandaag, deze week en deze maand.",
    "ad.kpi.horses": "Paarden in stal", "ad.kpi.h.delta": "+3 deze week",
    "ad.kpi.leads": "Open leads", "ad.kpi.l.delta": "+5 vandaag",
    "ad.kpi.sold": "Sold YTD", "ad.kpi.s.delta": "+18% YoY",
    "ad.kpi.rev": "Omzet (€)", "ad.kpi.r.delta": "-3% vs vorige maand",
    "ad.sales": "Verkoop per maand", "ad.sales.sub": "2026 — € in duizenden", "ad.export": "Export CSV",
    "ad.recent": "Recente activiteit", "ad.recent.sub": "Vandaag in de stal",
    "ad.act.1.t": "Nieuwe lead", "ad.act.1.d": "Zoekt 8-9 jaar merrie, ervaring 140cm · 12 min geleden",
    "ad.act.2.t": "Sold", "ad.act.2.d": "USA · Ward McClain · vandaag",
    "ad.act.3.t": "Transport gepland", "ad.act.3.d": "3 paarden · vertrek 18 mei · charter 'Sky Cargo'",
    "ad.act.4.t": "Embryo geïmplanteerd", "ad.act.4.d": "Kashmir van 't Schuttershof × Vaberlina",
    "ad.act.5.t": "News post gepubliceerd", "ad.act.5.d": "Rubel & Morinne 5° in Lier 3* · 1u geleden",
    "ad.top": "Top paarden (views)", "ad.top.sub": "Deze week",
    "ad.pipe": "Pipeline", "ad.pipe.sub": "Open deals",
    "ad.pipe.1": "Qualified", "ad.pipe.2": "Bezichtiging", "ad.pipe.3": "Veterinair check", "ad.pipe.4": "Onderhandeling", "ad.pipe.5": "Won", "ad.pipe.6": "Lost",
    "ad.stables": "Stallen", "ad.stables.sub": "Bezetting",
    "ad.st.1": "Indoor Stal A", "ad.st.1.s": "12/12 vol",
    "ad.st.2": "Outdoor Stal B", "ad.st.2.s": "9/14 5 vrij",
    "ad.st.3": "Foal Stal", "ad.st.3.s": "6/8 2 vrij",
    "ad.st.4": "Quarantaine", "ad.st.4.s": "2/4 2 vrij",
    "ad.st.5": "Walker capacity", "ad.st.5.s": "OK"
  },
  en: {
    "ad.suite": "Admin Suite", "ad.cms": "CMS", "ad.crm": "CRM", "ad.erp": "ERP", "ad.sys": "System",
    "ad.nav.dash": "Dashboard", "ad.nav.horses": "Horses", "ad.nav.ads": "Ads", "ad.nav.news": "News & updates", "ad.nav.refs": "References",
    "ad.nav.leads": "Leads & intakes", "ad.nav.cust": "Customers", "ad.nav.deals": "Deals pipeline",
    "ad.nav.inv": "Stables & inventory", "ad.nav.trans": "Transport & export", "ad.nav.staff": "Staff & jobs", "ad.nav.fin": "Finance",
    "ad.nav.set": "Supabase & Cloudinary", "ad.nav.sql": "SQL schema",
    "ad.owner": "Owner · admin@md.be", "ad.admin": "MD Admin",
    "ad.search": "Search horse, customer, lead…", "ad.newhorse": "+ New horse",
    "ad.status.no": "Supabase: not connected",
    "ad.h1": "Welcome back, Maarten.", "ad.sub": "An overview of the stable — today, this week and this month.",
    "ad.kpi.horses": "Horses in stable", "ad.kpi.h.delta": "+3 this week",
    "ad.kpi.leads": "Open leads", "ad.kpi.l.delta": "+5 today",
    "ad.kpi.sold": "Sold YTD", "ad.kpi.s.delta": "+18% YoY",
    "ad.kpi.rev": "Revenue (€)", "ad.kpi.r.delta": "-3% vs last month",
    "ad.sales": "Sales per month", "ad.sales.sub": "2026 — € in thousands", "ad.export": "Export CSV",
    "ad.recent": "Recent activity", "ad.recent.sub": "Today in the stable",
    "ad.act.1.t": "New lead", "ad.act.1.d": "Looking for 8-9 year mare, experience 140cm · 12 mins ago",
    "ad.act.2.t": "Sold", "ad.act.2.d": "USA · Ward McClain · today",
    "ad.act.3.t": "Transport planned", "ad.act.3.d": "3 horses · departure May 18 · charter 'Sky Cargo'",
    "ad.act.4.t": "Embryo implanted", "ad.act.4.d": "Kashmir van 't Schuttershof × Vaberlina",
    "ad.act.5.t": "News post published", "ad.act.5.d": "Rubel & Morinne 5° in Lier 3* · 1h ago",
    "ad.top": "Top horses (views)", "ad.top.sub": "This week",
    "ad.pipe": "Pipeline", "ad.pipe.sub": "Open deals",
    "ad.pipe.1": "Qualified", "ad.pipe.2": "Viewing", "ad.pipe.3": "Vet check", "ad.pipe.4": "Negotiation", "ad.pipe.5": "Won", "ad.pipe.6": "Lost",
    "ad.stables": "Stables", "ad.stables.sub": "Occupancy",
    "ad.st.1": "Indoor Stable A", "ad.st.1.s": "12/12 full",
    "ad.st.2": "Outdoor Stable B", "ad.st.2.s": "9/14 5 free",
    "ad.st.3": "Foal Stable", "ad.st.3.s": "6/8 2 free",
    "ad.st.4": "Quarantine", "ad.st.4.s": "2/4 2 free",
    "ad.st.5": "Walker capacity", "ad.st.5.s": "OK"
  },
  fr: {
    "ad.suite": "Suite Admin", "ad.cms": "CMS", "ad.crm": "CRM", "ad.erp": "ERP", "ad.sys": "Système",
    "ad.nav.dash": "Tableau de bord", "ad.nav.horses": "Chevaux", "ad.nav.ads": "Annonces", "ad.nav.news": "Actualités", "ad.nav.refs": "Références",
    "ad.nav.leads": "Leads & demandes", "ad.nav.cust": "Clients", "ad.nav.deals": "Pipeline d'offres",
    "ad.nav.inv": "Écuries et stock", "ad.nav.trans": "Transport & export", "ad.nav.staff": "Personnel & emplois", "ad.nav.fin": "Finances",
    "ad.nav.set": "Supabase & Cloudinary", "ad.nav.sql": "Schéma SQL",
    "ad.owner": "Propriétaire · admin@md.be", "ad.admin": "Admin MD",
    "ad.search": "Rechercher cheval, client, lead…", "ad.newhorse": "+ Nouveau cheval",
    "ad.status.no": "Supabase : non connecté",
    "ad.h1": "Bienvenue, Maarten.", "ad.sub": "Un aperçu de l'écurie — aujourd'hui, cette semaine et ce mois-ci.",
    "ad.kpi.horses": "Chevaux à l'écurie", "ad.kpi.h.delta": "+3 cette semaine",
    "ad.kpi.leads": "Leads ouverts", "ad.kpi.l.delta": "+5 aujourd'hui",
    "ad.kpi.sold": "Vendus (année)", "ad.kpi.s.delta": "+18% a/a",
    "ad.kpi.rev": "Revenus (€)", "ad.kpi.r.delta": "-3% par rapport au mois dernier",
    "ad.sales": "Ventes par mois", "ad.sales.sub": "2026 — € en milliers", "ad.export": "Exporter CSV",
    "ad.recent": "Activité récente", "ad.recent.sub": "Aujourd'hui à l'écurie",
    "ad.act.1.t": "Nouveau lead", "ad.act.1.d": "Cherche jument de 8-9 ans, expérience 140cm · il y a 12 min",
    "ad.act.2.t": "Vendu", "ad.act.2.d": "USA · Ward McClain · aujourd'hui",
    "ad.act.3.t": "Transport prévu", "ad.act.3.d": "3 chevaux · départ 18 mai · charter 'Sky Cargo'",
    "ad.act.4.t": "Embryon implanté", "ad.act.4.d": "Kashmir van 't Schuttershof × Vaberlina",
    "ad.act.5.t": "Article publié", "ad.act.5.d": "Rubel & Morinne 5° à Lier 3* · il y a 1h",
    "ad.top": "Top chevaux (vues)", "ad.top.sub": "Cette semaine",
    "ad.pipe": "Pipeline", "ad.pipe.sub": "Offres ouvertes",
    "ad.pipe.1": "Qualifié", "ad.pipe.2": "Visite", "ad.pipe.3": "Contrôle vétérinaire", "ad.pipe.4": "Négociation", "ad.pipe.5": "Gagné", "ad.pipe.6": "Perdu",
    "ad.stables": "Écuries", "ad.stables.sub": "Occupation",
    "ad.st.1": "Écurie intérieure A", "ad.st.1.s": "12/12 complet",
    "ad.st.2": "Écurie extérieure B", "ad.st.2.s": "9/14 5 libres",
    "ad.st.3": "Écurie Poulains", "ad.st.3.s": "6/8 2 libres",
    "ad.st.4": "Quarantaine", "ad.st.4.s": "2/4 2 libres",
    "ad.st.5": "Capacité marcheur", "ad.st.5.s": "OK"
  },
  de: {
    "ad.suite": "Admin-Suite", "ad.cms": "CMS", "ad.crm": "CRM", "ad.erp": "ERP", "ad.sys": "System",
    "ad.nav.dash": "Dashboard", "ad.nav.horses": "Pferde", "ad.nav.ads": "Anzeigen", "ad.nav.news": "News & Updates", "ad.nav.refs": "Referenzen",
    "ad.nav.leads": "Leads & Anfragen", "ad.nav.cust": "Kunden", "ad.nav.deals": "Deals-Pipeline",
    "ad.nav.inv": "Ställe & Bestand", "ad.nav.trans": "Transport & Export", "ad.nav.staff": "Personal & Jobs", "ad.nav.fin": "Finanzen",
    "ad.nav.set": "Supabase & Cloudinary", "ad.nav.sql": "SQL-Schema",
    "ad.owner": "Inhaber · admin@md.be", "ad.admin": "MD Admin",
    "ad.search": "Pferd, Kunde, Lead suchen…", "ad.newhorse": "+ Neues Pferd",
    "ad.status.no": "Supabase: nicht verbunden",
    "ad.h1": "Willkommen zurück, Maarten.", "ad.sub": "Ein Überblick über den Stall — heute, diese Woche und diesen Monat.",
    "ad.kpi.horses": "Pferde im Stall", "ad.kpi.h.delta": "+3 diese Woche",
    "ad.kpi.leads": "Offene Leads", "ad.kpi.l.delta": "+5 heute",
    "ad.kpi.sold": "Verkauft YTD", "ad.kpi.s.delta": "+18% YoY",
    "ad.kpi.rev": "Umsatz (€)", "ad.kpi.r.delta": "-3% ggü. Vormonat",
    "ad.sales": "Umsatz pro Monat", "ad.sales.sub": "2026 — € in Tausend", "ad.export": "CSV exportieren",
    "ad.recent": "Letzte Aktivität", "ad.recent.sub": "Heute im Stall",
    "ad.act.1.t": "Neuer Lead", "ad.act.1.d": "Sucht 8-9-jährige Stute, Erfahrung 140cm · vor 12 Min",
    "ad.act.2.t": "Verkauft", "ad.act.2.d": "USA · Ward McClain · heute",
    "ad.act.3.t": "Transport geplant", "ad.act.3.d": "3 Pferde · Abflug 18. Mai · Charter 'Sky Cargo'",
    "ad.act.4.t": "Embryo implantiert", "ad.act.4.d": "Kashmir van 't Schuttershof × Vaberlina",
    "ad.act.5.t": "News veröffentlicht", "ad.act.5.d": "Rubel & Morinne 5. in Lier 3* · vor 1 Std",
    "ad.top": "Top-Pferde (Aufrufe)", "ad.top.sub": "Diese Woche",
    "ad.pipe": "Pipeline", "ad.pipe.sub": "Offene Deals",
    "ad.pipe.1": "Qualifiziert", "ad.pipe.2": "Besichtigung", "ad.pipe.3": "Tierarzt-Check", "ad.pipe.4": "Verhandlung", "ad.pipe.5": "Gewonnen", "ad.pipe.6": "Verloren",
    "ad.stables": "Ställe", "ad.stables.sub": "Belegung",
    "ad.st.1": "Innenstall A", "ad.st.1.s": "12/12 voll",
    "ad.st.2": "Außenstall B", "ad.st.2.s": "9/14 5 frei",
    "ad.st.3": "Fohlenstall", "ad.st.3.s": "6/8 2 frei",
    "ad.st.4": "Quarantäne", "ad.st.4.s": "2/4 2 frei",
    "ad.st.5": "Führanlagen-Kapazität", "ad.st.5.s": "OK"
  }
};
function setLangAdmin(l) {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const k = el.getAttribute('data-i18n');
    if(I18N_ADMIN[l] && I18N_ADMIN[l][k]) el.innerHTML = I18N_ADMIN[l][k];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const k = el.getAttribute('data-i18n-placeholder');
    if(I18N_ADMIN[l] && I18N_ADMIN[l][k]) el.placeholder = I18N_ADMIN[l][k];
  });
  document.querySelectorAll('#langSwitchAdmin button').forEach(b => b.classList.toggle('active', b.dataset.lang === l));
}
document.querySelectorAll('#langSwitchAdmin button').forEach(b => b.addEventListener('click', () => setLangAdmin(b.dataset.lang)));
</script>
</body>"""

if 'setLangAdmin' not in html:
    html = html.replace('</body>', script_injection)

with open('admin.html', 'w') as f:
    f.write(html)
