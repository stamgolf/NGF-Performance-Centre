p='c226/index.html'
s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)

# 1. lege staten: geen emoji, alleen subtiele tekst
css1='''/* v318: lege staten zonder iconen */
.empty .em{display:none}
.empty{padding:22px 18px;opacity:1}
.empty h3{margin:0 0 4px;font-family:var(--fd);font-weight:500;font-size:15px;color:var(--muted)}
.empty p{margin:4px 0 12px;font-size:13px;color:var(--muted)}
'''
# 2/4. spelers zonder team: registry-spelers tellen mee in allPlayers en de Spelers-tab
rep('function allPlayers(){var out=[];(state.teams||[]).forEach(function(t){(t.players||[]).forEach(function(p){out.push({id:p.id,name:p.name,teamId:t.id,teamName:t.name});});});return out.sort(',
    'function allPlayers(){var out=[],seen={};(state.teams||[]).forEach(function(t){(t.players||[]).forEach(function(p){if(seen[p.id])return;seen[p.id]=1;out.push({id:p.id,name:p.name,teamId:t.id,teamName:t.name});});});(state.players||[]).forEach(function(p){if(seen[p.id])return;seen[p.id]=1;out.push({id:p.id,name:p.name,teamId:null,teamName:""});});return out.sort(')
rep(''' (state.groups||[]).forEach(function(g){(g.playerIds||[]).forEach(function(pid){if(seen[pid])seen[pid].grpIds.push(g.id);});});''',
    ''' (state.players||[]).forEach(function(p){if(seen[p.id])return;var o={p:p,teams:[],teamIds:[],grpIds:[]};seen[p.id]=o;out.push(o);});
 (state.groups||[]).forEach(function(g){(g.playerIds||[]).forEach(function(pid){if(seen[pid])seen[pid].grpIds.push(g.id);});});''')
# Spelers-tab: + speler zonder team
rep(''' box.innerHTML='<div class="zoekkop"><div class="row" style="gap:8px;align-items:center"><input class="in zoekpil" id="splQ" autocomplete="off" placeholder="Zoek op naam…" value="'+esc(splF.q)+'">'+filterKnop("splFilterB",n)+'</div></div>'
  +'<div class="card" id="splList">'+splListHtml()+'</div>';''',
''' box.innerHTML='<div class="zoekkop"><div class="row" style="gap:8px;align-items:center"><input class="in zoekpil" id="splQ" autocomplete="off" placeholder="Zoek op naam…" value="'+esc(splF.q)+'">'+filterKnop("splFilterB",n)+(rolIsSpeler()?'':'<button class="xbtn" id="splAdd" title="Speler toevoegen" aria-label="Speler toevoegen" style="font-size:20px;font-weight:700">+</button>')+'</div></div>'
  +'<div class="card" id="splList">'+splListHtml()+'</div>';
 var _sa=$("#splAdd");if(_sa)_sa.onclick=function(){promptDlg("Speler toevoegen","Naam","",function(v){var nm=(v||"").trim();if(!nm)return;var ex=(state.players||[]).find(function(x){return (x.name||"").toLowerCase()===nm.toLowerCase();});if(ex){toast("Deze speler bestaat al");return;}var pid=uid();state.players.push({id:pid,name:nm,birthYear:"",gender:""});try{rehydrate();}catch(e){}save();renderSpelers();toast(nm+" toegevoegd \\u2713 \\u00b7 een team is niet nodig");});};''')
# speler-account: persoonlijk team zodat klassement/challenge/doelen werken
rep('''  state.rol="speler";state.rolSpeler=pid;state.onboarded=true;
  try{rehydrate();}catch(e){}save();''',
'''  state.rol="speler";state.rolSpeler=pid;state.onboarded=true;
  spelerEigenTeam(pid);
  try{rehydrate();}catch(e){}save();''')
rep('function rolPas(){var vast=rolSpelerId();',
'''/* v318: speler zonder team krijgt een eigen (persoonlijk) team, zodat challenge/klassement en doelen direct werken */
function spelerEigenTeam(pid){var p=registryPlayer(pid);if(!p)return null;state.teams=state.teams||[];
 var inT=state.teams.find(function(t){return (t.playerIds||[]).indexOf(pid)>=0;});if(inT)return inT;
 var t={id:uid(),name:p.name||"Mijn team",playerIds:[pid],players:[],sessions:[],personal:true};state.teams.push(t);state.activeTeamId=t.id;try{rehydrate();}catch(e){}return t;}
function rolPas(){var vast=rolSpelerId();if(vast&&!state.kijkVanCoach){try{if(spelerEigenTeam(vast))save();}catch(e){}}''')

