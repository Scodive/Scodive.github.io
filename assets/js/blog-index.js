(() => {
  const root = document.getElementById('blog-index');
  if (!root) return;

  const buttons = [...root.querySelectorAll('[data-blog-lang]')];
  const textNodes = [...root.querySelectorAll('[data-en][data-zh]')];
  const linkNodes = [...root.querySelectorAll('[data-href-en][data-href-zh]')];
  const imgNodes = [...root.querySelectorAll('img[data-src-en][data-src-zh]')];

  function selectLanguage(lang, updateHash = false) {
    const isZh = lang === 'zh';
    root.lang = isZh ? 'zh-CN' : 'en';

    buttons.forEach(button => {
      const active = button.dataset.blogLang === lang;
      button.setAttribute('aria-pressed', String(active));
      button.setAttribute('aria-selected', String(active));
    });

    textNodes.forEach(node => {
      node.textContent = isZh ? node.dataset.zh : node.dataset.en;
    });

    linkNodes.forEach(link => {
      link.setAttribute('href', isZh ? link.dataset.hrefZh : link.dataset.hrefEn);
      if (link.classList.contains('blog-figure-frame')) {
        const titleNode = link.closest('article')?.querySelector('h2 a[data-en][data-zh]');
        if (titleNode) {
          link.setAttribute('aria-label', isZh ? titleNode.dataset.zh : titleNode.dataset.en);
        }
      }
    });

    imgNodes.forEach(img => {
      img.setAttribute('src', isZh ? img.dataset.srcZh : img.dataset.srcEn);
      img.setAttribute('alt', isZh ? img.dataset.altZh : img.dataset.altEn);
    });

    if (updateHash) {
      const nextUrl = isZh ? '#zh' : (window.location.pathname + window.location.search);
      window.history.replaceState(null, '', nextUrl);
    }
  }

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      selectLanguage(button.dataset.blogLang, true);
    });
  });

  window.addEventListener('hashchange', () => {
    selectLanguage(window.location.hash === '#zh' ? 'zh' : 'en', false);
  });

  selectLanguage(window.location.hash === '#zh' ? 'zh' : 'en', false);
})();
