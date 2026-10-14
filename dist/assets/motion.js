/* CODEM : couche de mouvement : route CODEM, titres révélés, parallaxe, boutons magnétiques,
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
 const imgs=[...document.querySelectorAll('.page-intro .image-wrap img,.split .image-wrap img,.layered-media img,.real-grid .image-wrap img,.europe-teaser img')].filter(i=>!i.classList.contains('video-poster'));
 imgs.forEach(i=>i.classList.add('plx'));
 onScroll.push(()=>{const vh=innerHeight;for(const i of imgs){const r=i.parentElement.getBoundingClientRect();if(r.bottom<0||r.top>vh)continue;const k=((r.top+r.height/2)-vh/2)/vh;i.style.transform=`translate3d(0,${(k*-34).toFixed(1)}px,0) scale(1.1)`;}});
}

/* 3. Boutons verts magnétiques */
if(!reduce&&fine){document.querySelectorAll('.btn-cta').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.22}px,${(e.clientY-r.top-r.height/2)*.32}px)`;});b.addEventListener('pointerleave',()=>{b.style.transform='';});});}

/* 4. La route CODEM : un camion descend la page et arrive au devis */
if(!isForm){
 const rail=document.createElement('div');rail.className='route-rail';
 rail.innerHTML=`<span class="rail-a" aria-hidden="true">A</span><span class="rail-line" aria-hidden="true"><span class="rail-fill"></span></span><span class="rail-truck rail-mini" aria-hidden="true"><img src="/assets/camion-mini.webp" width="96" height="69" alt=""></span><a class="rail-b" href="${quoteUrl}" aria-label="${tr('Demander un devis','Get a quote')}">B<span>${tr('Devis','Quote')}</span></a>`;
 const top=document.createElement('div');top.className='route-top';top.setAttribute('aria-hidden','true');top.innerHTML='<span class="rt-fill"></span>';
 body.append(rail,top);
 const line=rail.querySelector('.rail-line'),fill=rail.querySelector('.rail-fill'),truck=rail.querySelector('.rail-truck');
 const marks=[...document.querySelectorAll('main > section, main > .cta-strip')].filter(s=>s.offsetHeight>200);
 const dots=marks.map(()=>{const d=document.createElement('span');d.className='rail-dot';line.append(d);return d;});
 const place=()=>{const H=document.documentElement.scrollHeight-innerHeight;marks.forEach((s,i)=>{dots[i].style.top=Math.min(100,Math.max(0,(s.offsetTop-innerHeight*.35)/H*100))+'%';});};
 place();addEventListener('load',place);addEventListener('resize',place);
 onScroll.push(()=>{const H=document.documentElement.scrollHeight-innerHeight;const p=H>0?Math.min(1,scrollY/H):0;fill.style.height=(p*100)+'%';truck.style.top=`calc(${p*100}% + 38px)`;top.style.setProperty('--p',p);dots.forEach(d=>d.classList.toggle('lit',parseFloat(d.style.top)<=p*100+.5));rail.classList.toggle('arrived',p>.97);});
}

/* 5. Pastille « Recevoir mon devis gratuit » */
if(!isForm){
 const pill=document.createElement('a');pill.className='quick-pill';pill.href=quoteUrl;pill.innerHTML=`<span class="qp-dot"></span><span class="qp-text">${tr('Recevoir mon devis gratuit','Get my free quote')}<small>${tr('Sans engagement','No obligation')}</small></span><span aria-hidden="true">→</span>`;body.append(pill);
 const cta=document.querySelector('.cta');let ctaVisible=false;
 if(cta)new IntersectionObserver(es=>{ctaVisible=es[0].isIntersecting;loop();}).observe(cta);
 onScroll.push(()=>{const H=document.documentElement.scrollHeight-innerHeight;pill.classList.toggle('show',H>0&&scrollY/H>.3&&!ctaVisible);});
}

/* 7. Particuliers : les 4 actes */
const stage=document.querySelector('[data-act-stage]');
if(stage){
 const acts=[...document.querySelectorAll('.act')],dots=[...stage.querySelectorAll('.act-dot')];
 const set=n=>{stage.dataset.actStage=n;acts.forEach(a=>a.classList.toggle('active',a.dataset.act==n));dots.forEach(d=>d.classList.toggle('on',d.dataset.dot<=n));};
 set(1);
 const aio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)set(e.target.dataset.act);}),{rootMargin:'-45% 0px -45% 0px'});
 acts.forEach(a=>aio.observe(a));
 dots.forEach(d=>d.addEventListener('click',()=>{const n=d.dataset.dot;set(n);const a=acts.find(x=>x.dataset.act==n);if(a){const r=a.getBoundingClientRect();scrollTo({top:scrollY+r.top+r.height/2-innerHeight/2,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}}));
}

/* 8. Curseur « Je fais / CODEM fait » */
const ft=document.querySelector('.ft-control');
if(ft){
 const range=ft.querySelector('input'),tasks=[...document.querySelectorAll('.ft-tasks .task')],res=document.querySelector('.ft-result');
 const upd=()=>{const i=+range.value;const [name,desc,slug]=ft.dataset['f'+i].split('|');let n=0;
  let you=0,tbd=0;tasks.forEach((li,k)=>{const c=li.dataset.codes[i];li.dataset.who=c==='X'?'codem':c==='C'?'you':'tbd';if(c==='X')n++;else if(c==='C')you++;else tbd++;li.style.transitionDelay=(k*35)+'ms';});const tot=tasks.length||1,pc=Math.round(n/tot*100),py=Math.round(you/tot*100);const q=s=>res.querySelector(s);if(q('[data-pct-codem]')){q('[data-pct-codem]').textContent=pc+' %';q('[data-pct-you]').textContent=py+' %';q('[data-bar]').style.width=pc+'%';q('[data-tbd-note]').textContent=tbd?(document.documentElement.lang==='en'?` · ${tbd} to confirm`:` · ${tbd} à préciser`):'';}
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
/* Vidéos : l'image d'attente est affichée immédiatement ; la vidéo apparaît en fondu dès sa première image */
(()=>{const rm=matchMedia('(prefers-reduced-motion: reduce)').matches||navigator.connection?.saveData;document.querySelectorAll('video[data-video]').forEach(v=>{if(v.readyState>=3&&!v.paused)v.classList.add('vready');v.addEventListener('playing',()=>{const on=()=>v.classList.add('vready');v.requestVideoFrameCallback?v.requestVideoFrameCallback(on):on();},{once:true});});})();
/* Accueil : carrousels (services, destinations, avis) */
(()=>{const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,canHover=matchMedia('(hover:hover)').matches;
document.querySelectorAll('[data-carousel]').forEach(sec=>{
 const track=sec.querySelector('[data-track]'),cards=[...track.children],cur=sec.querySelector('[data-cur]'),prog=sec.querySelector('[data-progress]'),expand=sec.hasAttribute('data-expand');
 const DUR=+sec.dataset.autoplay||0;let i=0,timer=null,hover=false,started=false;
 let bars=[];if(prog){prog.innerHTML=cards.map((c,k)=>`<button type="button" aria-label="${k+1} / ${cards.length}"><i></i></button>`).join('');bars=[...prog.children];sec.style.setProperty('--dur',DUR+'ms');bars.forEach((b,k)=>b.addEventListener('click',()=>go(k)));}
 const pad=()=>parseFloat(getComputedStyle(track).scrollPaddingLeft)||parseFloat(getComputedStyle(track).paddingLeft)||0;
 const pos=c=>c.getBoundingClientRect().left-track.getBoundingClientRect().left+track.scrollLeft-pad();
 const nearest=()=>{let best=0,bd=1e9;cards.forEach((c,k)=>{const d=Math.abs(pos(c)-track.scrollLeft);if(d<bd){bd=d;best=k}});return best};
 const maxIdx=()=>{if(expand)return cards.length-1;let k=cards.length-1;const max=track.scrollWidth-track.clientWidth;while(k>0&&pos(cards[k-1])>=max-2)k--;return k};
 function mark(n){i=n;if(cur)cur.textContent=String(i+1).padStart(2,'0');if(expand)cards.forEach((c,k)=>c.classList.toggle('on',k===i));
  bars.forEach((b,k)=>{b.classList.remove('on');b.classList.toggle('done',k<i);void b.offsetWidth;if(k===i&&started)b.classList.add('on')});}
 function go(n,scroll=true){const m=maxIdx();n=n>m?0:n<0?m:n;mark(n);if(scroll)setTimeout(()=>track.scrollTo({left:pos(cards[n]),behavior:reduce?'auto':'smooth'}),expand?40:0);restart();}
 function restart(){clearTimeout(timer);if(!DUR||reduce||hover||document.hidden||!started)return;timer=setTimeout(()=>go(i+1),DUR);}
 sec.querySelector('[data-next]')?.addEventListener('click',()=>go(i+1));sec.querySelector('[data-prev]')?.addEventListener('click',()=>go(i-1));
 if(expand&&canHover)cards.forEach((c,k)=>c.addEventListener('mouseenter',()=>{if(k!==i)go(k,false)}));
 cards.forEach((c,k)=>c.addEventListener('focusin',()=>{if(k!==i)mark(k)}));
 sec.addEventListener('mouseenter',()=>{hover=true;sec.classList.add('paused');clearTimeout(timer)});sec.addEventListener('mouseleave',()=>{hover=false;sec.classList.remove('paused');restart()});
 sec.addEventListener('focusin',()=>{hover=true;clearTimeout(timer)});sec.addEventListener('focusout',()=>{hover=false;restart()});
 track.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();go(i+1)}if(e.key==='ArrowLeft'){e.preventDefault();go(i-1)}});
 document.addEventListener('visibilitychange',restart);
 let down=false,sx=0,sl=0,moved=false;
 track.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse'||e.button)return;down=true;moved=false;sx=e.clientX;sl=track.scrollLeft;});
 addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-sx;if(!moved&&Math.abs(dx)>5){moved=true;track.classList.add('dragging')}if(moved)track.scrollLeft=sl-dx});
 addEventListener('pointerup',()=>{if(!down)return;down=false;if(moved){track.classList.remove('dragging');go(nearest())}});
 track.addEventListener('click',e=>{if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
 track.addEventListener('dragstart',e=>e.preventDefault());
 let st;track.addEventListener('scroll',()=>{if(down)return;clearTimeout(st);st=setTimeout(()=>{if(expand&&canHover)return;const n=nearest();if(n!==i){mark(n);restart()}},140)},{passive:true});
 new IntersectionObserver((en,o)=>{if(en[0].isIntersecting){started=true;mark(i);restart();o.disconnect()}},{threshold:.3}).observe(sec);
 /* avis : « Lire la suite » quand le texte est coupé */
 sec.querySelectorAll('.rv-card').forEach(c=>{const q=c.querySelector('.rv-text'),bt=c.querySelector('.rv-more');if(!q||!bt)return;const chk=()=>{bt.hidden=!(q.scrollHeight>q.clientHeight+2)&&!c.classList.contains('open')};chk();addEventListener('resize',chk);bt.addEventListener('click',()=>{const o=c.classList.toggle('open');bt.textContent=o?(document.documentElement.lang==='fr'?'Réduire':'Show less'):(document.documentElement.lang==='fr'?'Lire la suite':'Read more');bt.hidden=false})});
});})();
/* Accueil : frise qui se remplit au défilement */
(()=>{const f=document.querySelector('[data-frise]');if(!f)return;const steps=[...f.querySelectorAll('.fr-step')],wrap=f.querySelector('.fr-wrap');
 const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;let raf=0;
 const upd=()=>{raf=0;const r=wrap.getBoundingClientRect(),vh=innerHeight;let p=(vh*0.75-r.top)/(r.height+vh*0.15);p=Math.max(0,Math.min(1,p));if(reduce)p=1;wrap.style.setProperty('--p',p);steps.forEach((s,k)=>s.classList.toggle('lit',p>=(k/(steps.length-1))*0.92+0.02||reduce));};
 addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(upd)},{passive:true});addEventListener('resize',upd);upd();})();
/* Accueil : cartes à retourner */
(()=>{const fl=[...document.querySelectorAll('.flip')];if(!fl.length)return;const hov=matchMedia('(hover:hover)').matches;
 const set=(b,on)=>{fl.forEach(x=>{const v=x===b&&on;x.classList.toggle('flipped',v);x.setAttribute('aria-pressed',String(v))});};
 fl.forEach(b=>{if(hov){b.addEventListener('mouseenter',()=>set(b,true));b.addEventListener('mouseleave',()=>set(b,false));b.addEventListener('click',()=>set(b,true));}
  else b.addEventListener('click',()=>set(b,!b.classList.contains('flipped')));
  b.addEventListener('blur',()=>{if(!hov)return;set(b,false)});});})();
/* Accueil : « Tous les intérieurs », la photo et le point actif suivent le défilement */
(()=>{const s=document.querySelector('[data-interieurs]');if(!s)return;const pts=[...s.querySelectorAll('.it-pt')],phs=[...s.querySelectorAll('.it-ph')],bar=s.querySelector('.it-bar');let cur=0,raf=0;
 const set=n=>{if(n===cur)return;cur=n;pts.forEach((p,k)=>p.classList.toggle('on',k===n));phs.forEach((p,k)=>p.classList.toggle('on',k===n));};
 const upd=()=>{raf=0;if(getComputedStyle(s.querySelector('.it-sticky')).position!=='sticky')return;const r=s.getBoundingClientRect(),tot=r.height-innerHeight;let p=tot>0?-r.top/tot:0;p=Math.max(0,Math.min(1,p));bar&&bar.style.setProperty('--p',p);set(Math.min(pts.length-1,Math.floor(p*pts.length*0.999)));};
 addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(upd)},{passive:true});addEventListener('resize',upd);upd();})();
/* Zones desservies : sélecteur de villes (onglets) */
(()=>{const box=document.querySelector('[data-vx]');if(!box)return;const tabs=[...box.querySelectorAll('.vx-tab')],panels=[...box.querySelectorAll('.vx-panel')];
 const show=(id,focus,scroll)=>{const k=panels.findIndex(p=>p.id===id);if(k<0)return;tabs.forEach((t,j)=>{const on=j===k;t.classList.toggle('on',on);t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1});
  panels.forEach((p,j)=>{const on=j===k;p.hidden=!on;p.classList.toggle('on',on);if(on){p.style.animation='none';void p.offsetWidth;p.style.animation='';p.querySelectorAll('.vx-card,.vx-photo img').forEach(c=>{c.style.animation='none';void c.offsetWidth;c.style.animation=''})}});
  tabs[k].scrollIntoView({block:'nearest',inline:'center',behavior:'smooth'});if(focus)tabs[k].focus();if(scroll)box.scrollIntoView({block:'start'});
  if(history.replaceState)history.replaceState(null,'','#'+id);};
 tabs.forEach((t,j)=>{t.addEventListener('click',()=>show(t.getAttribute('aria-controls')));t.addEventListener('keydown',e=>{let n=null;if(e.key==='ArrowRight')n=(j+1)%tabs.length;if(e.key==='ArrowLeft')n=(j-1+tabs.length)%tabs.length;if(e.key==='Home')n=0;if(e.key==='End')n=tabs.length-1;if(n!==null){e.preventDefault();show(tabs[n].getAttribute('aria-controls'),true)}})});
 const h=location.hash.slice(1);if(h&&panels.some(p=>p.id===h))setTimeout(()=>show(h,false,true),60);
 addEventListener('hashchange',()=>{const h=location.hash.slice(1);if(panels.some(p=>p.id===h))show(h,false,true)});})();

/* Camion mascotte : il entre en roulant quand sa section apparaît */
(()=>{const s=[...document.querySelectorAll('.truck-stage')];if(!s.length)return;const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.35});s.forEach(x=>io.observe(x));})();

/* Barre A → B : le camion « roule » (léger cahot) pendant le défilement */
(()=>{const t=document.querySelector('.rail-mini');if(!t)return;let tm;addEventListener('scroll',()=>{t.classList.add('moving');clearTimeout(tm);tm=setTimeout(()=>t.classList.remove('moving'),220)},{passive:true});})();
