(function () {
  var REPO = 'IAmiGOI/Module-Engine';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // mobile nav
  var nav = $('.nav'), bg = $('.burger');
  if (bg) bg.addEventListener('click', function () { nav.classList.toggle('open'); });

  // latest release -> every .dl-link points straight at the release zip
  fetch('https://api.github.com/repos/' + REPO + '/releases/latest', { headers: { Accept: 'application/vnd.github+json' } })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (rel) {
      if (!rel) return;
      var asset = (rel.assets || []).filter(function (a) { return /\.zip$/i.test(a.name); })[0];
      $$('.dl-link').forEach(function (a) { a.href = asset ? asset.browser_download_url : rel.html_url; });
      $$('.dl-version').forEach(function (e) { e.textContent = rel.tag_name || rel.name; });
      $$('.dl-meta').forEach(function (e) {
        var d = new Date(rel.published_at);
        var size = asset ? ' · ' + (asset.size / 1048576).toFixed(1) + ' MB' : '';
        e.textContent = (rel.tag_name || '') + ' · ' + d.toLocaleDateString('en', { year: 'numeric', month: 'short', day: 'numeric' }) + size;
      });
    }).catch(function () {});

  // copy buttons
  $$('.copy button').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.parentNode.querySelector('span').textContent;
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () {
        b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1400);
      }).catch(function () {});
    });
  });

  // reveal on scroll
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .12 });
    $$('.rv').forEach(function (e) { io.observe(e); });
  } else { $$('.rv').forEach(function (e) { e.classList.add('in'); }); }

  // docs: search over the prebuilt index
  var inp = $('.search'), res = $('.results');
  if (inp && res) {
    var idx = null, base = inp.getAttribute('data-base') || '';
    var load = function () { return idx ? Promise.resolve(idx) : fetch(base + 'search-index.json').then(function (r) { return r.json(); }).then(function (j) { return (idx = j); }); };
    inp.addEventListener('input', function () {
      var q = inp.value.trim().toLowerCase();
      var nav = $('.side-nav');
      if (!q) { res.style.display = 'none'; if (nav) nav.style.display = ''; return; }
      load().then(function (d) {
        var terms = q.split(/\s+/), out = [];
        d.forEach(function (p) {
          var t = p.title.toLowerCase(), x = p.text.toLowerCase(), s = 0;
          for (var i = 0; i < terms.length; i++) {
            var inT = t.indexOf(terms[i]) >= 0, inX = x.indexOf(terms[i]) >= 0;
            if (!inT && !inX) { s = 0; break; }
            s += (inT ? 10 : 0) + (inX ? 1 : 0);
          }
          if (s) { var k = x.indexOf(terms[0]); out.push({ p: p, s: s, snip: k >= 0 ? '…' + p.text.substr(Math.max(0, k - 30), 90) + '…' : '' }); }
        });
        out.sort(function (a, b) { return b.s - a.s; });
        res.innerHTML = out.length ? out.slice(0, 8).map(function (o) { return '<a href="' + base + o.p.url + '">' + o.p.title.replace(/</g, '&lt;') + '<small>' + o.snip.replace(/</g, '&lt;') + '</small></a>'; }).join('') : '<a style="pointer-events:none">No results</a>';
        res.style.display = 'block'; if (nav) nav.style.display = 'none';
      });
    });
    document.addEventListener('keydown', function (e) { if (e.key === '/' && document.activeElement !== inp && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); inp.focus(); } });
  }

  // docs: on-this-page highlight
  var tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {}; tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('on'); }); var a = map[e.target.id]; if (a) a.classList.add('on'); } });
    }, { rootMargin: '-80px 0px -70% 0px' });
    $$('.article h2[id]').forEach(function (h) { so.observe(h); });
  }
})();
