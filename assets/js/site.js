/* jachtymazury.pl — wspólny skrypt wszystkich stron */
(function(){
  document.documentElement.classList.add('js');
  function icons(){try{window.lucide&&lucide.createIcons()}catch(e){}}
  icons();addEventListener('load',icons);

  /* nagłówek na podstronach: cień linii po przewinięciu */
  var head=document.getElementById('head');
  if(head&&!head.classList.contains('on-photo')&&!head.classList.contains('solid')){
    var sync=function(){head.classList.toggle('is-scrolled',scrollY>8)};sync();addEventListener('scroll',sync,{passive:true});
  }

  /* menu rozwijane: kliknięcie, Esc, klawiatura */
  document.querySelectorAll('.nav .has').forEach(function(h){
    var b=h.querySelector('.nav__b');if(!b)return;
    b.addEventListener('click',function(e){e.stopPropagation();var o=!h.classList.contains('is-open');
      document.querySelectorAll('.nav .has.is-open').forEach(function(x){x.classList.remove('is-open');x.querySelector('.nav__b').setAttribute('aria-expanded','false')});
      h.classList.toggle('is-open',o);b.setAttribute('aria-expanded',o)});
    h.addEventListener('keydown',function(e){if(e.key==='Escape'){h.classList.remove('is-open');b.setAttribute('aria-expanded','false');b.focus()}});
  });
  document.addEventListener('click',function(){document.querySelectorAll('.nav .has.is-open').forEach(function(x){x.classList.remove('is-open');x.querySelector('.nav__b').setAttribute('aria-expanded','false')})});

  /* menu mobilne */
  var burger=document.querySelector('.burger'),mnav=document.getElementById('mnav');
  if(burger&&mnav){
    /* strona główna: pasek nad zdjęciem robi się jasny, gdy menu jest otwarte */
    var photoHead=head&&(head.classList.contains('on-photo')||head.classList.contains('solid'))?head:null;
    var open=function(){if(photoHead){photoHead.classList.add('solid');photoHead.classList.remove('on-photo')}mnav.hidden=false;requestAnimationFrame(function(){mnav.classList.add('is-open')});
      document.body.classList.add('mnav-open');burger.setAttribute('aria-expanded','true');burger.setAttribute('aria-label','Zamknij menu');
      var a=mnav.querySelector('a');a&&a.focus()};
    var close=function(){mnav.classList.remove('is-open');document.body.classList.remove('mnav-open');burger.setAttribute('aria-expanded','false');
      burger.setAttribute('aria-label','Otwórz menu');setTimeout(function(){mnav.hidden=true},260);if(photoHead&&scrollY<=8){photoHead.classList.remove('solid');photoHead.classList.add('on-photo')}burger.focus()};
    burger.addEventListener('click',function(){mnav.hidden?open():close()});
    mnav.addEventListener('keydown',function(e){if(e.key==='Escape')close();
      if(e.key!=='Tab')return;var f=[].slice.call(mnav.querySelectorAll('a,button'));f.unshift(burger);var a=f[0],z=f[f.length-1];
      if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}});
    mnav.addEventListener('click',function(e){if(e.target.closest('a'))close()});
    addEventListener('resize',function(){if(innerWidth>1023&&!mnav.hidden)close()});
  }

  /* filtr modeli na listach floty */
  document.querySelectorAll('.chips').forEach(function(g){
    var sec=g.closest('section'),cards=[].slice.call(sec.querySelectorAll('.fli')),st=sec.querySelector('.chips__st');
    g.addEventListener('click',function(e){var c=e.target.closest('.chip');if(!c)return;var f=c.dataset.f,n=0;
      g.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',x===c)});
      cards.forEach(function(k){var on=f==='*'||k.dataset.model===f;k.hidden=!on;if(on)n++});
      if(st)st.textContent=f==='*'?'':('Pokazano '+n+' z '+cards.length+' · '+f);});
    /* ?model=… — wejście z karty modelu na stronie głównej */
    try{var want=new URLSearchParams(location.search).get('model');
      if(want){var c=[].slice.call(g.querySelectorAll('.chip')).filter(function(x){return x.dataset.f===want})[0];if(c)c.click()}}catch(e){}
  });

  /* pojawianie sekcji */
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal:not(.in)').forEach(function(el){io.observe(el)});
  }else document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});
  /* zabezpieczenie: gdyby obserwator nie zadziałał, sekcja pojawia się, gdy wjedzie w ekran */
  var sweep=function(){document.querySelectorAll('.reveal:not(.in)').forEach(function(el){if(el.getBoundingClientRect().top<innerHeight*.95)el.classList.add('in')})};
  addEventListener('scroll',sweep,{passive:true});addEventListener('load',sweep);setTimeout(sweep,1200);
})();
