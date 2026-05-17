import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the nav CTA in HTML to add mobile-header-actions
mobile_actions_html = """
    <div class="mobile-header-actions">
      <a href="https://api.whatsapp.com/send?phone=%2B32474444059" class="icn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg></a>
      <a href="mailto:info@maartendriessen.be" class="icn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg></a>
      <a href="tel:+32474444059" class="icn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg></a>
      
      <span class="sep">|</span>
      
      <div class="lang-switch" id="langSwitchMobile">
        <button data-lang="nl" class="active">NL</button>
        <button data-lang="en">EN</button>
        <button data-lang="fr">FR</button>
        <button data-lang="de">DE</button>
      </div>
    </div>
  </div>
</header>
"""
if '<div class="mobile-header-actions">' not in html:
    html = html.replace('  </div>\n</header>', mobile_actions_html)

# 2. Add the CSS for mobile header and centering
mobile_css_fixes = """
.mobile-header-actions { display: none; }
@media (max-width: 740px) {
  .topbar { display: none; }
  .nav { flex-direction: column; gap: 14px; padding: 14px 0 18px; position: relative; }
  .brand { margin: 0 auto; }
  .nav-cta .btn { display: none; }
  .nav-cta { position: absolute; top: 14px; left: 18px; margin: 0; }
  
  .mobile-header-actions {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    width: 100%;
    margin-top: 4px;
  }
  .mobile-header-actions .icn {
    color: var(--ink);
    opacity: 0.85;
    display: grid;
    place-items: center;
  }
  .mobile-header-actions .sep { opacity: 0.2; color: var(--ink); }
  .mobile-header-actions .lang-switch button {
    color: var(--ink);
    border: 1px solid var(--line);
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 11px;
    margin: 0 2px;
    background: transparent;
  }
  .mobile-header-actions .lang-switch button.active {
    background: var(--ink);
    color: var(--bg);
    border-color: var(--ink);
  }

  /* Centering Hero */
  .hero-grid { text-align: center; justify-items: center; padding: 30px 0 50px; }
  .hero .eyebrow { margin: 0 auto; justify-content: center; }
  .hero h1 { font-size: 44px; margin-top: 16px !important; }
  .hero .lede { margin: 18px auto 32px; max-width: 90%; }
  .hero-meta { justify-content: center; gap: 24px; text-align: center; margin-top: 40px; padding-top: 24px; flex-wrap: wrap; }
}
"""

# inject CSS right before </style>
if '.mobile-header-actions { display: none; }' not in html:
    html = html.replace('</style>', mobile_css_fixes + '\n</style>')

# 3. Make JS update langSwitchMobile too
lang_update = """  document.querySelectorAll('#langSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));
  document.querySelectorAll('#mmLangSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));
  document.querySelectorAll('#langSwitchMobile button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));"""
if '#langSwitchMobile button' not in html:
    html = html.replace("  document.querySelectorAll('#langSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));\n  document.querySelectorAll('#mmLangSwitch button').forEach(b=>b.classList.toggle('active',b.dataset.lang===l));", lang_update)

# Add event listeners for langSwitchMobile
js_listeners = """
document.querySelectorAll('#langSwitchMobile button').forEach(b => {
  b.addEventListener('click', () => {
    setLang(b.dataset.lang);
  });
});
"""
if '#langSwitchMobile button' not in html.split('// Mobile menu logic')[1]:
    html = html.replace('// Mobile menu logic', js_listeners + '\n// Mobile menu logic')

with open('index.html', 'w') as f:
    f.write(html)
