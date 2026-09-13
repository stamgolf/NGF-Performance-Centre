import re,sys
p='c226/index.html'
s=open(p,encoding='utf-8').read()
L=s.split('\n')
def ln(i):return L[i-1]
def find(prefix,start=13600,end=13900):
    for i in range(start,end):
        if ln(i).startswith(prefix):return i
    raise Exception('not found '+prefix)

iHtml=find(' var html=(!rolIsSpeler()')
iEmpty=find(' if(!todayPlayer){box.innerHTML=html')
iWeek=find(' /* weekvoortgang')
iAg=find(' /* agenda */')
iActs=find(' /* acties */')
iAc=find(' var ac="";')
iTr=find(' var tr="";')
iUpc=find(' var _upc=[];')
iUpRow=find(' function _upRow(')
iFound=find(' if(rolIsSpeler()&&modusNu(pid)==="foundation"){')
iUpCard2=find("  upCard='<div class=\"card\"><h3 style=\"margin:0 0 8px\">Activiteiten",iFound,iFound+12)
iFoundEnd=iUpCard2+2
assert ln(iFoundEnd).strip()=='}', ln(iFoundEnd)
iAsm=find(" html+=upCard+'<div class=\"tdcols\">")
iTwb=find(' var _twb=$("#tdWeekBtn")')
assert iEmpty==iHtml+1

new_html=r''' var _back=(!rolIsSpeler()?'<button class="bkbtn" onclick="cvTerugKlik()" style="margin:0 0 8px;display:inline-block">‹ '+(cvTerugView==="spelers"?"Spelers":"Overzicht")+'</button>':'');
 var _zoekH=(!rolIsSpeler()?'<span class="acwrap" style="display:inline-block;min-width:0;margin-left:8px"><input class="in zoekpil" id="tdQ" autocomplete="off" placeholder="Zoek speler…" value="'+esc(todayPlayer?nameOf(todayPlayer):"")+'"></span>':'');
 var html=_back+startKaartHtml();
 if(!todayPlayer){box.innerHTML=html+'<div class="card"><div class="row" style="gap:11px;align-items:center;flex-wrap:wrap">'+_zoekH+'<span class="muted" style="font-size:13px">Kies een speler om het dagprogramma te zien.</span></div></div>';bindTodayTop();return;}'''

new_week=r''' /* v310: weekvoortgang (rendering in de kaart Deze week) */
 var _gc={d:0,t:0};try{_gc=gsComp(pid,ws);}catch(_e){}
 var _wkPct=null,_et={d:0,t:0},_motH="",_motA=false,_barc="",_wkToon=false;
 if((plan||_gc.t)&&(!rolIsSpeler()||modusToont(pid,"wk_voortgang"))){_wkToon=true;var _et0=plan?execTotals(plan.items):{d:0,t:0};_et={d:_et0.d+_gc.d,t:_et0.t+_gc.t};_wkPct=_et.t?Math.round(100*_et.d/_et.t):0;
  var _ws2=null;try{_ws2=wkStatus(pid,ws,dt);}catch(e){}
  _barc=(_wkPct>=WK_NORM)?"#17a05c":((_ws2&&_ws2.achter)?"var(--orange)":"");
  if(_ws2){
   var _rt=wkReeksTxt(_ws2.reeks);
   if(_ws2.achter){_motA=true;_motH='Nog '+_ws2.c.open+(_ws2.c.open===1?' onderdeel':' onderdelen')+' te gaan deze week — een kleine stap vandaag telt al.';}
   else if(_rt)_motH=esc(_rt);
   else if(_wkPct>=WK_NORM)_motH='Deze week boven de '+WK_NORM+'% — begin van een reeks.';
  }}'''

