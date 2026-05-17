import re
import json

with open('index.html', 'r') as f:
    html = f.read()

replacements = {
    '<span class="eyebrow">Featured</span>': '<span class="eyebrow" data-i18n="feat.eyebrow">Featured</span>',
    '<h2>Onze toppers, in de spotlight.</h2>': '<h2 data-i18n="feat.title">Onze toppers, in de spotlight.</h2>',
    '<div class="right">Drie van de meest besproken paarden uit onze huidige collectie — internationaal opgeleid, klaar voor topsport.</div>': '<div class="right" data-i18n="feat.desc">Drie van de meest besproken paarden uit onze huidige collectie — internationaal opgeleid, klaar voor topsport.</div>',
    
    '<span class="eyebrow">What we do</span>': '<span class="eyebrow" data-i18n="svc.eyebrow">What we do</span>',
    '<h2>Een huis dat meer levert dan een paard.</h2>': '<h2 data-i18n="svc.title">Een huis dat meer levert dan een paard.</h2>',
    '<div class="right" style="color:rgba(239,233,220,.7)">Van opsporen tot opleiden, van het stalleven tot het wereldwijde transport — alles onder één dak.</div>': '<div class="right" style="color:rgba(239,233,220,.7)" data-i18n="svc.desc">Van opsporen tot opleiden, van het stalleven tot het wereldwijde transport — alles onder één dak.</div>',
    
    '<h3>Wereldwijde verkoop</h3>': '<h3 data-i18n="svc.1.t">Wereldwijde verkoop</h3>',
    '<p>Premium springpaarden voor amateurs tot 5* niveau. Eerlijke matching tussen ruiter en paard, met internationale klantenkring in USA, Mexico, GCC en Europa.</p>': '<p data-i18n="svc.1.d">Premium springpaarden voor amateurs tot 5* niveau. Eerlijke matching tussen ruiter en paard, met internationale klantenkring in USA, Mexico, GCC en Europa.</p>',
    
    '<h3>Op zoek naar jouw paard</h3>': '<h3 data-i18n="svc.2.t">Op zoek naar jouw paard</h3>',
    '<p>Vertel ons wat je zoekt en wij doen het werk. Sexe, leeftijd, ervaring, kleur, budget — wij vinden het paard dat bij jou past, ook als het niet in onze stal staat.</p>': '<p data-i18n="svc.2.d">Vertel ons wat je zoekt en wij doen het werk. Sexe, leeftijd, ervaring, kleur, budget — wij vinden het paard dat bij jou past, ook als het niet in onze stal staat.</p>',

    '<h3>Opleiding &amp; verblijf</h3>': '<h3 data-i18n="svc.3.t">Opleiding &amp; verblijf</h3>',
    '<p>Moderne faciliteiten, ruime weides, indoor &amp; outdoor pistes, walker, lounge. Dagelijkse training onder de beste begeleiding.</p>': '<p data-i18n="svc.3.d">Moderne faciliteiten, ruime weides, indoor &amp; outdoor pistes, walker, lounge. Dagelijkse training onder de beste begeleiding.</p>',

    '<h3>Embryo\'s &amp; foals</h3>': '<h3 data-i18n="svc.4.t">Embryo\'s &amp; foals</h3>',
    '<p>Een uitgelezen selectie embryo\'s uit topmoederlijnen — Lorenta, Kayenne vd Broekkant — beschikbaar voor handel of eigen opfok.</p>': '<p data-i18n="svc.4.d">Een uitgelezen selectie embryo\'s uit topmoederlijnen — Lorenta, Kayenne vd Broekkant — beschikbaar voor handel of eigen opfok.</p>',

    '<h3>Wereldwijd transport</h3>': '<h3 data-i18n="svc.5.t">Wereldwijd transport</h3>',
    '<p>Volledige begeleiding bij export — gezondheidspapieren, quarantaine, charter naar USA, Latijns-Amerika, Midden-Oosten en Azië.</p>': '<p data-i18n="svc.5.d">Volledige begeleiding bij export — gezondheidspapieren, quarantaine, charter naar USA, Latijns-Amerika, Midden-Oosten en Azië.</p>',

    '<h3>Levenslang contact</h3>': '<h3 data-i18n="svc.6.t">Levenslang contact</h3>',
    '<p>Een paard verkopen is voor ons het begin van de relatie. We blijven betrokken bij de carrière en helpen waar we kunnen.</p>': '<p data-i18n="svc.6.d">Een paard verkopen is voor ons het begin van de relatie. We blijven betrokken bij de carrière en helpen waar we kunnen.</p>',
    
    '<span class="eyebrow">References</span>': '<span class="eyebrow" data-i18n="ref.eyebrow">References</span>',
    '<h2>Paarden die hun verhaal verder schrijven.</h2>': '<h2 data-i18n="ref.title">Paarden die hun verhaal verder schrijven.</h2>',
    '<div class="right">Een selectie van paarden die wij verkochten en die intussen succesvol hun weg vinden in de internationale ring.</div>': '<div class="right" data-i18n="ref.desc">Een selectie van paarden die wij verkochten en die intussen succesvol hun weg vinden in de internationale ring.</div>',
    '<a class="btn btn-ghost" href="#">Bekijk alle referenties</a>': '<a class="btn btn-ghost" href="#" data-i18n="ref.btn">Bekijk alle referenties</a>',
    
    '<span class="eyebrow">Our home</span>': '<span class="eyebrow" data-i18n="stb.eyebrow">Our home</span>',
    '<h2>Een stal die zorgt voor wat ze rijdt.</h2>': '<h2 data-i18n="stb.title">Een stal die zorgt voor wat ze rijdt.</h2>',
    '<div class="right">Indoor &amp; outdoor pistes, ruime stallen, paddocks, walker en een lounge die ruiters het gevoel geeft thuis te komen.</div>': '<div class="right" data-i18n="stb.desc">Indoor &amp; outdoor pistes, ruime stallen, paddocks, walker en een lounge die ruiters het gevoel geeft thuis te komen.</div>',

    '<span class="eyebrow">Intake module</span>': '<span class="eyebrow" data-i18n="int.eyebrow">Intake module</span>',
    '<h2 style="margin-top:22px">What can we<br/><em>do 4 you?</em></h2>': '<h2 style="margin-top:22px"><span data-i18n="int.title1">What can we</span><br/><em data-i18n="int.title2">do 4 you?</em></h2>',
    '<p style="margin-top:24px;font-size:16px;max-width:420px">\n        Vertel ons in een paar klikken wat je zoekt. We bekijken onze stal én ons internationale netwerk,\n        en komen terug met een persoonlijke shortlist. Geen verplichtingen — wél echte expertise.\n      </p>': '<p style="margin-top:24px;font-size:16px;max-width:420px" data-i18n="int.desc">\n        Vertel ons in een paar klikken wat je zoekt. We bekijken onze stal én ons internationale netwerk,\n        en komen terug met een persoonlijke shortlist. Geen verplichtingen — wél echte expertise.\n      </p>',
    '"Eerlijk advies, het juiste paard voor de juiste ruiter. Dat is het enige dat ons drijft."': '<span data-i18n="int.quote">"Eerlijk advies, het juiste paard voor de juiste ruiter. Dat is het enige dat ons drijft."</span>',
    '<div class="step">Step 01 — Profiel</div>': '<div class="step" data-i18n="int.step">Step 01 — Profiel</div>',
    '<h3 style="margin-bottom:30px">Vertel ons wat je zoekt.</h3>': '<h3 style="margin-bottom:30px" data-i18n="int.h3">Vertel ons wat je zoekt.</h3>',
    
    '<label>Geslacht</label>': '<label data-i18n="lbl.sex">Geslacht</label>',
    '<span class="opt">Hengst</span>': '<span class="opt" data-i18n="opt.stallion">Hengst</span>',
    '<span class="opt">Merrie</span>': '<span class="opt" data-i18n="opt.mare">Merrie</span>',
    '<span class="opt">Ruin</span>': '<span class="opt" data-i18n="opt.gelding">Ruin</span>',

    '<label>Leeftijd</label>': '<label data-i18n="lbl.age">Leeftijd</label>',
    '<span class="opt">2-3 jaar</span>': '<span class="opt" data-i18n="opt.2-3">2-3 jaar</span>',
    '<span class="opt">3-4 jaar</span>': '<span class="opt" data-i18n="opt.3-4">3-4 jaar</span>',
    '<span class="opt">4-5 jaar</span>': '<span class="opt" data-i18n="opt.4-5">4-5 jaar</span>',
    '<span class="opt">6-7 jaar</span>': '<span class="opt" data-i18n="opt.6-7">6-7 jaar</span>',
    '<span class="opt">8-9 jaar</span>': '<span class="opt" data-i18n="opt.8-9">8-9 jaar</span>',
    '<span class="opt">10-11 jaar</span>': '<span class="opt" data-i18n="opt.10-11">10-11 jaar</span>',
    '<span class="opt">12-13 jaar</span>': '<span class="opt" data-i18n="opt.12-13">12-13 jaar</span>',

    '<label>Ervaringsniveau</label>': '<label data-i18n="lbl.exp">Ervaringsniveau</label>',
    '<span class="opt">Niet beleerd</span>': '<span class="opt" data-i18n="opt.noexp">Niet beleerd</span>',
    '<span class="opt">Tot 90 cm</span>': '<span class="opt" data-i18n="opt.90">Tot 90 cm</span>',
    '<span class="opt">Tot 110 cm</span>': '<span class="opt" data-i18n="opt.110">Tot 110 cm</span>',
    '<span class="opt">Tot 130 cm</span>': '<span class="opt" data-i18n="opt.130">Tot 130 cm</span>',
    '<span class="opt">Tot 140 cm</span>': '<span class="opt" data-i18n="opt.140">Tot 140 cm</span>',
    '<span class="opt">150 cm &amp; hoger</span>': '<span class="opt" data-i18n="opt.150">150 cm &amp; hoger</span>',
    
    '<label>Voorkeurskleur</label>': '<label data-i18n="lbl.color">Voorkeurskleur</label>',
    '<span class="opt">Zwart</span>': '<span class="opt" data-i18n="opt.black">Zwart</span>',
    '<span class="opt">Bruin</span>': '<span class="opt" data-i18n="opt.brown">Bruin</span>',
    '<span class="opt">Wit</span>': '<span class="opt" data-i18n="opt.white">Wit</span>',
    '<span class="opt">Vos</span>': '<span class="opt" data-i18n="opt.chestnut">Vos</span>',
    '<span class="opt">Bay</span>': '<span class="opt" data-i18n="opt.bay">Bay</span>',
    '<span class="opt">Schimmel</span>': '<span class="opt" data-i18n="opt.grey">Schimmel</span>',

    '<label>Indicatief budget</label>': '<label data-i18n="lbl.budget">Indicatief budget</label>',
    '<span class="opt">€ 15-30k</span>': '<span class="opt" data-i18n="opt.15-30">€ 15-30k</span>',
    '<span class="opt">€ 30-60k</span>': '<span class="opt" data-i18n="opt.30-60">€ 30-60k</span>',
    '<span class="opt">€ 60-120k</span>': '<span class="opt" data-i18n="opt.60-120">€ 60-120k</span>',
    '<span class="opt">€ 120k +</span>': '<span class="opt" data-i18n="opt.120+">€ 120k +</span>',

    '<label>Opmerkingen of specifieke wensen</label>': '<label data-i18n="lbl.notes">Opmerkingen of specifieke wensen</label>',
    '<textarea class="input" rows="3" placeholder="Vertel ons over jezelf, je ruiterprofiel en wat je écht zoekt."></textarea>': '<textarea class="input" rows="3" data-i18n-placeholder="pl.notes" placeholder="Vertel ons over jezelf, je ruiterprofiel en wat je écht zoekt."></textarea>',
    '<input class="input" placeholder="Voornaam en naam" required>': '<input class="input" placeholder="Voornaam en naam" data-i18n-placeholder="pl.name" required>',
    '<input class="input" placeholder="E-mail" type="email" required>': '<input class="input" placeholder="E-mail" data-i18n-placeholder="pl.email" type="email" required>',
    '<input class="input" placeholder="Telefoon (+...)" required>': '<input class="input" placeholder="Telefoon (+...)" data-i18n-placeholder="pl.phone" required>',

    '<option>Land — selecteer</option>': '<option data-i18n="lbl.country">Land — selecteer</option>',
    '<option>België</option>': '<option data-i18n="opt.be">België</option>',
    '<option>Nederland</option>': '<option data-i18n="opt.nl">Nederland</option>',
    '<option>Frankrijk</option>': '<option data-i18n="opt.fr">Frankrijk</option>',
    '<option>Duitsland</option>': '<option data-i18n="opt.de">Duitsland</option>',
    '<option>USA</option>': '<option data-i18n="opt.us">USA</option>',
    '<option>Mexico</option>': '<option data-i18n="opt.mx">Mexico</option>',
    '<option>UK</option>': '<option data-i18n="opt.uk">UK</option>',
    '<option>UAE</option>': '<option data-i18n="opt.ae">UAE</option>',
    '<option>Andere</option>': '<option data-i18n="opt.other">Andere</option>',

    '<small>We bewaren je gegevens enkel om jouw vraag op te volgen.</small>': '<small data-i18n="form.privacy">We bewaren je gegevens enkel om jouw vraag op te volgen.</small>',
    '<button type="submit" class="btn btn-primary">Verstuur aanvraag</button>': '<button type="submit" class="btn btn-primary" data-i18n="form.submit">Verstuur aanvraag</button>',

    '<span class="eyebrow">News &amp; updates</span>': '<span class="eyebrow" data-i18n="news.eyebrow">News &amp; updates</span>',
    '<h2>Het laatste van de piste.</h2>': '<h2 data-i18n="news.title">Het laatste van de piste.</h2>',
    '<div class="right">Resultaten, wedstrijden en moves uit onze stal en die van onze klanten.</div>': '<div class="right" data-i18n="news.desc">Resultaten, wedstrijden en moves uit onze stal en die van onze klanten.</div>',

    '<h2>Klaar om<br/><em>jouw paard te vinden?</em></h2>': '<h2><span data-i18n="cta.title1">Klaar om</span><br/><em data-i18n="cta.title2">jouw paard te vinden?</em></h2>',
    '<p style="color:rgba(239,233,220,.7);margin:18px 0 0;max-width:520px">+32 474 444 059 · Maaseik, België · 7d/7 bereikbaar via WhatsApp.</p>': '<p style="color:rgba(239,233,220,.7);margin:18px 0 0;max-width:520px" data-i18n="cta.desc">+32 474 444 059 · Maaseik, België · 7d/7 bereikbaar via WhatsApp.</p>',
    '<a class="btn btn-sand" href="tel:+32474444059">Bel ons</a>': '<a class="btn btn-sand" href="tel:+32474444059" data-i18n="cta.call">Bel ons</a>',
    '<a class="btn btn-ghost" style="color:#fff;border-color:#fff" href="https://api.whatsapp.com/send?phone=%2B32474444059">WhatsApp</a>': '<a class="btn btn-ghost" style="color:#fff;border-color:#fff" href="https://api.whatsapp.com/send?phone=%2B32474444059" data-i18n="cta.wa">WhatsApp</a>',
    
    '<p>We find you your quality horse. Premium Belgian sporthorses,\n          hand-picked en wereldwijd geleverd, met de zorg van een familiestal en de schaal van een internationaal bedrijf.</p>': '<p data-i18n="ft.about">We find you your quality horse. Premium Belgian sporthorses,\n          hand-picked en wereldwijd geleverd, met de zorg van een familiestal en de schaal van een internationaal bedrijf.</p>',
    
    '<h5>Navigeer</h5>': '<h5 data-i18n="ft.nav">Navigeer</h5>',
    '<h5>Diensten</h5>': '<h5 data-i18n="ft.serv">Diensten</h5>',
    '<h5>Contact</h5>': '<h5 data-i18n="ft.contact">Contact</h5>',
    
    '<li><a href="#">Verkoop</a></li>': '<li><a href="#" data-i18n="ft.s1">Verkoop</a></li>',
    '<li><a href="#">Op zoek naar jouw paard</a></li>': '<li><a href="#" data-i18n="ft.s2">Op zoek naar jouw paard</a></li>',
    '<li><a href="#">Opleiding &amp; verblijf</a></li>': '<li><a href="#" data-i18n="ft.s3">Opleiding &amp; verblijf</a></li>',
    '<li><a href="#">Embryo\'s &amp; foals</a></li>': '<li><a href="#" data-i18n="ft.s4">Embryo\'s &amp; foals</a></li>',
    '<li><a href="#">Wereldwijd transport</a></li>': '<li><a href="#" data-i18n="ft.s5">Wereldwijd transport</a></li>',
    
    '<div>© 2026 Maarten Driessen Sporthorses — alle rechten voorbehouden.</div>': '<div data-i18n="ft.copy">© 2026 Maarten Driessen Sporthorses — alle rechten voorbehouden.</div>',
    '<a href="#">Privacy</a>': '<a href="#" data-i18n="ft.privacy">Privacy</a>',
    '<a href="#">Cookies</a>': '<a href="#" data-i18n="ft.cookies">Cookies</a>',
    '<a href="admin.html">Admin login</a>': '<a href="admin.html" data-i18n="ft.admin">Admin login</a>'
}

for k, v in replacements.items():
    html = html.replace(k, v)

with open('index.html', 'w') as f:
    f.write(html)
