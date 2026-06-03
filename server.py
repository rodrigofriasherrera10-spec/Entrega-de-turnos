/* EFE Turnos — Features: severidad, adjuntos, badge tabs, filtro, subir fotos */
function showToast(msg,type='success'){
  const t=document.getElementById('toast');t.textContent=msg;t.className=`show ${type}`;
  clearTimeout(t._t);t._t=setTimeout(()=>t.className='',3500);
}

// INIT
document.getElementById('f-fecha').value=NOW.toISOString().split('T')[0];
document.getElementById('f-hora').value=NOW.toTimeString().slice(0,5);

// ── NOVEDADES LOG ─────────────────────────────
function toggleNovLog() {
  const panel = document.getElementById('novLogPanel');
  const arrow = document.getElementById('novLogArrow');
  if (!panel) return;
  const open = panel.style.display !== 'none';
  panel.style.display = open ? 'none' : 'block';
  arrow.textContent = open ? '▼' : '▲';
}

function renderNovLog(lista) {
  const el  = document.getElementById('novLogList');
  const cnt = document.getElementById('novLogCount');
  if (!el) return;
  if (cnt) cnt.textContent = lista.length;
  if (!lista.length) {
    el.innerHTML = '<div style="text-align:center;padding:20px;color:var(--muted2);font-size:12px;font-style:italic;">Sin novedades aún</div>';
    return;
  }
  const secColor = {Limache:'#22C55E', Belloto:'#38BDF8', Puerto:'#F87171'};
  el.innerHTML = lista.map((n,i) => {
    const sc = secColor[n.sector] || 'var(--cyan)';
    const sb = n.sector
      ? `<span style="font-size:10px;background:${sc}22;color:${sc};padding:2px 8px;border-radius:10px;font-family:'IBM Plex Mono',monospace;font-weight:600;">${n.sector}</span>`
      : '';
    return `<div style="background:var(--bg3);border:1px solid var(--border2);border-radius:7px;padding:9px 12px;" data-idx="${i}">
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px;flex-wrap:wrap;">
        <span style="font-size:11px;font-weight:600;color:var(--cyan);">${n.autor||'—'}</span>
        ${sb}
        <span style="font-size:10px;color:var(--muted2);font-family:'IBM Plex Mono',monospace;margin-left:auto;">${n.hora||''}</span>
        <button onclick="eliminarNovedad(this)" style="background:none;border:none;cursor:pointer;color:var(--muted2);font-size:14px;line-height:1;padding:0 3px;" title="Eliminar" onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='var(--muted2)'">✕</button>
      </div>
      <div style="font-size:13px;color:var(--text);line-height:1.5;white-space:pre-wrap;">${n.texto||''}</div>
    </div>`;
  }).join('');
}

async function cargarNovLog() {
  try {
    const r = await fetch('/api/novedades_log');
    const data = await r.json();
    renderNovLog(data);
  } catch(e) {}
  await cargarTodosLogs();
}

async 
function agregarNovLogLocal(entrada) {
  const el  = document.getElementById('novLogList');
  const cnt = document.getElementById('novLogCount');
  if (!el) return;
  const ph = el.querySelector('[style*="font-style:italic"]');
  if (ph) el.innerHTML = '';
  const div = document.createElement('div');
  div.style.cssText = 'background:var(--bg3);border:1px solid var(--border2);border-radius:7px;padding:9px 12px;';
  div.dataset.id = entrada.id || Date.now();
  const secColor = {Limache:'#22C55E', Belloto:'#38BDF8', Puerto:'#F87171'};
  const sc = secColor[entrada.sector] || 'var(--cyan)';
  const sb = entrada.sector
    ? `<span style="font-size:10px;background:${sc}22;color:${sc};padding:2px 8px;border-radius:10px;font-family:'IBM Plex Mono',monospace;font-weight:600;border:1px solid ${sc}44;">${entrada.sector}</span>`
    : '';
  div.innerHTML = `
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px;flex-wrap:wrap;">
      <span style="font-size:11px;font-weight:600;color:var(--cyan);">${entrada.autor||'—'}</span>
      ${sb}
      <span style="font-size:10px;color:var(--muted2);font-family:'IBM Plex Mono',monospace;margin-left:auto;">${entrada.hora||''}</span>
      <button onclick="eliminarNovedad(this)" style="background:none;border:none;cursor:pointer;color:var(--muted2);font-size:14px;line-height:1;padding:0 3px;" title="Eliminar" onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='var(--muted2)'">✕</button>
    </div>
    <div style="font-size:13px;color:var(--text);line-height:1.5;white-space:pre-wrap;">${entrada.texto||''}</div>`;
  el.insertBefore(div, el.firstChild);
  if (cnt) cnt.textContent = el.children.length;
}

