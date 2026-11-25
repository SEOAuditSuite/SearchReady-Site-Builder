document.documentElement.classList.replace('no-js','js');
(() => {
  const button = document.querySelector('.menu-toggle');
  const menu = document.getElementById('primary-menu');
  if (button && menu) {
    const close = (returnFocus = false) => {
      if (button.getAttribute('aria-expanded') !== 'true') return;
      button.setAttribute('aria-expanded','false');
      button.setAttribute('aria-label','Open navigation');
      if (returnFocus) button.focus();
    };
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') === 'true';
      if (open) close();
      else {button.setAttribute('aria-expanded','true');button.setAttribute('aria-label','Close navigation');}
    });
    document.addEventListener('keydown', e => {if (e.key === 'Escape') close(true);});
    menu.addEventListener('click', e => {if(e.target.closest('a')) close();});
    window.addEventListener('resize', () => { if(window.innerWidth > 720) close(); });
  }
  const input=document.getElementById('filter-notes');
  if (input) {
    const cards=[...document.querySelectorAll('.story-card')];
    const empty=document.getElementById('no-results');
    const status=document.getElementById('result-status');
    input.addEventListener('input',()=>{
      const query=input.value.toLocaleLowerCase().trim();
      let count=0;
      cards.forEach(card=>{
        const match=card.dataset.search.includes(query);
        card.hidden=!match;
        if(match) count++;
      });
      empty.hidden=count>0;
      status.textContent=`${count} ${count===1?'note':'notes'} shown`;
    });
  }
})();