new_ag=r''' /* v310: agenda als dagkolom (cvDagKolomHtml) */
 var agI=[];
 cal.forEach(function(c){var tt=String(c.time||"").split("–");var t0=tt[0]?fmtHM(tt[0]):"",t1=tt[1]?fmtHM(tt[1]):"";
  agI.push({tijd:t0,tot:t1,naam:esc(c.label),sub:esc(c.sub||""),kleur:c.edId?CAL_KLEUR.wed:CAL_KLEUR.agenda,vol:!!c.edId,click:c.edId?"editionDetail('"+c.edId+"',{player:'"+pid+"'})":(c.evId?"eventDetail('"+c.evId+"',{player:'"+pid+"'})":"")});});
 bl.forEach(function(b){var mt=wkTypeMeta(b.type);
  agI.push({tijd:fmtHM(b.start),tot:fmtHM(b.end),naam:esc(b.label||mt[1]),sub:mt[1]+(b.mode?' · '+wkModeLabel(b.mode):'')+(b.loc?' · '+esc(b.loc):''),kleur:mt[2],click:"openRoosterBlock('"+pid+"','"+ws+"','"+b.id+"')"});});
 agI.sort(function(a,b){return (a.tijd||"99:99").localeCompare(b.tijd||"99:99");});'''

new_ac=r''' /* v310: acties als rijen met prioriteitschip rechts (actie › vandaag › later › klaar) */
 function _actP(a){if(a.klaar)return "klaar";if(a.kind==='well')return a.wId?"klaar":"actie";if(a.kind==='log')return a.ll?"klaar":"actie";if(a.kind==='teval')return a.tvId?"klaar":(/Laatste wedstrijddag/.test(a.sub||"")?"vandaag":"later");if(a.kind==='stats'||a.kind==='mp'||a.kind==='tm'||a.kind==='rondes')return "actie";if(a.kind==='wkplan')return "vandaag";if(a.kind==='gs')return a.herin?"vandaag":"later";return "later";}
 var _AR={actie:0,vandaag:1,later:2,klaar:3};
 var _actKl={mp:"#8b5cf6",stats:"var(--orange)",teval:"#854F0B",well:"#0ea5a3",tm:"#0f9e73",rondes:"var(--orange)",wkplan:"var(--orange)",oppstil:"#8b5cf6",backup:"#6b7785",log:"#c8791a",gs:"#0ea5a3"};
 var _actIdx=acts.map(function(a,i){return {a:a,i:i,p:_actP(a)};}).sort(function(x,y){return _AR[x.p]-_AR[y.p]||x.i-y.i;});
 var ac=_actIdx.map(function(o){var a=o.a;return '<div class="cvrow actrow" data-ask="'+o.i+'"><span class="cvdot" style="background:'+(o.p==="klaar"?"#17a05c":(_actKl[a.kind]||"#7A7F85"))+'"></span><span style="flex:1;min-width:0"><b>'+a.title+'</b>'+(a.sub?'<small>'+a.sub+'</small>':'')+'</span><span class="cvchip '+o.p+'">'+o.p+'</span></div>';}).join("");
 var _nActOpen=_actIdx.filter(function(o){return o.p!=="klaar";}).length;'''

new_tr=r''' var tr=trainActs.map(function(a){return '<div class="cvrow" data-topen="'+a.tt+'"'+(a.blkId?' data-tblk="'+a.blkId+'"':'')+'><span class="cvdot" style="background:'+a.mt[2]+'"></span><span style="flex:1;min-width:0"><b>'+a.title+'</b></span><span class="cvn'+(a.openN?'':' groen')+'" style="margin:0;vertical-align:0">'+(a.openN?a.openN+' open':'✓ klaar')+'</span><span class="cvpijl">›</span></div>';}).join("");
 var _nOpen=trainActs.reduce(function(s,a){return s+(a.openN||0);},0);'''

new_found_upcard=r'''  var _ntRow='<div class="cvrow"><span class="tlpk" style="background:#e6ebef;color:#16202B">TR</span><span style="flex:1;min-width:0"><b>'+(_nt?esc(_ntLbl):'Geen training gepland')+'</b><small>'+(_nt?('Eerstvolgende training · '+fmtDate(_nt.date)+(_nt.b.start?(' '+fmtHM(_nt.b.start)):'')):'plan een training in je weekschema')+'</small></span>'+(_nt?'<span class="cvtijd'+(_ntDays<=1?' nu':'')+'">'+(_ntDays===0?'vandaag':_ntDays===1?'morgen':'over '+_ntDays+' dgn')+'</span>':'')+'</div>';'''