function _publicarNovedad_base() {
  const input  = document.getElementById('f-novedad-input');
  const txt    = (input?.value || '').trim();
  const autor  = document.getElementById('f-entrega')?.value?.trim() || 'Sin nombre';
  const sector = document.getElementById('f-sector')?.value?.trim() || activeSec || '';
  if (!txt) { showToast('Escribe una novedad primero', 'error'); return; }
  if (input) input.value = '';
  const entrada = {
    texto: txt, autor: autor, sector: sector,
    hora: new Date().toLocaleTimeString('es-CL',{hour:'2-digit',minute:'2-digit'}),
    id: Date.now()
  };
  agregarNovLogLocal(entrada);
  const panel = document.getElementById('novLogPanel');
  const arrow = document.getElementById('novLogArrow');
  if (panel) panel.style.display = 'block';
  if (arrow) arrow.textContent = '▲';
  showToast('📢 Novedad publicada', 'success');
  fetch('/api/novedad', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({texto: txt, autor: autor, sector: sector})
  }).catch(() => {});
}

async function refreshTodo() {
  const borrarLogs = confirm('¿Limpiar TODO incluido el historial del día?\n\nOK = borra todo (Reset completo)\nCancelar = solo limpia el formulario');
  if (borrarLogs === null) return; // cerró el diálogo

  ['f-turno','f-entrega','f-recibe'].forEach(id => { const e = document.getElementById(id); if(e) e.value = ''; });
  const fd = document.getElementById('f-fecha');
  const fh = document.getElementById('f-hora');
  if (fd) fd.value = NOW.toISOString().split('T')[0];
  if (fh) fh.value = NOW.toTimeString().slice(0,5);
  const ni = document.getElementById('f-novedad-input');
  if (ni) ni.value = '';
  SECS.forEach(s => {
    fallas[s] = []; fC[s] = 0;
    const fc = document.getElementById('fallas-'+s);
    if (fc) fc.innerHTML = '';
    updateBadge(s);
    [s+'-infra', s+'-ops', s+'-pend'].forEach(id => { const e = document.getElementById(id); if(e) e.value = ''; });
  });
  try {
    await fetch('/api/live/limpiar', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({borrar_logs: borrarLogs})
    });
  } catch(e) {}
  if (borrarLogs) {
    // limpiar listas en pantalla
    ['Limache','Belloto','Puerto'].forEach(s => {
      ['infra','ops','pend'].forEach(t => {
        const el = document.getElementById(`obs-log-list-${s}-${t}`);
        if (el) el.innerHTML = '<div style="text-align:center;padding:10px;color:var(--muted2);font-size:11px;font-style:italic;">Sin registros</div>';
        const cnt = document.getElementById(`cnt-${s}-${t}`);
        if (cnt) cnt.textContent = '0';
      });
      const fl = document.getElementById(`fallas-log-list-${s}`);
      if (fl) fl.innerHTML = '<div style="text-align:center;padding:12px;color:var(--muted2);font-size:11px;font-style:italic;">Sin fallas registradas</div>';
      const fc = document.getElementById(`cnt-fallas-${s}`);
      if (fc) fc.textContent = '0';
    });
    // limpiar novedades
    const nl = document.getElementById('novLogList');
    if (nl) nl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--muted2);font-size:12px;font-style:italic;">Sin novedades aún</div>';
    const nc = document.getElementById('novLogCount');
    if (nc) nc.textContent = '0';
    showToast('🔄 Reset completo — todo borrado', 'warning');
  } else {
    showToast('🔄 Formulario limpiado — historial conservado', 'success');
  }
}

