/* CODEM — couche de mouvement : route CODEM, titres révélés, parallaxe, boutons magnétiques,
   pastille devis, aperçus de services, page Particuliers (4 actes, curseur de formule, galerie horizontale). */
(()=>{'use strict';
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine=matchMedia('(pointer:fine)').matches;
const en=document.documentElement.lang==='en';const tr=(a,b)=>en?b:a;
const body=document.body,isForm=body.classList.contains('form-page');
const quoteUrl=en?'/en/quote/':'/fr/devis/';
let ticking=false;const onScroll=[];
const loop=()=>{ticking=false;onScroll.forEach(f=>f());};
addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(loop);}},{passive:true});
addEventListener('resize',()=>requestAnimationFrame(loop));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:.18,rootMargin:'0px 0px -6% 0px'});

/* 1. Titres révélés ligne par ligne */
if(!reduce){
 document.querySelectorAll('main h1, main h2').forEach(h=>{if(h.closest('form,.quote-page,.cta-strip,.film-copy,.hero'))return;const parts=h.innerHTML.split(/<br\s*\/?>/i);h.innerHTML=parts.map((p,i)=>`<span class="ln"><span class="ln-i" style="--d:${i*110}ms">${p}</span></span>`).join('');h.classList.add('tsplit');});
 document.querySelectorAll('.tsplit,.draw,[data-in]').forEach(el=>io.observe(el));
 document.documentElement.classList.add('motion');
}

/* 2. Parallaxe douce des photos */
if(!reduce&&fine){
 const imgs=[...document.querySelectorAll('.page-intro .image-wrap img,.split .image-wrap img,.layered-media img,.real-grid img,.europe-teaser img')];
 imgs.forEach(i=>i.classList.add('plx'));
 onScroll.push(()=>{const vh=innerHeight;for(const i of imgs){const r=i.parentElement.getBoundingClientRect();if(r.bottom<0||r.top>vh)continue;const k=((r.top+r.height/2)-vh/2)/vh;i.style.transform=`translate3d(0,${(k*-34).toFixed(1)}px,0) scale(1.1)`;}});
}

