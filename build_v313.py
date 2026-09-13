p='c226/index.html'
s=open(p,encoding='utf-8').read()
L=s.split('\n')
def find(prefix,start=13600,end=14000):
    for i in range(start,end):
        if L[i-1].startswith(prefix):return i
    raise Exception('not found '+prefix)
iTr=find(' var tr=trainActs')
iNo=find(' var _nOpen=')
iWk=find(' /* v312: Deze week als ring')
iPk=find(' /* v312: Volgende piek')
iAsm=find(" html+='<div class=\"cvkop\">'")
iAsmEnd=find("  +'</div></div>';",iAsm,iAsm+12)

new_tr=r''' /* v313: Training = dezelfde categorieën als de To-do-lijst (+ Groepsopdrachten) */
 var _catRows=TODOCATS.map(function(c){var arr=allTodos([c[0]]);if(!arr.length)return null;var op=arr.filter(function(o){return !itemFull(o.it);}).length;return {mk:c[0],l:c[1],n:arr.length,open:op,col:mcAccent(c[0])};}).filter(Boolean);
 var tr=_catRows.map(function(c){return '<div class="cvrow" data-copen="'+c.mk+'"><span class="cvdot" style="background:'+c.col+'"></span><span style="flex:1;min-width:0"><b>'+c.l+'</b></span><span class="cvpijl">›</span></div>';}).join("")
  +(_gsT?'<div class="cvrow" data-topen="gs"><span class="cvdot" style="background:#0ea5a3"></span><span style="flex:1;min-width:0"><b>Groepsopdrachten'+(_gsw.length===1?' · '+esc(_gsw[0].s.name):'')+'</b></span><span class="cvpijl">›</span></div>':'');
 var _nOpen=_catRows.reduce(function(s,c){return s+c.open;},0)+(_gsT-_gsD);'''

new_week=r''' /* v313: Deze week als ring — categorieën van de To-do-lijst; verwacht volgt het trainingsschema (Golf Z / Fysiek Z) */
 var _wkBody='',_wkAchter=false,_wkAchterN=0,_wkExpPct=null;
 if(_wkToon){
  var _nowF=(isToday?((new Date().getHours()*60+new Date().getMinutes())/1440):1);
  var _dayFrac=Math.min(1,(di+_nowF)/7);
  function _blkFrac(type){var all=wb.blocks.filter(function(b){return b.type===type;});if(!all.length)return null;var n=0;all.forEach(function(b){if(b.day<di)n++;else if(b.day===di){if(!isToday)n++;else{var e=cvMin(fmtHM(b.end||b.start));var m=new Date().getHours()*60+new Date().getMinutes();if(e!=null&&e<=m)n++;}}});return n/all.length;}
  var _frG=_blkFrac('golf'),_frF=_blkFrac('fysiek');
  function _frFor(mk){var f=(mk==="fysiek")?_frF:_frG;return (f==null)?_dayFrac:f;}
  var _tl=TODOCATS.map(function(c){var arr=allTodos([c[0]]);var t=arr.length;if(!t)return null;var d=arr.filter(function(o){return itemFull(o.it);}).length;return {l:c[1],d:d,t:t,exp:t*_frFor(c[0]),col:mcAccent(c[0])};}).filter(Boolean);
  if(_gsT){var _ge=0;_gsw.forEach(function(o){(o.inh.drillIds||[]).forEach(function(did){var dd=_adPool2.find(function(x){return x.id===did;});_ge+=_frFor(dd?dd.mainCat:"golfskills");});});_tl.push({l:'Groep',d:_gsD,t:_gsT,exp:_ge,col:'#0ea5a3'});}
  var _expTot=_tl.reduce(function(a,x){return a+x.exp;},0),_doneTot=_tl.reduce(function(a,x){return a+x.d;},0),_tTot=_tl.reduce(function(a,x){return a+x.t;},0);
  _wkExpPct=_tTot?Math.round(100*_expTot/_tTot):0;
  _wkAchterN=Math.max(0,Math.round(_expTot)-_doneTot);_wkAchter=_wkAchterN>0;
  var _rc=_wkAchter?'var(--orange)':'#17a05c';var _C=2*Math.PI*44,_C2=2*Math.PI*50;
  var _ring='<div class="tdring"><svg viewBox="0 0 104 104"><circle cx="52" cy="52" r="44" fill="none" stroke="#e9eef4" stroke-width="9"/><circle cx="52" cy="52" r="44" fill="none" stroke="'+_rc+'" stroke-width="9" stroke-linecap="round" stroke-dasharray="'+(_C*(_wkPct||0)/100).toFixed(1)+' '+_C.toFixed(1)+'"/><circle cx="52" cy="52" r="50" fill="none" stroke="#E6E8EA" stroke-width="2"/><circle cx="52" cy="52" r="50" fill="none" stroke="#7A7F85" stroke-width="2" stroke-dasharray="'+(_C2*_wkExpPct/100).toFixed(1)+' '+_C2.toFixed(1)+'"/></svg><div class="c"><b>'+_wkPct+'%</b><small>'+_et.d+' van '+_et.t+'</small></div></div>';
  _wkBody='<div class="tdwk"><div class="tdwkl">'+_ring+'<div class="tdwkbox'+(_wkAchter?' achter':'')+'"><span class="cvchip '+(_wkAchter?'achter':'klaar')+'">'+(_wkAchter?(_wkAchterN+' achter'):'op schema')+'</span><small>'+(_wkAchter?('Volgens je schema had je nu '+Math.round(_expTot)+' van '+_tTot+' onderdelen gedaan.'):('Je loopt gelijk met je trainingsschema ('+_wkExpPct+'% verwacht).'))+'</small></div></div><div class="tdwkr">'
   +_tl.map(function(x){var pc=x.t?Math.round(100*x.d/x.t):0,ex=x.t?Math.min(100,Math.round(100*x.exp/x.t)):0;var ach=x.d<Math.round(x.exp);return '<div class="tdwkc"><span class="cvdot" style="background:'+x.col+'"></span><span class="nm">'+x.l+'</span><span class="tdbar sm"><i style="width:'+pc+'%;background:'+(ach?'var(--orange)':'#17a05c')+'"></i><span class="mk" style="left:'+ex+'%"></span></span><span class="cnt">'+x.d+'/'+x.t+'</span></div>';}).join("")
   +'</div></div>';}'''