// Socket listener para novedades en tiempo real
socket.on('novedad_nueva', entrada => {
  if (!entrada) return;
  if (document.querySelector(`[data-id="${entrada.id}"]`)) return;
  agregarNovLogLocal(entrada);
  const sc = {Limache:'Limache',Belloto:'Belloto',Puerto:'Puerto'}[entrada.sector]||'';
  showToast('📢 ' + (sc?'['+sc+'] ':'') + (entrada.autor||''), 'info');
});

// Cargar novedades al conectar
socket.on('connect', () => { setSyncOk(); cargarNovLog(); });


// ── OBS & FALLAS LOG ────────────────────────
function toggleLog(panelId) {
  const panel = document.getElementById(panelId);
  if (!panel) return;
  const arrId = panelId.replace('obs-log-','arr-').replace('fallas-log-','arr-fallas-');
  const arrow = document.getElementById(arrId);
  const open  = panel.style.display !== 'none';
  panel.style.display = open ? 'none' : 'block';
  if (arrow) arrow.textContent = open ? '▼' : '▲';
}

function addLogEntry(listId, cntId, entrada) {
  const el  = document.getElementById(listId);
  const cnt = document.getElementById(cntId);
  if (!el) return;
  const ph = el.querySelector('[style*="font-style:italic"]');
  if (ph) el.innerHTML = '';
  const div = document.createElement('div');
  div.style.cssText = 'background:var(--bg3);border:1px solid var(--border2);border-radius:6px;padding:8px 10px;position:relative;';
  div.dataset.id = entrada.id || Date.now();
  div.innerHTML = `
    <div style="display:flex;gap:8px;margin-bottom:3px;align-items:center;">
      <span style="font-size:11px;font-weight:600;color:var(--cyan);">${entrada.autor||'—'}</span>
      <span style="font-size:10px;color:var(--muted2);font-family:'IBM Plex Mono',monospace;">${entrada.hora||''}</span>
      <button onclick="eliminarEntradaLog(this)" style="margin-left:auto;background:none;border:none;cursor:pointer;color:var(--muted2);font-size:14px;line-height:1;padding:0 3px;border-radius:4px;transition:color .15s;" title="Eliminar esta entrada" onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='var(--muted2)'">✕</button>
    </div>
    <div style="font-size:12px;color:var(--text);line-height:1.5;white-space:pre-wrap;">${entrada.texto||''}</div>`;
  el.insertBefore(div, el.firstChild);
  if (cnt) cnt.textContent = el.children.length;
}

function eliminarEntradaLog(btn) {
  const item = btn.closest('[data-id]');
  const list = item?.parentElement;
  const cntEl = list?.parentElement?.parentElement?.querySelector('[id^="cnt-"]');
  if (!item) return;
  item.remove();
  if (cntEl) {
    const remaining = list.querySelectorAll('[data-id]').length;
    cntEl.textContent = remaining;
    if (remaining === 0) {
      list.innerHTML = '<div style="text-align:center;padding:10px;color:var(--muted2);font-size:11px;font-style:italic;">Sin registros</div>';
    }
  }
}

const _lastPub = {};
function publicarObs(sec, tipo) {
  const key = sec + '-' + tipo;
  const now = Date.now();
  if (_lastPub[key] && now - _lastPub[key] < 2000) return;
  _lastPub[key] = now;
  const input = document.getElementById(key);
  const txt   = (input ? input.value : '').trim();
  const autor = (document.getElementById('f-entrega') ? document.getElementById('f-entrega').value : '').trim() || 'Sin nombre';
  if (!txt) { showToast('Escribe algo primero', 'error'); return; }
  const entrada = {
    texto: txt, autor: autor, sector: sec,
    hora: new Date().toLocaleTimeString('es-CL',{hour:'2-digit',minute:'2-digit'}),
    id: Date.now()
  };
  addLogEntry('obs-log-list-' + sec + '-' + tipo, 'cnt-' + sec + '-' + tipo, entrada);
  const panel = document.getElementById('obs-log-' + sec + '-' + tipo);
  const arrow = document.getElementById('arr-' + sec + '-' + tipo);
  if (panel) panel.style.display = 'block';
  if (arrow) arrow.textContent = '▲';
  showToast('📢 ' + sec + ' — publicado', 'success');
  fetch('/api/obs_log', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({sector: sec, tipo: tipo, texto: txt, autor: autor})
  }).catch(function() {});
}

