(() => {
  const article = document.querySelector('[data-blog-article]');
  if (!article) return;

  const panels = {
    en: article.querySelector('#bm-content-en'),
    zh: article.querySelector('#bm-content-zh')
  };
  const buttons = article.querySelectorAll('[data-bm-language]');
  const backLink = article.querySelector('.bm-back-link');
  const blogIndex = backLink.getAttribute('href');
  const footer = document.querySelector('.blog-post-footer');

  function selectLanguage(language) {
    const isZh = language === 'zh';
    article.lang = isZh ? 'zh-CN' : 'en';
    panels.en.hidden = isZh;
    panels.zh.hidden = !isZh;
    document.title = `${panels[language].querySelector('h1').textContent} | ${article.dataset.siteTitle}`;

    buttons.forEach(button => {
      const active = String(button.dataset.bmLanguage === language);
      button.setAttribute('aria-selected', active);
      button.setAttribute('aria-pressed', active);
    });

    backLink.textContent = backLink.dataset[language];
    backLink.setAttribute('href', isZh ? `${blogIndex}#zh` : blogIndex);
    footer?.querySelectorAll('[data-en][data-zh]').forEach(node => {
      node.textContent = node.dataset[language];
    });
    footer?.querySelectorAll('[data-href-en][data-href-zh]').forEach(link => {
      link.setAttribute('href', isZh ? link.dataset.hrefZh : link.dataset.hrefEn);
    });
  }

  function followAnchor() {
    const target = document.getElementById(location.hash.slice(1));
    const isZh = target && panels.zh.contains(target);
    selectLanguage(isZh ? 'zh' : 'en');
    if (target && (panels.en.contains(target) || isZh) && target !== panels.en && target !== panels.zh) {
      target.scrollIntoView({ block: 'start' });
    }
  }

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const language = button.dataset.bmLanguage;
      const counterpart = location.hash.replace(/-(en|zh)$/, `-${language}`);
      const heading = document.getElementById(counterpart.slice(1));
      const hash = heading?.tagName === 'H2' && panels[language].contains(heading)
        ? counterpart
        : (language === 'zh' ? '#bm-content-zh' : '');
      history.replaceState(null, '', hash || location.pathname + location.search);
      selectLanguage(language);
    });
  });

  // Use the heading's scroll margin instead of the site's generic anchor offset.
  article.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const hash = link.getAttribute('href');
    const target = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!target || !article.contains(target)) return;
    event.preventDefault();
    event.stopPropagation();
    history.pushState(null, '', hash);
    followAnchor();
  }, true);

  window.addEventListener('hashchange', followAnchor);
  followAnchor();
})();
