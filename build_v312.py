p='c226/index.html'
s=open(p,encoding='utf-8').read()
L=s.split('\n')
def find(prefix,start=13600,end=13950):
    for i in range(start,end):
        if L[i-1].startswith(prefix):return i
    raise Exception('not found '+prefix)
iK1=find(' var _kansToon=')
iK2=find(' if(_kansToon){try')
iWb=find(" var _wkBody='';")
iWt=find(' if(_wkToon){var _tl=')
iNote=find(" var _wkNote=")
iAsm=find(" html+='<div class=\"cvkop\">'")
iEnd=find(" box.innerHTML=html;",iAsm,iAsm+15)
iSw=find(' cvSwipeBind($("#cvAgenda"),function(d){todayDate')
# kansen block spans iK2 .. iWb-1 ; week body spans iWb .. iNote-1

new_piek=r''' /* v312: Volgende piek — P3/P4/P5-toernooien, swipe/‹› door de reeks; P5 subtiel onderaan */
 var _pk=_upc.filter(function(x){return peakNum(x.pp.peak)>=3;});
 if(typeof tdPiekIdx!=="number")tdPiekIdx=0;if(tdPiekIdx>=_pk.length||tdPiekIdx<0)tdPiekIdx=0;
 var _p5n=_pk.find(function(x){return peakNum(x.pp.peak)===5;});var _cur=_pk[tdPiekIdx]||null;
 var _pkH="",_pkNote="";
 if(_cur){var _cm=edMeta(_cur.ed),_cpk=peakNum(_cur.pp.peak);var _cd=dDiffDays(dt,_cur.start);var _bezig=(_cur.start<=dt&&dt<=_cur.end);
  var _dagN=_bezig?(dDiffDays(_cur.start,dt)+1):0,_dagM=dDiffDays(_cur.start,_cur.end)+1;
  var _hero='<div class="tdpkhero"'+(_bezig?' data-uped="'+_cur.ed.id+'"':' data-uped="'+_cur.ed.id+'"')+'><span class="n"><b>'+(_bezig?_dagN:_cd)+'</b><small>'+(_bezig?('dag van '+_dagM):(_cd===1?'dag':'dagen'))+'</small></span><span class="tx"><b>'+esc(_cm.name)+'</b><small>'+fmtRange(_cur.ed)+(_cur.ed.location?' · '+esc(_cur.ed.location):'')+'</small><small>'+(_cm.vorm?esc(taxVormKort(_cm.vorm)):'Wedstrijd')+(_bezig?' · bezig':'')+'</small></span><span class="tlpk">P'+_cpk+'</span></div>';
  /* voorbereidingscheck */
  var _chk=[];
  var _tg=edTourGoalsGet(_cur.ed,pid);_chk.push({ok:!!String(_tg||"").trim(),t:'Toernooidoelen',s:_tg?esc(String(_tg).split(/\n/)[0]).slice(0,70):'nog geen doelen gezet',act:'tdpk-doel'});
  _chk.push({ok:(_wkToon&&!_wkAchter),t:'Trainingsweek op schema',s:_wkToon?(_wkAchter?(_wkAchterN+' achter · '+_wkPct+'%'):('op schema · '+_wkPct+'%')):'geen weekplan',act:'tdpk-week'});
  var _r7=[];try{wellness().filter(function(w){return w.playerId===pid&&w.date<=dt&&dDiffDays(w.date,dt)<7;}).forEach(function(w){var r=wellReadiness(w);if(r!=null)_r7.push(r);});}catch(_e){}
  var _r7g=_r7.length?Math.round(_r7.reduce(function(a,b){return a+b;},0)/_r7.length):null;
  _chk.push({ok:(_r7g!=null&&_r7g>=50),t:'Readiness op peil',s:_r7g!=null?('gem. '+_r7g+' afgelopen 7 dagen · '+_r7.length+(_r7.length===1?' check':' checks')):'nog geen wellness checks deze week',act:'tdpk-wel'});
  var _fw=null;try{var _wsT=weekStart(_cur.start);var _micT=perMicro(pid,+dAddDays(_wsT,3).slice(0,4));_fw=_micT.find(function(w){return w.start===_wsT;});}catch(_e){}
  var _fwd=(_fw&&_fw.phase)?phaseDef(_fw.phase):null;
  _chk.push({ok:!!_fwd,t:'Wedstrijdweek in jaarplan',s:_fwd?esc(_fwd[1]):'geen fase gepland in de wedstrijdweek',act:'tdpk-jaar'});
  _pkH='<div class="tdpk">'+_hero+_chk.map(function(c){return '<div class="cvrow" data-pkact="'+c.act+'"><span class="tdok'+(c.ok?' ja':'')+'">'+(c.ok?'✓':'')+'</span><span style="flex:1;min-width:0"><b>'+c.t+'</b><small>'+c.s+'</small></span><span class="cvpijl">›</span></div>';}).join("")
   +((_p5n&&_p5n!==_cur)?'<div class="tdpk5" data-uped="'+_p5n.ed.id+'"><span class="tlpk">P5</span><span>'+esc(edMeta(_p5n.ed).name)+'</span><small>'+fmtDate(_p5n.start)+' · over '+dDiffDays(dt,_p5n.start)+' dgn</small></div>':'')+'</div>';
  _pkNote='<span class="row tdpknav" style="gap:4px"><button class="xbtn sm" id="tdPkPrev"'+(_pk.length>1?'':' disabled')+'>‹</button><small>'+(tdPiekIdx+1)+'/'+_pk.length+'</small><button class="xbtn sm" id="tdPkNext"'+(_pk.length>1?'':' disabled')+'>›</button></span>';}'''

