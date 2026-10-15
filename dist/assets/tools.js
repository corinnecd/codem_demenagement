/* CODEM : outils interactifs des pages intérieures (orientation, jamais de prix) */
(()=>{'use strict';
const en=document.documentElement.lang==='en';const tr=(a,b)=>en?b:a;
const DEVIS=en?'/en/quote/':'/fr/devis/';
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const qs=(o)=>new URLSearchParams(Object.entries(o).filter(([,v])=>v!==''&&v!=null)).toString();
const val=(f,n)=>f.querySelector(`[name="${n}"]:checked`)?.value;
document.addEventListener('change',e=>{const q=e.target.closest('.tool-q');if(q)q.classList.toggle('done',!!q.querySelector(':checked'));});
const reveal=(res)=>{res.hidden=false;res.classList.remove('pop');void res.offsetWidth;res.classList.add('pop');};

/* Quiz « Quelle formule ? » */
const quiz=document.querySelector('[data-tool="quiz-formule"]');
if(quiz){const f=quiz.querySelector('form'),res=quiz.querySelector('.tool-result');
 const F={self:['Self','Vous emballez et préparez vos meubles ; CODEM protège, charge et transporte.','You pack and prepare furniture; CODEM protects, loads and transports.'],'self-plus':['Self plus','Vous faites les cartons ; CODEM démonte, remonte et met en place le mobilier.','You pack; CODEM dismantles, reassembles and places furniture.'],confort:['Confort','CODEM emballe aussi le fragile et fournit les emballages.','CODEM also packs fragile items and supplies materials.'],'confort-plus':['Confort plus','CODEM emballe tout ; vous ne déballez que le non-fragile.','CODEM packs everything; you only unpack non-fragile items.'],'grand-confort':['Grand Confort','CODEM s’occupe de tout, jusqu’au dernier carton déballé.','CODEM handles everything, down to the last box.']};
 const quizQuery=k=>{const p=new URLSearchParams([['service','particulier'],['formule',k]]);const e=val(f,'emballage'),m=val(f,'meubles'),a=val(f,'arrivee');if(e==='fragile')p.append('prestation','fragiles');if(e==='tout')p.append('prestation','emballage');if(m==='codem')p.append('prestation','demontage');const dl={moi:'Déballage par le client',fragile:'Déballage : CODEM, le fragile',tout:'Déballage : CODEM, tout'}[a];if(dl)p.set('objets',dl);return p.toString();};
 const pick=()=>{const e=val(f,'emballage'),m=val(f,'meubles'),a=val(f,'arrivee');if(!e||!m||!a)return null;
  if(e==='moi')return m==='moi'?'self':'self-plus';if(e==='fragile')return 'confort';return a==='tout'?'grand-confort':'confort-plus';};
 f.addEventListener('change',()=>{const k=pick();quiz.querySelectorAll('.tool-q').forEach(q=>q.classList.toggle('done',!!q.querySelector(':checked')));if(!k)return;const [n,fr,e]=F[k];
  res.querySelector('[data-out=name]').textContent=n;res.querySelector('[data-out=desc]').textContent=tr(fr,e);res.querySelector('[data-out=cta]').href=`${DEVIS}?${quizQuery(k)}`;reveal(res);
  document.querySelectorAll('.pc-card').forEach(c=>c.classList.toggle('pc-pick',c.dataset.slug===k));const see=quiz.querySelector('[data-quiz-see]');if(see)see.onclick=ev=>{const c=document.querySelector('.pc-card[data-slug="'+k+'"]');if(!c)return;ev.preventDefault();c.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center',inline:'center'});c.classList.remove('pc-flash');void c.offsetWidth;c.classList.add('pc-flash');};const r=document.querySelector('#ft-range');if(r){r.value=['self','self-plus','confort','confort-plus','grand-confort'].indexOf(k);r.dispatchEvent(new Event('input'));}});
 quiz.querySelector('.tool-reset').addEventListener('click',()=>{f.reset();res.hidden=true;quiz.querySelectorAll('.tool-q').forEach(q=>q.classList.remove('done'));});}

/* Test monte-meubles */
const mt=document.querySelector('[data-tool="test-monte"]');
if(mt){const f=mt.querySelector('form'),res=mt.querySelector('.tool-result');const lab=n=>f.querySelector(`[name="${n}"]:checked`)?.nextElementSibling.textContent||'';
 f.addEventListener('change',()=>{mt.querySelectorAll('.tool-q').forEach(q=>q.classList.toggle('done',!!q.querySelector(':checked')));
  const e=val(f,'etage'),w=val(f,'fenetre'),s=val(f,'stationnement'),o=val(f,'objets');if(!e||!w||!s||!o)return;
  let ok=w==='oui'&&s!=='non'&&e!=='6+';
  res.querySelector('[data-out=name]').textContent=ok?tr('Faisable a priori','Likely feasible'):tr('À étudier avec un conseiller','To review with an adviser');
  res.querySelector('[data-out=desc]').textContent=ok?tr('Votre configuration se prête au monte-meubles. Le conseiller confirme l’équipement, le créneau et l’autorisation de stationnement.','Your setup suits a furniture lift. The adviser confirms equipment, timing and parking permit.'):tr('Certains points demandent une vérification sur place : hauteur, ouverture ou stationnement. Une étude gratuite permet de trouver la bonne solution.','Some points need an on-site check: height, opening or parking. A free assessment finds the right solution.');
  const et={'1-2':'2','3-5':'4','6+':'6+'}[e];const ob={canape:tr('Canapé, armoire','Sofa, wardrobe'),piano:'Piano',tout:tr('Déménagement complet','Full move')}[o];
  res.querySelector('[data-out=cta]').href=`${DEVIS}?${qs({service:'monte-meubles',etage:et,prestation:'monte-meubles',objets:`${ob}, ${tr('fenêtre côté rue','street-side window')} : ${lab('fenetre')}, ${tr('stationnement','parking')} : ${lab('stationnement')}`})}`;reveal(res);});
 mt.querySelector('.tool-reset').addEventListener('click',()=>{f.reset();res.hidden=true;mt.querySelectorAll('.tool-q').forEach(q=>q.classList.remove('done'));});}

/* Jauge d'étages du monte-meubles (avancement au scroll) */
const lift=document.querySelector('.lift-band');
if(lift){const cab=lift.querySelector('.lift-cab'),read=lift.querySelector('[data-lift-floor]'),floors=[...lift.querySelectorAll('.lift-gauge li')];
 const upd=()=>{const r=lift.getBoundingClientRect();const p=Math.min(1,Math.max(0,(innerHeight-r.top)/(innerHeight+r.height*.4)));const n=Math.round(p*6);
  cab.style.bottom=`calc(${(n/6)*86}% + 4%)`;read.textContent=n?`${n}${n>1?tr('e étage','th floor'):tr('er étage','st floor')}`:tr('RDC','Ground floor');
  floors.forEach(li=>li.classList.toggle('lit',li.dataset.floor&&+li.dataset.floor<=n));};
 addEventListener('scroll',()=>requestAnimationFrame(upd),{passive:true});upd();}

/* Destinations France & Europe */
const dt=document.querySelector('.dest-tool');
if(dt){const name=dt.querySelector('[data-dest-name]'),cities=dt.querySelector('[data-dest-cities]'),country=dt.querySelector('[data-dest-country]'),card=dt.querySelector('.dest-card'),city=dt.querySelector('#dest-city');
 const go=()=>{card.classList.remove('go');void card.offsetWidth;card.classList.add('go');};
 dt.querySelectorAll('.dest').forEach(b=>b.addEventListener('click',()=>{dt.querySelectorAll('.dest').forEach(x=>x.classList.toggle('on',x===b));name.textContent=b.dataset.country;cities.textContent=b.dataset.cities;country.value=b.dataset.country;go();city.focus({preventScroll:true});}));
 city.addEventListener('input',()=>{if(city.value.trim().length>2){name.textContent=city.value.trim()+(country.value?`, ${country.value}`:'');if(!card.classList.contains('go'))go();}});}

/* Mini-formulaire entreprise */
const b2b=document.querySelector('.b2b-form');
if(b2b)b2b.addEventListener('submit',()=>{const p=b2b.querySelector('[data-b2b=postes]').value;b2b.querySelector('[data-b2b-objets]').value=p?`${p} ${tr('postes de travail','workstations')}`:'';b2b.querySelector('[data-b2b-contraintes]').value=b2b.querySelector('[data-b2b=horaires]').checked?tr('Intervention hors horaires souhaitée (soir, week-end)','Out-of-hours work requested (evening, weekend)'):'';[...b2b.elements].forEach(e=>{if(e.name&&!e.value)e.disabled=true;});setTimeout(()=>[...b2b.elements].forEach(e=>e.disabled=false),500);});

/* Box garde-meubles */
const bx=document.querySelector('.box-tool');
if(bx){const r=bx.querySelector('#box-range'),fill=bx.querySelector('.box-fill'),m3=bx.querySelector('[data-box-m3]'),hint=bx.querySelector('[data-box-hint]'),vol=bx.querySelector('[data-box-volume]'),f=bx.querySelector('form');
 const H=[[5,'Quelques meubles et cartons','A few items and boxes'],[12,'Un studio ou un T1','A studio'],[25,'Un T2 – T3','A 2–3 room flat'],[40,'Un T4 ou une petite maison','A 4-room flat or small house'],[61,'Une maison','A house']];
 const upd=()=>{const v=+r.value;fill.style.height=`${(v/60)*100}%`;m3.textContent=`${v} m³`;vol.value=v;const h=H.find(x=>v<x[0]);hint.textContent=tr('Environ : ','About: ')+tr(h[1],h[2]);r.style.setProperty('--v',(v-2)/58);};
 r.addEventListener('input',upd);upd();}

/* Fiche objet */
const ob=document.querySelector('.objet-form');
if(ob)ob.addEventListener('submit',()=>{const ty=val(ob,'type')||'';const d=ob.querySelector('[data-objet=dim]').value;ob.querySelector('[data-objet-out]').value=[ty,d&&`${tr('dimensions','size')} ${d}`].filter(Boolean).join(', ');[...ob.elements].forEach(e=>{if(e.name&&!e.value)e.disabled=true;});setTimeout(()=>[...ob.elements].forEach(e=>e.disabled=false),500);});

/* Zones : recherche de commune */
const zt=document.querySelector('.zone-tool');
if(zt){const f=zt.querySelector('form'),inp=f.querySelector('input'),ans=zt.querySelector('.zone-answer');
 const IDF={'75':'Paris','77':'Seine-et-Marne','78':'Yvelines','91':'Essonne','92':'Hauts-de-Seine','93':'Seine-Saint-Denis','94':'Val-de-Marne','95':'Val-d’Oise'};
 f.addEventListener('submit',e=>{e.preventDefault();const q=inp.value.trim();if(!q){inp.focus();return;}
  const cp=(q.match(/\b(\d{5})\b/)||[])[1];const dep=cp?cp.slice(0,2):null;let title,text;
  if(dep&&IDF[dep]){title=tr(`Oui, CODEM intervient ${dep==='75'?'à Paris':'en '+IDF[dep]}.`,`Yes, CODEM covers ${IDF[dep]}.`);text=tr('Nous sommes basés à Nogent-sur-Marne : votre commune fait partie de notre zone d’intervention en Île-de-France.','We are based in Nogent-sur-Marne: your town is within our Greater Paris area.');}
  else if(cp){title=tr('Oui, CODEM étudie votre trajet.','Yes, CODEM will review your route.');text=tr('Nous organisons des déménagements au départ de toute la France, vers la France ou l’Europe. Le conseiller confirme les modalités.','We organise moves from anywhere in France, to France or Europe. The adviser confirms arrangements.');}
  else{title=tr(`${q} : parlons de votre trajet.`,`${q}: let’s talk about your route.`);text=tr('CODEM dessert l’Île-de-France et étudie les déménagements partout en France et en Europe. Ajoutez votre code postal pour une réponse précise.','CODEM serves Greater Paris and reviews moves across France and Europe. Add your postcode for a precise answer.');}
  ans.querySelector('[data-zone-title]').textContent=title;ans.querySelector('[data-zone-text]').textContent=text;ans.querySelector('[data-zone-cta]').href=`${DEVIS}?${qs({service:'particulier',depart:q})}`;ans.hidden=false;ans.classList.remove('go');void ans.offsetWidth;ans.classList.add('go');});}

/* Checklist */
const ck=document.querySelector('.checklist');
if(ck){const boxes=[...ck.querySelectorAll('[data-ck]')],bar=ck.querySelector('.ck-bar span'),cnt=ck.querySelector('[data-ck-count]');const K='codem-checklist';
 let saved=[];try{saved=JSON.parse(localStorage.getItem(K)||'[]');}catch{}
 boxes.forEach(b=>{b.checked=saved.includes(+b.dataset.ck);});
 const upd=()=>{const on=boxes.filter(b=>b.checked);cnt.textContent=on.length;bar.style.width=`${on.length/boxes.length*100}%`;try{localStorage.setItem(K,JSON.stringify(on.map(b=>+b.dataset.ck)));}catch{}};
 ck.addEventListener('change',upd);upd();ck.querySelector('[data-ck-print]')?.addEventListener('click',()=>print());}

/* Contact : ouvert maintenant ? (heure de Paris) */
const ob2=document.querySelector('[data-open]');
if(ob2){const parts=Object.fromEntries(new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Paris',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()).map(p=>[p.type,p.value]));
 const d=parts.weekday,m=+parts.hour*60+ +parts.minute;const wk=['Mon','Tue','Wed','Thu'].includes(d);
 const open=(wk&&((m>=540&&m<720)||(m>=780&&m<1080)))||(d==='Fri'&&((m>=540&&m<720)||(m>=780&&m<1020)));
 ob2.hidden=false;ob2.classList.add(open?'is-open':'is-closed');
 ob2.innerHTML=open?`<span class="dot"></span>${tr('Ouvert maintenant · un conseiller vous répond','Open now · an adviser will answer')}`:`<span class="dot"></span>${tr('Fermé actuellement · demandez un rappel, nous vous recontactons dès l’ouverture','Closed now · request a callback, we’ll call when we open')}`;}
})();
/* Le guide CODEM : filtre par thème + sommaire actif */
(()=>{const h=document.querySelector('.guide-hub');if(h){const chips=[...h.querySelectorAll('[data-gfilter]')],cards=[...h.querySelectorAll('.gcard')],more=h.querySelector('[data-gmore]'),lim=+(h.querySelector('.ggrid').dataset.limit||0);let open=false,f='all';const fr=document.documentElement.lang!=='en',lab0=more?more.textContent:'';
 const apply=()=>{let n=0;cards.forEach(k=>{const ok=f==='all'||k.dataset.theme===f;const show=ok&&(open||f!=='all'||!lim||n<lim);if(ok)n++;k.hidden=!show});if(more){more.parentNode.hidden=f!=='all'||!lim||cards.length<=lim;more.textContent=open?(fr?'Voir moins':'Show less'):lab0;more.setAttribute('aria-expanded',String(open))}};
 chips.forEach(c=>c.addEventListener('click',()=>{f=c.dataset.gfilter;chips.forEach(x=>{x.classList.toggle('on',x===c);x.setAttribute('aria-pressed',String(x===c))});apply()}));
 if(more)more.addEventListener('click',()=>{open=!open;apply();if(open){cards[lim]&&cards[lim].focus()}else{const y=h.getBoundingClientRect().top;if(y<0)scrollBy({top:y-90,behavior:'smooth'})}});apply();}
 const toc=document.querySelector('.ga-toc');if(!toc||!('IntersectionObserver' in window))return;const items=[...toc.querySelectorAll('li')];
 const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){items.forEach(li=>li.classList.toggle('on',li.querySelector('a').getAttribute('href')==='#'+e.target.id))}})},{rootMargin:'-30% 0px -60% 0px'});
 document.querySelectorAll('.ga-sec[id]').forEach(s=>io.observe(s));})();
