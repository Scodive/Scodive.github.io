(() => {
  const article = document.getElementById('migration-essay');
  if (!article) return;

  const buttons = [...article.querySelectorAll('[data-bm-language]')];
  const footer = document.querySelector('.blog-post-footer');
  const titles = {
    en: 'When the Model Changes, What Happens to the Agent?',
    zh: '模型换了，Agent 为什么变了？'
  };

  function syncSharedControls(language) {
    const isZh = language === 'zh';
    const backLink = article.querySelector('.bm-back-link');
    if (backLink) {
      backLink.textContent = isZh ? backLink.dataset.zh : backLink.dataset.en;
      const baseHref = backLink.getAttribute('href').split('#')[0];
      backLink.setAttribute('href', isZh ? `${baseHref}#zh` : baseHref);
    }
    if (footer) {
      footer.querySelectorAll('[data-en][data-zh]').forEach(el => {
        el.textContent = isZh ? el.dataset.zh : el.dataset.en;
      });
      footer.querySelectorAll('[data-href-en][data-href-zh]').forEach(el => {
        el.setAttribute('href', isZh ? el.dataset.hrefZh : el.dataset.hrefEn);
      });
    }
  }

  function selectLanguage(language, updateHash = false) {
    buttons.forEach(button => {
      const active = button.dataset.bmLanguage === language;
      button.setAttribute('aria-pressed', String(active));
      button.setAttribute('aria-selected', String(active));
    });
    article.querySelectorAll('.bm-language-content').forEach(panel => {
      panel.hidden = panel.id !== `bm-content-${language}`;
    });
    article.lang = language === 'zh' ? 'zh-CN' : 'en';
    document.title = `${titles[language]} | Hengle JIANG`;
    syncSharedControls(language);

    if (updateHash && location.hash) {
      const id = decodeURIComponent(location.hash.slice(1));
      if (id === 'bm-content-en' || id === 'bm-content-zh') {
        history.replaceState(null, '', language === 'zh' ? '#bm-content-zh' : (location.pathname + location.search));
      } else {
        const translatedId = id.replace(/-(en|zh)$/, `-${language}`);
        if (document.getElementById(translatedId)) history.replaceState(null, '', `#${translatedId}`);
      }
    }
  }

  buttons.forEach(button => button.addEventListener('click', () => selectLanguage(button.dataset.bmLanguage, true)));

  function followAnchor() {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    if (id === 'bm-content-zh' || id === 'bm-content-en') {
      selectLanguage(id === 'bm-content-zh' ? 'zh' : 'en');
      return;
    }
    const target = document.getElementById(id);
    const panel = target && target.closest('.bm-language-content');
    if (panel) {
      selectLanguage(panel.id.endsWith('-zh') ? 'zh' : 'en');
      target.scrollIntoView({ block: 'start' });
    }
  }

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
  selectLanguage('en');
  if (location.hash) followAnchor();
})();
