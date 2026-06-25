function zwToggleTheme() {
  var cur = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
  var next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem('zw-theme', next); } catch (e) {}
}
