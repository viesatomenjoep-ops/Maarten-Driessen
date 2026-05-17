with open('admin.html', 'r') as f:
    html = f.read()

# Fix overflow-x
html = html.replace('html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;-webkit-font-smoothing:antialiased}', 
                    'html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;-webkit-font-smoothing:antialiased;overflow-x:hidden;max-width:100vw}')

# Add hamburger button
hamburger_html = """      <button id="adminMenuToggle" style="display:none;font-size:24px;color:var(--ink);margin-right:12px;background:none;border:none">≡</button>\n      <div class="crumbs">"""
html = html.replace('<div class="crumbs">', hamburger_html)

# CSS for hamburger
admin_css = """
  #adminMenuToggle{display:block !important;}
  .actions{justify-content:flex-start;}
  .search input{width:100% !important;}
  .search{width:100%;margin-bottom:12px}
  .status-pill{margin-bottom:12px}
"""
html = html.replace('aside.open{left:0}', 'aside.open{left:0}\n' + admin_css)

# Overlay HTML
overlay_html = '<div id="adminOverlay" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:50;"></div>\n  <aside>'
html = html.replace('<aside>', overlay_html)

# JS logic just before </body>
admin_js = """
<script>
const adToggle = document.getElementById('adminMenuToggle');
const adAside = document.querySelector('aside');
const adOverlay = document.getElementById('adminOverlay');
if(adToggle){
  adToggle.addEventListener('click', () => {
    adAside.classList.add('open');
    adOverlay.style.display = 'block';
    document.body.style.overflow = 'hidden';
  });
  adOverlay.addEventListener('click', () => {
    adAside.classList.remove('open');
    adOverlay.style.display = 'none';
    document.body.style.overflow = '';
  });
  document.querySelectorAll('.nav-item').forEach(n => {
    n.addEventListener('click', () => {
      adAside.classList.remove('open');
      adOverlay.style.display = 'none';
      document.body.style.overflow = '';
    });
  });
}
</script>
</body>
"""
html = html.replace('</body>', admin_js)

with open('admin.html', 'w') as f:
    f.write(html)
