import re

# ================================
# UPDATE INDEX.HTML
# ================================
with open('index.html', 'r') as f:
    html = f.read()

# Fix overflow-x
html = html.replace('html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;line-height:1.55}', 
                    'html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;line-height:1.55;overflow-x:hidden;max-width:100vw}')

mobile_css = """
/* MOBILE MENU */
.mobile-menu{position:fixed;inset:0;background:var(--bg);z-index:999;display:flex;flex-direction:column;transform:translateX(100%);transition:transform .4s cubic-bezier(.7,0,.2,1)}
.mobile-menu.open{transform:translateX(0)}
.mm-head{display:flex;justify-content:space-between;align-items:center;padding:18px 28px;border-bottom:1px solid var(--line)}
.mm-close{width:42px;height:42px;border-radius:50%;background:var(--bg-2);color:var(--ink);display:grid;place-items:center;font-size:18px;border:0;cursor:pointer}
.mm-body{padding:40px 28px;flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:40px}
.mm-nav{display:flex;flex-direction:column;gap:24px}
.mm-nav a{font-family:var(--display);font-size:32px;font-weight:400;color:var(--ink);text-decoration:none}
.mm-lang{display:flex;gap:12px;margin-top:auto}
.mm-lang button{padding:8px 16px;border-radius:8px;border:1px solid var(--line);background:var(--bg-2);color:var(--ink-2);font-size:14px;letter-spacing:.1em;transition:.2s;cursor:pointer}
.mm-lang button.active{background:var(--ink);color:var(--bg);border-color:var(--ink)}
"""
if '/* MOBILE MENU */' not in html:
    html = html.replace('/* HERO */', mobile_css + '\n/* HERO */')

mobile_html = """
<!-- MOBILE MENU OVERLAY -->
<div class="mobile-menu" id="mobileMenu">
  <div class="mm-head">
    <a href="#" class="brand" id="mmBrandClose">
      <img src="logo.png" alt="MD Logo" style="height: 42px; width: auto;" />
      <div class="brand-text">
        <strong>Maarten Driessen</strong>
        <span>Sporthorses · Belgium</span>
      </div>
    </a>
    <button class="mm-close" id="mmClose">✕</button>
  </div>
  <div class="mm-body">
    <nav class="mm-nav">
      <a href="#horses" data-i18n="nav.horses" class="mm-link">Paarden</a>
      <a href="#featured" data-i18n="nav.collection" class="mm-link">Collectie</a>
      <a href="#references" data-i18n="nav.references" class="mm-link">Referenties</a>
      <a href="#stable" data-i18n="nav.stable" class="mm-link">Stables</a>
      <a href="#news" data-i18n="nav.news" class="mm-link">News</a>
      <a href="#contact" data-i18n="nav.contact" class="mm-link">Contact</a>
      <a href="admin.html" data-i18n="ft.admin" class="mm-link" style="color:var(--sand-deep);margin-top:12px">Admin login</a>
    </nav>
    <div class="mm-lang" id="mmLangSwitch">
      <button data-lang="nl" class="active">NL</button>
      <button data-lang="en">EN</button>
      <button data-lang="fr">FR</button>
      <button data-lang="de">DE</button>
    </div>
  </div>
</div>
"""
if 'id="mobileMenu"' not in html:
    html = html.replace('<body>', '<body>\n' + mobile_html)

mobile_js = """
// Mobile menu logic
const mm = document.getElementById('mobileMenu');
document.querySelector('.menu-toggle').addEventListener('click', () => mm.classList.add('open'));
document.getElementById('mmClose').addEventListener('click', () => mm.classList.remove('open'));
document.getElementById('mmBrandClose').addEventListener('click', () => mm.classList.remove('open'));
document.querySelectorAll('.mm-link').forEach(l => l.addEventListener('click', () => mm.classList.remove('open')));
document.querySelectorAll('#mmLangSwitch button').forEach(b => {
  b.addEventListener('click', () => {
    setLang(b.dataset.lang);
  });
});
"""
if 'const mm = document.getElementById' not in html:
    html = html.replace('</script>', mobile_js + '\n</script>')

lang_update = """  document.querySelectorAll('#langSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));
  document.querySelectorAll('#mmLangSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));"""
if '#mmLangSwitch button' not in html:
    html = html.replace("document.querySelectorAll('#langSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));", lang_update)

with open('index.html', 'w') as f:
    f.write(html)

# ================================
# UPDATE ADMIN.HTML
# ================================
with open('admin.html', 'r') as f:
    html = f.read()

# Fix overflow-x
html = html.replace('html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;-webkit-font-smoothing:antialiased}', 
                    'html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;-webkit-font-smoothing:antialiased;overflow-x:hidden;max-width:100vw}')

# Add hamburger button to admin topnav
hamburger_html = """      <button id="adminMenuToggle" style="display:none;font-size:24px;color:var(--ink);margin-right:12px;background:none;border:none">≡</button>\n      <div class="crumbs">"""
if 'id="adminMenuToggle"' not in html:
    html = html.replace('<div class="crumbs">', hamburger_html)

# Add CSS for hamburger and mobile adjustments
admin_css = """
  #adminMenuToggle{display:block !important;}
  .actions{justify-content:flex-start;}
  .search input{width:100% !important;}
  .search{width:100%;margin-bottom:12px}
  .status-pill{margin-bottom:12px}
"""
if '#adminMenuToggle{display:block' not in html:
    html = html.replace('aside.open{left:0}', 'aside.open{left:0}\n' + admin_css)

# Add mobile overlay for sidebar
overlay_html = '<div id="adminOverlay" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:50;"></div>\n  <aside>'
if 'id="adminOverlay"' not in html:
    html = html.replace('<aside>', overlay_html)

# Add JS for admin sidebar toggle
admin_js = """
const adToggle = document.getElementById('adminMenuToggle');
const adAside = document.querySelector('aside');
const adOverlay = document.getElementById('adminOverlay');
if(adToggle){
  adToggle.addEventListener('click', () => {
    adAside.classList.add('open');
    adOverlay.style.display = 'block';
  });
  adOverlay.addEventListener('click', () => {
    adAside.classList.remove('open');
    adOverlay.style.display = 'none';
  });
  document.querySelectorAll('.nav-item').forEach(n => {
    n.addEventListener('click', () => {
      adAside.classList.remove('open');
      adOverlay.style.display = 'none';
    });
  });
}
"""
if 'const adToggle = document.getElementById' not in html:
    html = html.replace('</script>', admin_js + '\n</script>')

with open('admin.html', 'w') as f:
    f.write(html)
