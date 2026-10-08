(() => {
  const article = document.getElementById('benchmark-essay');
  if (!article) return;
  const buttons = [...article.querySelectorAll('[data-bm-language]')];
  const titles = { en: 'What Makes a Benchmark Worth Testing?', zh: '怎样设计一个真正有评测价值的 Benchmark？' };
  const originalTitle = document.title;
  function selectLanguage(language, updateHash = false) {
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.bmLanguage === language)));
    article.querySelectorAll('.bm-language-content').forEach(panel => { panel.hidden = panel.id !== `bm-content-${language}`; });
    article.lang = language === 'zh' ? 'zh-CN' : 'en';
    document.title = originalTitle.replace(titles.en, titles[language]);
    if (updateHash && location.hash) {
      const id = decodeURIComponent(location.hash.slice(1));
      const translatedId = id.replace(/-(en|zh)$/, `-${language}`);
      if (document.getElementById(translatedId)) history.replaceState(null, '', `#${translatedId}`);
    }
  }
  buttons.forEach(button => button.addEventListener('click', () => selectLanguage(button.dataset.bmLanguage, true)));
  function followAnchor() {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    const panel = target && target.closest('.bm-language-content');
    if (panel) {
      selectLanguage(panel.id.endsWith('-zh') ? 'zh' : 'en');
      target.scrollIntoView();
    }
  }
  window.addEventListener('hashchange', followAnchor);
  // A normal visit starts in English; a specific translated anchor opens its language.
  selectLanguage('en');
  if (location.hash) followAnchor();
})();
