import re

with open('index.html', 'r') as f:
    html = f.read()

new_i18n = """const I18N = {
  nl: {
    "nav.horses": "Paarden", "nav.collection": "Collectie", "nav.references": "Referenties", "nav.stable": "Stables", "nav.news": "News", "nav.contact": "Contact", "nav.findhorse": "Vind je paard",
    "hero.eyebrow": "Belgian Sporthorses · Est. 1995",
    "hero.l1": "We find you", "hero.l2": "your quality horse.",
    "hero.lede": "Een zorgvuldig samengestelde selectie internationale springpaarden, van veelbelovende veulens tot wedstrijdrijp talent. Premium kwaliteit, eerlijke begeleiding en wereldwijde service vanuit hartje België.",
    "hero.cta1": "Bekijk collectie", "hero.cta2": "Stel je wensen samen",
    "meta.horses": "Paarden", "meta.horses.s": "in onze database", "meta.refs": "Referenties", "meta.refs.s": "5* prestaties wereldwijd", "meta.years": "Ervaring", "meta.years.s": "in topsport & handel",
    "hor.eyebrow": "Onze collectie", "hor.title": "Jumping horses, by year of birth.", "hor.desc": "Verken onze uitzonderlijke selectie veelbelovende springpaarden. Filter op geboortejaar.",
    
    "feat.eyebrow": "Featured", "feat.title": "Onze toppers, in de spotlight.", "feat.desc": "Drie van de meest besproken paarden uit onze huidige collectie — internationaal opgeleid, klaar voor topsport.",
    
    "svc.eyebrow": "What we do", "svc.title": "Een huis dat meer levert dan een paard.", "svc.desc": "Van opsporen tot opleiden, van het stalleven tot het wereldwijde transport — alles onder één dak.",
    "svc.1.t": "Wereldwijde verkoop", "svc.1.d": "Premium springpaarden voor amateurs tot 5* niveau. Eerlijke matching tussen ruiter en paard, met internationale klantenkring in USA, Mexico, GCC en Europa.",
    "svc.2.t": "Op zoek naar jouw paard", "svc.2.d": "Vertel ons wat je zoekt en wij doen het werk. Sexe, leeftijd, ervaring, kleur, budget — wij vinden het paard dat bij jou past, ook als het niet in onze stal staat.",
    "svc.3.t": "Opleiding & verblijf", "svc.3.d": "Moderne faciliteiten, ruime weides, indoor & outdoor pistes, walker, lounge. Dagelijkse training onder de beste begeleiding.",
    "svc.4.t": "Embryo's & foals", "svc.4.d": "Een uitgelezen selectie embryo's uit topmoederlijnen — Lorenta, Kayenne vd Broekkant — beschikbaar voor handel of eigen opfok.",
    "svc.5.t": "Wereldwijd transport", "svc.5.d": "Volledige begeleiding bij export — gezondheidspapieren, quarantaine, charter naar USA, Latijns-Amerika, Midden-Oosten en Azië.",
    "svc.6.t": "Levenslang contact", "svc.6.d": "Een paard verkopen is voor ons het begin van de relatie. We blijven betrokken bij de carrière en helpen waar we kunnen.",
    
    "ref.eyebrow": "References", "ref.title": "Paarden die hun verhaal verder schrijven.", "ref.desc": "Een selectie van paarden die wij verkochten en die intussen succesvol hun weg vinden in de internationale ring.",
    "ref.btn": "Bekijk alle referenties",
    
    "stb.eyebrow": "Our home", "stb.title": "Een stal die zorgt voor wat ze rijdt.", "stb.desc": "Indoor & outdoor pistes, ruime stallen, paddocks, walker en een lounge die ruiters het gevoel geeft thuis te komen.",
    
    "int.eyebrow": "Intake module", "int.title1": "What can we", "int.title2": "do 4 you?", 
    "int.desc": "Vertel ons in een paar klikken wat je zoekt. We bekijken onze stal én ons internationale netwerk, en komen terug met een persoonlijke shortlist. Geen verplichtingen — wél echte expertise.",
    "int.quote": "\"Eerlijk advies, het juiste paard voor de juiste ruiter. Dat is het enige dat ons drijft.\"",
    "int.step": "Step 01 — Profiel", "int.h3": "Vertel ons wat je zoekt.",
    
    "lbl.sex": "Geslacht", "opt.stallion": "Hengst", "opt.mare": "Merrie", "opt.gelding": "Ruin",
    "lbl.age": "Leeftijd", "opt.2-3": "2-3 jaar", "opt.3-4": "3-4 jaar", "opt.4-5": "4-5 jaar", "opt.6-7": "6-7 jaar", "opt.8-9": "8-9 jaar", "opt.10-11": "10-11 jaar", "opt.12-13": "12-13 jaar",
    "lbl.exp": "Ervaringsniveau", "opt.noexp": "Niet beleerd", "opt.90": "Tot 90 cm", "opt.110": "Tot 110 cm", "opt.130": "Tot 130 cm", "opt.140": "Tot 140 cm", "opt.150": "150 cm & hoger",
    "lbl.color": "Voorkeurskleur", "opt.black": "Zwart", "opt.brown": "Bruin", "opt.white": "Wit", "opt.chestnut": "Vos", "opt.bay": "Bay", "opt.grey": "Schimmel",
    "lbl.budget": "Indicatief budget", "opt.15-30": "€ 15-30k", "opt.30-60": "€ 30-60k", "opt.60-120": "€ 60-120k", "opt.120+": "€ 120k +",
    "lbl.notes": "Opmerkingen of specifieke wensen", "pl.notes": "Vertel ons over jezelf, je ruiterprofiel en wat je écht zoekt.",
    "pl.name": "Voornaam en naam", "pl.email": "E-mail", "pl.phone": "Telefoon (+...)",
    "lbl.country": "Land — selecteer", "opt.be": "België", "opt.nl": "Nederland", "opt.fr": "Frankrijk", "opt.de": "Duitsland", "opt.us": "USA", "opt.mx": "Mexico", "opt.uk": "UK", "opt.ae": "UAE", "opt.other": "Andere",
    "form.privacy": "We bewaren je gegevens enkel om jouw vraag op te volgen.", "form.submit": "Verstuur aanvraag",
    
    "news.eyebrow": "News & updates", "news.title": "Het laatste van de piste.", "news.desc": "Resultaten, wedstrijden en moves uit onze stal en die van onze klanten.",
    
    "cta.title1": "Klaar om", "cta.title2": "jouw paard te vinden?", "cta.desc": "+32 474 444 059 · Maaseik, België · 7d/7 bereikbaar via WhatsApp.",
    "cta.call": "Bel ons", "cta.wa": "WhatsApp",
    "ft.about": "We find you your quality horse. Premium Belgian sporthorses, hand-picked en wereldwijd geleverd, met de zorg van een familiestal en de schaal van een internationaal bedrijf.",
    "ft.nav": "Navigeer", "ft.serv": "Diensten", "ft.contact": "Contact",
    "ft.s1": "Verkoop", "ft.s2": "Op zoek naar jouw paard", "ft.s3": "Opleiding & verblijf", "ft.s4": "Embryo's & foals", "ft.s5": "Wereldwijd transport",
    "ft.copy": "© 2026 Maarten Driessen Sporthorses — alle rechten voorbehouden.", "ft.privacy": "Privacy", "ft.cookies": "Cookies", "ft.admin": "Admin login"
  },
  en: {
    "nav.horses": "Horses", "nav.collection": "Collection", "nav.references": "References", "nav.stable": "Stables", "nav.news": "News", "nav.contact": "Contact", "nav.findhorse": "Find your horse",
    "hero.eyebrow": "Belgian Sporthorses · Est. 1995",
    "hero.l1": "We find you", "hero.l2": "your quality horse.",
    "hero.lede": "A carefully curated selection of international jumping horses, from promising foals to competition-ready talent. Premium quality, honest guidance and worldwide service from the heart of Belgium.",
    "hero.cta1": "View collection", "hero.cta2": "Tell us what you want",
    "meta.horses": "Horses", "meta.horses.s": "in our database", "meta.refs": "References", "meta.refs.s": "5* results worldwide", "meta.years": "Experience", "meta.years.s": "in top sport & trade",
    "hor.eyebrow": "Our collection", "hor.title": "Jumping horses, by year of birth.", "hor.desc": "Discover our exceptional selection of promising jumping horses. Filter by year of birth.",
    
    "feat.eyebrow": "Featured", "feat.title": "Our top horses, in the spotlight.", "feat.desc": "Three of the most talked-about horses from our current collection — internationally trained, ready for top sport.",
    
    "svc.eyebrow": "What we do", "svc.title": "A home that delivers more than a horse.", "svc.desc": "From scouting to training, from daily care to worldwide transport — everything under one roof.",
    "svc.1.t": "Worldwide sales", "svc.1.d": "Premium jumping horses for amateurs up to 5* level. Honest matching between rider and horse, with an international clientele in the USA, Mexico, GCC and Europe.",
    "svc.2.t": "Finding your horse", "svc.2.d": "Tell us what you are looking for and we do the work. Sex, age, experience, color, budget — we find the horse that fits you, even if it's not currently in our stable.",
    "svc.3.t": "Training & stay", "svc.3.d": "Modern facilities, spacious pastures, indoor & outdoor arenas, walker, lounge. Daily training under the best guidance.",
    "svc.4.t": "Embryos & foals", "svc.4.d": "An exquisite selection of embryos from top motherlines — Lorenta, Kayenne vd Broekkant — available for trade or own breeding.",
    "svc.5.t": "Worldwide transport", "svc.5.d": "Full support for export — health certificates, quarantine, charters to the USA, Latin America, Middle East and Asia.",
    "svc.6.t": "Lifelong contact", "svc.6.d": "Selling a horse is just the beginning of our relationship. We stay involved in their career and help wherever we can.",
    
    "ref.eyebrow": "References", "ref.title": "Horses continuing their story.", "ref.desc": "A selection of horses we sold that are now successfully making their way in the international ring.",
    "ref.btn": "View all references",
    
    "stb.eyebrow": "Our home", "stb.title": "A stable that cares for what it rides.", "stb.desc": "Indoor & outdoor arenas, spacious stables, paddocks, walker and a lounge that makes riders feel at home.",
    
    "int.eyebrow": "Intake module", "int.title1": "What can we", "int.title2": "do 4 you?", 
    "int.desc": "Tell us what you are looking for in a few clicks. We'll check our stable and international network, and get back to you with a personal shortlist. No obligations — just real expertise.",
    "int.quote": "\"Honest advice, the right horse for the right rider. That is the only thing that drives us.\"",
    "int.step": "Step 01 — Profile", "int.h3": "Tell us what you are looking for.",
    
    "lbl.sex": "Sex", "opt.stallion": "Stallion", "opt.mare": "Mare", "opt.gelding": "Gelding",
    "lbl.age": "Age", "opt.2-3": "2-3 years", "opt.3-4": "3-4 years", "opt.4-5": "4-5 years", "opt.6-7": "6-7 years", "opt.8-9": "8-9 years", "opt.10-11": "10-11 years", "opt.12-13": "12-13 years",
    "lbl.exp": "Experience level", "opt.noexp": "Not broken in", "opt.90": "Up to 90 cm", "opt.110": "Up to 110 cm", "opt.130": "Up to 130 cm", "opt.140": "Up to 140 cm", "opt.150": "150 cm & higher",
    "lbl.color": "Preferred color", "opt.black": "Black", "opt.brown": "Brown", "opt.white": "White", "opt.chestnut": "Chestnut", "opt.bay": "Bay", "opt.grey": "Grey",
    "lbl.budget": "Indicative budget", "opt.15-30": "€ 15-30k", "opt.30-60": "€ 30-60k", "opt.60-120": "€ 60-120k", "opt.120+": "€ 120k +",
    "lbl.notes": "Remarks or specific wishes", "pl.notes": "Tell us about yourself, your rider profile and what you are really looking for.",
    "pl.name": "First and last name", "pl.email": "E-mail", "pl.phone": "Phone (+...)",
    "lbl.country": "Country — select", "opt.be": "Belgium", "opt.nl": "Netherlands", "opt.fr": "France", "opt.de": "Germany", "opt.us": "USA", "opt.mx": "Mexico", "opt.uk": "UK", "opt.ae": "UAE", "opt.other": "Other",
    "form.privacy": "We only keep your data to follow up on your request.", "form.submit": "Submit request",
    
    "news.eyebrow": "News & updates", "news.title": "The latest from the arena.", "news.desc": "Results, competitions and moves from our stable and those of our clients.",
    
    "cta.title1": "Ready to", "cta.title2": "find your horse?", "cta.desc": "+32 474 444 059 · Maaseik, Belgium · 7d/7 reachable via WhatsApp.",
    "cta.call": "Call us", "cta.wa": "WhatsApp",
    "ft.about": "We find you your quality horse. Premium Belgian sporthorses, hand-picked and delivered worldwide, with the care of a family stable and the scale of an international company.",
    "ft.nav": "Navigate", "ft.serv": "Services", "ft.contact": "Contact",
    "ft.s1": "Sales", "ft.s2": "Finding your horse", "ft.s3": "Training & stay", "ft.s4": "Embryos & foals", "ft.s5": "Worldwide transport",
    "ft.copy": "© 2026 Maarten Driessen Sporthorses — all rights reserved.", "ft.privacy": "Privacy", "ft.cookies": "Cookies", "ft.admin": "Admin login"
  },
  fr: {
    "nav.horses": "Chevaux", "nav.collection": "Collection", "nav.references": "Références", "nav.stable": "Écurie", "nav.news": "Actualités", "nav.contact": "Contact", "nav.findhorse": "Trouvez votre cheval",
    "hero.eyebrow": "Chevaux de sport belges · Depuis 1995",
    "hero.l1": "Nous vous trouvons", "hero.l2": "votre cheval d'exception.",
    "hero.lede": "Une sélection soignée de chevaux de saut internationaux, du poulain prometteur au talent prêt à concourir. Qualité premium, conseils honnêtes et service mondial depuis le cœur de la Belgique.",
    "hero.cta1": "Voir la collection", "hero.cta2": "Dites-nous ce que vous cherchez",
    "meta.horses": "Chevaux", "meta.horses.s": "dans notre base", "meta.refs": "Références", "meta.refs.s": "performances 5* mondiales", "meta.years": "Expérience", "meta.years.s": "sport & commerce",
    "hor.eyebrow": "Notre collection", "hor.title": "Chevaux de saut, par année de naissance.", "hor.desc": "Explorez notre sélection exceptionnelle de chevaux de saut prometteurs. Filtrez par année de naissance.",
    
    "feat.eyebrow": "En vedette", "feat.title": "Nos meilleurs chevaux, sous les projecteurs.", "feat.desc": "Trois des chevaux les plus remarquables de notre collection actuelle — formés à l'international, prêts pour le sport de haut niveau.",
    
    "svc.eyebrow": "Ce que nous faisons", "svc.title": "Une maison qui offre plus qu'un cheval.", "svc.desc": "De la recherche à la formation, des soins quotidiens au transport mondial — tout sous un même toit.",
    "svc.1.t": "Ventes mondiales", "svc.1.d": "Chevaux de saut premium pour amateurs jusqu'au niveau 5*. Accord parfait entre cavalier et cheval, avec une clientèle internationale aux USA, au Mexique, dans le CCG et en Europe.",
    "svc.2.t": "Recherche de votre cheval", "svc.2.d": "Dites-nous ce que vous cherchez et nous faisons le reste. Sexe, âge, expérience, robe, budget — nous trouvons le cheval qui vous correspond.",
    "svc.3.t": "Formation et hébergement", "svc.3.d": "Installations modernes, vastes pâturages, pistes intérieures et extérieures, marcheur, salon. Entraînement quotidien sous la meilleure direction.",
    "svc.4.t": "Embryons et poulains", "svc.4.d": "Une sélection exquise d'embryons issus des meilleures lignées maternelles — Lorenta, Kayenne vd Broekkant — disponibles pour le commerce ou votre propre élevage.",
    "svc.5.t": "Transport mondial", "svc.5.d": "Accompagnement complet pour l'exportation — certificats sanitaires, quarantaine, vols charters vers les USA, l'Amérique latine, le Moyen-Orient et l'Asie.",
    "svc.6.t": "Contact à vie", "svc.6.d": "Vendre un cheval n'est pour nous que le début de la relation. Nous restons impliqués dans leur carrière et aidons là où nous le pouvons.",
    
    "ref.eyebrow": "Références", "ref.title": "Des chevaux qui continuent leur histoire.", "ref.desc": "Une sélection de chevaux que nous avons vendus et qui poursuivent aujourd'hui avec succès leur chemin sur la scène internationale.",
    "ref.btn": "Voir toutes les références",
    
    "stb.eyebrow": "Notre domaine", "stb.title": "Une écurie qui prend soin de ce qu'elle monte.", "stb.desc": "Pistes intérieures et extérieures, écuries spacieuses, paddocks, marcheur et un salon qui permet aux cavaliers de se sentir chez eux.",
    
    "int.eyebrow": "Module d'admission", "int.title1": "Que pouvons-nous", "int.title2": "faire pour vous?", 
    "int.desc": "Dites-nous ce que vous cherchez en quelques clics. Nous examinerons notre écurie et notre réseau international, et vous répondrons avec une présélection personnelle. Sans obligation — avec une véritable expertise.",
    "int.quote": "\"Des conseils honnêtes, le bon cheval pour le bon cavalier. C'est la seule chose qui nous anime.\"",
    "int.step": "Étape 01 — Profil", "int.h3": "Dites-nous ce que vous cherchez.",
    
    "lbl.sex": "Sexe", "opt.stallion": "Étalon", "opt.mare": "Jument", "opt.gelding": "Hongre",
    "lbl.age": "Âge", "opt.2-3": "2-3 ans", "opt.3-4": "3-4 ans", "opt.4-5": "4-5 ans", "opt.6-7": "6-7 ans", "opt.8-9": "8-9 ans", "opt.10-11": "10-11 ans", "opt.12-13": "12-13 ans",
    "lbl.exp": "Niveau d'expérience", "opt.noexp": "Non débourré", "opt.90": "Jusqu'à 90 cm", "opt.110": "Jusqu'à 110 cm", "opt.130": "Jusqu'à 130 cm", "opt.140": "Jusqu'à 140 cm", "opt.150": "150 cm et plus",
    "lbl.color": "Robe préférée", "opt.black": "Noir", "opt.brown": "Bai brun", "opt.white": "Blanc", "opt.chestnut": "Alezan", "opt.bay": "Bai", "opt.grey": "Gris",
    "lbl.budget": "Budget indicatif", "opt.15-30": "15-30 k€", "opt.30-60": "30-60 k€", "opt.60-120": "60-120 k€", "opt.120+": "120 k€ +",
    "lbl.notes": "Remarques ou souhaits spécifiques", "pl.notes": "Parlez-nous de vous, de votre profil de cavalier et de ce que vous cherchez vraiment.",
    "pl.name": "Prénom et nom", "pl.email": "E-mail", "pl.phone": "Téléphone (+...)",
    "lbl.country": "Pays — sélectionner", "opt.be": "Belgique", "opt.nl": "Pays-Bas", "opt.fr": "France", "opt.de": "Allemagne", "opt.us": "États-Unis", "opt.mx": "Mexique", "opt.uk": "Royaume-Uni", "opt.ae": "EAU", "opt.other": "Autre",
    "form.privacy": "Nous ne conservons vos données que pour donner suite à votre demande.", "form.submit": "Envoyer la demande",
    
    "news.eyebrow": "Actualités & mises à jour", "news.title": "Les dernières nouvelles de la piste.", "news.desc": "Résultats, compétitions et actualités de notre écurie et de celles de nos clients.",
    
    "cta.title1": "Prêt à", "cta.title2": "trouver votre cheval?", "cta.desc": "+32 474 444 059 · Maaseik, Belgique · Joignable 7j/7 via WhatsApp.",
    "cta.call": "Appelez-nous", "cta.wa": "WhatsApp",
    "ft.about": "Nous trouvons votre cheval de qualité. Chevaux de sport belges premium, sélectionnés avec soin et livrés dans le monde entier, avec l'attention d'une écurie familiale et l'envergure d'une entreprise internationale.",
    "ft.nav": "Naviguer", "ft.serv": "Services", "ft.contact": "Contact",
    "ft.s1": "Ventes", "ft.s2": "Recherche de votre cheval", "ft.s3": "Formation et hébergement", "ft.s4": "Embryons et poulains", "ft.s5": "Transport mondial",
    "ft.copy": "© 2026 Maarten Driessen Sporthorses — tous droits réservés.", "ft.privacy": "Confidentialité", "ft.cookies": "Cookies", "ft.admin": "Connexion admin"
  },
  de: {
    "nav.horses": "Pferde", "nav.collection": "Kollektion", "nav.references": "Referenzen", "nav.stable": "Stall", "nav.news": "News", "nav.contact": "Kontakt", "nav.findhorse": "Pferd finden",
    "hero.eyebrow": "Belgische Sportpferde · Seit 1995",
    "hero.l1": "Wir finden für Sie", "hero.l2": "Ihr Qualitätspferd.",
    "hero.lede": "Eine sorgfältig ausgewählte Kollektion internationaler Springpferde, vom vielversprechenden Fohlen bis zum turnierreifen Talent. Premium-Qualität, ehrliche Beratung und weltweiter Service aus dem Herzen Belgiens.",
    "hero.cta1": "Kollektion ansehen", "hero.cta2": "Sagen Sie uns, was Sie suchen",
    "meta.horses": "Pferde", "meta.horses.s": "in unserer Datenbank", "meta.refs": "Referenzen", "meta.refs.s": "5* Resultate weltweit", "meta.years": "Erfahrung", "meta.years.s": "Spitzensport & Handel",
    "hor.eyebrow": "Unsere Kollektion", "hor.title": "Springpferde, nach Geburtsjahr.", "hor.desc": "Entdecken Sie unsere außergewöhnliche Auswahl vielversprechender Springpferde. Filtern Sie nach Geburtsjahr.",
    
    "feat.eyebrow": "Ausgewählt", "feat.title": "Unsere Top-Pferde im Rampenlicht.", "feat.desc": "Drei der meistbesprochenen Pferde aus unserer aktuellen Kollektion — international ausgebildet, bereit für den Spitzensport.",
    
    "svc.eyebrow": "Was wir tun", "svc.title": "Ein Haus, das mehr liefert als ein Pferd.", "svc.desc": "Vom Scouting bis zur Ausbildung, von der täglichen Pflege bis zum weltweiten Transport — alles unter einem Dach.",
    "svc.1.t": "Weltweiter Verkauf", "svc.1.d": "Premium-Springpferde für Amateure bis zum 5*-Niveau. Ehrliches Matching zwischen Reiter und Pferd, mit einer internationalen Kundschaft in den USA, Mexiko, der GCC und Europa.",
    "svc.2.t": "Auf der Suche nach Ihrem Pferd", "svc.2.d": "Sagen Sie uns, was Sie suchen, und wir erledigen die Arbeit. Geschlecht, Alter, Erfahrung, Farbe, Budget — wir finden das Pferd, das zu Ihnen passt.",
    "svc.3.t": "Ausbildung & Aufenthalt", "svc.3.d": "Moderne Anlagen, weitläufige Weiden, Innen- und Außenplätze, Führanlage, Lounge. Tägliches Training unter bester Anleitung.",
    "svc.4.t": "Embryonen & Fohlen", "svc.4.d": "Eine exquisite Auswahl an Embryonen aus Top-Mutterlinien — Lorenta, Kayenne vd Broekkant — verfügbar für den Handel oder die eigene Zucht.",
    "svc.5.t": "Weltweiter Transport", "svc.5.d": "Umfassende Betreuung beim Export — Gesundheitszertifikate, Quarantäne, Charterflüge in die USA, nach Lateinamerika, in den Nahen Osten und nach Asien.",
    "svc.6.t": "Lebenslanger Kontakt", "svc.6.d": "Ein Pferd zu verkaufen ist für uns erst der Anfang der Beziehung. Wir bleiben an ihrer Karriere beteiligt und helfen, wo wir können.",
    
    "ref.eyebrow": "Referenzen", "ref.title": "Pferde, die ihre Geschichte weiterschreiben.", "ref.desc": "Eine Auswahl von Pferden, die wir verkauft haben und die nun erfolgreich ihren Weg im internationalen Sport gehen.",
    "ref.btn": "Alle Referenzen ansehen",
    
    "stb.eyebrow": "Unser Zuhause", "stb.title": "Ein Stall, der sich um das kümmert, was er reitet.", "stb.desc": "Innen- und Außenplätze, geräumige Ställe, Paddocks, Führanlage und eine Lounge, in der sich Reiter wie zu Hause fühlen.",
    
    "int.eyebrow": "Anfrage-Modul", "int.title1": "Was können wir", "int.title2": "für Sie tun?", 
    "int.desc": "Sagen Sie uns mit wenigen Klicks, was Sie suchen. Wir prüfen unseren Stall und unser internationales Netzwerk und melden uns mit einer persönlichen Vorauswahl bei Ihnen. Unverbindlich — aber mit echter Expertise.",
    "int.quote": "\"Ehrliche Beratung, das richtige Pferd für den richtigen Reiter. Das ist das Einzige, was uns antreibt.\"",
    "int.step": "Schritt 01 — Profil", "int.h3": "Sagen Sie uns, was Sie suchen.",
    
    "lbl.sex": "Geschlecht", "opt.stallion": "Hengst", "opt.mare": "Stute", "opt.gelding": "Wallach",
    "lbl.age": "Alter", "opt.2-3": "2-3 Jahre", "opt.3-4": "3-4 Jahre", "opt.4-5": "4-5 Jahre", "opt.6-7": "6-7 Jahre", "opt.8-9": "8-9 Jahre", "opt.10-11": "10-11 Jahre", "opt.12-13": "12-13 Jahre",
    "lbl.exp": "Erfahrungsniveau", "opt.noexp": "Nicht angeritten", "opt.90": "Bis 90 cm", "opt.110": "Bis 110 cm", "opt.130": "Bis 130 cm", "opt.140": "Bis 140 cm", "opt.150": "150 cm & höher",
    "lbl.color": "Bevorzugte Farbe", "opt.black": "Rappe", "opt.brown": "Braun", "opt.white": "Schimmel", "opt.chestnut": "Fuchs", "opt.bay": "Bay", "opt.grey": "Grau",
    "lbl.budget": "Indikatives Budget", "opt.15-30": "15-30 k€", "opt.30-60": "30-60 k€", "opt.60-120": "60-120 k€", "opt.120+": "120 k€ +",
    "lbl.notes": "Bemerkungen oder besondere Wünsche", "pl.notes": "Erzählen Sie uns von sich, Ihrem Reiterprofil und was Sie wirklich suchen.",
    "pl.name": "Vorname und Nachname", "pl.email": "E-Mail", "pl.phone": "Telefon (+...)",
    "lbl.country": "Land — auswählen", "opt.be": "Belgien", "opt.nl": "Niederlande", "opt.fr": "Frankreich", "opt.de": "Deutschland", "opt.us": "USA", "opt.mx": "Mexiko", "opt.uk": "Großbritannien", "opt.ae": "VAE", "opt.other": "Andere",
    "form.privacy": "Wir speichern Ihre Daten nur, um Ihre Anfrage zu bearbeiten.", "form.submit": "Anfrage senden",
    
    "news.eyebrow": "News & Updates", "news.title": "Das Neueste vom Platz.", "news.desc": "Ergebnisse, Turniere und Neuigkeiten aus unserem Stall und von unseren Kunden.",
    
    "cta.title1": "Bereit,", "cta.title2": "Ihr Pferd zu finden?", "cta.desc": "+32 474 444 059 · Maaseik, Belgien · 7 Tage/Woche erreichbar über WhatsApp.",
    "cta.call": "Rufen Sie uns an", "cta.wa": "WhatsApp",
    "ft.about": "Wir finden Ihr Qualitätspferd. Premium belgische Sportpferde, handverlesen und weltweit geliefert, mit der Sorgfalt eines Familienbetriebs und der Größe eines internationalen Unternehmens.",
    "ft.nav": "Navigation", "ft.serv": "Dienstleistungen", "ft.contact": "Kontakt",
    "ft.s1": "Verkauf", "ft.s2": "Auf der Suche nach Ihrem Pferd", "ft.s3": "Ausbildung & Aufenthalt", "ft.s4": "Embryonen & Fohlen", "ft.s5": "Weltweiter Transport",
    "ft.copy": "© 2026 Maarten Driessen Sporthorses — alle Rechte vorbehalten.", "ft.privacy": "Datenschutz", "ft.cookies": "Cookies", "ft.admin": "Admin-Login"
  }
};
function setLang(l){
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const k=el.getAttribute('data-i18n');
    if(I18N[l]&&I18N[l][k]) el.innerHTML=I18N[l][k];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>{
    const k=el.getAttribute('data-i18n-placeholder');
    if(I18N[l]&&I18N[l][k]) el.placeholder=I18N[l][k];
  });
  document.querySelectorAll('#langSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));
  document.documentElement.lang=l;
}
document.querySelectorAll('#langSwitch button').forEach(b=>b.addEventListener('click',()=>setLang(b.dataset.lang)));"""

# Replace everything from `const I18N = {` to `document.querySelectorAll('#langSwitch button').forEach(...)`
pattern = re.compile(r'const I18N = \{.*?(?=/\* ---------- HORSES grid ---------- \*/)', re.DOTALL)
html = pattern.sub(new_i18n + '\n\n', html)

with open('index.html', 'w') as f:
    f.write(html)