ICO=r'''function tdIco(id,title,svg){return '<button class="xbtn sm" id="'+id+'" title="'+title+'" aria-label="'+title+'">'+svg+'</button>';}
var TD_ICO={
 todo:'<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6h11M9 12h11M9 18h11"/><path d="M3.5 6l1.2 1.2L7 4.8M3.5 12l1.2 1.2L7 10.8M3.5 18l1.2 1.2L7 16.8"/></svg>',
 week:'<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11.5M15 9v11.5"/></svg>',
 doel:'<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1.2" fill="currentColor" stroke="none"/></svg>',
 kal:'<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/><circle cx="12" cy="15.5" r="1.8" fill="currentColor" stroke="none"/></svg>'};
'''

new_asm=r''' /* v310: spelers-Vandaag op het coach-skelet (kop + agenda-ruggengraat + wand) */
 var _isF=(rolIsSpeler()&&modusNu(pid)==="foundation");
 var _wedRows=_upc.map(function(e){var m2=edMeta(e.ed);var pk=e.pp.peak;var days=dDiffDays(dt,e.start);var ddTxt=(e.start<dt)?'bezig':(days===0?'vandaag':days===1?'morgen':'over '+days+' dgn');
  return '<div class="cvrow" data-uped="'+e.ed.id+'"><span class="tlpk" style="background:'+(peakNum(pk)?peakColor(pk):'#e6ebef')+';color:'+(peakNum(pk)>=4?"#fff":"#16202B")+'">'+(peakNum(pk)?'P'+peakNum(pk):'–')+'</span><span style="flex:1;min-width:0"><b>'+esc(m2.name)+'</b><small>'+fmtRange(e.ed)+(e.ed.location?' · '+esc(e.ed.location):'')+'</small></span><span class="cvtijd'+((e.start<=dt||days<=1)?' nu':'')+'">'+ddTxt+'</span><span class="cvpijl">›</span></div>';}).join("");
 if(typeof _ntRow!=="undefined")_wedRows=_ntRow+_wedRows;
 var _pk45=_upc.find(function(x){return peakNum(x.pp.peak)>=4;});var _pkD=_pk45?dDiffDays(dt,_pk45.start):null;
 var _rdy=null;try{var _wl=wellness().filter(function(w){return w.playerId===pid&&w.date<=dt;}).sort(function(a,b){return String(b.date).localeCompare(String(a.date));})[0];if(_wl){_rdy=wellReadiness(_wl);}}catch(_e){}
 var _kansToon=(!rolIsSpeler()||modusToont(pid,"kansen"));var _kansH="",_nKans=0;
 if(_kansToon){try{var _OPSa=opportunities(pid);var _F=_OPSa.filter(function(o){return o.kwadrant==="kans"||o.kwadrant==="uitbouwen";}).slice(0,4);
  if(_F.length<3)_OPSa.filter(function(o){return _F.indexOf(o)<0&&o.niveau!=="sterk";}).sort(function(a,b){return b.score-a.score;}).slice(0,3-_F.length).forEach(function(o){_F.push(o);});
  _nKans=_F.length;
  _kansH=_F.map(function(o,i){var e=oppEffect(pid,o);var col=KW_COL[o.kwadrant]||"#9AA0A6";var w=(o.hard&&o.slagen!=null)?(_n1(o.slagen)+' slag/ronde'):('impact '+o.score);
   var r=e?(e.stil?'<span class="cvchip monitor">stil</span>':'<span class="cvn groen" style="margin:0;vertical-align:0">in training</span>'):'<span class="cvn" style="margin:0;vertical-align:0">'+(KW_LBL[o.kwadrant]||'')+'</span>';
   return '<div class="cvrow" data-kans="'+esc(o.key)+'"><span class="cvdot" style="background:'+col+'"></span><span style="flex:1;min-width:0"><b>'+esc(o.label)+'</b><small>'+w+' · '+esc(oppDomLabel(o.dom))+(e?(' · '+(e.stil?('staat al '+oppPeriodeTxt(e.dagen)+' op je lijst'):('sinds '+fmtDate(e.start)))):'')+'</small></span>'+r+'<span class="cvpijl">›</span></div>';}).join("");}catch(_e){_kansH="";}}
 var _wkBody='';
 if(_wkToon){var _tl=[['Golf',_tG],['Fysiek',_tF]].map(function(x){var t=x[1].length,d=x[1].filter(function(o){return itemFull(o.it);}).length;return {l:x[0],d:d,t:t};});if(_gsT)_tl.push({l:'Groep',d:_gsD,t:_gsT});
  _wkBody='<div class="tdprog" style="margin:6px 0 4px"><div class="tdbar"><i style="width:'+_wkPct+'%'+(_barc?(';background:'+_barc):'')+'"></i></div><span class="tdpct">'+_wkPct+'% <small class="sx" style="font-weight:600">('+_et.d+'/'+_et.t+')</small></span></div>'
   +(_motH?'<div class="motiv'+(_motA?' achter':'')+'" style="margin:2px 0 8px"><span class="mb"></span><span>'+_motH+'</span></div>':'')
   +'<div class="tdtl">'+_tl.map(function(x){return '<div class="tdtile"><span class="l">'+x.l+'</span><span class="v">'+x.d+'<small>/'+x.t+'</small></span><span class="s">'+((x.t-x.d)?((x.t-x.d)+' open'):'klaar ✓')+'</span></div>';}).join("")+'</div>';}
 var _wkNote='wk '+isoWeek(new Date(dt+"T12:00:00"))+(_pd?' · '+esc(_pd[1]):'');
 var _kpi='<div class="cvkpi">'
  +'<span><b'+(_wkPct!=null&&_wkPct>=WK_NORM?' class="groen"':(_motA?' class="oranje"':''))+'>'+(_wkPct!=null?_wkPct+'%':'–')+'</b><small>week</small></span>'
  +'<span'+(_nActOpen?' class="rood"':'')+'><b>'+_nActOpen+'</b><small>acties</small></span>'
  +'<span><b>'+_nOpen+'</b><small>open</small></span>'
  +'<span><b'+(_pkD!=null&&_pkD<=7?' class="oranje"':'')+'>'+(_pkD==null?'–':_pkD)+'</b><small>'+(_pk45?('dgn tot P'+peakNum(_pk45.pp.peak)):'wedstrijd')+'</small></span>'
  +'<span><b'+(_rdy!=null&&_rdy<50?' class="rood"':'')+'>'+(_rdy!=null?_rdy:'–')+'</b><small>readiness</small></span></div>';
 var _kopL='<div class="row" style="align-items:center;gap:5px;flex-wrap:wrap"><button class="xbtn sm" id="tdPrev">‹</button><span style="position:relative;display:inline-flex"><button class="tdDateBtn" id="tdDateBtn"><b>'+(isToday?'Vandaag':new Date(dt+"T12:00:00").toLocaleDateString("nl-NL",{weekday:"long"}))+'</b><small>'+fmtDate(dt)+' ▾</small></button><input type="date" id="tdDateInp" value="'+dt+'"></span><button class="xbtn sm" id="tdNext">›</button>'+(isToday?'':'<button class="xbtn sm" id="tdToday" title="Vandaag" aria-label="Vandaag">'+TD_ICO.kal+'</button>')+(_fbH?'<span style="margin-left:10px">'+_fbH+'</span>':'')+_zoekH+'</div>';
 html+='<div class="cvkop">'+_kopL+_kpi+'</div><div class="cvgrid cv2 tdgrid"><div class="cvlinks">'
  +cvKaart('cvAgenda',cvTitel('Agenda',agI.length),(isToday?"vandaag":fmtDate(dt)),cvDagKolomHtml(agI,dt),"")
  +cvKaart('tdTraining',cvTitel('Training',_nOpen),'<span class="row" style="gap:6px">'+tdIco('tdPlanBtn','To-do',TD_ICO.todo)+tdIco('tdWeekBtn','Weekplan',TD_ICO.week)+'</span>',tr,"Geen trainingsonderdelen deze week.")
  +'</div><div class="cvwand">'
  +cvKaart('tdActies',cvTitel('Vandaag te doen',_nActOpen,_nActOpen>0),"actie › vandaag › later",ac,"Geen acties voor vandaag.").replace('class="card" id="tdActies"','class="card span" id="tdActies"')
  +cvKaart('tdWeek','Deze week',_wkNote,_wkBody,"Geen weekplan voor deze week.")
  +cvKaart('tdWed',cvTitel(_isF?'Activiteiten':'Wedstrijden',_upc.length),'<span class="row" style="gap:6px">'+(_upc.length?tdIco('tdTgB','Toernooidoelen',TD_ICO.doel):'')+tdIco('tdKalB','Kalender',TD_ICO.kal)+'</span>',_wedRows,"Geen wedstrijden gepland.")
  +(_kansToon?cvKaart('tdKansen',cvTitel('Kansen',_nKans),"grootste kans eerst",_kansH,"Nog geen kansen — voeg testen, rondes of een Upgame-snapshot toe.").replace('class="card" id="tdKansen"','class="card span" id="tdKansen"'):'')
  +'</div></div>';'''

