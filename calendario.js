/* EFE Turnos — Historial: calendario, turno cards, obs */
/* HISTORIAL */
.hist-filters{display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap;}
.hist-filters input,.hist-filters select{font-family:'Inter',sans-serif;font-size:12px;background:var(--card2);color:var(--text);border:1px solid var(--border2);border-radius:7px;padding:7px 10px;}
.hist-filters input{flex:1;min-width:160px;}
.hist-filters input:focus,.hist-filters select:focus{outline:none;border-color:var(--blue);}

/* CALENDARIO */
.cal-wrap{background:var(--card);border:1px solid var(--border);border-radius:12px;margin-bottom:12px;overflow:hidden;}
.cal-nav{display:flex;align-items:center;gap:6px;padding:10px 14px;border-bottom:1px solid var(--border);background:var(--bg2);}
.cal-nav-btn{width:28px;height:28px;background:var(--bg3);border:1px solid var(--border2);border-radius:6px;cursor:pointer;color:var(--text);font-size:14px;display:flex;align-items:center;justify-content:center;}
.cal-nav-btn:hover{background:var(--border);}
.cal-month{font-weight:700;font-size:13px;color:var(--cyan);flex:1;text-align:center;font-family:'IBM Plex Mono',monospace;}
.cal-sel{font-family:'IBM Plex Mono',monospace;font-size:11px;background:var(--bg3);color:var(--text);border:1px solid var(--border2);border-radius:5px;padding:3px 6px;cursor:pointer;}
.cal-today{font-size:10px;padding:3px 8px;background:var(--bg3);border:1px solid var(--border2);border-radius:5px;cursor:pointer;color:var(--muted);font-family:'IBM Plex Mono',monospace;}
.cal-today:hover{color:var(--cyan);}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);}
.cal-dow{font-size:10px;font-weight:600;font-family:'IBM Plex Mono',monospace;color:var(--muted2);text-align:center;padding:8px 0;background:var(--bg2);text-transform:uppercase;}
.cal-day{min-height:46px;padding:5px 4px;border-top:1px solid var(--border);border-right:1px solid var(--border);cursor:pointer;transition:background .1s;display:flex;flex-direction:column;align-items:center;gap:2px;}
.cal-day:nth-child(7n){border-right:none;}
.cal-day.empty{cursor:default;background:rgba(0,0,0,.2);opacity:.4;}
.cal-day:not(.empty):hover{background:var(--bg3);}
.cal-day.sel{background:rgba(37,99,235,.2)!important;border-color:var(--blue);}
.cal-day-num{font-size:11px;font-family:'IBM Plex Mono',monospace;color:var(--muted);width:22px;height:22px;display:flex;align-items:center;justify-content:center;border-radius:50%;}
.cal-day.has-data .cal-day-num{color:var(--text);font-weight:700;}
.cal-day.today .cal-day-num{background:var(--blue);color:#fff;}
.cal-day.sel .cal-day-num{color:var(--cyan);font-weight:700;}
.cal-dots{display:flex;gap:2px;flex-wrap:wrap;justify-content:center;}
.cal-dot{width:5px;height:5px;border-radius:50%;}
.cal-legend{display:flex;gap:14px;padding:7px 14px;border-top:1px solid var(--border);background:var(--bg2);}
.cal-leg{display:flex;align-items:center;gap:4px;font-size:10px;color:var(--muted);font-family:'IBM Plex Mono',monospace;}
.cal-leg-dot{width:7px;height:7px;border-radius:50%;}
.af{display:flex;align-items:center;gap:8px;padding:7px 12px;margin-bottom:10px;background:rgba(37,99,235,.1);border:1px solid rgba(37,99,235,.3);border-radius:7px;font-size:12px;color:var(--cyan);}
.af span{flex:1;}
.af button{background:none;border:1px solid rgba(56,189,248,.4);border-radius:4px;padding:2px 7px;font-size:10px;color:var(--cyan);cursor:pointer;font-family:'Inter',sans-serif;}

/* TURNO CARD historial */
.tc{background:var(--card);border:1px solid var(--border);border-radius:12px;margin-bottom:10px;overflow:hidden;transition:border-color .2s;}
.tc:hover{border-color:var(--border2);}
.tc-badge-parcial{display:inline-flex;align-items:center;gap:4px;font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(245,158,11,.15);color:var(--orange);border:1px solid rgba(245,158,11,.3);font-family:'IBM Plex Mono',monospace;font-weight:600;}
.tc-badge-total{display:inline-flex;align-items:center;gap:4px;font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(56,189,248,.15);color:var(--cyan);border:1px solid rgba(56,189,248,.3);font-family:'IBM Plex Mono',monospace;font-weight:600;}
.bfalla{display:inline-flex;align-items:center;gap:3px;font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(239,68,68,.15);color:#F87171;border:1px solid rgba(239,68,68,.3);font-family:'IBM Plex Mono',monospace;font-weight:600;}
.bok{display:inline-flex;align-items:center;gap:3px;font-size:10px;padding:2px 8px;border-radius:20px;background:rgba(34,197,94,.12);color:var(--green);border:1px solid rgba(34,197,94,.3);font-family:'IBM Plex Mono',monospace;font-weight:600;}
.tc-actions{display:flex;gap:6px;padding:7px 14px 0;background:var(--bg2);}
.tc-head{display:flex;align-items:flex-start;gap:10px;padding:11px 14px;background:var(--bg2);border-bottom:1px solid var(--border);cursor:pointer;user-select:none;}
.tc-who{font-weight:700;font-size:13px;color:var(--text);}
.tc-meta{font-size:11px;color:var(--muted);font-family:'IBM Plex Mono',monospace;margin-top:3px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;}
.expand-btn{margin-left:auto;align-self:center;font-size:10px;color:var(--muted2);font-family:'IBM Plex Mono',monospace;display:flex;align-items:center;gap:4px;flex-shrink:0;}
.expand-icon{transition:transform .2s;}
.tc-head.expanded .expand-icon{transform:rotate(180deg);}
.tc-body{padding:14px;display:none;}
.tc-body.open{display:block;}
.det-title{font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted2);font-family:'IBM Plex Mono',monospace;padding-bottom:6px;margin-bottom:8px;border-bottom:1px solid var(--border);}
.nov-block{background:var(--bg3);border-radius:7px;padding:10px 12px;font-size:12px;color:var(--text);line-height:1.6;margin-bottom:12px;white-space:pre-wrap;}
.nov-block.empty{color:var(--muted);font-style:italic;}
.sec-det{border:1px solid var(--border);border-radius:8px;overflow:hidden;margin-bottom:8px;}
.sec-det-head{display:flex;align-items:center;gap:8px;padding:8px 12px;font-size:12px;font-weight:600;}
.sec-det-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.sec-falla-badge{font-size:10px;padding:2px 7px;border-radius:20px;background:rgba(239,68,68,.15);color:#F87171;border:1px solid rgba(239,68,68,.3);font-family:'IBM Plex Mono',monospace;}
.sec-det-body{padding:10px 12px;background:var(--bg2);}
.htren{border:1px solid rgba(239,68,68,.35);border-radius:6px;padding:7px 10px;margin-bottom:6px;background:rgba(239,68,68,.06);}
.htren-title{font-size:11px;font-weight:700;color:#F87171;margin-bottom:2px;font-family:'IBM Plex Mono',monospace;}
.htren-obs{font-size:11px;color:var(--text);margin-top:3px;line-height:1.4;}
.obs-grid{display:flex;flex-direction:column;gap:5px;margin-top:6px;}
.obs-row{display:flex;gap:8px;}
.obs-lbl{font-size:10px;font-family:'IBM Plex Mono',monospace;color:var(--muted2);min-width:100px;padding-top:1px;text-transform:uppercase;}
.obs-val{font-size:12px;color:var(--text);line-height:1.4;white-space:pre-wrap;}
.obs-val.empty{color:var(--muted2);font-style:italic;}
.empty-state{text-align:center;padding:50px 24px;color:var(--muted);}
.empty-state .ico{font-size:40px;display:block;margin-bottom:10px;opacity:.25;}

/* MODAL */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:1000;display:flex;align-items:center;justify-content:center;padding:20px;}
.modal{background:var(--card);border:1px solid var(--border2);border-radius:14px;padding:24px;max-width:400px;width:100%;}
.modal-title{font-size:15px;font-weight:700;color:var(--text);margin-bottom:5px;}
.modal-sub{font-size:12px;color:var(--muted);margin-bottom:18px;line-height:1.5;}
.modal-btns{display:flex;gap:10px;margin-top:16px;}
.modal-btns .btn{flex:1;justify-content:center;}

#toast{position:fixed;bottom:20px;right:20px;padding:10px 16px;border-radius:8px;font-size:12px;font-weight:600;z-index:9999;transform:translateY(60px);opacity:0;transition:all .3s cubic-bezier(.34,1.56,.64,1);pointer-events:none;border:1px solid transparent;}
#toast.show{transform:translateY(0);opacity:1;}
#toast.success{background:rgba(34,197,94,.15);color:var(--green);border-color:rgba(34,197,94,.3);}
#toast.error{background:rgba(239,68,68,.15);color:#F87171;border-color:rgba(239,68,68,.3);}
#toast.info{background:rgba(37,99,235,.2);color:var(--cyan);border-color:rgba(56,189,248,.3);}
#toast.warning{background:rgba(245,158,11,.15);color:var(--orange);border-color:rgba(245,158,11,.3);}

@media(max-width:768px){
  .sidebar{display:none;}
  .g2,.g3,.falla-grid,.live-grid,[style*="grid-template-columns:1fr 1fr 1fr 1fr"]{grid-template-columns:1fr 1fr!important;}
  .mobile-bottom-bar{display:flex!important;}
  .content-area{padding:14px 12px 100px;}
}
@media(max-width:480px){
  .g2,[style*="grid-template-columns:1fr 1fr 1fr 1fr"]{grid-template-columns:1fr!important;}
}
@media(min-width:769px){.mobile-bottom-bar{display:none!important;}}