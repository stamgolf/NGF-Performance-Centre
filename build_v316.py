p='c226/index.html'
s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)

# 1. wellness: readiness/slaap/schaal-staven donkerder tegen de papieren achtergrond
rep('var WL_C={grey:"#D9DCE0",','var WL_C={grey:"#B9BEC4",')

# 2. klachten-toggle standaard op Lichaam
rep('var wlKlView="stroken",klZone=null','var wlKlView="body",klZone=null')

# 3. scoring scoreverloop: staafdiagram + volgorde
rep('scScKind="dot", scYrMetric="score", scXMode="time",','scScKind="bar", scYrMetric="score", scXMode="seq",')

# 4. logboek periodefilter: deze week / deze maand
rep('\n if(f.mode==="m1"||f.mode==="m3"||f.mode==="m6"||f.mode==="m12"||f.mode==="m60"){var cut=scMonthsAgo({m1:1,m3:3,m6',
    '\n if(f.mode==="wk"){var _ws=weekStart(todayISO());return L.filter(function(e){return e.date>=_ws&&e.date<=dAddDays(_ws,6);});}\n if(f.mode==="mnd"){var _m0=todayISO().slice(0,7);return L.filter(function(e){return String(e.date).slice(0,7)===_m0;});}\n if(f.mode==="m1"||f.mode==="m3"||f.mode==="m6"||f.mode==="m12"||f.mode==="m60"){var cut=scMonthsAgo({m1:1,m3:3,m6')
rep('<option value="all"\'+(f.mode==="all"?" selected":"")+\'>Alles</option><option value="m1"',
    '<option value="all"\'+(f.mode==="all"?" selected":"")+\'>Alles</option><option value="wk"\'+(f.mode==="wk"?" selected":"")+\'>Deze week</option><option value="mnd"\'+(f.mode==="mnd"?" selected":"")+\'>Deze maand</option><option value="m1"')

# 5. toernooidoelen-kiezer bij meerdere toernooien
rep(' var _ttg=$("#tdTgB");if(_ttg)_ttg.onclick=function(){if(_upc.length)openTourGoalsForm(_upc[0].ed.id,pid);};',
    ' var _ttg=$("#tdTgB");if(_ttg)_ttg.onclick=function(){if(!_upc.length)return;if(_upc.length===1){openTourGoalsForm(_upc[0].ed.id,pid);return;}tdKiesToernooi(_upc,pid,dt);};')
kies=r'''/* v316: kiezer "voor welk toernooi?" (toernooidoelen vanuit Vandaag) */
function tdKiesToernooi(upc,pid,dt){var sh=$("#sheet");if(!sh)return;
 sh.innerHTML='<div class="shead"><div><h2>Toernooidoelen</h2><div class="sx">Voor welk toernooi? · '+esc(nameOf(pid))+'</div></div><button class="xbtn" onclick="closeSheet()">×</button></div>'
  +'<div class="card">'+upc.map(function(e){var m2=edMeta(e.ed);var pk=peakNum(e.pp.peak);var days=dDiffDays(dt,e.start);var tg=edTourGoalsGet(e.ed,pid);
   return '<div class="cvrow" data-kies-ed="'+e.ed.id+'"><span class="tlpk" style="background:'+(pk?peakColor(pk):'#e6ebef')+';color:'+(pk>=4?"#fff":"#16202B")+'">'+(pk?'P'+pk:'–')+'</span><span style="flex:1;min-width:0"><b>'+esc(m2.name)+'</b><small>'+fmtRange(e.ed)+(e.ed.location?' · '+esc(e.ed.location):'')+(tg?' · doelen gezet ✓':'')+'</small></span><span class="cvtijd">'+(e.start<=dt?'bezig':(days===0?'vandaag':'over '+days+' dgn'))+'</span><span class="cvpijl">›</span></div>';}).join("")+'</div>';
 sh.querySelectorAll("[data-kies-ed]").forEach(function(r){r.onclick=function(){openTourGoalsForm(r.dataset.kiesEd,pid);};});
 openSheet();}
'''
rep('function tdIco(id,title,svg){',kies+'function tdIco(id,title,svg){')