new_week=r''' /* v312: Deze week als ring — verwacht volgt het trainingsschema (Golf Z / Fysiek Z / groepssessies) */
 var _wkBody='',_wkAchter=false,_wkAchterN=0,_wkExpPct=null;
 if(_wkToon){
  var _nowF=(isToday?((new Date().getHours()*60+new Date().getMinutes())/1440):1);
  var _dayFrac=Math.min(1,(di+_nowF)/7);
  function _blkFrac(type){var all=wb.blocks.filter(function(b){return b.type===type;});if(!all.length)return null;var n=0;all.forEach(function(b){if(b.day<di)n++;else if(b.day===di){if(!isToday)n++;else{var e=cvMin(fmtHM(b.end||b.start));var m=new Date().getHours()*60+new Date().getMinutes();if(e!=null&&e<=m)n++;}}});return n/all.length;}
  var _gsFrac=null;try{var _gss=gsSessiesVoor(pid,ws,dAddDays(ws,6));if(_gss.length){var _gn=_gss.filter(function(o){return o.x.datum<dt||(o.x.datum===dt&&!isToday);}).length;_gsFrac=_gn/_gss.length;}}catch(_e){}
  var _tl=[{l:'Golf',arr:_tG,fr:_blkFrac('golf'),col:wkTypeMeta('golf')[2]},{l:'Fysiek',arr:_tF,fr:_blkFrac('fysiek'),col:wkTypeMeta('fysiek')[2]}].map(function(x){var t=x.arr.length,d=x.arr.filter(function(o){return itemFull(o.it);}).length;var fr=(x.fr==null)?_dayFrac:x.fr;return {l:x.l,d:d,t:t,exp:t*fr,col:x.col};}).filter(function(x){return x.t>0;});
  if(_gsT)_tl.push({l:'Groep',d:_gsD,t:_gsT,exp:_gsT*((_gsFrac==null)?_dayFrac:_gsFrac),col:'#0ea5a3'});
  var _expTot=_tl.reduce(function(a,x){return a+x.exp;},0),_doneTot=_tl.reduce(function(a,x){return a+x.d;},0),_tTot=_tl.reduce(function(a,x){return a+x.t;},0);
  _wkExpPct=_tTot?Math.round(100*_expTot/_tTot):0;
  _wkAchterN=Math.max(0,Math.round(_expTot)-_doneTot);_wkAchter=_wkAchterN>0;
  var _rc=_wkAchter?'var(--orange)':'#17a05c';var _C=2*Math.PI*44,_C2=2*Math.PI*50;
  var _ring='<div class="tdring"><svg viewBox="0 0 104 104"><circle cx="52" cy="52" r="44" fill="none" stroke="#e9eef4" stroke-width="9"/><circle cx="52" cy="52" r="44" fill="none" stroke="'+_rc+'" stroke-width="9" stroke-linecap="round" stroke-dasharray="'+(_C*(_wkPct||0)/100).toFixed(1)+' '+_C.toFixed(1)+'"/><circle cx="52" cy="52" r="50" fill="none" stroke="#E6E8EA" stroke-width="2"/><circle cx="52" cy="52" r="50" fill="none" stroke="#7A7F85" stroke-width="2" stroke-dasharray="'+(_C2*_wkExpPct/100).toFixed(1)+' '+_C2.toFixed(1)+'"/></svg><div class="c"><b>'+_wkPct+'%</b><small>'+_et.d+' van '+_et.t+'</small></div></div>';
  _wkBody='<div class="tdwk">'+_ring+'<div class="tdwkr"><div><span class="cvchip '+(_wkAchter?'achter':'klaar')+'">'+(_wkAchter?(_wkAchterN+' achter'):'op schema')+'</span></div>'
   +_tl.map(function(x){var pc=x.t?Math.round(100*x.d/x.t):0,ex=x.t?Math.min(100,Math.round(100*x.exp/x.t)):0;var ach=x.d<Math.round(x.exp);return '<div class="tdcat"><span class="cvdot" style="background:'+x.col+'"></span><span class="nm">'+x.l+'</span><span class="tdbar sm"><i style="width:'+pc+'%;background:'+(ach?'var(--orange)':'#17a05c')+'"></i><span class="mk" style="left:'+ex+'%"></span></span><span class="cnt">'+x.d+'/'+x.t+'</span></div>';}).join("")
   +'<small class="tdwkx">buitenring = waar je nu zou zijn volgens je schema ('+_wkExpPct+'%)</small></div></div>';}'''

