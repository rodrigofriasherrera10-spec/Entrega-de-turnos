/* EFE Turnos — Calendario: navegación, render, filtro fecha */
function initCal(){calYear=NOW.getFullYear();calMonth=NOW.getMonth();buildCalSels();renderCal();}
function buildCalSels(){
  const m=document.getElementById('calM'),y=document.getElementById('calY');if(!m||!y)return;
  m.innerHTML=MESES.map((x,i)=>`<option value="${i}"${i===calMonth?' selected':''}>${x}</option>`).join('');
  const cy=NOW.getFullYear();let yh='';
  for(let i=cy-4;i<=cy+1;i++)yh+=`<option value="${i}"${i===calYear?' selected':''}>${i}</option>`;
  y.innerHTML=yh;document.getElementById('calTitle').textContent=MESES[calMonth]+' '+calYear;
}
function calGoTo(){calMonth=+document.getElementById('calM').value;calYear=+document.getElementById('calY').value;buildCalSels();renderCal();}
function calPrev(){if(calMonth===0){calMonth=11;calYear--;}else calMonth--;buildCalSels();renderCal();}
function calNext(){if(calMonth===11){calMonth=0;calYear++;}else calMonth++;buildCalSels();renderCal();}
function calToday(){calYear=NOW.getFullYear();calMonth=NOW.getMonth();dateFilter=null;clearDF();buildCalSels();renderCal();}
function renderCal(){
  const g=document.getElementById('calGrid');if(!g)return;
  const byDate={};
  turnos.forEach(t=>{if(!t.fecha)return;if(!byDate[t.fecha])byDate[t.fecha]=[];byDate[t.fecha].push(t);});
  const ts=NOW.toISOString().split('T')[0];
  const fd=new Date(calYear,calMonth,1).getDay();
  const dim=new Date(calYear,calMonth+1,0).getDate();
  let h=DIAS.map(d=>`<div class="cal-dow">${d}</div>`).join('');
  for(let i=0;i<fd;i++)h+=`<div class="cal-day empty"></div>`;
  for(let d=1;d<=dim;d++){
    const ds=`${calYear}-${String(calMonth+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const dt=byDate[ds]||[];
    let dots='';
    if(dt.some(t=>t.tipo_cierre==='total'))dots+=`<div class="cal-dot" style="background:var(--cyan)"></div>`;
    if(dt.some(t=>t.tipo_cierre==='parcial'))dots+=`<div class="cal-dot" style="background:var(--orange)"></div>`;
    if(dt.some(t=>SECS.some(s=>t.sectores?.[s]?.trenesFalla?.length>0)))dots+=`<div class="cal-dot" style="background:var(--red)"></div>`;
    h+=`<div class="cal-day${ds===ts?' today':''}${ds===dateFilter?' sel':''}${dt.length?' has-data':''}" onclick="selDate('${ds}')">
      <div class="cal-day-num">${d}</div>
      ${dots?`<div class="cal-dots">${dots}</div>`:''}
    </div>`;
  }
  const rem=(7-(fd+dim)%7)%7;for(let i=0;i<rem;i++)h+=`<div class="cal-day empty"></div>`;
  g.innerHTML=h;
}
function selDate(ds){
  dateFilter=dateFilter===ds?null:ds;renderCal();
  if(dateFilter){const[y,m,d]=ds.split('-');
    document.getElementById('afLabel').textContent=`📅 ${parseInt(d)} de ${MESES[parseInt(m)-1]} de ${y}`;
    document.getElementById('af').style.display='flex';
  }else document.getElementById('af').style.display='none';
  renderHist();
}
function clearDF(){dateFilter=null;document.getElementById('af').style.display='none';renderCal();renderHist();}
function toggleCal(){const w=document.getElementById('calWrap');w.style.display=w.style.display==='none'?'block':'none';if(w.style.display==='block')initCal();}