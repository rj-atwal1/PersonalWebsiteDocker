// Toggle mobile navigation (simple and accessible)
(function(){
  const toggles = document.querySelectorAll('.nav-toggle');
  if(!toggles) return;
  toggles.forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const controls = btn.getAttribute('aria-controls');
      const nav = document.getElementById(controls);
      if(!nav) return;
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('show');
      const hb = btn.querySelector('.hamburger');
      if(hb) hb.classList.toggle('open');
    });
  });
})();
