# -*- coding: utf-8 -*-
"""Cuadernillo de práctica AMC — problemas ABIERTOS (con espacio para respuesta y
justificación), para trabajar y conversar con docentes. Parecidos pero NO iguales a
los ítems de opción múltiple de la app. 16 problemas, 4 bandas de dificultad, temas
variados y contextualizados. Clave de respuestas para docentes al final.
Aritmética de la clave verificada al final del script antes de construir el PDF."""
import os, sys, datetime, html
sys.stdout.reconfigure(encoding="utf-8")
from math import comb, floor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 KeepTogether, PageBreak, Flowable)

ROOT = r"C:\Users\alvaj\OneDrive\Documents\Práctica MAT"

# ---------- fuentes ----------
F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Ar",  os.path.join(F, "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArB", os.path.join(F, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("ArI", os.path.join(F, "ariali.ttf")))
pdfmetrics.registerFont(TTFont("Ser",  os.path.join(F, "georgia.ttf")))
pdfmetrics.registerFont(TTFont("SerB", os.path.join(F, "georgiab.ttf")))

INK   = colors.HexColor("#232733")
SOFT  = colors.HexColor("#5b6470")
FAINT = colors.HexColor("#9aa1ad")
LINEC = colors.HexColor("#c9cedb")
CREAM = colors.HexColor("#faf9f6")
BORD  = colors.HexColor("#e7e5df")

# banda -> (etiqueta, color, fondo suave)
BANDS = {
 "ini": ("Iniciación",  colors.HexColor("#0f9d58"), colors.HexColor("#e9f7ef")),
 "bas": ("Básico",      colors.HexColor("#2563eb"), colors.HexColor("#e8f0fe")),
 "int": ("Intermedio",  colors.HexColor("#ea580c"), colors.HexColor("#fdeee2")),
 "avz": ("Avanzado",    colors.HexColor("#7c3aed"), colors.HexColor("#f0e9fd")),
}
BAND_ORDER = ["ini", "bas", "int", "avz"]