const _lastFalla = {};
function publicarFalla(sec) {
  const now = Date.now();
  if (_lastFalla[sec] && now - _lastFalla[sec] < 2000) return;
  _lastFalla[sec] = now;
  const entradaEl = document.getElementById('f-entrega');
  const autor = (entradaEl ? entradaEl.value : '').trim() || 'Sin nombre';
  const fl = getFallas(sec);
  if (!fl.length) { showToast('Agrega al menos una falla primero', 'error'); return; }
  const entrada = {
    fallas: fl, autor: autor, sector: sec,
    hora: new Date().toLocaleTimeString('es-CL',{hour:'2-digit',minute:'2-digit'}),
    id: Date.now()
  };
  renderFallaLogEntry(sec, entrada);
  const panel = document.getElementById('fallas-log-' + sec);
  const arrow = document.getElementById('arr-fallas-' + sec);
  if (panel) panel.style.display = 'block';
  if (arrow) arrow.textContent = '▲';
  showToast('🚨 Falla registrada — ' + sec, 'success');
  fetch('/api/falla_log', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({sector: sec, fallas: fl, autor: autor})
  }).catch(function() {});
}

async function cargarTodosLogs() {
  try {
    const r = await fetch('/api/logs_dia');
    const d = await r.json();
    // obs logs
    if (d.obs_log) {
      d.obs_log.forEach(e => {
        addLogEntry(`obs-log-list-${e.sector}-${e.tipo}`, `cnt-${e.sector}-${e.tipo}`, e);
      });
    }
    // fallas log
    if (d.fallas_log) {
      d.fallas_log.forEach(e => {
        renderFallaLogEntry(e.sector, e);
      });
    }
  } catch(e) {}
}

function renderFallaLogEntry(sec, entrada) {
  const el  = document.getElementById(`fallas-log-list-${sec}`);
  const cnt = document.getElementById(`cnt-fallas-${sec}`);
  if (!el) return;
  const ph = el.querySelector('[style*="font-style:italic"]');
  if (ph) el.innerHTML = '';
  const div = document.createElement('div');
  div.style.cssText = 'background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.3);border-radius:6px;padding:8px 10px;position:relative;';
  div.dataset.id = entrada.id || Date.now();
  const fallasHtml = (entrada.fallas||[]).map(f =>
    `<div style="font-size:12px;color:#F87171;font-family:'IBM Plex Mono',monospace;">🚨 ${f.tid||'?'} | ${f.tipo||'?'} | Andén: ${f.anden||'?'}</div>
     ${f.obs?`<div style="font-size:11px;color:var(--text);padding-left:14px;">${f.obs}</div>`:''}`
  ).join('');
  div.innerHTML = `
    <div style="display:flex;gap:8px;margin-bottom:4px;align-items:center;">
      <span style="font-size:11px;font-weight:600;color:#F87171;">${entrada.autor||'—'}</span>
      <span style="font-size:10px;color:var(--muted2);font-family:'IBM Plex Mono',monospace;">${entrada.hora||''}</span>
      <button onclick="eliminarEntradaLog(this)" style="margin-left:auto;background:none;border:none;cursor:pointer;color:var(--muted2);font-size:14px;line-height:1;padding:0 3px;border-radius:4px;transition:color .15s;" title="Eliminar esta entrada" onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='var(--muted2)'">✕</button>
    </div>
    ${fallasHtml}`;
  el.insertBefore(div, el.firstChild);
  if (cnt) cnt.textContent = el.children.length;
}

// Socket listeners para obs y fallas en tiempo real
socket.on('obs_nueva', e => {
  addLogEntry(`obs-log-list-${e.sector}-${e.tipo}`, `cnt-${e.sector}-${e.tipo}`, e);
  const panelId = `obs-log-${e.sector}-${e.tipo}`;
  const panel   = document.getElementById(panelId);
  if (panel) panel.style.display = 'block';
  const arr = document.getElementById(`arr-${e.sector}-${e.tipo}`);
  if (arr) arr.textContent = '▲';
  showToast(`📢 ${e.sector}: nueva observación de ${e.autor||'alguien'}`, 'info');
});

socket.on('falla_nueva', e => {
  renderFallaLogEntry(e.sector, e);
  const panel = document.getElementById(`fallas-log-${e.sector}`);
  if (panel) panel.style.display = 'block';
  const arr = document.getElementById(`arr-fallas-${e.sector}`);
  if (arr) arr.textContent = '▲';
  showToast(`🚨 ${e.sector}: nueva falla de ${e.autor||'alguien'}`, 'warning');
});


