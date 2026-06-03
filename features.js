/* EFE Turnos — Features: severidad, adjuntos, clima, badges, búsqueda */
/* ── SEVERIDAD ── */
.sev-bar{display:flex;gap:5px;margin-bottom:8px;flex-wrap:wrap;}
.sev-btn{padding:4px 12px;border-radius:20px;border:1px solid;font-size:11px;font-weight:600;cursor:pointer;font-family:'IBM Plex Mono',monospace;background:none;transition:all .15s;}
.sev-btn:hover,.sev-btn.active{color:#fff!important;}
.sev-info{color:#38BDF8;border-color:#38BDF8;}
.sev-info.active,.sev-info:hover{background:#38BDF8;}
.sev-prec{color:#F59E0B;border-color:#F59E0B;}
.sev-prec.active,.sev-prec:hover{background:#F59E0B;}
.sev-crit{color:#EF4444;border-color:#EF4444;}
.sev-crit.active,.sev-crit:hover{background:#EF4444;}

/* ── ADJUNTOS ── */
.attach-btn{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border:1px dashed var(--border2);border-radius:6px;cursor:pointer;font-size:11px;color:var(--muted);background:none;font-family:'Inter',sans-serif;transition:all .15s;}
.attach-btn:hover{color:var(--cyan);border-color:var(--cyan);}
.attach-list{display:flex;flex-wrap:wrap;gap:5px;margin-top:5px;}
.attach-item{display:flex;align-items:center;gap:4px;padding:3px 9px;background:var(--bg3);border:1px solid var(--border2);border-radius:5px;font-size:11px;color:var(--text);}
.attach-item button{background:none;border:none;cursor:pointer;color:var(--muted2);font-size:13px;line-height:1;padding:0 2px;}
.attach-item button:hover{color:var(--red);}

/* ── CLIMA ── */
.clima-select{font-family:'Inter',sans-serif;font-size:13px;color:var(--text);background:var(--bg3);border:1px solid var(--border2);border-radius:7px;padding:8px 10px;width:100%;appearance:none;cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24'%3E%3Cpath fill='%237A90B8' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 9px center;padding-right:28px;}
.clima-select option{background:var(--bg3);color:var(--text);}

/* ── BADGE NUEVO en pestaña inactiva ── */
.tab-new-badge{position:absolute;top:-5px;left:-5px;width:9px;height:9px;border-radius:50%;background:var(--red);display:none;animation:pulseBadge 1.5s infinite;}
.tab-new-badge.show{display:block;}
@keyframes pulseBadge{0%,100%{transform:scale(1);opacity:1;}50%{transform:scale(1.4);opacity:.7;}}

/* ── BÚSQUEDA NOVEDADES ── */
.nov-search{width:100%;font-family:'Inter',sans-serif;font-size:12px;background:var(--bg3);color:var(--text);border:1px solid var(--border2);border-radius:7px;padding:7px 10px;margin-bottom:8px;transition:border-color .2s;}
.nov-search:focus{outline:none;border-color:var(--cyan);}

/* ── BOTÓN FALLA = ÁMBAR ── */
.btn-add-falla{width:100%;padding:8px;margin-bottom:0;border:1px dashed rgba(245,158,11,.6);border-radius:7px;background:none;cursor:pointer;color:var(--orange);font-size:12px;font-weight:600;font-family:'Inter',sans-serif;display:flex;align-items:center;justify-content:center;gap:6px;transition:background .15s;}
.btn-add-falla:hover{background:rgba(245,158,11,.1);}