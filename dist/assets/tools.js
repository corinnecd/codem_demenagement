/* CODEM — outils interactifs des pages intérieures (orientation, jamais de prix) */
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
 const pick=()=>{const e=val(f,'emballage'),m=val(f,'meubles'),a=val(f,'arrivee');if(!e||!m||!a)return null;
  if(e==='moi')return m==='moi'?'self':'self-plus';if(e==='fragile')return 'confort';return a==='tout'?'grand-confort':'confort-plus';};
 f.addEventListener('change',()=>{const k=pick();quiz.querySelectorAll('.tool-q').forEach(q=>q.classList.toggle('done',!!q.querySelector(':checked')));if(!k)return;const [n,fr,e]=F[k];
  res.querySelector('[data-out=name]').textContent=n;res.querySelector('[data-out=desc]').textContent=tr(fr,e);res.querySelector('[data-out=cta]').href=`${DEVIS}?${qs({service:'particulier',formule:k})}`;reveal(res);
  const r=document.querySelector('#ft-range');if(r){r.value=['self','self-plus','confort','confort-plus','grand-confort'].indexOf(k);r.dispatchEvent(new Event('input'));}});
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
  res.querySelector('[data-out=cta]').href=`${DEVIS}?${qs({service:'monte-meubles',etage:et,prestation:'monte-meubles',objets:`${ob} — ${tr('fenêtre côté rue','street-side window')} : ${lab('fenetre')}, ${tr('stationnement','parking')} : ${lab('stationnement')}`})}`;reveal(res);});
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
if(bx){const r=bx.querySelector('#box-range'),fill=bx.querySelector('.box-fill'),m3=bx.querySelector('[data-box-m3]'),hint=bx.querySelector('[data-box-hint]'),vol=bx.querySelector('[data-box-volume]'),ann=bx.querySelector('[data-box-annexes]'),f=bx.querySelector('form');
 const H=[[5,'Quelques meubles et cartons','A few items and boxes'],[12,'Un studio ou un T1','A studio'],[25,'Un T2 – T3','A 2–3 room flat'],[40,'Un T4 ou une petite maison','A 4-room flat or small house'],[61,'Une maison','A house']];
 const upd=()=>{const v=+r.value;fill.style.height=`${(v/60)*100}%`;m3.textContent=`${v} m³`;vol.value=v;const h=H.find(x=>v<x[0]);hint.textContent=tr('Environ : ','About: ')+tr(h[1],h[2]);r.style.setProperty('--v',(v-2)/58);};
 r.addEventListener('input',upd);upd();f.addEventListener('submit',()=>{ann.value=`${tr('Garde-meubles','Storage')} : ${val(f,'duree')||''}`;});}

/* Fiche objet */
const ob=document.querySelector('.objet-form');
if(ob)ob.addEventListener('submit',()=>{const ty=val(ob,'type')||'';const d=ob.querySelector('[data-objet=dim]').value;ob.querySelector('[data-objet-out]').value=[ty,d&&`${tr('dimensions','size')} ${d}`].filter(Boolean).join(' — ');[...ob.elements].forEach(e=>{if(e.name&&!e.value)e.disabled=true;});setTimeout(()=>[...ob.elements].forEach(e=>e.disabled=false),500);});

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
 ck.addEventListener('change',upd);upd();ck.querySelector('[data-ck-print]').addEventListener('click',()=>print());}

/* Contact : ouvert maintenant ? (heure de Paris) */
const ob2=document.querySelector('[data-open]');
if(ob2){const parts=Object.fromEntries(new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Paris',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()).map(p=>[p.type,p.value]));
 const d=parts.weekday,m=+parts.hour*60+ +parts.minute;const wk=['Mon','Tue','Wed','Thu'].includes(d);
 const open=(wk&&((m>=540&&m<720)||(m>=780&&m<1080)))||(d==='Fri'&&((m>=540&&m<720)||(m>=780&&m<1020)));
 ob2.hidden=false;ob2.classList.add(open?'is-open':'is-closed');
 ob2.innerHTML=open?`<span class="dot"></span>${tr('Ouvert maintenant · un conseiller vous répond','Open now · an adviser will answer')}`:`<span class="dot"></span>${tr('Fermé actuellement · demandez un rappel, nous vous recontactons dès l’ouverture','Closed now · request a callback, we’ll call when we open')}`;}
})();
