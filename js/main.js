(function () {
  // Menú en celular
  var btn = document.getElementById('menuBtn'), nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var o = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', o);
    });
  }

  // Filtros por línea (proyectos y publicaciones)
  function filterer(attr, containerId) {
    var box = document.getElementById(containerId);
    if (!box) return null;
    var btns = document.querySelectorAll('button[' + attr + ']');
    function apply(f) {
      btns.forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute(attr) === f ? 'true' : 'false'); });
      Array.prototype.forEach.call(box.children, function (it) {
        it.hidden = !(f === 'all' || (it.dataset.l || '').split(' ').indexOf(f) > -1);
      });
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { apply(b.getAttribute(attr)); }); });
    return apply;
  }
  var fp = filterer('data-f', 'projGrid');
  filterer('data-p', 'pubList');
  // proyectos.html#l1 o #l2 abre la lista ya filtrada
  var h = (location.hash || '').replace('#', '');
  if (fp && (h === 'l1' || h === 'l2')) fp(h);

  // Fotos: si el archivo no existe, se quedan las iniciales
  document.querySelectorAll('.photo img').forEach(function (img) {
    function fail() { img.hidden = true; }
    if (img.complete && img.naturalWidth === 0) fail();
    img.addEventListener('error', fail);
  });

  // Copiar correos
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.dataset.copy;
      var done = function () { b.textContent = 'Copiado'; setTimeout(function () { b.textContent = 'Copiar'; }, 1600); };
      try { navigator.clipboard.writeText(t).then(done, function () { sel(b); }); } catch (e) { sel(b); }
    });
  });
  function sel(b) {
    var c = b.previousElementSibling, r = document.createRange();
    r.selectNodeContents(c);
    var s = getSelection(); s.removeAllRanges(); s.addRange(r);
  }
})();