function eliminarNovedad(btn) {
  const item = btn.closest('div[style]');
  const list = document.getElementById('novLogList');
  const cnt  = document.getElementById('novLogCount');
  if (!item || !list) return;
  item.remove();
  const remaining = list.querySelectorAll('div[style]').length;
  if (cnt) cnt.textContent = remaining;
  if (remaining === 0) {
    list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--muted2);font-size:12px;font-style:italic;">Sin novedades aún</div>';
  }
}

// ── TEMA ─────────────────────────────────────
const THEME_ICONS = {dark:'🌙', light:'☀️', system:'💻'};

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('efe-theme', theme);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = THEME_ICONS[theme];
  // update active state
  ['dark','light','system'].forEach(t => {
    const el = document.getElementById('topt-' + t);
    if (el) el.classList.toggle('active', t === theme);
  });
  closeThemeMenu();
}

function toggleThemeMenu() {
  const m = document.getElementById('themeMenu');
  if (!m) return;
  m.style.display = m.style.display === 'none' ? 'block' : 'none';
}

function closeThemeMenu() {
  const m = document.getElementById('themeMenu');
  if (m) m.style.display = 'none';
}

// Cerrar al clic fuera
document.addEventListener('click', e => {
  if (!e.target.closest('#themeBtn') && !e.target.closest('#themeMenu')) {
    closeThemeMenu();
  }
});