new_asm=r''' html+='<div class="cvkop">'+_kopL+_kpi+'</div><div class="cvgrid cv2 tdgrid"><div class="cvlinks">'
  +cvKaart('cvAgenda',cvTitel('Agenda',agI.length),(isToday?"vandaag":fmtDate(dt)),cvDagKolomHtml(agI,dt),"")
  +cvKaart('tdPiek','Volgende piek',_pkNote,_pkH,"Geen piekwedstrijd gepland — geef je toernooien een piek (P3–P5) in de wedstrijdplanning.")
  +'</div><div class="cvwand">'
  +cvKaart('tdActies',cvTitel('Vandaag te doen',_nActOpen,_nActOpen>0),"actie › vandaag › later",ac,"Geen acties voor vandaag.").replace('class="card" id="tdActies"','class="card span" id="tdActies"')
  +cvKaart('tdWeek','Deze week',_wkNote,_wkBody,"Geen weekplan voor deze week.")
  +cvKaart('tdTraining',cvTitel('Training',_nOpen),'<span class="row" style="gap:6px">'+tdIco('tdPlanBtn','To-do',TD_ICO.todo)+tdIco('tdWeekBtn','Weekplan',TD_ICO.week)+'</span>',tr,"Geen trainingsonderdelen deze week.")
  +cvKaart('tdWed',cvTitel(_isF?'Activiteiten':'Wedstrijden',_upc.length),'<span class="row" style="gap:6px">'+(_upc.length?tdIco('tdTgB','Toernooidoelen',TD_ICO.doel):'')+tdIco('tdKalB','Kalender',TD_ICO.kal)+'</span>',_wedRows,"Geen wedstrijden gepland.").replace('class="card" id="tdWed"','class="card span" id="tdWed"')
  +'</div></div>';'''