new_bind=r''' var _twb=$("#tdWeekBtn");if(_twb&&rolIsSpeler()&&!modusToont(pid,"plan_timeline"))_twb.style.display="none";if(_twb)_twb.onclick=function(){state.calMode="week";save();planTab="timeline";show("planning");};
 var _tkb=$("#tdKalB");if(_tkb&&rolIsSpeler()&&!modusToont(pid,"plan_timeline"))_tkb.style.display="none";if(_tkb)_tkb.onclick=function(){state.calMode="maand";save();planTab="timeline";show("planning");};
 var _ttg=$("#tdTgB");if(_ttg)_ttg.onclick=function(){if(_upc.length)openTourGoalsForm(_upc[0].ed.id,pid);};
 box.querySelectorAll("[data-kans]").forEach(function(r){r.onclick=function(){spPlayer=pid;show("kansen");};});
 cvScrollPas(box);setTimeout(function(){cvScrollPas(box);},50);
 cvSwipeBind($("#cvAgenda"),function(d){todayDate=dAddDays(todayDate,d);renderToday();});'''

# apply from bottom to top so indices stay valid
out=L[:]
def repl(a,b,text):  # replace lines a..b inclusive (1-based) with text
    global out
    out[a-1:b]=text.split('\n')
repl(iTwb,iTwb,new_bind)
repl(iAsm,iAsm,new_asm)
repl(iUpCard2,iUpCard2+1,new_found_upcard)   # upCard= line + continuation line
repl(iUpRow,iFound-1,'')                    # _upRow .. upCard
repl(iTr,iUpc-1,new_tr)
repl(iAc,iTr-1,new_ac)
repl(iAg,iActs-1,new_ag)
repl(iWeek,iAg-1,new_week)
repl(iHtml,iEmpty,new_html)
s='\n'.join(out)
# ICO helpers before renderToday
k='function renderToday(){var box=$("#todayBody");if(!box)return;'
assert s.count(k)==1
s=s.replace(k,ICO+k)
# CSS
css='''/* v310: spelers-Vandaag op het coach-skelet */
.cvkpi b.groen{color:#17a05c}.cvkpi b.oranje{color:var(--orange)}
.cvn.groen{color:#17a05c}
#tdActies .cvchip{width:68px;min-width:0;margin-left:auto}#tdActies .cvchip.klaar{background:#17a05c}
.cvtijd.nu{color:var(--orange)}
.tdgrid .tlpk{flex:0 0 auto}
.tdtl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:4px}
.tdtile{background:var(--paper);border-radius:12px;padding:8px 11px;min-width:0}
.tdtile .l{display:block;font-size:9.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.tdtile .v{display:block;font-family:var(--fd);font-size:20px;font-weight:600;line-height:1.2}.tdtile .v small{font-size:12px;color:var(--muted);font-weight:600}
.tdtile .s{display:block;font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tdgrid .motiv{font-size:12.5px}
.tdgrid #tdTraining .cvbody,.tdgrid #tdWed .cvbody{overflow:auto}
@media(max-width:700px){.tdtl{grid-template-columns:repeat(3,minmax(0,1fr))}#tdActies .cvchip{width:60px}}
'''
k2='@keyframes splweg{to{opacity:0;visibility:hidden}}'
assert s.count(k2)==1
s=s.replace(k2,k2+'\n'+css)
s=s.replace('const APP_VERSION="v309";','const APP_VERSION="v310";')
open(p,'w',encoding='utf-8').write(s)
w=open('c226/sw.js').read();open('c226/sw.js','w').write(w.replace('jo-ladder-v309','jo-ladder-v310'))
print('ok')