# ---------- problemas ----------
# cada uno: banda, tema, enunciado, líneas de respuesta, respuesta (clave docente)
P = [
 # ---- Iniciación ----
 dict(band="ini", tema="Numeración", lines=5,
  text="En la feria de la escuela, Sofía juntó $48 vendiendo limonadas a $6 cada vaso. "
       "Tomás vendió los suyos al mismo precio y juntó el doble de dinero que Sofía. "
       "¿Cuántos vasos vendió cada uno? Explicá cómo lo pensaste.",
  ans="Sofía: 48÷6 = 8 vasos. Tomás juntó $96, entonces 96÷6 = 16 vasos."),
 dict(band="ini", tema="Geometría", lines=5,
  text="Un patio rectangular mide 8 m de largo y 5 m de ancho. Se quiere rodear todo su "
       "borde con una guirnalda de luces que cuesta $300 el metro. ¿Cuánto se gasta en total? "
       "Mostrá tu razonamiento.",
  ans="Perímetro = 2·(8+5) = 26 m. Costo = 26·300 = $7.800."),
 dict(band="ini", tema="Lógica", lines=6,
  text="Cinco chicos hacen una fila. Delia está última y Emi justo delante de ella. "
       "Ana está delante de Beto, pero detrás de Caro. ¿En qué orden quedan los cinco, "
       "del primero al último? Justificá tu respuesta.",
  ans="Caro, Ana, Beto, Emi, Delia. (Delia 5°, Emi 4°; entre los tres primeros Caro<Ana<Beto.)"),
 dict(band="ini", tema="Probabilidad", lines=5,
  text="Se tira una vez un dado común de 6 caras. Escribí todos los resultados posibles e "
       "indicá cuántos son números pares. ¿Qué fracción del total representan los pares? Explicá.",
  ans="Resultados 1..6; pares {2,4,6} = 3 de 6 → 3/6 = 1/2."),
 # ---- Básico ----
 dict(band="bas", tema="Numeración", lines=6,
  text="Un número de dos cifras cumple dos cosas: la suma de sus cifras es 9 y, al invertir "
       "el orden de las cifras, el número aumenta en 27. ¿Cuál es el número? Explicá cómo lo hallaste.",
  ans="36. (a+b=9; 9(b−a)=27 → b−a=3 → a=3, b=6. Se verifica: 63−36=27.)"),
 dict(band="bas", tema="Geometría", lines=6,
  text="Se arma una figura pegando 5 cuadraditos iguales de 2 cm de lado en forma de cruz: "
       "uno en el centro y los otros cuatro pegados a cada uno de sus lados. Dibujá la figura "
       "y calculá su perímetro.",
  ans="La cruz tiene 12 lados de 2 cm en su contorno → perímetro = 12·2 = 24 cm."),
 dict(band="bas", tema="Combinatoria", lines=6,
  text="Con las cifras 1, 2, 3 y 4, sin repetir ninguna, se forman números de tres cifras. "
       "Escribí al menos cinco de ellos y explicá cómo contarías cuántos se pueden formar en total.",
  ans="4·3·2 = 24 números."),
 dict(band="bas", tema="Estadística", lines=5,
  text="Las notas de Juan en cuatro pruebas fueron 6, 7, 8 y 7. ¿Qué nota necesita en la quinta "
       "prueba para que su promedio final sea exactamente 7? Justificá.",
  ans="Suma actual 28; para promedio 7 en 5 pruebas hace falta 35 → quinta nota = 7."),
 # ---- Intermedio ----
 dict(band="int", tema="Numeración", lines=6,
  text="¿Cuántos números enteros entre 1 y 200 (inclusive) son múltiplos de 3 pero no de 5? "
       "Explicá tu conteo.",
  ans="Múltiplos de 3: 66. Múltiplos de 15: 13. Respuesta: 66 − 13 = 53."),
 dict(band="int", tema="Geometría", lines=6,
  text="Un triángulo tiene base 10 cm y área 30 cm². Otro triángulo tiene la misma altura, pero "
       "el doble de base. ¿Cuál es el área del segundo triángulo? Tratá de justificarlo sin calcular "
       "la altura.",
  ans="El área es proporcional a la base con igual altura → se duplica: 60 cm²."),
 dict(band="int", tema="Lógica", lines=6,
  text="En un cajón hay medias rojas y medias azules mezcladas, a oscuras. ¿Cuántas medias hay que "
       "sacar como mínimo para estar seguro de tener un par del mismo color? ¿Y si hubiera medias de "
       "tres colores? Explicá el razonamiento.",
  ans="Con 2 colores: 3 medias. Con 3 colores: 4 medias (principio del palomar)."),
 dict(band="int", tema="Probabilidad", lines=6,
  text="Se tiran dos dados comunes y se suman los resultados. ¿Cuál es la suma más probable y qué "
       "probabilidad tiene? Mostrá el razonamiento (por ejemplo, con una tabla de las 36 combinaciones).",
  ans="La suma 7, con 6 de 36 casos → 6/36 = 1/6."),
 # ---- Avanzado ----
 dict(band="avz", tema="Álgebra", lines=7,
  text="Encontrá todos los pares de enteros positivos (a, b) tales que a·b = a + b + 4. "
       "Justificá que no hay otros además de los que encontrás.",
  ans="(a−1)(b−1)=5 → {a−1,b−1}={1,5} → (2,6) y (6,2). No hay más (5 es primo)."),
 dict(band="avz", tema="Geometría", lines=7,
  text="En un cuadrado de 6 cm de lado se marca el punto medio de cada lado y se los une formando "
       "un nuevo cuadrado inscripto. ¿Cuál es el área del cuadrado inscripto y qué fracción del "
       "original representa? Justificá.",
  ans="Área inscripta = 18 cm² = la mitad del original (36 cm²) → 1/2."),
 dict(band="avz", tema="Combinatoria", lines=7,
  text="¿De cuántas maneras se pueden repartir 10 caramelos idénticos entre 3 chicos si cada uno "
       "debe recibir al menos un caramelo? Explicá tu conteo.",
  ans="Combinatoria con repartos: C(9,2) = 36 maneras."),
 dict(band="avz", tema="Combinatoria", lines=7,
  text="Cinco amigos hacen un amigo invisible: cada uno saca al azar el papel con el nombre de otro, "
       "y nadie puede sacarse a sí mismo. Empezá analizando el caso de 3 amigos y luego averiguá de "
       "cuántas formas distintas puede quedar el sorteo con 5 amigos.",
  ans="Desarreglos: con 3 amigos hay 2; con 5 amigos hay 44."),
]

