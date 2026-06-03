"""
EFE Metro Valparaíso — Sistema de Entrega de Turnos v4
Flujo colaborativo: cada sector escribe desde su PC en tiempo real
Cierre parcial (por turno) y cierre total del día
"""
from flask import Flask, jsonify, request, send_file, abort
from flask_socketio import SocketIO, emit
import json, os, io, time, socket as socket_lib, smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, Image as RLImage)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
LOGO_FILE = os.path.join(BASE_DIR, "static_logo.png")

# Usar /data si existe (Railway Volume), si no usar directorio local
DATA_DIR  = "/data" if os.path.isdir("/data") else BASE_DIR
DATA_FILE = os.path.join(DATA_DIR, "turnos_data.json")
LIVE_FILE = os.path.join(DATA_DIR, "turno_activo.json")

SMTP_HOST   = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT   = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER   = os.environ.get("SMTP_USER", "")
SMTP_PASS   = os.environ.get("SMTP_PASS", "")
CORREO_DEST = "ilinea@metrovalparaiso.cl"
PORT        = int(os.environ.get("PORT", "5000"))

EFE_AZUL  = colors.HexColor("#0B2D6B")
EFE_ROJO  = colors.HexColor("#C8102E")
EFE_GRIS  = colors.HexColor("#F2F5F9")
EFE_GRIS2 = colors.HexColor("#DCE3EC")
EFE_NEGRO = colors.HexColor("#1A1A2E")
EFE_MUTED = colors.HexColor("#5A6A82")
WHITE     = colors.white
SEC_COL   = {"Limache": colors.HexColor("#1D9E75"),
             "Belloto": colors.HexColor("#0B5EA8"),
             "Puerto":  colors.HexColor("#C8102E")}
SECTORES  = ["Limache","Belloto","Puerto"]

app = Flask(__name__, 
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY","efe_v4_2024")
socketio = SocketIO(app, cors_allowed_origins="*")

# ── Persistencia ─────────────────────────────
_cache_turnos = None
_cache_live   = None

def load_turnos():
    global _cache_turnos
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE,"r",encoding="utf-8") as f:
                _cache_turnos = json.load(f)
                return _cache_turnos
    except: pass
    if _cache_turnos is None: _cache_turnos = []
    return _cache_turnos