new_asm=r''' html+='<div class="cvkop">'+_kopL+_kpi+'</div><div class="cvgrid cv2 tdgrid"><div class="cvlinks">'
  +cvKaart('cvAgenda',cvTitel('Agenda',agI.length),(isToday?"vandaag":fmtDate(dt)),cvDagKolomHtml(agI,dt),"")
  +'</div><div class="cvwand">'
  +cvKaart('tdActies',cvTitel('Vandaag te doen',_nActOpen,_nActOpen>0),"actie › vandaag › later",ac,"Geen acties voor vandaag.").replace('class="card" id="tdActies"','class="card span" id="tdActies"')
  +cvKaart('tdWeek','Deze week',_wkNote,_wkBody,"Geen weekplan voor deze week.")
  +cvKaart('tdTraining',cvTitel('Training',_nOpen),'<span class="row" style="gap:6px">'+tdIco('tdPlanBtn','To-do',TD_ICO.todo)+tdIco('tdWeekBtn','Weekplan',TD_ICO.week)+'</span>',tr,"Geen trainingsonderdelen deze week.")
  +cvKaart('tdPiek','Volgende piek',_pkNote,_pkH,"Geen piekwedstrijd gepland — geef je toernooien een piek (P3–P5) in de wedstrijdplanning.")
  +cvKaart('tdWed',cvTitel(_isF?'Activiteiten':'Wedstrijden',_upc.length),'<span class="row" style="gap:6px">'+(_upc.length?tdIco('tdTgB','Toernooidoelen',TD_ICO.doel):'')+tdIco('tdKalB','Kalender',TD_ICO.kal)+'</span>',_wedRows,"Geen wedstrijden gepland.")
  +'</div></div>';'''

new_bind=r''' cvSwipeBind($("#cvAgenda"),function(d){todayDate=dAddDays(todayDate,d);renderToday();});
 var _pkN=(typeof _pk!=="undefined")?_pk.length:0;
 function _pkGo(d){if(_pkN<2)return;tdPiekIdx=((tdPiekIdx+d)%_pkN+_pkN)%_pkN;renderToday();}
 var _pkp=$("#tdPkPrev"),_pkn=$("#tdPkNext");if(_pkp)_pkp.onclick=function(){_pkGo(-1);};if(_pkn)_pkn.onclick=function(){_pkGo(1);};
 cvSwipeBind($("#tdPiek"),function(d){_pkGo(d);});
 box.querySelectorAll("[data-pkact]").forEach(function(r){r.onclick=function(){var k=r.dataset.pkact;if(!_cur)return;
  if(k==="tdpk-doel")openTourGoalsForm(_cur.ed.id,pid);
  else if(k==="tdpk-week"){tpPlayer=pid;tpWeek=ws;planTab="todo";show("planning");}
  else if(k==="tdpk-wel"){if(isToday&&typeof openWellness==="function")openWellness(pid,dt);else show("wellness");}
  else if(k==="tdpk-jaar"){if(!rolIsSpeler()||modusToont(pid,"plan_period")){tpPlayer=pid;planTab="period";show("planning");}else editionDetail(_cur.ed.id,{player:pid});}};});'''