# 6. Jaarplan: weergaven Jaar · 6 mnd · 3 mnd · Periode; maand-slider in jaarweergave; icoonknoppen
rep('if(perView.mode==="year")panels=[{m0:0,m1:11,t:"HELE JAAR "+year}];',
    'var _cm=(String(year)===todayISO().slice(0,4))?(+todayISO().slice(5,7)-1):0;\n if(perView.mode==="year"){var _yf=(perView.from||0),_yt=(perView.to==null?11:perView.to);if(_yt<_yf)_yt=_yf;panels=[{m0:_yf,m1:_yt,t:(_yf===0&&_yt===11)?("HELE JAAR "+year):((MFULL[_yf]+" \\u2013 "+MFULL[_yt]).toUpperCase()+" "+year)}];}\n else if(perView.mode==="half"){var _h0=Math.min(_cm,6);panels=[{m0:_h0,m1:Math.min(11,_h0+5),t:"KOMENDE 6 MAANDEN \\u00b7 "+(MFULL[_h0]+" \\u2013 "+MFULL[Math.min(11,_h0+5)]).toUpperCase()}];}\n else if(perView.mode==="quarter"){var _q0=Math.min(_cm,9);panels=[{m0:_q0,m1:Math.min(11,_q0+2),t:"KOMENDE 3 MAANDEN \\u00b7 "+(MFULL[_q0]+" \\u2013 "+MFULL[Math.min(11,_q0+2)]).toUpperCase()}];}')
rep('+[["year","Jaar"],["half","Halfjaar"],["quarter","Kwartaal"],["period","Periode"]].map(',
    '+[["year","Jaar"],["half","6 mnd"],["quarter","3 mnd"],["period","Periode"]].map(')
# componenten-checkbox -> icoonknoppen (volume/intensiteit, componenten)
rep('''+'<label class="rubtoggle percomptg"><input type="checkbox" id="perCompTg"'+(perCompOn?" checked":"")+'><span class="sx">Componenten</span></label></div>';''',
    '''+'<span class="row" style="gap:6px;margin-left:auto"><button class="xbtn sm pertg'+(perVolOn?" on":"")+'" id="perVolTg" title="Volume en intensiteit tonen/verbergen" aria-label="Volume en intensiteit">'+PER_ICO.vol+'</button><button class="xbtn sm pertg'+(perCompOn?" on":"")+'" id="perCompTg" title="Componenten (fundament · scherpte · ritme · frisheid)" aria-label="Componenten">'+PER_ICO.comp+'</button></span></div>';''')
rep(''' var _ct=bar.querySelector("#perCompTg");if(_ct)_ct.onchange=function(){perCompOn=_ct.checked;renderPlanning();};''',
    ''' var _ct=bar.querySelector("#perCompTg");if(_ct)_ct.onclick=function(){perCompOn=!perCompOn;renderPlanning();};
 var _vt=bar.querySelector("#perVolTg");if(_vt)_vt.onclick=function(){perVolOn=!perVolOn;renderPlanning();};
 var _ma=$("#perMA"),_mb=$("#perMB"),_ml=$("#perMLbl");
 function _mlab(){if(_ml)_ml.textContent=MFULL[+_ma.value]+" \\u2013 "+MFULL[+_mb.value];}
 if(_ma&&_mb){_ma.oninput=function(){if(+_ma.value>+_mb.value)_mb.value=_ma.value;_mlab();};_mb.oninput=function(){if(+_mb.value<+_ma.value)_ma.value=_mb.value;_mlab();};
  _ma.onchange=_mb.onchange=function(){perView={mode:"year",idx:null,from:+_ma.value,to:+_mb.value};renderPlanning();};}''')

rep('''perView=(m==="period")?{mode:"period",from:(perView.from||0),to:(perView.to==null?11:perView.to)}:{mode:m,idx:null};renderPlanning();''',
    '''perView=(m==="period")?{mode:"period",from:(perView.from||0),to:(perView.to==null?11:perView.to)}:{mode:m,idx:null,from:0,to:11};renderPlanning();''')
# vol/int alleen tekenen als perVolOn
rep('''   if(!perCompOn){
   var area="M"+volPts[0][0].toFixed(1)''','''   if(!perCompOn&&perVolOn){
   var area="M"+volPts[0][0].toFixed(1)''')