# ---------- verificación de la clave (antes de construir) ----------
CHK = []
CHK.append(("feria", 48//6 == 8 and (2*48)//6 == 16))
CHK.append(("patio", 2*(8+5)*300 == 7800))
CHK.append(("dado_par", (3, 6) == (len([n for n in range(1,7) if n%2==0]), 6)))
# número 36
n36 = [10*a+b for a in range(1,10) for b in range(0,10) if a+b==9 and (10*b+a)-(10*a+b)==27]
CHK.append(("num36", n36 == [36]))
CHK.append(("cruz", 12*2 == 24))
CHK.append(("perm3", 4*3*2 == 24))
CHK.append(("promedio", (35-(6+7+8+7)) == 7))
m3 = sum(1 for k in range(1,201) if k%3==0); m15 = sum(1 for k in range(1,201) if k%15==0)
CHK.append(("mult", m3==66 and m15==13 and m3-m15==53))
CHK.append(("area2x", 2*30 == 60))
CHK.append(("palomar", (3,4) == (2+1, 3+1)))
# suma de dos dados
from collections import Counter
c = Counter(i+j for i in range(1,7) for j in range(1,7))
CHK.append(("dados", max(c, key=c.get)==7 and c[7]==6))
# a*b=a+b+4
pairs = [(a,b) for a in range(1,50) for b in range(1,50) if a*b==a+b+4]
CHK.append(("abpair", set(pairs)=={(2,6),(6,2)}))
CHK.append(("cuad_medio", 18*2 == 36))
CHK.append(("caramelos", comb(9,2) == 36))
def derange(n):
    if n==0: return 1
    if n==1: return 0
    a,b=1,0
    for k in range(2,n+1): a,b=b,(k-1)*(a+b)
    return b
CHK.append(("desarreglo", derange(3)==2 and derange(5)==44))
bad = [name for name, ok in CHK if not ok]
if bad:
    raise SystemExit("CLAVE MAL: " + ", ".join(bad))
print(f"Clave verificada: {len(CHK)}/{len(CHK)} chequeos OK. Problemas: {len(P)}")

# ---------- flowable: líneas de respuesta punteadas ----------
class Lines(Flowable):
    def __init__(self, width, n, gap=8.2*mm):
        Flowable.__init__(self); self.width=width; self.n=n; self.gap=gap
        self.height=n*gap
    def draw(self):
        c=self.canv; c.setStrokeColor(LINEC); c.setLineWidth(0.5); c.setDash(1,2)
        for i in range(self.n):
            y=self.height-(i+1)*self.gap
            c.line(0,y,self.width,y)
        c.setDash()

# ---------- estilos ----------
st_tema  = ParagraphStyle("tema", fontName="ArB", fontSize=7.5, textColor=colors.white)
st_num   = ParagraphStyle("num", fontName="SerB", fontSize=13, textColor=INK)
st_body  = ParagraphStyle("body", fontName="Ar", fontSize=10.5, leading=15.5, textColor=INK)
st_lbl   = ParagraphStyle("lbl", fontName="ArI", fontSize=7.5, textColor=FAINT)

CONTENT_W = A4[0] - 34*mm  # márgenes 17mm

def chip(band):
    lbl, col, bg = BANDS[band]
    t = Table([[Paragraph(lbl.upper(), st_tema)]], colWidths=[pdfmetrics.stringWidth(lbl.upper(),"ArB",7.5)+14])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),col),("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2.5)]))
    return t

def problem(p, n):
    lbl, col, bg = BANDS[p["band"]]
    cw = pdfmetrics.stringWidth(lbl.upper(),"ArB",7.5)+14
    chip_tema = Table([[chip(p["band"]),
                        Paragraph(f"<font color='#5b6470'>{p['tema']}</font>",
                                  ParagraphStyle("tm", fontName="ArB", fontSize=8.5, textColor=SOFT))]],
                      colWidths=[cw, CONTENT_W-cw-16])
    chip_tema.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(1,0),(1,0),8)]))
    stmt = Table([[Paragraph(f"{n}.", st_num), Paragraph(p["text"], st_body)]],
                 colWidths=[24, CONTENT_W-24-16])
    stmt.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(0,0),"TOP")]))
    inner = [chip_tema, Spacer(1,6), stmt, Spacer(1,7),
             Paragraph("Respuesta y justificación", st_lbl), Spacer(1,3),
             Lines(CONTENT_W-16, p["lines"])]
    card = Table([[inner]], colWidths=[CONTENT_W])
    card.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CREAM),("BOX",(0,0),(-1,-1),0.6,BORD),
        ("LINEBEFORE",(0,0),(0,0),3,col),("ROUNDEDCORNERS",[2,2,2,2]),
        ("LEFTPADDING",(0,0),(-1,-1),13),("RIGHTPADDING",(0,0),(-1,-1),11),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),11)]))
    return KeepTogether([card, Spacer(1, 9)])

# ---------- portada ----------
story = []
story.append(Spacer(1, 42*mm))
story.append(Paragraph("Cuadernillo de práctica",
    ParagraphStyle("t", fontName="SerB", fontSize=30, textColor=INK, leading=34)))
story.append(Paragraph("Active Maths Championship · camino al AMC",
    ParagraphStyle("s", fontName="Ser", fontSize=13, textColor=BANDS["avz"][1], spaceBefore=6)))
