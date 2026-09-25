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


  /* galeria jednostki: miniatura i duże zdjęcie otwierają powiększenie */
  var ug=document.querySelector('.ugal');
  if(ug){
    var th=[].slice.call(ug.querySelectorAll('.ugal__thumbs button')),fig=ug.querySelector('.ugal__main'),nEl=ug.querySelector('.ugal__n'),cur=0,from=null;
    var big=function(i,sizes){var p=th[i].querySelector('picture').cloneNode(true);[].forEach.call(p.querySelectorAll('[sizes]'),function(x){x.setAttribute('sizes',sizes)});var im=p.querySelector('img');im.removeAttribute('loading');im.alt='';return p};
    var setMain=function(i){cur=i;th.forEach(function(b,k){if(k===i)b.setAttribute('aria-current','true');else b.removeAttribute('aria-current')});
      var old=fig.querySelector('picture');if(old)fig.replaceChild(big(i,'(min-width:1024px) 60vw, 100vw'),old);if(nEl)nEl.textContent=i+1};
    var lb=document.createElement('div');lb.className='lb';lb.hidden=true;lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Zdjęcia jachtu');
    lb.innerHTML='<div class="lb__bar"><span class="lb__n num"></span><span class="lb__cap"></span><button class="lb__x" type="button" aria-label="Zamknij zdjęcia"><i data-lucide="x" class="lucide"></i></button></div><div class="lb__stage"></div><button class="lb__nav lb__nav--prev" type="button" aria-label="Poprzednie zdjęcie"><i data-lucide="arrow-left" class="lucide"></i></button><button class="lb__nav lb__nav--next" type="button" aria-label="Następne zdjęcie"><i data-lucide="arrow-right" class="lucide"></i></button>';
    document.body.appendChild(lb);icons();
    var stage=lb.querySelector('.lb__stage'),lbN=lb.querySelector('.lb__n'),lbCap=lb.querySelector('.lb__cap'),title=(document.querySelector('.unit__h')||{}).textContent||'';
    var show=function(i){i=(i+th.length)%th.length;var p=big(i,'100vw');stage.innerHTML='';stage.appendChild(p);lbN.textContent=(i+1)+' / '+th.length;lbCap.textContent=title;setMain(i)};
    var open=function(i,el){from=el||document.activeElement;lb.hidden=false;document.body.classList.add('lb-open');show(i);requestAnimationFrame(function(){lb.classList.add('is-open')});lb.querySelector('.lb__x').focus()};
    var close=function(){lb.classList.remove('is-open');document.body.classList.remove('lb-open');lb.hidden=true;if(from)from.focus()};
    th.forEach(function(b,i){b.addEventListener('click',function(){open(i,b)})});
    var z=fig.querySelector('.ugal__zoom');if(z)z.addEventListener('click',function(){open(cur,z)});
    [].forEach.call(document.querySelectorAll('.uh__arrow'),function(b){b.addEventListener('click',function(){setMain((cur+(+b.dataset.dir)+th.length)%th.length)})});
    lb.querySelector('.lb__x').addEventListener('click',close);
    lb.querySelector('.lb__nav--prev').addEventListener('click',function(){show(cur-1)});
    lb.querySelector('.lb__nav--next').addEventListener('click',function(){show(cur+1)});
    stage.addEventListener('click',function(e){if(e.target===stage)close()});
    lb.addEventListener('keydown',function(e){
      if(e.key==='Escape')return close();if(e.key==='ArrowLeft')return show(cur-1);if(e.key==='ArrowRight')return show(cur+1);
      if(e.key==='Tab'){var f=[].slice.call(lb.querySelectorAll('button')),a=f[0],zz=f[f.length-1];
        if(e.shiftKey&&document.activeElement===a){e.preventDefault();zz.focus()}else if(!e.shiftKey&&document.activeElement===zz){e.preventDefault();a.focus()}}});
    var tx=null;stage.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
    stage.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(dx)>45)show(cur+(dx<0?1:-1))});
    /* duże wersje od razu do pamięci — przełączanie bez czekania */
    addEventListener('load',function(){var w=document.createElement('div');w.className='lb__warm';w.setAttribute('aria-hidden','true');th.forEach(function(_,i){w.appendChild(big(i,'100vw'))});document.body.appendChild(w)});
  }

  /* spacer wirtualny: ramka ładuje się dopiero po kliknięciu */
  [].forEach.call(document.querySelectorAll('.vt'),function(v){var b=v.querySelector('.vt__play');if(b)b.addEventListener('click',function(){
    v.innerHTML='<iframe src="'+v.dataset.src+'" title="Spacer wirtualny po jachcie" allow="fullscreen; xr-spatial-tracking" allowfullscreen loading="lazy"></iframe>'})});

  /* pojawianie sekcji */
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal:not(.in)').forEach(function(el){io.observe(el)});
  }else document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});
  /* zabezpieczenie: gdyby obserwator nie zadziałał, sekcja pojawia się, gdy wjedzie w ekran */
  var sweep=function(){document.querySelectorAll('.reveal:not(.in)').forEach(function(el){if(el.getBoundingClientRect().top<innerHeight*.95)el.classList.add('in')})};
  addEventListener('scroll',sweep,{passive:true});addEventListener('load',sweep);setTimeout(sweep,1200);
})();