def save_turnos(data):
    global _cache_turnos
    _cache_turnos = data
    try:
        with open(DATA_FILE,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
    except Exception as e: print(f"Warning save_turnos: {e}")

def load_live():
    global _cache_live
    try:
        if os.path.exists(LIVE_FILE):
            with open(LIVE_FILE,"r",encoding="utf-8") as f:
                _cache_live = json.load(f)
                return _cache_live
    except: pass
    if _cache_live is None: _cache_live = {}
    return _cache_live

def save_live(data):
    global _cache_live
    _cache_live = data
    try:
        with open(LIVE_FILE,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
    except Exception as e: print(f"Warning save_live: {e}")

# ── API TURNO ACTIVO (colaborativo en tiempo real) ──
@app.route("/api/live", methods=["GET"])
def get_live():
    return jsonify(load_live())





@app.route("/api/novedades_log", methods=["GET"])
def get_novedades_log():
    log = load_live().get("novedades_log", [])
    return jsonify(log)

@app.route("/api/novedad", methods=["POST"])
def post_novedad():
    d = request.get_json()
    txt = d.get("texto","").strip()
    autor = d.get("autor","").strip() or "Sin nombre"
    if not txt:
        return jsonify({"ok": False, "msg": "Novedad vacía"})
    live = load_live() or {}
    if not live.get("id"):
        live["id"] = int(time.time()*1000)
    if "novedades_log" not in live:
        live["novedades_log"] = []
    sector   = d.get("sector","").strip()
    severidad = d.get("severidad","info")
    adjuntos  = d.get("adjuntos",[])
    entrada = {
        "id":        int(time.time()*1000),
        "texto":     txt,
        "autor":     autor,
        "sector":    sector,
        "severidad": severidad,
        "adjuntos":  adjuntos,
        "hora":      datetime.now().strftime("%H:%M"),
        "fecha":     datetime.now().strftime("%d/%m/%Y"),
    }
    live["novedades_log"].insert(0, entrada)
    save_live(live)
    socketio.emit("novedad_nueva", entrada)
    socketio.emit("live_update", live)
    return jsonify({"ok": True, "entrada": entrada})

@app.route("/api/live/update", methods=["POST"])
def update_live():
    d = request.get_json()
    live = load_live() or {}
    # Merge incoming data into live state
    for key in ["turno","fecha","hora","entrega","recibe","sector","clima","novedades"]:
        if key in d: live[key] = d[key]
    if "sectores" in d:
        if "sectores" not in live: live["sectores"] = {}
        for sec, val in d["sectores"].items():
            live["sectores"][sec] = val
    if not live.get("id"): live["id"] = int(time.time()*1000)
    save_live(live)
    socketio.emit("live_update", live)
    return jsonify({"ok": True})

@app.route("/api/live/iniciar", methods=["POST"])
def iniciar_turno():
    d = request.get_json()
    live = {
        "id":         int(time.time()*1000),
        "fecha":      d.get("fecha",""),
        "turno":      d.get("turno",""),
        "iniciado":   datetime.now().isoformat(),
        "estado":     "activo",
        "sectores": {
            "Limache": {"inspector":"","trenesFalla":[],"infra":"","ops":"","pend":"","cerrado":False},
            "Belloto": {"inspector":"","trenesFalla":[],"infra":"","ops":"","pend":"","cerrado":False},
            "Puerto":  {"inspector":"","trenesFalla":[],"infra":"","ops":"","pend":"","cerrado":False},
        },
        "novedades":  "",
        "responsable": d.get("responsable",""),
    }
    save_live(live)
    socketio.emit("live_update", live)
    return jsonify({"ok":True,"live":live})

@app.route("/api/live/sector", methods=["POST"])
def update_sector():
    d = request.get_json()
    live = load_live()
    if not live: return jsonify({"ok":False,"msg":"No hay turno activo"}),400
    sec = d.get("sector")
    if sec not in SECTORES: return jsonify({"ok":False,"msg":"Sector inválido"}),400
    live["sectores"][sec]["inspector"]   = d.get("inspector","")
    live["sectores"][sec]["trenesFalla"] = d.get("trenesFalla",[])
    live["sectores"][sec]["infra"]       = d.get("infra","")
    live["sectores"][sec]["ops"]         = d.get("ops","")
    live["sectores"][sec]["pend"]        = d.get("pend","")
    live["novedades"] = d.get("novedades", live.get("novedades",""))
    save_live(live)
    socketio.emit("live_update", live)
    return jsonify({"ok":True})

@app.route("/api/live/cerrar", methods=["POST"])
def cerrar_turno():
    d = request.get_json()
    tipo = d.get("tipo","parcial")  # "parcial" o "total"
    quien = d.get("quien","")
    live = load_live()
    if not live: return jsonify({"ok":False,"msg":"No hay turno activo"}),400

    registro = {
        "id":            int(time.time()*1000),
        "timestamp":     datetime.now().isoformat(),
        "tipo_cierre":   tipo,
        "cerrado_por":   quien,
        "hora_cierre":   datetime.now().strftime("%H:%M"),
        "fecha":         d.get("fecha","") or live.get("fecha",""),
        "turno":         d.get("turno","") or live.get("turno",""),
        "sector":        d.get("sector","") or live.get("sector",""),
        "clima":         d.get("clima","") or live.get("clima",""),
        "entrega":       d.get("entrega","") or live.get("entrega",""),
        "recibe":        d.get("recibe","") or live.get("recibe",""),
        "novedades":     d.get("novedades","") or live.get("novedades",""),
        "novedades_log": live.get("novedades_log",[]),
        "sectores":      live.get("sectores",{}),
    }

    turnos = load_turnos()
    turnos.insert(0, registro)
    save_turnos(turnos)

    if tipo == "total":
        save_live({})
        socketio.emit("live_update", {})
    else:
        live["estado"] = "activo"
        save_live(live)
        socketio.emit("live_update", live)

    socketio.emit("turno_cerrado", registro)
    return jsonify({"ok":True,"id":registro["id"]})

@app.route("/api/live/cancelar", methods=["POST"])
def cancelar_live():
    save_live({})
    socketio.emit("live_update", {})
    return jsonify({"ok":True})

# ── API HISTORIAL ────────────────────────────

@app.route("/api/live/limpiar", methods=["POST"])
def limpiar_live():
    d = request.get_json() or {}
    borrar_logs = d.get("borrar_logs", False)
    live = load_live() or {}
    if borrar_logs:
        nueva_live = {}
    else:
        # Conserva todos los logs
        nueva_live = {
            "novedades_log": live.get("novedades_log", []),
            "obs_log":       live.get("obs_log", []),
            "fallas_log":    live.get("fallas_log", []),
        }
    save_live(nueva_live)
    socketio.emit("live_update", nueva_live)
    return jsonify({"ok": True})


@app.route("/api/obs_log", methods=["POST"])
def post_obs_log():
    d = request.get_json()
    sec   = d.get("sector","")
    tipo  = d.get("tipo","")
    txt   = d.get("texto","").strip()
    autor = d.get("autor","Sin nombre")
    if not txt or sec not in ["Limache","Belloto","Puerto"]:
        return jsonify({"ok": False, "msg": "Datos inválidos"})
    live = load_live() or {}
    if not live.get("id"): live["id"] = int(time.time()*1000)
    if "obs_log" not in live: live["obs_log"] = []
    entrada = {
        "id": int(time.time()*1000),
        "sector": sec, "tipo": tipo,
        "texto": txt, "autor": autor,
        "hora": datetime.now().strftime("%H:%M"),
        "fecha": datetime.now().strftime("%d/%m/%Y"),
    }
    live["obs_log"].insert(0, entrada)
    save_live(live)
    socketio.emit("obs_nueva", entrada)
    return jsonify({"ok": True})

@app.route("/api/falla_log", methods=["POST"])
def post_falla_log():
    d = request.get_json()
    sec    = d.get("sector","")
    fallas = d.get("fallas",[])
    autor  = d.get("autor","Sin nombre")
    if not fallas or sec not in ["Limache","Belloto","Puerto"]:
        return jsonify({"ok": False, "msg": "Datos inválidos"})
    live = load_live() or {}
    if not live.get("id"): live["id"] = int(time.time()*1000)
    if "fallas_log" not in live: live["fallas_log"] = []
    entrada = {
        "id": int(time.time()*1000),
        "sector": sec, "fallas": fallas,
        "autor": autor,
        "hora": datetime.now().strftime("%H:%M"),
        "fecha": datetime.now().strftime("%d/%m/%Y"),
    }
    live["fallas_log"].insert(0, entrada)
    save_live(live)
    socketio.emit("falla_nueva", entrada)
    return jsonify({"ok": True})

@app.route("/api/logs_dia", methods=["GET"])
def get_logs_dia():
    live = load_live() or {}
    return jsonify({
        "obs_log":    live.get("obs_log", []),
        "fallas_log": live.get("fallas_log", []),
    })


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"ok": False, "msg": "No file"})
    file = request.files['file']
    context = request.form.get('context','general')
    if not file.filename:
        return jsonify({"ok": False, "msg": "Empty filename"})
    import re, uuid
    # Sanitize filename
    ext = os.path.splitext(file.filename)[1].lower()
    safe_name = re.sub(r'[^a-zA-Z0-9_-]','_', os.path.splitext(file.filename)[0])
    filename = f"{safe_name}_{uuid.uuid4().hex[:8]}{ext}"
    upload_dir = os.path.join(DATA_DIR, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    return jsonify({"ok": True, "url": f"/uploads/{filename}", "filename": filename})

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    import re
    if re.search(r'[^a-zA-Z0-9._-]', filename):
        abort(400)
    upload_dir = os.path.join(DATA_DIR, "uploads")
    return send_file(os.path.join(upload_dir, filename))

@app.route("/api/turnos", methods=["GET"])
def get_turnos():
    return jsonify(load_turnos())

@app.route("/api/turnos/<int:tid>", methods=["DELETE"])
def delete_turno(tid):
    data = [t for t in load_turnos() if t.get("id")!=tid]
    save_turnos(data)
    socketio.emit("turno_eliminado",{"id":tid})
    return jsonify({"ok":True})

@app.route("/api/pdf/<int:tid>")
def get_pdf(tid):
    t = next((x for x in load_turnos() if x.get("id")==tid),None)
    if not t: abort(404)
    buf = generar_pdf(t)
    return send_file(buf, mimetype="application/pdf", as_attachment=True,
                     download_name=f"Turno_{t.get('fecha','').replace('/','_')}_{t.get('turno','')}.pdf")

@app.route("/api/email/<int:tid>", methods=["POST"])
def send_email_route(tid):
    t = next((x for x in load_turnos() if x.get("id")==tid),None)
    if not t: return jsonify({"ok":False,"msg":"No encontrado"}),404
    dest = (request.get_json() or {}).get("destino",CORREO_DEST)
    if not SMTP_USER or not SMTP_PASS:
        return jsonify({"ok":False,"msg":"SMTP no configurado","pdf_url":f"/api/pdf/{tid}"})
    try:
        buf = generar_pdf(t); enviar_correo(t,buf,dest)
        return jsonify({"ok":True,"msg":f"Enviado a {dest}"})
    except Exception as e:
        return jsonify({"ok":False,"msg":str(e)}),500

@app.route("/api/status")
def status():
    try: ip = socket_lib.gethostbyname(socket_lib.gethostname())
    except: ip = "cloud"
    live = load_live()
    return jsonify({"ok":True,"ip":ip,"total":len(load_turnos()),
                    "turno_activo": bool(live),
                    "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S")})