// Cargar tema guardado
(function initTheme() {
  const saved = localStorage.getItem('efe-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = THEME_ICONS[saved];
  ['dark','light','system'].forEach(t => {
    const el = document.getElementById('topt-' + t);
    if (el) el.classList.toggle('active', t === saved);
  });
})();


function buildNovLog(log) {
  if (!log || !log.length) return '';
  const secColor = {Limache:'#22C55E', Belloto:'#38BDF8', Puerto:'#F87171'};
  const items = log.map(n => {
    const sc = secColor[n.sector] || 'var(--cyan)';
    const sb = n.sector ? `<span style="font-size:10px;background:${sc}22;color:${sc};padding:1px 7px;border-radius:10px;font-family:'IBM Plex Mono',monospace;">${n.sector}</span>` : '';
    return `<div style="background:var(--bg3);border:1px solid var(--border2);border-radius:6px;padding:8px 10px;">
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;flex-wrap:wrap;">
        <span style="font-size:11px;font-weight:600;color:var(--cyan);">${n.autor||'—'}</span>
        ${sb}
        <span style="font-size:10px;color:var(--muted2);font-family:'IBM Plex Mono',monospace;margin-left:auto;">${n.hora||''}</span>
      </div>
      <div style="font-size:12px;color:var(--text);line-height:1.4;white-space:pre-wrap;">${n.texto||''}</div>
    </div>`;
  }).join('');
  return `<div style="margin-bottom:12px;">
    <div style="font-size:10px;font-weight:600;color:var(--muted2);letter-spacing:.08em;text-transform:uppercase;font-family:'IBM Plex Mono',monospace;margin-bottom:6px;">📋 Novedades del día (${log.length})</div>
    <div style="display:flex;flex-direction:column;gap:5px;">${items}</div>
  </div>`;
}

// ══════════════════════════════════════════════
// NUEVAS FUNCIONALIDADES
// ══════════════════════════════════════════════

// ── SEVERIDAD ─────────────────────────────────
let _severidad = 'info';
const SEV_COLORS = {
  info: {color:'#38BDF8', label:'ℹ️ Info',      bg:'rgba(56,189,248,.12)'},
  prec: {color:'#F59E0B', label:'⚠️ Precaución', bg:'rgba(245,158,11,.12)'},
  crit: {color:'#EF4444', label:'🔴 Crítico',    bg:'rgba(239,68,68,.12)'},
};
function setSeveridad(sev) {
  _severidad = sev;
  ['info','prec','crit'].forEach(s => {
    const btn = document.getElementById('sev-' + s);
    if (btn) btn.classList.toggle('active', s === sev);
  });
  const ta = document.getElementById('f-novedad-input');
  if (ta) ta.style.borderColor = SEV_COLORS[sev].color;
}

// ── ADJUNTOS ──────────────────────────────────
const _attachments = {};
function addAttach(context, input) {
  if (!_attachments[context]) _attachments[context] = [];
  Array.from(input.files).forEach(f => _attachments[context].push(f));
  renderAttachList(context);
  input.value = '';
}
function removeAttach(context, idx) {
  if (_attachments[context]) _attachments[context].splice(idx, 1);
  renderAttachList(context);
}
function renderAttachList(context) {
  const list = document.getElementById('attach-list-' + context);
  if (!list) return;
  const files = _attachments[context] || [];
  list.innerHTML = files.map((f, i) => {
    const icon = f.type.startsWith('image/') ? '🖼️' : '📄';
    const name = f.name.length > 18 ? f.name.slice(0,15)+'…' : f.name;
    return `<div class="attach-item">${icon} ${name}
      <button onclick="removeAttach('${context}',${i})">✕</button></div>`;
  }).join('');
}
function getAttachNames(ctx) {
  return (_attachments[ctx]||[]).map(f=>f.name);
}

// ── BADGE EN PESTAÑAS ─────────────────────────
function showTabBadge(sec) {
  if (sec === activeSec) return;
  const b = document.getElementById('tnb-' + sec);
  if (b) b.classList.add('show');
}
function clearTabBadge(sec) {
  const b = document.getElementById('tnb-' + sec);
  if (b) b.classList.remove('show');
}

// Override switchSector to clear badge
const _origSwitch = switchSector;
switchSector = function(sec) { _origSwitch(sec); clearTabBadge(sec); };

// ── FILTRO NOVEDADES ──────────────────────────
function filtrarNovLog(q) {
  q = q.toLowerCase().trim();
  document.querySelectorAll('#novLogList > div').forEach(el => {
    el.style.display = (!q || el.textContent.toLowerCase().includes(q)) ? '' : 'none';
  });
}

// ── NOVEDAD CON SEVERIDAD + ADJUNTOS ─────────
// Reemplaza publicarNovedad completamente
function _publicarNovedad_v2() {
  const input  = document.getElementById('f-novedad-input');
  const txt    = (input ? input.value : '').trim();
  const autor  = (document.getElementById('f-entrega')||{value:''}).value.trim() || 'Sin nombre';
  const sector = (document.getElementById('f-sector')||{value:''}).value.trim() || activeSec || '';
  if (!txt) { showToast('Escribe una novedad primero','error'); return; }
  if (input) input.value = '';
  const sev      = _severidad;
  const sevInfo  = SEV_COLORS[sev];
  const adjuntos = getAttachNames('nov');
  _attachments['nov'] = [];
  renderAttachList('nov');
  setSeveridad('info'); // reset
  const entrada = {
    texto:txt, autor:autor, sector:sector, severidad:sev,
    adjuntos:adjuntos,
    hora: new Date().toLocaleTimeString('es-CL',{hour:'2-digit',minute:'2-digit'}),
    id: Date.now()
  };
  _renderNovEntry(entrada);
  const panel = document.getElementById('novLogPanel');
  const arrow = document.getElementById('novLogArrow');
  if (panel) panel.style.display = 'block';
  if (arrow) arrow.textContent = '▲';
  showToast('📢 ' + sevInfo.label + ' publicado','success');
  fetch('/api/novedad',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({texto:txt,autor:autor,sector:sector,severidad:sev,adjuntos:adjuntos})
  }).catch(()=>{});
}

