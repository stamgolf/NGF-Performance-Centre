p='c226/index.html'
s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)

# ---------- A. Week: fase naast weeklabel + ingeklapte Urenbalans ----------
rep(""" if(pid){
  var pd=(mw&&mw.phase)?phaseDef(mw.phase):null;
  var phB=pd?'<button class="tpphase" onclick="openPhaseInfo(\\''+mw.phase+'\\')"><span class="phbadge sm" style="background:'+pd[2]+'">'+pd[5]+'</span><b>'+esc(pd[1])+'</b></button>':'<span class="muted" style="font-size:12.5px">Geen periodisering</span>';
  var _cats=[["golf","Golf (Z)"],["golfb","Golf (B)"],["fysiek","Fysiek (Z)"],["fysb","Fysiek (B)"]];
  var _tot=0;var subStats=_cats.map(function(c){var m2=typeMinutesWeek(pid,ws,c[0]);_tot+=m2;return '<span class="wg-si"><i style="background:'+wkTypeMeta(c[0])[2]+'"></i>'+c[1]+' '+fmtUren(m2)+'</span>';}).join("");
  subStats='<div class="wg-sub">'+subStats+'<span class="wg-si wg-tot">Totaal '+fmtUren(_tot)+'</span></div>';
  K+='<div class="card"><div class="cardhd"><h3>Uren deze week</h3>'+phB+'</div>'+wkUrenHtml(pid,ws)+'</div>';
 }
 return K;}""",
""" if(pid){
  /* v317: fase naast het weeklabel; uren als ingeklapte Urenbalans onder het weekraster */
  var pd=(mw&&mw.phase)?phaseDef(mw.phase):null;
  var phB=pd?'<button class="tpphase" onclick="openPhaseInfo(\\''+mw.phase+'\\')" style="margin-left:4px"><span class="phbadge sm" style="background:'+pd[2]+'">'+pd[5]+'</span><b>'+esc(pd[1])+'</b></button>':'';
  if(phB)K=K.replace('data-cnav="1">\\u203a</button>','data-cnav="1">\\u203a</button>'+phB);
  K+=wkUrenBalansCard(pid,ws);
 }
 return K;}
var wkUrenOpen=false;
function wkUrenBalansCard(pid,ws){
 var gz=0,gb=0,fz=0,fb=0;try{gz=typeMinutesWeek(pid,ws,"golf");gb=typeMinutesWeek(pid,ws,"golfb");fz=typeMinutesWeek(pid,ws,"fysiek");fb=typeMinutesWeek(pid,ws,"fysb");}catch(_e){}
 var tot=gz+gb+fz+fb;var N=urenNormFor(pid,ws);var nT=N.golf+N.fysiek;
 function pil(v,lab,norm){var ok=norm>0?(v>=norm):null;return '<span class="ubpil"><b'+(ok===true?' class="groen"':(ok===false?' class="oranje"':''))+'>'+fmtUren(v)+'</b><small>'+lab+'</small></span>';}
 var sum=tot?(pil(gz+gb,"golf",N.golf)+pil(fz+fb,"fysiek",N.fysiek)+pil(tot,"totaal",nT)+'<span class="ubpil"><b>'+fmtUren(nT)+'</b><small>norm</small></span>'):'<span class="sx">nog geen trainingsuren</span>';
 function balk(lab,z,b,norm,cz,cb){var mx=Math.max(norm,z+b,1);var pz=Math.round(100*z/mx),pb=Math.round(100*b/mx),pn=Math.round(100*norm/mx);
  return '<div class="ub"><div class="t"><span>'+lab+'</span><small>'+fmtUren(z+b)+(norm?' · norm '+fmtUren(norm):'')+'</small></div><div class="tr"><i style="left:0;width:'+pz+'%;background:'+cz+'"></i><i style="left:'+pz+'%;width:'+pb+'%;background:'+cb+'"></i>'+(norm?'<span class="mk" style="left:'+Math.min(99,pn)+'%"></span>':'')+'</div></div>';}
 var body='';
 if(!tot)body='<p class="muted" style="margin:0;font-size:13px">Nog geen trainingsuren in deze week — zet je weekrooster klaar via het roostericoon bovenin.</p>';
 else{
  var wb=null;try{wb=activeBlocksWeek(pid,ws);}catch(_e){}
  var perDag=[0,0,0,0,0,0,0];if(wb)wb.blocks.forEach(function(b){if(["golf","golfb","fysiek","fysb"].indexOf(b.type)<0)return;perDag[b.day]+=blockMin(b);});
  var mxD=Math.max.apply(null,perDag.concat([1]));var vandaag=todayISO();
  var dag='<div class="ubmini">'+CAL_WD.map(function(w,i){var dd=dAddDays(ws,i);return '<span class="'+(dd===vandaag?'nu':'')+'"><i style="height:'+Math.round(100*perDag[i]/mxD)+'%"></i><small>'+w+'</small><b>'+(perDag[i]?fmtUren(perDag[i]).replace(' u',''):'')+'</b></span>';}).join("")+'</div>';
  body='<div class="ubwrap"><div>'+balk("Golf",gz,gb,N.golf,wkTypeMeta("golf")[2],wkTypeMeta("golfb")[2])+balk("Fysiek",fz,fb,N.fysiek,wkTypeMeta("fysiek")[2],wkTypeMeta("fysb")[2])+balk("Totaal",gz+fz,gb+fb,nT,"#B9BEC4","#2B2F33")
   +'<div class="ulegend" style="margin-top:8px"><span><i style="background:'+wkTypeMeta("golf")[2]+'"></i>golf zelfst.</span><span><i style="background:'+wkTypeMeta("golfb")[2]+'"></i>golf begeleid</span><span><i style="background:'+wkTypeMeta("fysiek")[2]+'"></i>fysiek zelfst.</span><span><i style="background:'+wkTypeMeta("fysb")[2]+'"></i>fysiek begeleid</span><span class="unorm">streepje = norm'+(N.fase?' · fase '+esc(phaseAb(N.fase)):'')+'</span></div></div>'
   +'<div><div class="trlbl" style="margin:0 0 6px">Per dag</div>'+dag+'</div></div>';}
 return '<div class="card ubcard'+(wkUrenOpen?' open':'')+'"><div class="ubh" onclick="wkUrenOpen=!wkUrenOpen;renderPlanning()"><h3>Urenbalans</h3><span class="ubsum">'+sum+'</span><span class="chev">\\u25b6</span></div>'+(wkUrenOpen?'<div class="ubb">'+body+'</div>':'')+'</div>';}""")

