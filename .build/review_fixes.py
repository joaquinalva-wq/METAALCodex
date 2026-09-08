# -*- coding: utf-8 -*-
"""Auditoria de los 117 'problemas' AMC conservados:
 - REPLACE: items rotos o figura-dependientes (basico/geo#7, intermedio/geo#0/#2/#8).
 - REWORD:  redaccion densa (basico/logica#5/#9, intermedio/num#8/#28).
 - UPGRADE: 13 items triviales de un paso en pitagoras/numeracion -> problemas de
            material concreto de un par de pasos, tono Iniciacion.
Se localiza cada item por (nivel,eje,idx) usando su pregunta actual del dump.
Aritmetica verificada. Brace-match acotado a la region DATA_AMC."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\alvaj\OneDrive\Documents\Práctica MAT"
PATH = os.path.join(ROOT, "index.html")
s = open(PATH, encoding="utf-8").read()
d = json.load(open(os.path.join(ROOT, ".build", "dump.json"), encoding="utf-8"))["mc"]
AMC_START = s.index("const DATA_AMC")


def cur_q(nivel, eje, idx):
    for r in d:
        if (r["track"], r["nivel"], r["eje"], r["idx"]) == ("AMC", nivel, eje, idx):
            return r["question"]
    raise SystemExit(f"no encontrado {nivel}/{eje}/#{idx}")


def raw_obj(question):
    anchor = '"question":"' + question.replace("\n", "\\n") + '","options"'
    region = s[AMC_START:]
    n = region.count(anchor)
    if n != 1:
        raise SystemExit(f"ANCLA no unica ({n}): {question[:60]}")
    i = AMC_START + region.index(anchor); st = s.rfind("{", 0, i); dep = 0
    for j in range(st, len(s)):
        if s[j] == "{": dep += 1
        elif s[j] == "}":
            dep -= 1
            if dep == 0: return st, j + 1
    raise SystemExit("brace")


def obj(q, opts, correct):
    assert set(opts) == {"A", "B", "C", "D"} and correct in opts
    assert len(set(opts.values())) == 4, f"opciones repetidas: {q[:40]}"
    assert q and "\n" not in q, f"salto o vacio: {q[:40]}"
    return json.dumps({"question": q, "options": opts, "correct": correct, "skill": "problemas"},
                      ensure_ascii=False, separators=(",", ":"))


# (nivel, eje, idx, nueva_pregunta, opciones, correct)
FIXES = [
 # --- REPLACE: figura-dependientes / roto ---
 ("basico","geometria",7,
  "Un rectángulo mide 12 cm de largo y 8 cm de ancho. Si le recortás un cuadrado de 3 cm de lado en una de sus esquinas, ¿cuál es el perímetro de la figura que queda?",
  {"A":"34 cm","B":"40 cm","C":"46 cm","D":"52 cm"},"B"),  # el perimetro no cambia: 2(12+8)=40
 ("intermedio","geometria",0,
  "En un triángulo rectángulo, un cateto mide 9 cm y la hipotenusa 15 cm. ¿Cuál es el área del triángulo?",
  {"A":"54 cm²","B":"60 cm²","C":"67,5 cm²","D":"108 cm²"},"A"),  # otro cateto 12
 ("intermedio","geometria",2,
  "Los lados de un triángulo miden 13 cm, 14 cm y 15 cm. ¿Cuál es su área?",
  {"A":"80 cm²","B":"84 cm²","C":"91 cm²","D":"168 cm²"},"B"),  # Heron
 ("intermedio","geometria",8,
  "El área de un rombo es 48 cm² y una de sus diagonales mide 12 cm. ¿Cuánto mide la otra diagonal?",
  {"A":"4 cm","B":"6 cm","C":"8 cm","D":"16 cm"},"C"),  # 48=12*d/2
 # --- REWORD: aclarar redaccion ---
 ("basico","logica",5,
  "¿De cuántas maneras se pueden pintar 3 casilleros puestos en fila usando los colores rojo, azul y verde, si dos casilleros vecinos no pueden tener el mismo color?",
  {"A":"6","B":"9","C":"12","D":"18"},"C"),  # 3*2*2
 ("basico","logica",9,
  "En una reunión, cada persona saludó con la mano a todas las demás exactamente una vez, y hubo 28 saludos en total. ¿Cuántas personas había?",
  {"A":"7","B":"8","C":"14","D":"28"},"B"),  # C(n,2)=28 -> n=8
 ("intermedio","numeracion",8,
  "¿Cuántos pares de números enteros (x, y) cumplen que x² + x·y + y² = 67?",
  {"A":"4","B":"6","C":"8","D":"12"},"D"),
 ("intermedio","numeracion",28,
  "Se reparten $200 entre dos personas en la razón 2 : 3. ¿Cuánto recibe la persona que más recibe?",
  {"A":"$80","B":"$100","C":"$120","D":"$150"},"C"),  # 3/5*200
 # --- UPGRADE: pitagoras/numeracion triviales -> un par de pasos ---
 ("pitagoras","numeracion",11,
  "Vale tiene 4 monedas de $5 y algunas monedas de $2. En total junta $26. ¿Cuántas monedas de $2 tiene?",
  {"A":"2","B":"3","C":"4","D":"6"},"B"),  # 26-20=6 -> 3
 ("pitagoras","numeracion",17,
  "Con $50 compro lápices que cuestan $8 cada uno. Si llevo la mayor cantidad posible, ¿cuánto dinero me sobra?",
  {"A":"$2","B":"$4","C":"$6","D":"$8"},"A"),  # 6 lapices=48
 ("pitagoras","numeracion",19,
  "En una granja hay 5 gallinas (2 patas cada una) y 3 conejos (4 patas cada uno). ¿Cuántas patas hay en total?",
  {"A":"20","B":"22","C":"24","D":"26"},"B"),  # 10+12
 ("pitagoras","numeracion",20,
  "Se reparten 20 caramelos entre 3 chicos, dándole a cada uno la misma cantidad. ¿Cuántos caramelos sobran?",
  {"A":"0","B":"1","C":"2","D":"3"},"C"),  # 20=6*3+2
 ("pitagoras","numeracion",21,
  "Tengo 10 figuritas y regalo la mitad. Después me regalan 3. ¿Cuántas figuritas tengo ahora?",
  {"A":"5","B":"7","C":"8","D":"10"},"C"),  # 5+3
 ("pitagoras","numeracion",28,
  "Quiero juntar $30 usando monedas de $10 y de $2. Si uso 2 monedas de $10, ¿cuántas monedas de $2 necesito?",
  {"A":"4","B":"5","C":"6","D":"10"},"B"),  # 30-20=10 -> 5
 ("pitagoras","numeracion",29,
  "Con $50 compro 2 chocolates de $20 cada uno y, con lo que sobra, figuritas de $5. ¿Cuántas figuritas puedo comprar?",
  {"A":"1","B":"2","C":"3","D":"4"},"B"),  # 50-40=10 -> 2
 ("pitagoras","numeracion",35,
  "En un salón hay 4 mesas y en cada mesa se sientan 5 chicos. Si cada chico levanta sus 2 manos, ¿cuántas manos se levantan en total?",
  {"A":"20","B":"30","C":"40","D":"50"},"C"),  # 20*2
 ("pitagoras","numeracion",38,
  "En un garaje hay 2 bicicletas (2 ruedas cada una) y 2 triciclos (3 ruedas cada uno). ¿Cuántas ruedas hay en total?",
  {"A":"8","B":"10","C":"12","D":"14"},"B"),  # 4+6
 ("pitagoras","numeracion",39,
  "Tengo 3 cajas con 2 fichas cada una y otra caja con 4 fichas. ¿Cuántas fichas tengo en total?",
  {"A":"8","B":"9","C":"10","D":"12"},"C"),  # 6+4
 ("pitagoras","numeracion",43,
  "Tengo una moneda de $10, dos monedas de $5 y una moneda de $2. ¿Cuánto dinero tengo en total?",
  {"A":"$20","B":"$22","C":"$24","D":"$25"},"B"),  # 10+10+2
 ("pitagoras","numeracion",44,
  "Tengo 6 caramelos y quiero llegar a tener 10. Si cada paquete trae 2 caramelos, ¿cuántos paquetes necesito comprar?",
  {"A":"1","B":"2","C":"3","D":"4"},"B"),  # faltan 4 -> 2
 ("pitagoras","numeracion",45,
  "Para llenar un álbum necesito 20 figuritas y ya tengo 15. Si cada sobre trae 3 figuritas, ¿cuántos sobres necesito comprar como mínimo?",
  {"A":"1","B":"2","C":"3","D":"5"},"B"),  # faltan 5 -> ceil(5/3)=2
]

edits = []
for nivel, eje, idx, q, opts, correct in FIXES:
    st, en = raw_obj(cur_q(nivel, eje, idx))
    edits.append((s[st:en], obj(q, opts, correct)))

news = [n for _, n in edits]
if len(set(news)) != len(news):
    raise SystemExit("colision entre items nuevos")

for old, new in edits:
    if s.count(old) != 1:
        raise SystemExit(f"old no unico: {old[:70]}")
    s = s.replace(old, new, 1)

if "--apply" in sys.argv:
    open(PATH, "w", encoding="utf-8").write(s)
    print(f"Correcciones aplicadas: {len(edits)} (4 reemplazos, 4 reescrituras, 13 upgrades).")
else:
    print(f"OK dry-run: {len(edits)} correcciones listas.")