// Render una entrada de novedad con severidad y sector
function _renderNovEntry(entrada) {
  const el  = document.getElementById('novLogList');
  const cnt = document.getElementById('novLogCount');
  if (!el) return;
  const ph = el.querySelector('[style*="font-style:italic"]');
  if (ph) el.innerHTML = '';
  if (document.querySelector(`#novLogList [data-id="${entrada.id}"]`)) return;
  const secColor = {Limache:'#22C55E',Belloto:'#38BDF8',Puerto:'#F87171'};
  const sev     = entrada.severidad || 'info';
  const sevInfo = SEV_COLORS[sev] || SEV_COLORS.info;
  const sc      = secColor[entrada.sector] || 'var(--cyan)';
  const sb      = entrada.sector
    ? `<span style="font-size:10px;background:${sc}22;color:${sc};padding:2px 8px;border-radius:10px;font-family:'IBM Plex Mono',monospace;font-weight:600;">${entrada.sector}</span>` : '';
  const sevBadge = `<span style="font-size:10px;background:${sevInfo.bg};color:${sevInfo.color};padding:2px 8px;border-radius:10px;font-family:'IBM Plex Mono',monospace;font-weight:600;">${sevInfo.label}</span>`;
  const adjHTML  = (entrada.adjuntos||[]).length
    ? `<div style="margin-top:4px;display:flex;flex-wrap:wrap;gap:4px;">${(entrada.adjuntos).map(f=>`<span style="font-size:10px;background:var(--bg3);border:1px solid var(--border2);border-radius:5px;padding:2px 7px;">📎 ${f}</span>`).join('')}</div>` : '';
  const div = document.createElement('div');
  div.style.cssText = `background:${sevInfo.bg};border:1px solid ${sevInfo.color}44;border-radius:7px;padding:9px 12px;`;
  div.dataset.id = entrada.id || Date.now();
  div.innerHTML = `
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px;flex-wrap:wrap;">
      <span style="font-size:11px;font-weight:600;color:var(--cyan);">${entrada.autor||'—'}</span>
      ${sb} ${sevBadge}
      <span style="font-size:10px;color:var(--muted2);font-family:'IBM Plex Mono',monospace;margin-left:auto;">${entrada.hora||''}</span>
      <button onclick="eliminarNovedad(this)" style="background:none;border:none;cursor:pointer;color:var(--muted2);font-size:14px;line-height:1;padding:0 3px;" onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='var(--muted2)'">✕</button>
    </div>
    <div style="font-size:13px;color:var(--text);line-height:1.5;white-space:pre-wrap;">${entrada.texto||''}</div>
    ${adjHTML}`;
  el.insertBefore(div, el.firstChild);
  if (cnt) cnt.textContent = el.children.length;
}

// Override publicarNovedad y agregarNovLogLocal con versiones limpias
publicarNovedad = _publicarNovedad_v2;
agregarNovLogLocal = _renderNovEntry;

// ── SOCKET para obs y fallas con badge ────────
socket.off('obs_nueva');
socket.on('obs_nueva', e => {
  if(!e) return;
  addLogEntry('obs-log-list-'+e.sector+'-'+e.tipo, 'cnt-'+e.sector+'-'+e.tipo, e);
  showTabBadge(e.sector);
  const panel = document.getElementById('obs-log-'+e.sector+'-'+e.tipo);
  if(panel) panel.style.display='block';
  const arr = document.getElementById('arr-'+e.sector+'-'+e.tipo);
  if(arr) arr.textContent='▲';
  showToast('📢 '+e.sector+': obs de '+(e.autor||'alguien'),'info');
});
socket.off('falla_nueva');
socket.on('falla_nueva', e => {
  if(!e) return;
  renderFallaLogEntry(e.sector, e);
  showTabBadge(e.sector);
  const panel = document.getElementById('fallas-log-'+e.sector);
  if(panel) panel.style.display='block';
  const arr = document.getElementById('arr-fallas-'+e.sector);
  if(arr) arr.textContent='▲';
  showToast('🚨 '+e.sector+': falla de '+(e.autor||'alguien'),'warning');
});
socket.off('novedad_nueva');
socket.on('novedad_nueva', e => {
  if(!e) return;
  if(document.querySelector('#novLogList [data-id="'+e.id+'"]')) return;
  _renderNovEntry(e);
  showToast('📢 '+(e.sector?'['+e.sector+'] ':' ')+(e.autor||''),'info');
});

// ── CLIMA en pushLive ──────────────────────────
const _basePushLive = pushLive;
pushLive = async function() {
  // patch clima into the payload before sending
  const climaEl = document.getElementById('f-clima');
  if(climaEl && climaEl.value) {
    // override will be captured by fetch in pushLive via f-clima field
  }
  return _basePushLive();
};

// ── UPLOAD fotos a /data (Railway Volume) ──────
async function subirFoto(file, context) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('context', context);
  try {
    const r = await fetch('/api/upload', {method:'POST', body: formData});
    const d = await r.json();
    return d.ok ? d.url : null;
  } catch(e) { return null; }
}

// Init
setSeveridad('info');