/* Questions : centre d'aide (recherche + thèmes + une seule réponse ouverte) */
(()=>{document.querySelectorAll('[data-help]').forEach(sec=>{const rows=[...sec.querySelectorAll('.hc-row')],ths=[...sec.querySelectorAll('.hc-th')],inp=sec.querySelector('#hc-input'),title=sec.querySelector('.hc-title'),empty=sec.querySelector('.hc-empty'),list=sec.querySelector('.hc-list');
 const fr=document.documentElement.lang!=='en';let f='top';
 const norm=s=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[’']/g,' ');
 const close=()=>rows.forEach(r=>{r.classList.remove('open');r.querySelector('.hc-q').setAttribute('aria-expanded','false');r.querySelector('.hc-a').hidden=true});
 const apply=()=>{const q=norm(inp.value.trim());close();let shown=[];
  rows.forEach(r=>{const ok=q?norm(r.textContent).includes(q):f==='top'?r.dataset.top!==undefined:r.dataset.theme===f;r.hidden=!ok;r.classList.toggle('tagged',!!q||f==='top');if(ok)shown.push(r)});
  if(f==='top'&&!q)shown.sort((a,b)=>a.dataset.top-b.dataset.top).forEach(r=>list.insertBefore(r,empty));
  const lab=ths.find(x=>x.dataset.hc===f);title.textContent=q?(fr?`${shown.length} résultat${shown.length>1?'s':''} pour « ${inp.value.trim()} »`:`${shown.length} result${shown.length>1?'s':''} for “${inp.value.trim()}”`):(f==='top'?(fr?'Les questions les plus posées':'Most asked questions'):lab.firstChild.textContent);
  empty.hidden=shown.length>0;};
 ths.forEach(b=>b.addEventListener('click',()=>{f=b.dataset.hc;inp.value='';ths.forEach(x=>{x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',String(x===b))});apply()}));
 let tm;inp.addEventListener('input',()=>{clearTimeout(tm);tm=setTimeout(apply,120)});
 rows.forEach(r=>{const btn=r.querySelector('.hc-q');btn.addEventListener('click',()=>{const was=r.classList.contains('open');close();if(!was){r.classList.add('open');btn.setAttribute('aria-expanded','true');r.querySelector('.hc-a').hidden=false;const y=r.getBoundingClientRect().top;if(y<90)scrollBy({top:y-110,behavior:'smooth'})}})});
 apply();});})();
/* Formulaires : bouton pour intervertir départ et arrivée */
(()=>{const fr=document.documentElement.lang!=='en';
 const PAIRS=[['depart','arrivee'],['depart_commune','arrivee_commune'],['depart_pays','arrivee_pays']];
 function setup(form){if(form.dataset.swap)return;const a=form.querySelector('input[name=depart],input[name=depart_commune]'),b=form.querySelector('input[name=arrivee],input[name=arrivee_commune]');if(!a||!b)return;form.dataset.swap='1';
  const btn=document.createElement('button');btn.type='button';btn.className='swap-btn';btn.setAttribute('aria-label',fr?'Intervertir départ et arrivée':'Swap departure and arrival');btn.title=btn.getAttribute('aria-label');
  btn.innerHTML='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 4v14M7 18l-3-3M7 18l3-3M17 20V6M17 6l-3 3M17 6l3 3"/></svg>';
  if(getComputedStyle(form).position==='static')form.style.position='relative';form.appendChild(btn);
  const place=()=>{if(!a.offsetParent||!b.offsetParent){btn.hidden=true;return}btn.hidden=false;const fr_=form.getBoundingClientRect(),ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect();const side=Math.abs(ra.top-rb.top)<10;btn.classList.toggle('h',side);
   if(side){btn.style.left=((ra.right+rb.left)/2-fr_.left-17)+'px';btn.style.top=(ra.top+ra.height/2-fr_.top-17)+'px'}else{btn.style.left=(Math.max(ra.right,rb.right)-fr_.left-17-44)+'px';btn.style.top=((ra.bottom+rb.top)/2-fr_.top-17)+'px'}};
  btn.addEventListener('click',()=>{PAIRS.forEach(([x,y])=>{const p=form.querySelector(`[name=${x}]`),q=form.querySelector(`[name=${y}]`);if(!p||!q||p.type==='hidden')return;const v=p.value;p.value=q.value;q.value=v;[p,q].forEach(el=>{el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))})});btn.classList.remove('spin');void btn.offsetWidth;btn.classList.add('spin');try{window.track&&track('trajet_inverse')}catch{}});
  place();addEventListener('resize',place);new ResizeObserver(place).observe(form);form.addEventListener('input',()=>requestAnimationFrame(place));document.addEventListener('click',()=>setTimeout(place,60));}
 const scan=()=>document.querySelectorAll('form').forEach(setup);scan();
 new MutationObserver(m=>{if(m.some(r=>r.addedNodes.length))scan()}).observe(document.body,{childList:true,subtree:true});})();
/* Bouton « Retour » : page précédente du site si elle existe */
(()=>{document.querySelectorAll('[data-back]').forEach(a=>a.addEventListener('click',e=>{try{const r=document.referrer&&new URL(document.referrer);if(r&&r.origin===location.origin&&history.length>1){e.preventDefault();history.back()}}catch{}}))})();
/* Calculateur de volume : une seule pièce dépliée à la fois */
(()=>{const rooms=[...document.querySelectorAll('.vc-room')];rooms.forEach(r=>r.addEventListener('toggle',()=>{if(r.open)rooms.forEach(o=>{if(o!==r)o.open=false})}))})();
/* Arrivée sur le formulaire de rappel : mise en avant et curseur dans le champ Prénom */
(()=>{const go=()=>{if(location.hash!=='#callback-form')return;const f=document.getElementById('callback-form');if(!f)return;f.classList.add('hl');setTimeout(()=>f.classList.remove('hl'),2200);const i=f.querySelector('input:not([type=hidden]):not([name=website])');if(i)setTimeout(()=>i.focus({preventScroll:true}),350)};go();addEventListener('hashchange',go)})();
