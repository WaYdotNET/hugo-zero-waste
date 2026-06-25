var ZW_CLIPBOARD = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
var ZW_CHECK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.highlight').forEach(function (block) {
    var pre = block.querySelector('pre');
    if (!pre) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-code';
    btn.innerHTML = ZW_CLIPBOARD;
    btn.setAttribute('aria-label', 'Copia il codice negli appunti');
    btn.setAttribute('title', 'Copia');
    btn.addEventListener('click', function () {
      var code = block.querySelector('code') || pre;
      var text = code.innerText.replace(/\n$/, '');
      navigator.clipboard.writeText(text).then(function () {
        btn.innerHTML = ZW_CHECK;
        btn.classList.add('copied');
        setTimeout(function () { btn.innerHTML = ZW_CLIPBOARD; btn.classList.remove('copied'); }, 1600);
      }).catch(function () {});
    });
    block.appendChild(btn);
  });
});
