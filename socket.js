/* EFE Turnos — Componentes: cards, fields, botones, sectores, fallas */
/* CARDS */
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px;margin-bottom:12px;}
.card-title{font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:12px;display:flex;align-items:center;gap:8px;font-family:'IBM Plex Mono',monospace;}
.card-title::after{content:'';flex:1;height:1px;background:var(--border);}

/* GRID */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:11px;}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:11px;margin-bottom:11px;}

/* FIELDS */
.field{display:flex;flex-direction:column;gap:4px;}
.field label{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;}
.field input,.field select,.field textarea{font-family:'Inter',sans-serif;font-size:13px;color:var(--text);background:var(--bg3);border:1px solid var(--border2);border-radius:7px;padding:8px 10px;width:100%;transition:border-color .2s,box-shadow .2s;}
.field input:focus,.field select:focus,.field textarea:focus{outline:none;border-color:var(--blue);box-shadow:0 0 0 3px rgba(37,99,235,.2);}
.field textarea{resize:vertical;min-height:66px;}
.field select{appearance:none;cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24'%3E%3Cpath fill='%237A90B8' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 9px center;padding-right:28px;}
.field select option{background:var(--bg3);color:var(--text);}

/* SECTOR TABS */
.sector-tabs{display:flex;gap:5px;margin-bottom:12px;}
.stab{flex:1;padding:9px 6px;text-align:center;font-size:12px;font-weight:600;border-radius:7px;cursor:pointer;background:var(--bg3);color:var(--muted);border:1px solid var(--border2);transition:all .2s;position:relative;}
.stab.al{background:rgba(34,197,94,.12);color:#22C55E;border-color:rgba(34,197,94,.4);}
.stab.ab{background:rgba(56,189,248,.12);color:#38BDF8;border-color:rgba(56,189,248,.4);}
.stab.ap{background:rgba(239,68,68,.12);color:#F87171;border-color:rgba(239,68,68,.4);}
.fbadge{position:absolute;top:-7px;right:-7px;background:var(--red);color:#fff;font-size:9px;font-weight:700;width:17px;height:17px;border-radius:50%;display:none;align-items:center;justify-content:center;}
.fbadge.show{display:flex;}
.spanel{display:none;}
.spanel.active{display:block;}

/* FALLA */
.falla-item{border:1px solid rgba(239,68,68,.4);border-radius:8px;padding:11px 13px;margin-bottom:9px;background:rgba(239,68,68,.06);animation:fadeIn .2s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(-5px);}to{opacity:1;transform:translateY(0);}}
.falla-head{display:flex;align-items:center;gap:8px;margin-bottom:9px;}
.falla-num{font-size:10px;font-family:'IBM Plex Mono',monospace;color:var(--red);background:rgba(239,68,68,.15);padding:2px 8px;border-radius:4px;font-weight:500;}
.falla-del{margin-left:auto;background:none;border:none;cursor:pointer;color:var(--red);font-size:16px;line-height:1;padding:2px 5px;border-radius:4px;}
.falla-del:hover{background:rgba(239,68,68,.2);}
.falla-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin-bottom:8px;}
.falla-grid .field input,.falla-grid .field select,.falla-item .field textarea{background:var(--bg2);border-color:var(--border2);}
.falla-item .field textarea{min-height:50px;}
.btn-add-falla{width:100%;padding:8px;margin-bottom:12px;border:1px dashed rgba(239,68,68,.5);border-radius:7px;background:none;cursor:pointer;color:var(--red);font-size:12px;font-weight:600;font-family:'Inter',sans-serif;display:flex;align-items:center;justify-content:center;gap:6px;transition:background .15s;}
.btn-add-falla:hover{background:rgba(239,68,68,.08);}
.divider{height:1px;background:var(--border);margin:12px 0;}

/* VISTA OTROS SECTORES */
.live-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:4px;}
.live-sec{background:var(--bg3);border:1px solid var(--border2);border-radius:8px;padding:10px 12px;}
.live-sec-head{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;display:flex;align-items:center;gap:6px;}
.live-sec-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.live-sec-insp{font-size:11px;color:var(--cyan);margin-bottom:4px;}
.live-sec-falla{font-size:11px;color:#F87171;padding:2px 0;}
.live-sec-obs{font-size:11px;color:var(--muted);margin-top:2px;line-height:1.4;}
.live-sec-obs strong{color:var(--text);font-weight:500;}
.live-sec-empty{font-size:11px;color:var(--muted2);font-style:italic;}

/* AUTOSAVE */
.autosave-bar{display:flex;align-items:center;justify-content:space-between;margin-top:12px;}
.autosave-label{font-size:11px;color:var(--muted);font-family:'IBM Plex Mono',monospace;}

/* BOTONES CIERRE */
.cierre-bar{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px;}
@media(max-width:600px){.cierre-bar{grid-template-columns:1fr;}}

/* BUTTONS */
.btn{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:7px;font-family:'Inter',sans-serif;font-size:12px;font-weight:600;cursor:pointer;border:none;transition:all .2s;white-space:nowrap;}
.btn-primary{background:var(--blue);color:#fff;}
.btn-primary:hover{background:#1D4ED8;transform:translateY(-1px);box-shadow:0 4px 12px rgba(37,99,235,.4);}
.btn-warning{background:rgba(245,158,11,.2);color:var(--orange);border:1px solid rgba(245,158,11,.4);}
.btn-warning:hover{background:var(--orange);color:#fff;}
.btn-danger{background:rgba(239,68,68,.2);color:var(--red);border:1px solid rgba(239,68,68,.4);}
.btn-danger:hover{background:var(--red);color:#fff;}
.btn-ghost{background:var(--bg3);color:var(--muted);border:1px solid var(--border2);}
.btn-ghost:hover{color:var(--text);}
.btn-full{width:100%;justify-content:center;padding:11px;font-size:13px;}
.btn-sm{padding:4px 9px;font-size:11px;}