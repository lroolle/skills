'use strict';

// Page-local contents. The primary nav is plain HTML and never depends on JS.
const tocHost = document.querySelector('[data-page-toc]');
const tocAside = tocHost && tocHost.closest('.page-toc');
const pageHeadings = [...document.querySelectorAll('main > section > h2[id]')];

if (tocHost && tocAside && pageHeadings.length >= 3) {
  for (const heading of pageHeadings) {
    const link = document.createElement('a');
    link.href = '#' + heading.id;
    link.textContent = heading.textContent;
    tocHost.appendChild(link);
  }
  tocAside.classList.add('is-ready');

  if ('IntersectionObserver' in window) {
    const links = [...tocHost.querySelectorAll('a')];
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        for (const link of links) link.classList.remove('active');
        const current = links.find((link) =>
          link.getAttribute('href') === '#' + entry.target.id);
        if (current) current.classList.add('active');
      }
    }, { rootMargin: '-15% 0px -68% 0px' });
    for (const heading of pageHeadings) observer.observe(heading);
  }
}

addEventListener('beforeprint', () => {
  document.querySelectorAll('details:not([open])').forEach((details) => {
    details.dataset.printOpened = '';
    details.open = true;
  });
});

addEventListener('afterprint', () => {
  document.querySelectorAll('details[data-print-opened]').forEach((details) => {
    details.open = false;
    delete details.dataset.printOpened;
  });
});