out=L[:]
def repl(a,b,text): out[a-1:b]=text.split('\n')
repl(iAsm,iAsmEnd,new_asm)
repl(iWk,iPk-1,new_week)
repl(iTr,iNo,new_tr)
s='\n'.join(out)
# binding voor data-copen
k=' box.querySelectorAll("[data-kans]").forEach(function(r){r.onclick=function(){spPlayer=pid;show("kansen");};});'
assert s.count(k)==1
s=s.replace(k,' box.querySelectorAll("[data-copen]").forEach(function(r){r.onclick=function(){openCatTodos(pid,ws,r.dataset.copen);};});')
# CSS
old_css_start=s.index('/* v312: Deze week ring + Volgende piek */')
old_css_end=s.index('/* v310: spelers-Vandaag op het coach-skelet */')
css='''/* v312/v313: Deze week ring + Volgende piek */
.tdgrid #cvAgenda{height:auto;flex:1 1 0;min-height:0}
.tdgrid #cvAgenda .cvbody{overflow:auto}
.tdgrid .cvlinks>#tdPiek{height:var(--cvvh,300px);flex:0 0 auto;margin-bottom:14px}
.tdgrid #tdWeek .cvbody,.tdgrid #tdPiek .cvbody{display:flex;flex-direction:column}
.tdwk{display:flex;gap:16px;align-items:center;flex:1;min-height:0}
.tdwkl{flex:0 0 150px;display:flex;flex-direction:column;align-items:center;gap:8px}
.tdring{position:relative;width:104px;height:104px;flex:0 0 auto}
.tdring svg{width:104px;height:104px;transform:rotate(-90deg);display:block}
.tdring .c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.tdring .c b{font-family:var(--fd);font-size:22px;font-weight:600;line-height:1}
.tdring .c small{font-size:10px;color:var(--muted);font-weight:600;margin-top:2px}
.tdwkbox{width:100%;background:#EAF6EF;border-radius:10px;padding:8px 10px;display:flex;flex-direction:column;gap:4px;align-items:flex-start}
.tdwkbox.achter{background:#FDEEDF}
.tdwkbox small{font-size:11px;line-height:1.35;color:var(--ink)}
.cvchip.achter{background:var(--orange)}
.tdwkr{flex:1;min-width:0;display:flex;flex-direction:column;justify-content:center}
.tdwkc{display:flex;align-items:center;gap:8px;padding:5px 0}
.tdwkc .nm{width:96px;font-size:12px;font-weight:600;flex:0 0 auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tdwkc .cnt{width:36px;text-align:right;font-size:11.5px;color:var(--muted);font-weight:600;flex:0 0 auto}
.tdbar.sm{position:relative;height:6px;overflow:visible;flex:1}
.tdbar.sm i{border-radius:5px}
.tdbar.sm .mk{position:absolute;top:-3px;bottom:-3px;width:1.5px;background:#7A7F85;border-radius:1px}
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
.tdpk5{display:flex;align-items:center;gap:8px;margin:2px 0 4px;padding:0 4px;font-size:11.5px;color:var(--muted);cursor:pointer}
.tdpk5 .tlpk{background:#FBDCC7;color:#2B2F33;opacity:.9}
.tdpk5 span:nth-child(2){font-weight:600;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.tdpk5 small{white-space:nowrap;margin-left:auto;font-size:11px}
.tdpknav small{font-size:11px;color:var(--muted);font-weight:700;min-width:26px;text-align:center}
.tdpknav .xbtn[disabled]{opacity:.35}
@media(max-width:699px){.tdgrid #cvAgenda{height:420px;flex:none}.tdgrid .cvlinks>#tdPiek{margin-bottom:0}.tdwk{gap:10px}.tdwkl{flex:0 0 128px}.tdring,.tdring svg{width:92px;height:92px}.tdwkc .nm{width:70px}}
'''
s=s[:old_css_start]+css+s[old_css_end:]
s=s.replace('const APP_VERSION="v312";','const APP_VERSION="v313";')
open(p,'w',encoding='utf-8').write(s)
w=open('c226/sw.js').read();open('c226/sw.js','w').write(w.replace('jo-ladder-v312','jo-ladder-v313'))
print('ok')
