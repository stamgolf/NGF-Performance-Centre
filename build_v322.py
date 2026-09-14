p='c226/index.html'
s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)

# A/B. labels + categorieboom opschonen (migratie, eenmalig)
rep('''  if(!state.tourLabels||!state.tourLabels.length)state.tourLabels=defaultTourLabels();''',
'''  if(!state.tourLabels||!state.tourLabels.length)state.tourLabels=defaultTourLabels();
  if(!state.tourLabelsV322){state.tourLabelsV322=1;/* v322: leeftijdscategorieën = TAX_CATS (U15/U21 erbij), eigen extra labels blijven achteraan */var _std=defaultTourLabels();var _extra=(state.tourLabels||[]).filter(function(l){return _std.indexOf(l)<0;});state.tourLabels=_std.concat(_extra);}
  if(!state.tourCatTreeV322){state.tourCatTreeV322=1;/* v322: oude filtercategorieën (WK/EK, Jeugdtour …) uit de MJOP-ladder halen */if(state.tourCatTree&&state.tourCatTree.length){var _std2={};defaultTourCatTree().forEach(function(g){g.subs.forEach(function(x){_std2[String(x).toLowerCase()]=1;});});var _leg={};Object.keys(TAX_MIGRATIE).forEach(function(k){_leg[k]=1;});TOURCAT_EXTRA.forEach(function(k){_leg[String(k).toLowerCase()]=1;});var _geen=state.tourCatTree.find(function(g){return g.k==="geen";});state.tourCatTree.forEach(function(g){if(g.k==="geen")return;g.subs=g.subs.filter(function(x){var k=String(x).toLowerCase();if(_std2[k])return true;if(_leg[k])return false;if(_geen&&_geen.subs.indexOf(x)<0)_geen.subs.push(x);return false;});});}tourCatSync();}''')
# tourCatTree: onbekende (oude) categorieën niet meer in laag 4 stoppen
rep('''  (state.tourCats||[]).forEach(function(c){if(c&&!known[String(c).toLowerCase()]){t[3].subs.push(String(c));known[String(c).toLowerCase()]=1;}});''',
'''  var _gn=t.find(function(g){return g.k==="geen";})||t[t.length-1];
  (state.tourCats||[]).forEach(function(c){var k=String(c||"").toLowerCase();if(!c||known[k])return;if(TAX_MIGRATIE[k]!=null||TOURCAT_EXTRA.some(function(x){return String(x).toLowerCase()===k;}))return;_gn.subs.push(String(c));known[k]=1;});''')

# C. bibliotheek: editie aanmaken vanuit de lijst
rep('''    function itemHtml(d){var t=[];if(d.klasse)t.push("Klasse "+esc(d.klasse));if(d.cat)t.push(esc(d.cat));(d.labels||[]).forEach(function(l){t.push(esc(l));});return '<button class="bkpitem" data-def="'+d.id+'"><b>'+esc(d.name)+'</b>'+(t.length?' <small class="muted">'+t.join(" \\u00b7 ")+'</small>':'')+'</button>';}''',
'''    function itemHtml(d){var t=[];if(d.klasse)t.push("Klasse "+esc(d.klasse));if(d.cat)t.push(esc(d.cat));(d.labels||[]).forEach(function(l){t.push(esc(l));});var nEd=(state.tourEditions||[]).filter(function(e){return e.defId===d.id&&e.year===planYear;}).length;return '<div class="lbrow"><button class="bkpitem" data-def="'+d.id+'"><b>'+esc(d.name)+'</b>'+(t.length?' <small class="muted">'+t.join(" \\u00b7 ")+'</small>':'')+(nEd?' <span class="rtag">'+nEd+'× '+planYear+'</span>':'')+'</button>'+(rolIsSpeler()?'':'<button class="xbtn sm" data-newed="'+d.id+'" title="Editie aanmaken in '+planYear+'" aria-label="Editie aanmaken" style="font-size:15px;font-weight:700">+</button>')+'</div>';}''')
rep('''    sh.querySelectorAll("[data-def]").forEach(function(b){b.onclick=function(){openDefForm(b.dataset.def);};});
  }''','''    sh.querySelectorAll("[data-def]").forEach(function(b){b.onclick=function(){openDefForm(b.dataset.def);};});
    sh.querySelectorAll("[data-newed]").forEach(function(b){b.onclick=function(ev){ev.stopPropagation();newEditionFromDef(b.dataset.newed);};});
  }''')