/* 3. Boutons verts magnétiques */
if(!reduce&&fine){document.querySelectorAll('.btn-cta').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.22}px,${(e.clientY-r.top-r.height/2)*.32}px)`;});b.addEventListener('pointerleave',()=>{b.style.transform='';});});}

/* 4. La route CODEM : un camion descend la page et arrive au devis */
if(!isForm){
 const rail=document.createElement('div');rail.className='route-rail';
 rail.innerHTML=`<span class="rail-a" aria-hidden="true">A</span><span class="rail-line" aria-hidden="true"><span class="rail-fill"></span></span><span class="rail-truck" aria-hidden="true"><svg viewBox="0 0 64 34"><rect x="1" y="2" width="40" height="24" rx="3" fill="#fff" stroke="#22264f" stroke-width="2"/><path d="M41 9h12l9 9v8H41z" fill="#5fb03a" stroke="#22264f" stroke-width="2"/><circle cx="13" cy="28" r="5" fill="#22264f"/><circle cx="51" cy="28" r="5" fill="#22264f"/></svg></span><a class="rail-b" href="${quoteUrl}" aria-label="${tr('Demander un devis','Get a quote')}">B<span>${tr('Devis','Quote')}</span></a>`;
 const top=document.createElement('div');top.className='route-top';top.setAttribute('aria-hidden','true');top.innerHTML='<span class="rt-fill"></span>';
 body.append(rail,top);
 const line=rail.querySelector('.rail-line'),fill=rail.querySelector('.rail-fill'),truck=rail.querySelector('.rail-truck');
 const marks=[...document.querySelectorAll('main > section, main > .cta-strip')].filter(s=>s.offsetHeight>200);
 const dots=marks.map(()=>{const d=document.createElement('span');d.className='rail-dot';line.append(d);return d;});
 const place=()=>{const H=document.documentElement.scrollHeight-innerHeight;marks.forEach((s,i)=>{dots[i].style.top=Math.min(100,Math.max(0,(s.offsetTop-innerHeight*.35)/H*100))+'%';});};
 place();addEventListener('load',place);addEventListener('resize',place);
 onScroll.push(()=>{const H=document.documentElement.scrollHeight-innerHeight;const p=H>0?Math.min(1,scrollY/H):0;fill.style.height=(p*100)+'%';truck.style.top=`calc(${p*100}% + 38px)`;top.style.setProperty('--p',p);dots.forEach(d=>d.classList.toggle('lit',parseFloat(d.style.top)<=p*100+.5));rail.classList.toggle('arrived',p>.97);});
}

/* 5. Pastille « Devis en 2 min » */
if(!isForm){
 const pill=document.createElement('a');pill.className='quick-pill';pill.href=quoteUrl;pill.innerHTML=`<span class="qp-dot"></span>${tr('Devis gratuit en 2 min','Free quote in 2 min')}<span aria-hidden="true">→</span>`;body.append(pill);
 const cta=document.querySelector('.cta');let ctaVisible=false;
 if(cta)new IntersectionObserver(es=>{ctaVisible=es[0].isIntersecting;loop();}).observe(cta);
 onScroll.push(()=>{const H=document.documentElement.scrollHeight-innerHeight;pill.classList.toggle('show',H>0&&scrollY/H>.3&&!ctaVisible);});
}

/* 6. Aperçu photo qui suit la souris sur les listes de services */
if(!reduce&&fine){
 const map={'particuliers':'ancien-07','home-moving':'ancien-07','entreprises':'entreprises','office-moving':'entreprises','france-europe':'europe','garde-meubles':'stockage','storage':'stockage','monte-meubles':'monte-meubles','furniture-lift':'monte-meubles','objets-specialises':'piano','specialist-items':'piano'};
 const prev=document.createElement('div');prev.className='hover-preview';prev.innerHTML='<img alt="">';body.append(prev);const pi=prev.querySelector('img');
 document.querySelectorAll('.services-band a,.service-tabs a').forEach(a=>{const k=Object.keys(map).find(k=>a.getAttribute('href').includes(k));if(!k)return;a.addEventListener('pointerenter',()=>{pi.src=`/assets/${map[k]}-640.webp`;prev.classList.add('on');});a.addEventListener('pointerleave',()=>prev.classList.remove('on'));a.addEventListener('pointermove',e=>{prev.style.transform=`translate(${e.clientX+18}px,${e.clientY+18}px)`;});});
}

/* 7. Particuliers — les 4 actes */
const stage=document.querySelector('[data-act-stage]');
if(stage){
 const acts=[...document.querySelectorAll('.act')],dots=[...stage.querySelectorAll('.act-dot')];
 const set=n=>{stage.dataset.actStage=n;acts.forEach(a=>a.classList.toggle('active',a.dataset.act==n));dots.forEach(d=>d.classList.toggle('on',d.dataset.dot<=n));};
 set(1);
 const aio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)set(e.target.dataset.act);}),{rootMargin:'-45% 0px -45% 0px'});
 acts.forEach(a=>aio.observe(a));
}

/* 8. Curseur « Je fais / CODEM fait » */
const ft=document.querySelector('.ft-control');
if(ft){
 const range=ft.querySelector('input'),tasks=[...document.querySelectorAll('.ft-tasks .task')],res=document.querySelector('.ft-result');
 const upd=()=>{const i=+range.value;const [name,desc,slug]=ft.dataset['f'+i].split('|');let n=0;
  tasks.forEach((li,k)=>{const c=li.dataset.codes[i];li.dataset.who=c==='X'?'codem':c==='C'?'you':'tbd';if(c==='X')n++;li.style.transitionDelay=(k*35)+'ms';});
  res.querySelector('.ft-name').textContent=name;res.querySelector('.ft-desc').textContent=desc;res.querySelector('[data-count]').textContent=n;res.querySelector('.ft-cta-name').textContent=name;
  res.querySelector('.ft-cta').href=`${quoteUrl}?service=particulier&formule=${slug}`;range.style.setProperty('--v',i/4);
  ft.querySelectorAll('.ft-ticks span').forEach((s,k)=>s.classList.toggle('on',k===i));res.classList.remove('pop');void res.offsetWidth;res.classList.add('pop');};
 range.addEventListener('input',upd);ft.querySelectorAll('.ft-ticks span').forEach((s,k)=>s.addEventListener('click',()=>{range.value=k;upd();}));upd();
}

/* 9. Galerie horizontale pilotée par le scroll */
const hs=document.querySelector('.hscroll');
if(hs&&!reduce&&matchMedia('(min-width:901px)').matches){
 const track=hs.querySelector('.hs-track');hs.classList.add('pinned');
 const size=()=>{const extra=track.scrollWidth-innerWidth+80;hs.style.height=(innerHeight+Math.max(0,extra))+'px';return extra;};
 let extra=size();addEventListener('resize',()=>{extra=size();});addEventListener('load',()=>{extra=size();});
 onScroll.push(()=>{const r=hs.getBoundingClientRect();const p=Math.min(1,Math.max(0,-r.top/(hs.offsetHeight-innerHeight)));track.style.transform=`translate3d(${-p*Math.max(0,extra)}px,0,0)`;});
}

/* 10. Titres du hero synchronisés avec les séquences de la vidéo */
const ht=document.querySelector('.hero-title[data-titles]');
if(ht){
 const list=[[0,ht.innerHTML]].concat(JSON.parse(ht.dataset.titles));
 ht.innerHTML='<span class="ht-stack">'+list.map((x,i)=>`<span class="ht${i?'':' on'}"${i?' aria-hidden="true"':''}>${x[1]}</span>`).join('')+'</span>';
 const spans=[...ht.querySelectorAll('.ht')];const v=document.querySelector('.hero video');let cur=0;
 const show=i=>{if(i===cur)return;spans[cur].classList.remove('on');spans[i].classList.add('on');cur=i;};
 if(v&&!reduce){v.addEventListener('timeupdate',()=>{const tm=v.currentTime;let i=0;list.forEach((x,k)=>{if(tm>=x[0])i=k;});show(i);});}
}
loop();
})();
