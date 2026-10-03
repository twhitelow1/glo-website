/* GLO shared behaviour: gentle scroll reveals. Content is fully visible without JS. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('glo-js');
  var skip = '.glo-split-hero, .glo-mobile-menu, .glo-footer, .glo-marquee, [data-cond]';
  var targets = document.querySelectorAll('.glo-container, .cat-container, .mem-container, .tv-container, .glo-band-copy');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  Array.prototype.forEach.call(targets, function (el) {
    if (el.closest(skip) || el.getBoundingClientRect().top < window.innerHeight * 0.9) return;
    el.classList.add('glo-reveal');
    io.observe(el);
  });
})();

/* Cherry floating payment estimator on every page except /financing (which has the full calculator).
   Sits above the mobile Book/Call bar on phones and tablets. */
(function () {
  if (/^\/financing(\.html)?\/?$/.test(location.pathname)) return;
  var mobile = window.matchMedia && window.matchMedia('(max-width: 900px)').matches;
  var holder = document.createElement('div');
  holder.id = 'floatingEstimator';
  document.body.appendChild(holder);
  (function (w, d, s, o, f, js, fjs) {
    w[o] = w[o] || function () { (w[o].q = w[o].q || []).push(arguments); };
    (js = d.createElement(s)), (fjs = d.getElementsByTagName(s)[0]);
    js.id = o; js.src = f; js.async = 1;
    fjs.parentNode.insertBefore(js, fjs);
  })(window, document, 'script', '_hw', 'https://files.withcherry.com/widgets/widget.js');
  window._hw('init', {
    debug: false,
    variables: {
      slug: 'glo-aesthetics-wellness-lounge',
      name: 'GLO Aesthetics + Wellness Lounge',
      images: [26],
      customLogo: '',
      defaultPurchaseAmount: 750,
      customImage: '',
      imageCategory: 'medspa',
      language: 'en'
    },
    styles: {
      primaryColor: '#B8894F',
      secondaryColor: '#B8894F10',
      fontFamily: 'Montserrat',
      headerFontFamily: 'Montserrat',
      floatingEstimator: {
        position: 'bottom-right',
        offset: { x: mobile ? '8px' : '16px', y: mobile ? '80px' : '16px' },
        zIndex: 9999,
        ctaFontFamily: 'Montserrat',
        bodyFontFamily: 'Montserrat',
        ctaColor: '#B8894F',
        ctaTextColor: '#FFFFFF'
      }
    }
  }, ['floatingEstimator']);
})();
