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
