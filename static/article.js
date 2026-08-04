(() => {
  const copyButton = document.querySelector('[data-copy-page]');

  if (copyButton) {
    copyButton.addEventListener('click', async () => {
      const label = copyButton.querySelector('span');
      const original = copyButton.dataset.label || 'Скопировать ссылку';

      try {
        await navigator.clipboard.writeText(window.location.href);
        if (label) label.textContent = 'Ссылка скопирована';
      } catch {
        const field = document.createElement('textarea');
        field.value = window.location.href;
        field.setAttribute('readonly', '');
        field.style.position = 'fixed';
        field.style.opacity = '0';
        document.body.appendChild(field);
        field.select();
        document.execCommand('copy');
        field.remove();
        if (label) label.textContent = 'Ссылка скопирована';
      }

      window.setTimeout(() => {
        if (label) label.textContent = original;
      }, 1800);
    });
  }

  const tocLinks = Array.from(document.querySelectorAll('.article-toc a[href^="#"]'));
  const headings = tocLinks
    .map((link) => document.getElementById(decodeURIComponent(link.hash.slice(1))))
    .filter(Boolean);

  if (!tocLinks.length || !headings.length || !('IntersectionObserver' in window)) return;

  const setActive = (id) => {
    tocLinks.forEach((link) => {
      const active = decodeURIComponent(link.hash.slice(1)) === id;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };

  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (visible[0]) setActive(visible[0].target.id);
  }, { rootMargin: '-12% 0px -72% 0px', threshold: [0, 1] });

  headings.forEach((heading) => observer.observe(heading));
  setActive(headings[0].id);
})();