# 3. To-do: verwijderen (selectiemodus), aantal per week, handmatig samenstellen
rep(""" if(!plan){body='<div class="card"><h3 style="margin:0 0 6px">To-do deze week</h3><p class="muted" style="margin:0 0 10px">Nog geen weekplan. De generator gebruikt het weekrooster (Golf (Z)- en Fysiek (Z)-tijd), de fase en de focus.</p><button class="btn block blue" id="tpGen">Genereer weekplan</button></div>';}""",
"""  if(!plan){body='<div class="card"><h3 style="margin:0 0 6px">To-do deze week</h3><p class="muted" style="margin:0 0 10px">Nog geen weekplan. Laat de generator een plan maken (weekrooster, fase en focus) of stel de lijst zelf samen.</p><div class="edacts" style="margin-top:0"><button class="btn blue" id="tpGen">Genereer weekplan</button><button class="btn ghost" id="tpHand">Handmatig samenstellen</button></div></div>';}""")
rep(""" var gen=$("#tpGen");if(gen)gen.onclick=function(){var p=genWeekPlan(pid,ws);state.trainPlans=state.trainPlans||[];state.trainPlans.push(p);save();renderPlanning();toast("Weekplan gegenereerd ✓");};""",
""" var gen=$("#tpGen");if(gen)gen.onclick=function(){var p=genWeekPlan(pid,ws);state.trainPlans=state.trainPlans||[];state.trainPlans.push(p);save();renderPlanning();toast("Weekplan gegenereerd ✓");};
 var hnd=$("#tpHand");if(hnd)hnd.onclick=function(){state.trainPlans=state.trainPlans||[];state.trainPlans.push({id:uid(),playerId:pid,weekStart:ws,phase:(wk&&wk.phase)||null,items:[],edited:true,manual:true,created:todayISO()});save();renderPlanning();toast("Lege lijst aangemaakt — voeg oefeningen toe met +");};""")
# rijen: aantal-chip + selectiemodus
rep("""  function _row(o){var x=o.it.x||1,dn=Math.min(o.it.doneN||0,x);var dots='';for(var i=0;i<x;i++)dots+='<i class="'+(i>=x-dn?'on':'')+'"></i>';return '<div class="tdtodo'+(itemFull(o.it)?' done':'')+'" data-open="'+o.d.id+'">'+tickBtnHtml(o.it,o.d.id)+'<span class="tdtnm">'+esc(o.d.title)+'</span>'+(o.d.always?'':whyChipHtml(drillReason(o.d,_wctxT)))+'<span class="tddots">'+dots+'</span></div>';}""",
"""  function _row(o,del){var x=o.it.x||1,dn=Math.min(o.it.doneN||0,x);var dots='';for(var i=0;i<x;i++)dots+='<i class="'+(i>=x-dn?'on':'')+'"></i>';
   if(del)return '<div class="tdtodo tpdel" data-sel="'+o.d.id+'"><span class="tpselbox"></span><span class="tdtnm">'+esc(o.d.title)+'</span><span class="sx">'+x+'\\u00d7</span></div>';
   return '<div class="tdtodo'+(itemFull(o.it)?' done':'')+'" data-open="'+o.d.id+'">'+tickBtnHtml(o.it,o.d.id)+'<span class="tdtnm">'+esc(o.d.title)+'</span>'+(o.d.always?'':whyChipHtml(drillReason(o.d,_wctxT)))+'<button class="tprep" data-rep="'+o.d.id+'" title="Aantal keer deze week">'+x+'\\u00d7</button><span class="tddots">'+dots+'</span></div>';}""")
rep("""   return '<div class="card tpcol"><div class="cardhd"><h3><span class="cvdot" style="background:'+mcAccent(c[0])+'"></span>'+c[1]+'</h3><span class="row" style="gap:6px;align-items:center"><span class="hdnote">'+e2.d+'/'+e2.t+'</span><button class="xbtn sm" data-tpadd="'+c[0]+'" title="Oefening toevoegen" style="font-size:15px;font-weight:700">+</button></span></div><div class="tpkbar"><i style="width:'+p2+'%;background:'+mcAccent(c[0])+'"></i></div>'
    +(arr.length?arr.map(_row).join(""):'<p class="muted" style="margin:6px 0 0;font-size:12.5px">Geen oefeningen in deze categorie.</p>')+'</div>';}).join("");""",
"""   var del=(tpDelCat===c[0]+"|"+ws);
   return '<div class="card tpcol'+(del?' del':'')+'"><div class="cardhd"><h3><span class="cvdot" style="background:'+mcAccent(c[0])+'"></span>'+c[1]+'</h3><span class="row" style="gap:6px;align-items:center"><span class="hdnote">'+e2.d+'/'+e2.t+'</span>'+(arr.length?'<button class="xbtn sm'+(del?' on':'')+'" data-tpdel="'+c[0]+'" title="Oefeningen verwijderen" aria-label="Oefeningen verwijderen">'+TP_ICO_TRASH+'</button>':'')+'<button class="xbtn sm" data-tpadd="'+c[0]+'" title="Oefening toevoegen" style="font-size:15px;font-weight:700">+</button></span></div><div class="tpkbar"><i style="width:'+p2+'%;background:'+mcAccent(c[0])+'"></i></div>'
    +(arr.length?arr.map(function(o){return _row(o,del);}).join(""):'<p class="muted" style="margin:6px 0 0;font-size:12.5px">Geen oefeningen in deze categorie.</p>')
    +(del?'<div class="tpdelacts"><button class="btn sm" data-tpdelgo="'+c[0]+'" disabled>Verwijder</button><button class="btn ghost sm" data-tpdelx="'+c[0]+'">Klaar</button></div>':'')+'</div>';}).join("");""")