@app.route("/")
def index():
    from flask import render_template
    return render_template("index.html")

@app.route("/logo.png")
def logo():
    return send_file(LOGO_FILE, mimetype="image/png")

@socketio.on("connect")
def on_connect():
    emit("sync_turnos", load_turnos())
    emit("live_update",  load_live())

# ── PDF ──────────────────────────────────────
def generar_pdf(t):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.8*cm, rightMargin=1.8*cm,
                            topMargin=1.2*cm, bottomMargin=1.8*cm)
    W = A4[0]-3.6*cm
    story = []
    def sty(n,**k): return ParagraphStyle(n,**k)

    logo_img = RLImage(LOGO_FILE,width=3.5*cm,height=3.0*cm) if os.path.exists(LOGO_FILE) else Paragraph("EFE",sty("l",fontName="Helvetica-Bold",fontSize=24,textColor=EFE_AZUL))

    tipo_cierre = t.get("tipo_cierre","parcial")
    badge_cierre = "CIERRE PARCIAL" if tipo_cierre=="parcial" else "CIERRE TOTAL DEL DÍA"
    badge_col = colors.HexColor("#F59E0B") if tipo_cierre=="parcial" else EFE_AZUL

    sector_txt = t.get('sector','')
    sector_txt  = t.get('sector','')
    clima_txt   = t.get('clima','')
    sector_line = f"Sector: {sector_txt}   " if sector_txt else ""
    clima_line  = f"Clima: {clima_txt}   " if clima_txt else ""
    hdr_right = [
        Paragraph("EFE VALPARAÍSO", sty("t",fontName="Helvetica-Bold",fontSize=13,textColor=EFE_AZUL,alignment=TA_CENTER)),
        Spacer(1,3),
        Paragraph("Inspectores de Línea — Entrega de Turno", sty("s",fontName="Helvetica",fontSize=9,textColor=EFE_MUTED,alignment=TA_CENTER)),
        Spacer(1,4),
        Paragraph(f"{t.get('turno','')}  ·  {badge_cierre}", sty("tr",fontName="Helvetica-Bold",fontSize=10,textColor=badge_col,alignment=TA_CENTER)),
        Spacer(1,3),
        Paragraph(f"{sector_line}{clima_line}Fecha: {t.get('fecha','')}   Cierre: {t.get('hora_cierre','')}   Cerrado por: {t.get('cerrado_por','')}", sty("d",fontName="Helvetica",fontSize=8,textColor=EFE_MUTED,alignment=TA_CENTER)),
    ]
    hdr = Table([[logo_img,hdr_right]],colWidths=[3.8*cm,W-3.8*cm])
    hdr.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6)]))
    story += [hdr, Spacer(1,0.3*cm),
              HRFlowable(width=W,thickness=3,color=EFE_AZUL),
              HRFlowable(width=W,thickness=2,color=EFE_ROJO,spaceAfter=6)]

    def tbl_h(txt,col=EFE_AZUL):
        tb = Table([[Paragraph(f"  {txt}",sty(f"h{txt[:5]}",fontName="Helvetica-Bold",fontSize=9,textColor=WHITE))]],colWidths=[W])
        tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),col),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        return tb

    story.append(tbl_h("DATOS DEL TURNO"))
    story.append(Spacer(1,2))
    # Tabla datos turno - 2 filas
    dt1 = Table([[
        Paragraph("Quien entrega:",sty("fl0",fontName="Helvetica-Bold",fontSize=8,textColor=EFE_AZUL)),
        Paragraph(t.get("entrega","—"),sty("fv0",fontName="Helvetica",fontSize=9,textColor=EFE_NEGRO)),
        Paragraph("Quien recibe:",sty("fl0b",fontName="Helvetica-Bold",fontSize=8,textColor=EFE_AZUL)),
        Paragraph(t.get("recibe","—") or "—",sty("fv0b",fontName="Helvetica",fontSize=9,textColor=EFE_NEGRO)),
    ]],colWidths=[2.8*cm,W/2-2.8*cm,2.8*cm,W/2-2.8*cm])
    dt1.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),EFE_GRIS),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),8)]))

    sector_val = t.get("sector","—") or "—"
    dt2 = Table([[
        Paragraph("Sector:",sty("fl1",fontName="Helvetica-Bold",fontSize=8,textColor=EFE_AZUL)),
        Paragraph(sector_val,sty("fv1",fontName="Helvetica",fontSize=9,textColor=EFE_NEGRO)),
        Paragraph("Novedades:",sty("fl2",fontName="Helvetica-Bold",fontSize=8,textColor=EFE_AZUL)),
        Paragraph(t.get("novedades","—") or "—",sty("fv2",fontName="Helvetica",fontSize=9,textColor=EFE_NEGRO,leading=11)),
    ]],colWidths=[2.8*cm,W/2-2.8*cm,2.8*cm,W/2-2.8*cm])
    dt2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),EFE_GRIS),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),8)]))
    story += [dt1, Spacer(1,1), dt2, Spacer(1,0.4*cm)]

    # Novedades del día log
    nov_log = t.get("novedades_log", [])
    if nov_log:
        story.append(tbl_h("NOVEDADES DEL DÍA"))
        story.append(Spacer(1,3))
        sec_colors_hex = {"Limache": colors.HexColor("#1D9E75"),
                          "Belloto": colors.HexColor("#1A5FBB"),
                          "Puerto":  colors.HexColor("#C8102E")}
        for i, nov in enumerate(nov_log):
            sec_n  = nov.get("sector","")
            sc     = sec_colors_hex.get(sec_n, EFE_AZUL)
            sec_badge = f" [{sec_n}]" if sec_n else ""
            cab_s  = sty(f"nc{i}", fontName="Helvetica-Bold", fontSize=7,
                         textColor=sc)
            txt_s  = sty(f"nt{i}", fontName="Helvetica", fontSize=8,
                         textColor=EFE_NEGRO, leading=11)
            hora   = nov.get("hora","")
            autor  = nov.get("autor","—")
            texto  = nov.get("texto","")
            nr = Table([[
                Paragraph(f"{autor}{sec_badge}  {hora}", cab_s),
                Paragraph(texto, txt_s)
            ]], colWidths=[4*cm, W-4*cm])
            nr.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,-1), EFE_GRIS if i%2==0 else WHITE),
                ('TOPPADDING',(0,0),(-1,-1),3),
                ('BOTTOMPADDING',(0,0),(-1,-1),3),
                ('LEFTPADDING',(0,0),(0,-1),8),
                ('LEFTPADDING',(1,0),(1,-1),6),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LINEBELOW',(0,0),(-1,-1),0.3,EFE_GRIS2),
            ]))
            story.append(nr)
        story.append(Spacer(1,0.3*cm))

    story.append(tbl_h("SECTORES"))
    story.append(Spacer(1,4))

    for sec in SECTORES:
        sd = t.get("sectores",{}).get(sec,{})
        col = SEC_COL.get(sec,EFE_AZUL)
        nf = len(sd.get("trenesFalla",[]))
        insp = sd.get("inspector","")
        badge = f"  ⚠ {nf} en falla" if nf else "  ✔ Sin fallas"
        sh = Table([[
            Paragraph(f"  {sec.upper()}{('  ·  '+insp) if insp else ''}",sty(f"sh{sec}",fontName="Helvetica-Bold",fontSize=9,textColor=WHITE)),
            Paragraph(badge,sty(f"sb{sec}",fontName="Helvetica-Bold",fontSize=8,textColor=WHITE if nf else colors.HexColor("#AAFFCC")))
        ]],colWidths=[W*0.6,W*0.4])
        sh.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),col),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(0,-1),8),('ALIGN',(1,0),(1,0),'RIGHT'),('RIGHTPADDING',(1,0),(1,0),8)]))
        story.append(sh)
        for tren in sd.get("trenesFalla",[]):
            tr = Table([[Paragraph(f"🚨 {tren.get('tid','—')}  |  Tipo: {tren.get('tipo','')}  |  Andén: {tren.get('anden','')}",sty(f"tr{sec}",fontName="Helvetica-Bold",fontSize=8,textColor=EFE_ROJO))]],colWidths=[W])
            tr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor("#FEF0F0")),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),12),('BOX',(0,0),(-1,-1),0.5,EFE_ROJO)]))
            story.append(tr)
            if tren.get("obs"):
                ob = Table([[Paragraph(f"   Obs: {tren['obs']}",sty(f"to{sec}",fontName="Helvetica",fontSize=8,textColor=EFE_NEGRO,leading=11))]],colWidths=[W])
                ob.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor("#FFF8F8")),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),12)]))
                story.append(ob)
        lbl_s = sty(f"obsLbl{sec}",fontName="Helvetica-Bold",fontSize=8,textColor=EFE_AZUL)
        val_s = sty(f"obsVal{sec}",fontName="Helvetica",fontSize=9,textColor=EFE_NEGRO,leading=13)
        val_empty = sty(f"obsEmp{sec}",fontName="Helvetica",fontSize=9,textColor=EFE_MUTED,leading=13)

        def obs_row(lbl, val):
            v_sty = val_s if val and val.strip() else val_empty
            v_txt = val if val and val.strip() else "Sin observaciones"
            r = Table([[Paragraph(lbl, lbl_s), Paragraph(v_txt, v_sty)]],
                      colWidths=[3.5*cm, W-3.5*cm])
            r.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,-1),EFE_GRIS),
                ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                ('LEFTPADDING',(0,0),(0,-1),10),('LEFTPADDING',(1,0),(1,-1),8),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LINEBELOW',(0,0),(-1,-1),0.5,EFE_GRIS2),
            ]))
            return r

        story.append(obs_row("Infraestructura:", sd.get("infra","")))
        story.append(Spacer(1,1))
        story.append(obs_row("Personal / Operaciones:", sd.get("ops","")))
        story.append(Spacer(1,1))
        story.append(obs_row("Pendientes siguiente turno:", sd.get("pend","")))
        story.append(Spacer(1,0.35*cm))

    story += [
        HRFlowable(width=W,thickness=1.5,color=EFE_AZUL,spaceBefore=4),
        HRFlowable(width=W,thickness=1,color=EFE_ROJO,spaceAfter=4),
        Paragraph(f"EFE Metro Valparaíso  |  {badge_cierre}  |  {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                  sty("pie",fontName="Helvetica",fontSize=7,textColor=EFE_MUTED,alignment=TA_CENTER))
    ]
    doc.build(story)
    buf.seek(0)
    return buf

def enviar_correo(t,pdf_buf,destino):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER; msg["To"] = destino
    tipo = "CIERRE PARCIAL" if t.get("tipo_cierre")=="parcial" else "CIERRE TOTAL"
    msg["Subject"] = f"EFE Turnos — {tipo} — {t.get('turno','')} — {t.get('fecha','')}"
    msg.attach(MIMEText(f"EFE Metro Valparaíso\n{tipo}\n\nTurno: {t.get('turno','')}\nFecha: {t.get('fecha','')}\nCerrado por: {t.get('cerrado_por','')}\nHora: {t.get('hora_cierre','')}\n\nSe adjunta el PDF.", "plain","utf-8"))
    part = MIMEBase("application","octet-stream")
    part.set_payload(pdf_buf.read()); encoders.encode_base64(part)
    part.add_header("Content-Disposition",f'attachment; filename="Turno_{t.get("fecha","").replace("/","_")}.pdf"')
    msg.attach(part)
    with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as srv:
        srv.starttls(); srv.login(SMTP_USER,SMTP_PASS)
        srv.sendmail(msg["From"],[destino],msg.as_string())

if __name__ == "__main__":
    try: ip = socket_lib.gethostbyname(socket_lib.gethostname())
    except: ip = "127.0.0.1"
    print(f"\n  EFE TURNOS v4  →  http://localhost:{PORT}  |  http://{ip}:{PORT}\n")
    socketio.run(app, host="0.0.0.0", port=PORT, debug=False)
