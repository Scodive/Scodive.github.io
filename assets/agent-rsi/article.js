(() => {
  const article = document.getElementById('rsi-essay');
  if (!article) return;
  const buttons = [...article.querySelectorAll('[data-bm-language]')];
  const titles = { en: 'What Is Actually Evolving in a Self-Evolving Agent?', zh: 'Agent 自进化，到底在进化什么？' };
  function selectLanguage(language, updateHash = false) {
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.bmLanguage === language)));
    article.querySelectorAll('.bm-language-content').forEach(panel => { panel.hidden = panel.id !== `bm-content-${language}`; });
    article.lang = language === 'zh' ? 'zh-CN' : 'en';
    document.title = `${titles[language]} | Hengle JIANG`;
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
      for (let parent = target.parentElement; parent && parent !== article; parent = parent.parentElement) {
        if (parent.tagName === 'DETAILS') parent.open = true;
      }
      target.scrollIntoView({ block: 'start' });
    }
  }
  // Keep article anchors below the fixed navigation; the site's generic
  // smooth-scroll offset is too small for headings in this article.
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
  // A normal visit starts in English; a specific translated anchor opens its language.
  selectLanguage('en');
  if (location.hash) followAnchor();
})();