rep(""" box.querySelectorAll("[data-tpadd]").forEach(function(b){b.onclick=function(){openDrillPicker(pid,ws,b.dataset.tpadd);};});""",
""" box.querySelectorAll("[data-tpadd]").forEach(function(b){b.onclick=function(){openDrillPicker(pid,ws,b.dataset.tpadd);};});
 box.querySelectorAll("[data-tpdel]").forEach(function(b){b.onclick=function(){var k=b.dataset.tpdel+"|"+ws;tpDelCat=(tpDelCat===k)?null:k;renderPlanning();};});
 box.querySelectorAll("[data-tpdelx]").forEach(function(b){b.onclick=function(){tpDelCat=null;renderPlanning();};});
 box.querySelectorAll(".tpdel[data-sel]").forEach(function(r){r.onclick=function(){r.classList.toggle("sel");var col=r.closest(".tpcol");var n=col.querySelectorAll(".tpdel.sel").length;var go=col.querySelector("[data-tpdelgo]");if(go){go.disabled=!n;go.textContent=n?("Verwijder ("+n+")"):"Verwijder";}};});
 box.querySelectorAll("[data-tpdelgo]").forEach(function(b){b.onclick=function(){var col=b.closest(".tpcol");var ids=[].map.call(col.querySelectorAll(".tpdel.sel"),function(r){return r.dataset.sel;});if(!ids.length)return;var pl=planItemsNorm(planFor(pid,ws));if(!pl)return;var oud=pl.items.slice();pl.items=pl.items.filter(function(it){return ids.indexOf(it.id)<0;});pl.edited=true;tpDelCat=null;save();renderPlanning();toastUndo(ids.length+(ids.length===1?" oefening verwijderd":" oefeningen verwijderd"),function(){var p2=planItemsNorm(planFor(pid,ws));if(p2){p2.items=oud;save();renderPlanning();}});};});
 box.querySelectorAll("[data-rep]").forEach(function(b){b.onclick=function(ev){ev.stopPropagation();var pl=planItemsNorm(planFor(pid,ws));if(!pl)return;var it=pl.items.find(function(i){return i.id===b.dataset.rep;});if(!it)return;promptDlg("Hoe vaak deze week?","Aantal (1–14)",String(it.x||1),function(v){var n=parseInt(v,10);if(isNaN(n)||n<1||n>14){toast("Vul een getal van 1 t/m 14 in");return;}it.x=n;if((it.doneN||0)>n)it.doneN=n;it.done=(it.doneN||0)>=n;pl.edited=true;save();renderPlanning();});};});""")
rep('var tpTodoCat=null;','''var tpTodoCat=null;var tpDelCat=null;
var TP_ICO_TRASH='<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg>';''')
# cat-verandering of weekwissel: selectiemodus uit


css3='''/* v318: to-do verwijderen / aantal */
.tprep{flex:0 0 auto;border:1.5px solid var(--line);background:#fff;border-radius:999px;font-size:10.5px;font-weight:800;color:var(--muted);padding:1px 7px;cursor:pointer;font-family:inherit;line-height:1.4}
.tprep:hover{border-color:#7A7F85;color:var(--ink)}
.tpcol.del{box-shadow:0 0 0 1.5px #E08A8D,var(--shadow)}
.tpdel{cursor:pointer}
.tpselbox{width:20px;height:20px;border-radius:6px;border:1.5px solid var(--line);flex:0 0 auto;background:#fff}
.tpdel.sel .tpselbox{background:#C2383A;border-color:#C2383A;position:relative}
.tpdel.sel .tpselbox:after{content:"";position:absolute;left:6px;top:2px;width:5px;height:10px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}
.tpdel.sel .tdtnm{color:#C2383A}
.tpdelacts{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:8px;margin-top:10px}
.xbtn.sm.on{background:#7A7F85;color:#fff;border-color:#7A7F85}
'''
rep('/* v317: Urenbalans (week) + To-do kolommen */',css1+css3+'/* v317: Urenbalans (week) + To-do kolommen */')
s=s.replace('const APP_VERSION="v317";','const APP_VERSION="v318";')
open(p,'w',encoding='utf-8').write(s)
w=open('c226/sw.js').read();open('c226/sw.js','w').write(w.replace('jo-ladder-v317','jo-ladder-v318'))
print('ok')