out=L[:]
def repl(a,b,text): out[a-1:b]=text.split('\n')
# bottom-up
repl(iSw,iSw,new_bind)
repl(iAsm,iEnd-1,new_asm)
repl(iWb,iNote-1,new_week)
repl(iK1,iWb-1,new_piek)
s='\n'.join(out)
# tdPiekIdx global + week status needed before piek block? piek uses _wkToon/_wkAchter → piek block must come AFTER week block. Swap: move piek block after week block.
# Simpler: ensure order by construction: we replaced kansen(before week) with piek → wrong order. Fix by moving.
a=s.index(' /* v312: Volgende piek'); b=s.index(' /* v312: Deze week als ring'); c=s.index(" var _wkNote=")
piek=s[a:b]; week=s[b:c]
s=s[:a]+week+piek+s[c:]
s=s.replace('var TD_ICO={','var tdPiekIdx=0;\nvar TD_ICO={',1)
css='''/* v312: Deze week ring + Volgende piek */
.tdgrid #cvAgenda{height:auto;flex:1 1 0;min-height:0}
.tdgrid #cvAgenda .cvbody{overflow:auto}
.tdwk{display:flex;gap:14px;align-items:center;flex:1;min-height:0;padding-top:4px}
.tdring{position:relative;width:104px;height:104px;flex:0 0 auto}
.tdring svg{width:104px;height:104px;transform:rotate(-90deg);display:block}
.tdring .c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.tdring .c b{font-family:var(--fd);font-size:22px;font-weight:600;line-height:1}
.tdring .c small{font-size:10px;color:var(--muted);font-weight:600;margin-top:2px}
.tdwkr{flex:1;min-width:0}
.tdwkr .cvchip{margin-bottom:4px}.cvchip.achter{background:var(--orange)}
.tdcat{display:flex;align-items:center;gap:8px;padding:4px 0}
.tdcat .nm{width:50px;font-size:12px;font-weight:600;flex:0 0 auto}
.tdcat .cnt{width:36px;text-align:right;font-size:11.5px;color:var(--muted);font-weight:600;flex:0 0 auto}
.tdbar.sm{position:relative;height:6px;overflow:visible;flex:1}
.tdbar.sm i{border-radius:5px}
.tdbar.sm .mk{position:absolute;top:-3px;bottom:-3px;width:1.5px;background:#7A7F85;border-radius:1px}
.tdwkx{display:block;font-size:10.5px;color:var(--muted);margin-top:6px}
.tdpk{display:flex;flex-direction:column;flex:1;min-height:0}
.tdpkhero{display:flex;align-items:center;gap:12px;background:var(--orange);color:#fff;border-radius:12px;padding:9px 12px;margin:4px 0 4px;cursor:pointer;-webkit-tap-highlight-color:transparent}
.tdpkhero .n{display:flex;flex-direction:column;align-items:center;flex:0 0 auto;min-width:54px}
.tdpkhero .n b{font-family:var(--fd);font-size:32px;font-weight:500;line-height:1}
.tdpkhero .n small{font-size:9.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;opacity:.9;white-space:nowrap}
.tdpkhero .tx{flex:1;min-width:0}
.tdpkhero .tx b{display:block;font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tdpkhero .tx small{display:block;font-size:11px;opacity:.9;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tdpkhero .tlpk{background:#fff;color:var(--orange);flex:0 0 auto}
.tdpk .cvrow{padding:5px 2px}
.tdok{width:18px;height:18px;border-radius:50%;flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;border:1.5px solid var(--line);color:var(--muted)}
.tdok.ja{background:#17a05c;border-color:#17a05c;color:#fff}
.tdpk5{display:flex;align-items:center;gap:8px;margin-top:auto;padding-top:6px;font-size:12px;color:var(--muted);cursor:pointer}
.tdpk5 .tlpk{background:#FBDCC7;color:#2B2F33;opacity:.9}
.tdpk5 span:nth-child(2){font-weight:600;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.tdpk5 small{white-space:nowrap;margin-left:auto;font-size:11px}
.tdpknav small{font-size:11px;color:var(--muted);font-weight:700;min-width:26px;text-align:center}
.tdpknav .xbtn[disabled]{opacity:.35}
@media(max-width:699px){.tdgrid #cvAgenda{height:420px;flex:none}.tdwk{gap:10px}.tdring,.tdring svg{width:92px;height:92px}}
'''
k='/* v310: spelers-Vandaag op het coach-skelet */'
assert s.count(k)==1
s=s.replace(k,css+k)
s=s.replace('const APP_VERSION="v311";','const APP_VERSION="v312";')
open(p,'w',encoding='utf-8').write(s)
w=open('c226/sw.js').read();open('c226/sw.js','w').write(w.replace('jo-ladder-v311','jo-ladder-v312'))
print('ok')
