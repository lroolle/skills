'use strict';

/* DIAGRAM_VIEWER_START */
const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

function makeElement(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

const diagramStates = [];
let fullscreenState = null;

function setDiagramZoom(state, nextZoom, resetPosition = false) {
  const viewport = state.viewport;
  const centerX = state.pendingCenter
    ? state.pendingCenter.x
    : (viewport.scrollLeft + viewport.clientWidth / 2) /
      Math.max(viewport.scrollWidth, 1);
  const centerY = state.pendingCenter
    ? state.pendingCenter.y
    : (viewport.scrollTop + viewport.clientHeight / 2) /
      Math.max(viewport.scrollHeight, 1);

  if (state.zoomFrame) cancelAnimationFrame(state.zoomFrame);
  state.pendingCenter = resetPosition ? null : { x: centerX, y: centerY };

  state.zoom = clamp(Math.round(nextZoom / 25) * 25, 50, 500);
  state.range.value = String(state.zoom);
  state.output.value = state.zoom + '%';
  state.output.textContent = state.zoom + '%';
  state.svg.style.width = state.zoom + '%';
  state.svg.style.maxWidth = 'none';

  state.zoomFrame = requestAnimationFrame(() => {
    if (resetPosition) {
      viewport.scrollTo(0, 0);
    } else {
      viewport.scrollLeft = centerX * viewport.scrollWidth - viewport.clientWidth / 2;
      viewport.scrollTop = centerY * viewport.scrollHeight - viewport.clientHeight / 2;
    }
    state.zoomFrame = 0;
    state.pendingCenter = null;
  });
}

function closeFullscreen(state, restoreFocus = true) {
  if (!state || fullscreenState !== state) return;
  state.figure.classList.remove('is-fullscreen');
  state.fullButton.textContent = 'Full';
  state.fullButton.setAttribute('aria-pressed', 'false');
  if (state.placeholder) state.placeholder.remove();
  state.placeholder = null;
  document.body.classList.remove('diagram-open');
  fullscreenState = null;
  if (restoreFocus && state.returnFocus && state.returnFocus.isConnected) {
    state.returnFocus.focus();
  }
}

function openFullscreen(state) {
  if (fullscreenState === state) return;
  if (fullscreenState) closeFullscreen(fullscreenState, false);

  const placeholder = makeElement('div', 'diagram-placeholder');
  placeholder.style.height = state.figure.getBoundingClientRect().height + 'px';
  state.figure.before(placeholder);
  state.placeholder = placeholder;
  state.returnFocus = document.activeElement;
  state.figure.classList.add('is-fullscreen');
  state.fullButton.textContent = 'Exit';
  state.fullButton.setAttribute('aria-pressed', 'true');
  document.body.classList.add('diagram-open');
  fullscreenState = state;
  state.fullButton.focus();
}

function toggleFullscreen(state) {
  if (fullscreenState === state) closeFullscreen(state);
  else openFullscreen(state);
}

function enhanceDiagram(figure, index) {
  const svg = figure.querySelector(':scope > svg');
  if (!svg) return;

  const toolbar = makeElement('div', 'diagram-toolbar');
  toolbar.setAttribute('role', 'group');
  toolbar.setAttribute('aria-label', 'Diagram view controls');

  const zoomOut = makeElement('button', '', '\u2212');
  zoomOut.type = 'button';
  zoomOut.setAttribute('aria-label', 'Zoom out');

  const range = makeElement('input');
  range.type = 'range';
  range.min = '50';
  range.max = '500';
  range.step = '25';
  range.value = '100';
  range.setAttribute('aria-label', 'Diagram zoom');

  const output = makeElement('output', 'diagram-zoom-output', '100%');
  output.value = '100%';
  output.setAttribute('aria-live', 'polite');

  const zoomIn = makeElement('button', '', '+');
  zoomIn.type = 'button';
  zoomIn.setAttribute('aria-label', 'Zoom in');

  const fit = makeElement('button', '', 'Fit');
  fit.type = 'button';
  fit.setAttribute('aria-label', 'Fit diagram');

  const spacer = makeElement('span', 'diagram-toolbar-spacer');
  spacer.setAttribute('aria-hidden', 'true');

  const full = makeElement('button', '', 'Full');
  full.type = 'button';
  full.setAttribute('aria-label', 'Toggle fullscreen diagram');
  full.setAttribute('aria-pressed', 'false');

  toolbar.append(zoomOut, range, output, zoomIn, fit, spacer, full);

  const viewport = makeElement('div', 'diagram-viewport');
  viewport.tabIndex = 0;
  const caption = figure.querySelector('figcaption');
  viewport.setAttribute('aria-label', caption && caption.textContent.trim()
    ? 'Diagram: ' + caption.textContent.trim()
    : 'Diagram ' + (index + 1));

  svg.before(viewport);
  viewport.appendChild(svg);
  figure.insertBefore(toolbar, viewport);
  figure.classList.add('is-enhanced');

  const state = {
    figure,
    svg,
    viewport,
    range,
    output,
    fullButton: full,
    zoom: 100,
    zoomFrame: 0,
    pendingCenter: null,
    placeholder: null,
    returnFocus: null
  };
  diagramStates.push(state);
  setDiagramZoom(state, 100, true);

  zoomOut.addEventListener('click', () => setDiagramZoom(state, state.zoom - 25));
  zoomIn.addEventListener('click', () => setDiagramZoom(state, state.zoom + 25));
  fit.addEventListener('click', () => setDiagramZoom(state, 100, true));
  full.addEventListener('click', () => toggleFullscreen(state));
  range.addEventListener('input', () => setDiagramZoom(state, Number(range.value)));

  viewport.addEventListener('wheel', (event) => {
    if (!event.ctrlKey && !event.metaKey) return;
    event.preventDefault();
    setDiagramZoom(state, state.zoom + (event.deltaY < 0 ? 25 : -25));
  }, { passive: false });

  figure.addEventListener('keydown', (event) => {
    if (event.key === '+' || event.key === '=') {
      event.preventDefault();
      setDiagramZoom(state, state.zoom + 25);
    } else if (event.key === '-') {
      event.preventDefault();
      setDiagramZoom(state, state.zoom - 25);
    } else if (event.key === '0') {
      event.preventDefault();
      setDiagramZoom(state, 100, true);
    } else if (event.key.toLowerCase() === 'f') {
      event.preventDefault();
      toggleFullscreen(state);
    }
  });
}

document.querySelectorAll('figure.diagram').forEach(enhanceDiagram);

document.addEventListener('keydown', (event) => {
  if (!fullscreenState) return;
  if (event.key === 'Escape') {
    event.preventDefault();
    closeFullscreen(fullscreenState);
    return;
  }
  if (event.key !== 'Tab') return;

  const focusable = [...fullscreenState.figure.querySelectorAll(
    'button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
  )].filter((node) => !node.hidden);
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (!fullscreenState.figure.contains(document.activeElement)) {
    event.preventDefault();
    (event.shiftKey ? last : first).focus();
  } else if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});

addEventListener('beforeprint', () => {
  if (fullscreenState) closeFullscreen(fullscreenState, false);
  for (const state of diagramStates) setDiagramZoom(state, 100, true);
});
/* DIAGRAM_VIEWER_END */