# ---------- B. To-do: kolommen per categorie, groepsopdrachten erboven ----------
rep("""  body='<div class="card"><div class="row spread" style="align-items:center"><h3 style="margin:0">To-do deze week'+(plan.edited?' <span class="sx">(aangepast)</span>':'')+'</h3><button class="xbtn sm" id="tpRegen" title="Opnieuw genereren">↻</button></div>'+progRow+'<div class="tdcatlist">'+catRows+'</div></div>';
 }""",
"""  /* v317: kolommen per categorie met de oefeningen direct op de pagina */
  var _wctxT=null;try{_wctxT=planCtxFor(pid,ws);}catch(e){}
  function _row(o){var x=o.it.x||1,dn=Math.min(o.it.doneN||0,x);var dots='';for(var i=0;i<x;i++)dots+='<i class="'+(i>=x-dn?'on':'')+'"></i>';return '<div class="tdtodo'+(itemFull(o.it)?' done':'')+'" data-open="'+o.d.id+'">'+tickBtnHtml(o.it,o.d.id)+'<span class="tdtnm">'+esc(o.d.title)+'</span>'+(o.d.always?'':whyChipHtml(drillReason(o.d,_wctxT)))+'<span class="tddots">'+dots+'</span></div>';}
  var cols=TODOCATS.map(function(c){var arr=itemsOf(c[0]);var e2=execTotals(arr.map(function(o){return o.it;}));var p2=e2.t?Math.round(100*e2.d/e2.t):0;
   arr.sort(function(a,b){return (itemFull(a.it)?1:0)-(itemFull(b.it)?1:0)||(a.d.title||"").localeCompare(b.d.title||"","nl");});
   return '<div class="card tpcol"><div class="cardhd"><h3><span class="cvdot" style="background:'+mcAccent(c[0])+'"></span>'+c[1]+'</h3><span class="row" style="gap:6px;align-items:center"><span class="hdnote">'+e2.d+'/'+e2.t+'</span><button class="xbtn sm" data-tpadd="'+c[0]+'" title="Oefening toevoegen" style="font-size:15px;font-weight:700">+</button></span></div><div class="tpkbar"><i style="width:'+p2+'%;background:'+mcAccent(c[0])+'"></i></div>'
    +(arr.length?arr.map(_row).join(""):'<p class="muted" style="margin:6px 0 0;font-size:12.5px">Geen oefeningen in deze categorie.</p>')+'</div>';}).join("");
  body='<div class="tpkan">'+cols+'</div>';
  var _regen='<button class="xbtn sm" id="tpRegen" title="Opnieuw genereren">↻</button>';
  head=head.replace('<button class="xbtn sm" id="tpNext">›</button>','<button class="xbtn sm" id="tpNext">›</button>'+(plan.edited?'<span class="sx">(aangepast)</span>':'')+(progRow?'<span class="tpprog">'+progRow+'</span>':'')).replace('id="tpToday" style="margin-left:auto;','id="tpToday" style="').replace('</svg></button></div>','</svg></button>'+_regen+'</div>');
 }""")
