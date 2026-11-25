'use strict';
(function(){
  const toggle=document.querySelector('[data-menu-toggle]');
  const navigation=document.querySelector('[data-navigation]');
  if(toggle&&navigation){
    const closeMenu=()=>{navigation.classList.remove('open');toggle.setAttribute('aria-expanded','false');};
    toggle.addEventListener('click',()=>{const opened=navigation.classList.toggle('open');toggle.setAttribute('aria-expanded',String(opened));});
    navigation.addEventListener('click',(event)=>{if(event.target.closest('a'))closeMenu();});
    document.addEventListener('keydown',(event)=>{if(event.key==='Escape'&&navigation.classList.contains('open')){closeMenu();toggle.focus();}});
    window.addEventListener('resize',()=>{if(window.innerWidth>700)closeMenu();});
  }
  const form=document.querySelector('[data-brief-form]');
  if(form){
    form.addEventListener('submit',(event)=>{
      event.preventDefault();
      if(!form.reportValidity())return;
      const data=new FormData(form);
      const lines=['CLEARROOM — DEMO PLANNING BRIEF','',
        'Name: '+String(data.get('name')||''),
        'Project focus: '+String(data.get('project')||''),
        'What you would like help with: '+String(data.get('message')||''),
        '', 'This file was created in your browser. No information was transmitted to a business.'];
      const blob=new Blob([lines.join('\n')],{type:'text/plain;charset=utf-8'});
      const url=URL.createObjectURL(blob);
      const a=document.createElement('a');a.href=url;a.download='clearroom-demo-brief.txt';document.body.appendChild(a);a.click();a.remove();
      setTimeout(()=>URL.revokeObjectURL(url),1000);
      document.querySelector('[data-form-status]').textContent='Your brief was downloaded locally. Nothing was sent.';
    });
  }
})();