story.append(Spacer(1, 4*mm))
story.append(Table([[""]], colWidths=[70*mm], style=[("LINEBELOW",(0,0),(-1,-1),1.5,BANDS["int"][1])]))
story.append(Spacer(1, 9*mm))
intro = ("Este cuadernillo reúne <b>16 problemas para pensar</b>, con distintos niveles de "
 "dificultad y temas variados. No son de opción múltiple: en cada uno tenés espacio para "
 "<b>escribir tu respuesta y, sobre todo, justificar cómo llegaste a ella</b>. "
 "No importa solo el resultado —importa el razonamiento.")
story.append(Paragraph(intro, ParagraphStyle("i", fontName="Ar", fontSize=11, leading=17, textColor=INK)))
story.append(Spacer(1, 5*mm))
tip = ("Trabajá los problemas a tu ritmo, probá con dibujos, ejemplos y tanteos. "
 "Después <b>conversalos con tus profes</b>: compartir distintas maneras de resolver "
 "un mismo problema es parte del entrenamiento.")
story.append(Paragraph(tip, ParagraphStyle("i2", fontName="Ar", fontSize=11, leading=17, textColor=SOFT)))
story.append(Spacer(1, 9*mm))
# leyenda de bandas
leg = [[chip(b), Paragraph(f"<font color='#5b6470'>{BANDS[b][0]}</font>",
        ParagraphStyle("lg", fontName="Ar", fontSize=9, textColor=SOFT))] for b in BAND_ORDER]
legt = Table([[chip(b) for b in BAND_ORDER]], colWidths=[CONTENT_W/4]*4)
legt.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),
    ("BOTTOMPADDING",(0,0),(-1,-1),0),("ALIGN",(0,0),(-1,-1),"LEFT")]))
story.append(Paragraph("Los problemas están agrupados por nivel de dificultad:",
    ParagraphStyle("lgh", fontName="ArB", fontSize=9, textColor=INK, spaceAfter=5)))
story.append(legt)
story.append(PageBreak())

# ---------- problemas por banda ----------
st_bandh = ParagraphStyle("bh", fontName="SerB", fontSize=15, textColor=colors.white, leading=18)
def band_header(band):
    lbl, col, bg = BANDS[band]
    t = Table([[Paragraph(lbl, st_bandh)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),col),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),7),("LEFTPADDING",(0,0),(-1,-1),11),("ROUNDEDCORNERS",[3,3,3,3])]))
    return t

n = 1
for band in BAND_ORDER:
    grp = [p for p in P if p["band"]==band]
    story.append(band_header(band))
    story.append(Spacer(1, 7))
    for p in grp:
        story.append(problem(p, n)); n += 1
    story.append(Spacer(1, 4))

# ---------- clave para docentes ----------
story.append(PageBreak())
story.append(Paragraph("Clave de respuestas — para docentes",
    ParagraphStyle("kh", fontName="SerB", fontSize=15, textColor=INK, spaceAfter=3)))
story.append(Paragraph("Orientativa: varios problemas admiten más de un camino de resolución. "
    "El foco está en la justificación de los estudiantes.",
    ParagraphStyle("ks", fontName="ArI", fontSize=9.5, textColor=SOFT, spaceAfter=9)))
krows = []
for i, p in enumerate(P, 1):
    krows.append([Paragraph(f"<b>{i}.</b>", ParagraphStyle("kn", fontName="ArB", fontSize=9.5, textColor=BANDS[p['band']][1])),
                  Paragraph(f"<font color='#9aa1ad'>{p['tema']}</font>", ParagraphStyle("kt", fontName="Ar", fontSize=8.5, textColor=FAINT)),
                  Paragraph(html.escape(p["ans"]), ParagraphStyle("ka", fontName="Ar", fontSize=9.5, leading=13, textColor=INK))])
kt = Table(krows, colWidths=[10, 60, CONTENT_W-70])
kt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),4),
    ("BOTTOMPADDING",(0,0),(-1,-1),4),("LINEBELOW",(0,0),(-1,-2),0.4,BORD),
    ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),4)]))
story.append(kt)

# ---------- build ----------
out = os.path.join(ROOT, "Cuadernillo de práctica - AMC.pdf")
doc = SimpleDocTemplate(out, pagesize=A4, topMargin=17*mm, bottomMargin=16*mm,
                        leftMargin=17*mm, rightMargin=17*mm, title="Cuadernillo de práctica - AMC")
def deco(canvas, doc):
    canvas.saveState()
    canvas.setFont("Ar", 7.5); canvas.setFillColor(FAINT)
    canvas.drawString(17*mm, 9*mm, "Active Learning · Cuadernillo de práctica AMC")
    canvas.drawRightString(A4[0]-17*mm, 9*mm, f"pág. {doc.page}")
    canvas.restoreState()
doc.build(story, onFirstPage=deco, onLaterPages=deco)
print("PDF:", out, "| páginas ~", doc.page)