# groepsopdrachten boven de categorieën
rep(" box.innerHTML=head+focusCard+body+gsCards;"," box.innerHTML=head+focusCard+gsCards+body;")
# bindings voor de kolommen (chk, open, add)
rep(""" box.querySelectorAll("[data-copen]").forEach(function(r){r.onclick=function(){openCatTodos(pid,ws,r.dataset.copen);};});
}
function openDrillPicker(pid,ws,mk){""",
""" box.querySelectorAll("[data-copen]").forEach(function(r){r.onclick=function(){openCatTodos(pid,ws,r.dataset.copen);};});
 box.querySelectorAll(".tpkan [data-chk]").forEach(function(b){b.onclick=function(ev){ev.stopPropagation();var pl=planItemsNorm(planFor(pid,ws));planTick(pl,pid,b.dataset.chk,null);};});
 box.querySelectorAll(".tpkan .tdtodo[data-open]").forEach(function(r){r.onclick=function(e){if(e.target.closest("[data-chk]"))return;drillDetail(r.dataset.open,{mode:'plan',pid:pid,ws:ws});};});
 box.querySelectorAll("[data-tpadd]").forEach(function(b){b.onclick=function(){openDrillPicker(pid,ws,b.dataset.tpadd);};});
}
function openDrillPicker(pid,ws,mk){""")

css='''/* v317: Urenbalans (week) + To-do kolommen */
.ubcard{padding:0;overflow:hidden}
.ubh{display:flex;align-items:center;gap:10px;padding:12px 15px;cursor:pointer;-webkit-tap-highlight-color:transparent}
.ubh h3{margin:0;font-family:var(--fd);font-weight:500;font-size:16.5px;flex:0 0 auto}
.ubsum{display:flex;gap:6px;flex-wrap:wrap;flex:1;min-width:0;justify-content:flex-end}
.ubpil{display:inline-flex;align-items:baseline;gap:5px;background:var(--paper);border-radius:999px;padding:4px 11px;white-space:nowrap}
.ubpil b{font-family:var(--fd);font-size:14px;font-weight:600}.ubpil b.groen{color:#17a05c}.ubpil b.oranje{color:var(--orange)}
.ubpil small{font-size:9.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.ubh .chev{color:var(--muted);font-size:12px;transition:.2s;display:inline-block;flex:0 0 auto}
.ubcard.open .ubh .chev{transform:rotate(90deg)}
.ubb{padding:4px 15px 14px;border-top:1px solid var(--line)}
.ubwrap{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:20px;padding-top:10px}
.ub{margin:4px 0 12px}
.ub .t{display:flex;justify-content:space-between;font-size:12.5px;font-weight:600;margin-bottom:5px}.ub .t small{color:var(--muted);font-weight:600;font-size:11.5px}
.ub .tr{position:relative;height:10px;background:#e9eef4;border-radius:5px}
.ub .tr i{position:absolute;top:0;bottom:0;border-radius:5px}
.ub .tr .mk{position:absolute;top:-4px;bottom:-4px;width:2px;background:#7A7F85;border-radius:1px}
.ubmini{display:flex;gap:4px;align-items:flex-end;height:96px;padding-top:4px}
.ubmini span{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;min-width:0}
.ubmini span i{display:block;width:100%;background:#D5DDE9;border-radius:3px 3px 0 0;min-height:2px}
.ubmini span.nu i{background:#4A6FA5}
.ubmini span small{font-size:9px;color:#9A9EA3;font-weight:700;margin-top:4px;text-transform:uppercase}
.ubmini span b{font-size:10px;font-weight:700;color:var(--muted);order:-1;margin-bottom:3px;height:12px}
.tpkan{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;align-items:start;margin-bottom:14px}
.tpcol{padding:11px 12px}
.tpcol .cardhd{padding-bottom:6px;margin-bottom:0}
.tpcol .cardhd h3{margin:0;font-family:var(--fd);font-weight:500;font-size:14.5px;display:flex;align-items:center;gap:7px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tpcol .cardhd>span.row{flex:0 0 auto}
.tpkbar{height:5px;border-radius:3px;background:#e9eef4;margin:6px 0 6px;overflow:hidden}.tpkbar i{display:block;height:100%;border-radius:3px}
.tpcol .tdtodo{padding:6px 0;border-bottom:1px solid var(--line);font-size:12.5px}
.tpcol .tdtodo:last-child{border-bottom:0}
.tpcol .tdtodo.done .tdtnm{text-decoration:line-through}
.tpprog{display:inline-flex;align-items:center;min-width:180px;margin-left:auto}
.tpprog .tdprog{margin:0;flex:1}
@media(max-width:1000px){.tpkan{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:699px){.tpkan{grid-template-columns:1fr}.ubwrap{grid-template-columns:1fr}.ubsum{justify-content:flex-start}}
'''
rep('/* v316: jaarplan icoonknoppen + maandslider */',css+'/* v316: jaarplan icoonknoppen + maandslider */')
s=s.replace('const APP_VERSION="v316";','const APP_VERSION="v317";')
open(p,'w',encoding='utf-8').write(s)
w=open('c226/sw.js').read();open('c226/sw.js','w').write(w.replace('jo-ladder-v316','jo-ladder-v317'))
print('ok')
