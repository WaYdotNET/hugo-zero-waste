document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.highlight').forEach(function (block) {
    var pre = block.querySelector('pre');
    if (!pre) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-code label';
    btn.textContent = 'copia';
    btn.setAttribute('aria-label', 'Copia il codice negli appunti');
    btn.addEventListener('click', function () {
      var code = block.querySelector('code') || pre;
      var text = code.innerText.replace(/\n$/, '');
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = 'copiato ✓';
        setTimeout(function () { btn.textContent = 'copia'; }, 1600);
      }).catch(function () {
        btn.textContent = 'errore';
        setTimeout(function () { btn.textContent = 'copia'; }, 1600);
      });
    });
    block.appendChild(btn);
  });
});
