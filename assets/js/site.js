/*
 * site.js — small enhancements on top of Chirpy.
 * Code blocks: a highlight band follows the hovered line (fine pointers only).
 * Section arrival: the heading a reader lands on (shared link, search, TOC)
 * is briefly marked; the look lives in the stylesheet (.is-arrived).
 * Opening a post from a card: only the clicked card's image gets a
 * view-transition-name, so it alone travels into the post's header image.
 * Posts ending in a summary section (The Short Version / TL;DR / Summary)
 * get a "Skip to ..." link under the byline. Wide code blocks get a fade
 * at the edge while there is more to scroll. [data-open-search] opens search.
 * No dependencies.
 */
(function () {
  'use strict';

  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

  /* ------------------------------------------------------------------ */
  /* Code blocks: line hover band                                        */
  /* ------------------------------------------------------------------ */

  function initCodeLines() {
    var blocks = document.querySelectorAll('div[class^="language-"]');

    Array.prototype.forEach.call(blocks, function (block) {
      var pre = block.querySelector('td.rouge-code > pre') || block.querySelector('.highlight pre');
      if (!pre) return;

      var band = document.createElement('span');
      band.className = 'cb-line';
      band.setAttribute('aria-hidden', 'true');
      block.appendChild(band);

      var lineCount = 0;
      var lineHeight = 0;

      function measure() {
        lineHeight = parseFloat(window.getComputedStyle(pre).lineHeight) || 0;
        var text = pre.textContent || '';
        lineCount = text.replace(/\n$/, '').split('\n').length;
        band.style.height = lineHeight + 'px';
      }

      block.addEventListener('pointerenter', function () {
        measure();
      });

      block.addEventListener('pointermove', function (e) {
        if (!lineHeight) return;
        var preRect = pre.getBoundingClientRect();
        var blockRect = block.getBoundingClientRect();
        var idx = Math.floor((e.clientY - preRect.top) / lineHeight);

        if (idx < 0 || idx >= lineCount) {
          block.classList.remove('cb-hover');
          return;
        }

        var top = preRect.top - blockRect.top + idx * lineHeight;
        band.style.transform = 'translateY(' + top.toFixed(1) + 'px)';
        block.classList.add('cb-hover');
      });

      block.addEventListener('pointerleave', function () {
        block.classList.remove('cb-hover');
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* Section arrival mark                                                */
  /* ------------------------------------------------------------------ */
  function initArrival() {
    var last = 0;
    function mark(id) {
      if (!id) return;
      var el;
      try { el = document.getElementById(decodeURIComponent(id)); } catch (e) { return; }
      if (!el || !/^H[2-4]$/.test(el.tagName) || !el.closest('.content')) return;
      last = Date.now();
      el.classList.remove('is-arrived');
      void el.offsetWidth; // restart the animation
      el.classList.add('is-arrived');
      el.addEventListener('animationend', function done(e) {
        if (e.animationName !== 'heading-mark') return;
        el.classList.remove('is-arrived');
        el.removeEventListener('animationend', done);
      });
    }
    window.addEventListener('hashchange', function () {
      if (Date.now() - last > 600) mark(location.hash.slice(1));
    });
    // TOC and in-page links scroll without always changing the hash
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a || a.getAttribute('href').length < 2) return;
      setTimeout(function () { mark(a.getAttribute('href').slice(1)); }, 300);
    });
    if (location.hash) {
      var go = function () { setTimeout(function () { mark(location.hash.slice(1)); }, 150); };
      if (document.readyState === 'complete') go(); else window.addEventListener('load', go, { once: true });
    }
  }

  /* ------------------------------------------------------------------ */
  /* Card -> post image transition (cross-document View Transitions)     */
  /* ------------------------------------------------------------------ */
  function initCardTransition() {
    document.addEventListener('click', function (e) {
      var link = e.target.closest && e.target.closest('.post-card-link, .featured-link');
      if (!link) return;
      Array.prototype.forEach.call(document.querySelectorAll('img[data-vt]'), function (img) {
        img.style.viewTransitionName = '';
      });
      var img = link.querySelector('img[data-vt]');
      if (img) img.style.viewTransitionName = img.getAttribute('data-vt');
    });
  }

  /* ------------------------------------------------------------------ */
  /* Skip-to-summary link under the byline                               */
  /* ------------------------------------------------------------------ */
  function initJumpFix() {
    var row = document.querySelector('article.post .post-byline-row');
    if (!row) return;
    var hs = document.querySelectorAll('article.post .content > h2[id]');
    var target = null;
    for (var i = hs.length - 1; i >= 0; i--) {
      if (/short version|tl;?\s*dr|summary|the fix/i.test(hs[i].textContent)) { target = hs[i]; break; }
    }
    if (!target) return;
    var a = document.createElement('a');
    a.className = 'jump-fix';
    a.href = '#' + target.id;
    var label = target.textContent.replace(/#\s*$/, '').trim();
    a.innerHTML = '<i class="fa-solid fa-arrow-down" aria-hidden="true"></i><span></span>';
    a.querySelector('span').textContent = 'Skip to ' + label;
    row.insertAdjacentElement('afterend', a);
  }

  /* ------------------------------------------------------------------ */
  /* Code blocks: fade the edge while there is more to scroll            */
  /* ------------------------------------------------------------------ */
  function initCodeScroll() {
    Array.prototype.forEach.call(document.querySelectorAll('.content div[class^="language-"]'), function (block) {
      var sc = block.querySelector('.highlight');
      if (!sc) return;
      function update() {
        var more = sc.scrollWidth - sc.clientWidth > 2;
        block.classList.toggle('is-scrollable', more);
        block.classList.toggle('is-scrolled-end', more && sc.scrollLeft + sc.clientWidth >= sc.scrollWidth - 2);
      }
      update();
      sc.addEventListener('scroll', update, { passive: true });
      window.addEventListener('resize', update, { passive: true });
    });
  }

  /* ------------------------------------------------------------------ */
  /* Buttons that open the site search (404 page)                        */
  /* ------------------------------------------------------------------ */
  function initSearchOpeners() {
    var resumeAt = null;
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('[data-open-search]');
      if (b) {
        // the phone topbar scrolls away; jump up to it, come back on cancel
        if (window.scrollY > 0 && b.closest('#toc-bar')) {
          resumeAt = window.scrollY;
          window.scrollTo({ top: 0, behavior: 'instant' });
        }
        var trigger = document.getElementById('search-trigger');
        if (trigger && trigger.offsetParent !== null) trigger.click();
        var input = document.getElementById('search-input');
        if (input) setTimeout(function () { input.focus(); }, 60);
        return;
      }
      if (resumeAt !== null && e.target.closest && e.target.closest('#search-cancel')) {
        var y = resumeAt; resumeAt = null;
        setTimeout(function () { window.scrollTo({ top: y, behavior: 'instant' }); }, 60);
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* Phones: back-to-top hides while scrolling down (it covers text)     */
  /* ------------------------------------------------------------------ */
  function initBackToTop() {
    var btn = document.getElementById('back-to-top');
    if (!btn || !window.matchMedia('(pointer: coarse)').matches) return;
    var lastY = window.scrollY, ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        if (Math.abs(y - lastY) > 6) { btn.classList.toggle('is-tucked', y > lastY); lastY = y; }
        ticking = false;
      });
    }, { passive: true });
  }

  /* ------------------------------------------------------------------ */
  /* Code copy: the button already flips to "Copied", so drop Chirpy's   */
  /* duplicate "Copied!" tooltip beside it                               */
  /* ------------------------------------------------------------------ */
  function initCopyFeedback() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest && e.target.closest('div[class^="language-"] .code-header button');
      if (!btn) return;
      [0, 60].forEach(function (ms) {
        setTimeout(function () {
          var id = btn.getAttribute('aria-describedby');
          var tip = id && document.getElementById(id);
          if (tip && tip.classList.contains('tooltip')) tip.remove();
        }, ms);
      });
    });
  }

  function init() {
    initArrival();
    initCopyFeedback();
    initCardTransition();
    initJumpFix();
    initCodeScroll();
    initSearchOpeners();
    initBackToTop();
    if (!finePointer.matches) return;
    initCodeLines();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