# D. coach: eigen toernooi in de kalender, coach-dagen oranje, overige dagen gedimd
rep('''  if(pid){if(!(ed.participants||{})[pid])return;}else if(!wie.length)return;
  var m=edMeta(ed);var d=(ed.start>van?ed.start:van),last=(e<tot?e:tot);
  while(d<=last){var _lg=(pid||edCoachDag(ed,d))?"wed":"swed";if(L[_lg])out.push({date:d,laag:_lg,tijd:"",tot:"",naam:m.name,sub:pid?"Wedstrijd":((wie.length===1?nameOf(wie[0]):wie.length+" spelers")+(_lg==="wed"?" · coach aanwezig":"")),open:"ed",id:ed.id});d=dAddDays(d,1);}});''',
'''  var _eigen=(!pid&&!wie.length);/* v322: toernooi zonder deelnemers = eigen coachtoernooi */
  if(pid){if(!(ed.participants||{})[pid])return;}
  var m=edMeta(ed);var d=(ed.start>van?ed.start:van),last=(e<tot?e:tot);
  while(d<=last){var _cd=edCoachDag(ed,d);var _lg=(pid||_cd)?"wed":"swed";
   if(_eigen){if(L.wed)out.push({date:d,laag:"wed",dim:!_cd,tijd:"",tot:"",naam:m.name,sub:_cd?"coach aanwezig":"niet aanwezig",open:"ed",id:ed.id});}
   else if(L[_lg])out.push({date:d,laag:_lg,tijd:"",tot:"",naam:m.name,sub:pid?"Wedstrijd":((wie.length===1?nameOf(wie[0]):wie.length+" spelers")+(_lg==="wed"?" · coach aanwezig":"")),open:"ed",id:ed.id});
   d=dAddDays(d,1);}});''')
# dim in maand/week/lijst
rep('''.map(function(i){return '<em style="'+calBlokStyle(CAL_KLEUR[i.laag],i.laag==="wed")+'">'+(i.tijd?i.tijd+" ":"")+esc(i.naam)+'</em>';}).join("")''',
    '''.map(function(i){return '<em style="'+calBlokStyle(CAL_KLEUR[i.laag],i.laag==="wed"&&!i.dim)+(i.dim?';opacity:.55':'')+'">'+(i.tijd?i.tijd+" ":"")+esc(i.naam)+'</em>';}).join("")''')
rep('''laag==="wed")+'">'+esc(i.naam)+'</span>';los++;return;}''','''laag==="wed"&&!i.dim)+(i.dim?';opacity:.55':'')+'">'+esc(i.naam)+'</span>';los++;return;}''')
# na opslaan van een nieuw toernooi zonder deelnemers (coach): meteen het toernooivenster openen om dagen te markeren
rep('''  save();closeSheet();planYear=d.year;renderPlanning();toast("Toernooi opgeslagen \\u2713");
}''','''  save();closeSheet();planYear=d.year;renderPlanning();toast("Toernooi opgeslagen \\u2713");
  if(!rolIsSpeler()&&edIsNew&&!Object.keys(d.participants||{}).length){setTimeout(function(){try{editionDetail(d.id);toast("Markeer de dagen waarop je aanwezig bent");}catch(e){}},80);}
}''')
css='''/* v322: bibliotheekrij met +-knop */
.lbrow{display:flex;align-items:center;gap:6px;margin-bottom:6px}
.lbrow .bkpitem{flex:1;margin-bottom:0}
'''
rep('/* v318: lege staten zonder iconen */',css+'/* v318: lege staten zonder iconen */')
s=s.replace('const APP_VERSION="v321";','const APP_VERSION="v322";')
open(p,'w',encoding='utf-8').write(s)
w=open('c226/sw.js').read();open('c226/sw.js','w').write(w.replace('jo-ladder-v321','jo-ladder-v322'))
print('ok')