rep('''  +(perCompOn?'<span class="perlegi"><i style="background:#1baf7a"></i>Fundament</span><span class="perlegi"><i style="background:#eda100"></i>Scherpte</span><span class="perlegi"><i style="background:#2a78d6"></i>Ritme</span><span class="perlegi"><i style="background:#008300"></i>Frisheid</span>':'<span class="perlegi"><i style="background:#5B7A94"></i>Volume</span><span class="perlegi"><i style="background:#F47C20"></i>Intensiteit</span>')+'</div>';''',
    '''  +(perCompOn?'<span class="perlegi"><i style="background:#1baf7a"></i>Fundament</span><span class="perlegi"><i style="background:#eda100"></i>Scherpte</span><span class="perlegi"><i style="background:#2a78d6"></i>Ritme</span><span class="perlegi"><i style="background:#008300"></i>Frisheid</span>':(perVolOn?'<span class="perlegi"><i style="background:#5B7A94"></i>Volume</span><span class="perlegi"><i style="background:#F47C20"></i>Intensiteit</span>':''))+'</div>';''')
# kopknoppen: Wat als? -> icoon, + Fase -> +
rep('''<div style="display:flex;align-items:center;gap:10px"><button class="btn '+(perSimActive(pid,year)?'':'ghost ')+'sm" id="perSimBtn">'+(perSimActive(pid,year)?'Simulatie aan':'Wat als?')+'</button><button class="btn ghost sm" id="perAdd">+ Fase</button></div></div>'+vsel''',
    '''<div style="display:flex;align-items:center;gap:6px"><button class="xbtn sm pertg'+(perSimActive(pid,year)?' on':'')+'" id="perSimBtn" title="'+(perSimActive(pid,year)?'Simulatie aan — klik om te stoppen':'Wat als? · simulatie')+'" aria-label="Wat als">'+PER_ICO.sim+'</button><button class="xbtn sm" id="perAdd" title="Fase toevoegen" aria-label="Fase toevoegen" style="font-size:18px;font-weight:700">+</button></div></div>'+vsel''')
# slider onder het jaarplan (alleen jaarweergave)
rep('''  +panels.map(function(pn,i){return '<div class="perhalf"'+(i?' style="margin-top:14px"':'')+'><div class="perhalf-t">'+pn.t+'</div>'+halfSvg(pn.m0,pn.m1)+'</div>';}).join("")
  +legend;''',
    '''  +panels.map(function(pn,i){return '<div class="perhalf"'+(i?' style="margin-top:14px"':'')+'><div class="perhalf-t">'+pn.t+'</div>'+halfSvg(pn.m0,pn.m1)+'</div>';}).join("")
  +(perView.mode==="year"?('<div class="yrng permrng"><span class="sx">jan</span><div class="yrngs"><input type="range" id="perMA" min="0" max="11" step="1" value="'+(perView.from||0)+'"><input type="range" id="perMB" min="0" max="11" step="1" value="'+(perView.to==null?11:perView.to)+'"></div><span class="sx">dec</span><span class="sx" id="perMLbl" style="min-width:150px;text-align:right;font-weight:700">'+MFULL[perView.from||0]+' \\u2013 '+MFULL[perView.to==null?11:perView.to]+'</span></div>'):'')
  +legend;''')
rep('var perFasenOpen=false;var perCompOn=false;','''var perFasenOpen=false;var perCompOn=false;var perVolOn=true;
var PER_ICO={
 vol:'<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-6 4 3 5-7 4 4"/><path d="M3 21h18"/></svg>',
 comp:'<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 18V9M10 18V5M16 18v-8M22 18H2"/></svg>',
 sim:'<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3v6l-3.5 8a2 2 0 0 0 1.8 3h15.4a2 2 0 0 0 1.8-3L18 9V3"/><path d="M5 3h14M8 14h8"/></svg>'};''')

css='''/* v316: jaarplan icoonknoppen + maandslider */
.xbtn.sm.pertg.on{background:#7A7F85;color:#fff;border-color:#7A7F85}
.permrng{margin:8px 0 2px}
.percomptg{display:none}
'''
k='/* v312/v313: Deze week ring + Volgende piek */'
rep(k,css+k)
s=s.replace('const APP_VERSION="v315";','const APP_VERSION="v316";')
open(p,'w',encoding='utf-8').write(s)
w=open('c226/sw.js').read();open('c226/sw.js','w').write(w.replace('jo-ladder-v315','jo-ladder-v316'))
print('ok')
