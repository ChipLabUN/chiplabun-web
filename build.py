#!/usr/bin/env python3
"""Genera las páginas de site/ con encabezado y pie compartidos.
Uso: python3 build.py   (edita el contenido aquí y vuelve a correrlo)"""
import os, html

_HERE = os.path.dirname(os.path.abspath(__file__))
# Si build.py está junto a index.html (repositorio), escribe ahí; si no, en ./site
OUT = _HERE if os.path.isdir(os.path.join(_HERE, "css")) else os.path.join(_HERE, "site")

NAV = [
    ("index.html", "Inicio"),
    ("conocenos.html", "Conócenos"),
    ("proyectos.html", "Proyectos"),
    ("resultados.html", "Resultados"),
    ("personas.html", "Personas"),
    ("publicaciones.html", "Publicaciones"),
    ("contacto.html", "Contáctanos"),
]

# ---------------- datos ----------------
DIRECTOR = dict(slug="johan-eslava", ini="JE", name="Johan Sebastián Eslava Garzón",
                title="Ph.D., M.Sc. · Director del semillero",
                mail="jseslavag@unal.edu.co")
MEMBERS = [
    dict(slug="ronny-rueda", ini="RR", name="Ronny Alberto Rueda Méndez", line="l1",
         role="Exploración de multiplicadores con RL", mail="rruedam@unal.edu.co"),
    dict(slug="juan-caviedes", ini="JC", name="Juan Sebastián Caviedes Bernal", line="l1",
         role="Exploración multiagente y escalamiento", mail="jcaviedesb@unal.edu.co", pos="75% center"),
    dict(slug="miguel-alvarado", ini="MA", name="Miguel Ángel Alvarado Senejoa", line="l1",
         role="Línea 1", mail="mialvarados@unal.edu.co"),
    dict(slug="juan-rodriguez", ini="JR", name="Juan David Rodríguez Hernández", line="l1",
         role="Línea 1", mail="juarodriguezhe@unal.edu.co"),
    dict(slug="diana-maldonado", ini="DM", name="Diana Maldonado", line="l2",
         role="Diseño y verificación del ASIC brUNo", mail=""),
    dict(slug="kevin-patino", ini="KP", name="Kevin Patiño", line="l2",
         role="Verificación e implementación física", mail=""),
]

PUBS = [
    dict(l="l2", yr="2026",
         t="Design, Implementation and Verification of an Open-Source ASIC for Grayscale and Sobel Edge Detection",
         au="D. Maldonado, J. S. Eslava y K. Patiño",
         v="17th IEEE Latin American Symposium on Circuits and Systems (LASCAS)"),
    dict(l="l1", yr="2026",
         t="Strategies for Scaling Up RL-Based Multiplier Architectures to Higher Bit-widths",
         au="<u>R. A. Rueda</u>, J. S. Caviedes y J. S. Eslava", v="IEEE"),
    dict(l="l1", yr="2026",
         t="Reinforcement Learning-Enhanced Design Space Exploration for Digital Multipliers",
         au="<u>R. A. Rueda</u>, J. S. Caviedes y J. S. Eslava",
         v="International Conference on Soft Computing &amp; Machine Intelligence (ISCMI)"),
    dict(l="l1", yr="2026",
         t="Automated Design Space Exploration of Approximate Digital Multipliers Using Tabular Reinforcement Learning",
         au="<u>R. A. Rueda</u>, J. S. Eslava, M. A. Alvarado y J. D. Rodríguez",
         v="Universidad Nacional de Colombia"),
]

PROJECTS = [
    dict(l="l1", st="Activo", t="Entorno RL sin simulación",
         d="Grilla de productos parciales como entorno de aprendizaje, vectorizado en CUDA con 512 instancias en paralelo. Agentes Monte Carlo, Q-learning, SARSA y SARSA de n pasos con recompensa por columna y por error final.",
         f="Multiplicadores de 2 bits con <b>error cero</b>; a 4 bits, error pico <b>4</b> frente a 64 de los métodos de un paso."),
    dict(l="l1", st="Activo", t="Exploración multiagente",
         d="Cinco esquemas de cooperación entre agentes (IND, COOP, CN, CA y CAN) para paralelizar la exploración del espacio de diseño de multiplicadores.",
         f="La cooperación total logra <b>el menor error</b>; la cooperación por ventaja, <b>la convergencia más rápida</b>."),
    dict(l="l1", st="Activo", t="Escalamiento a 8 bits",
         d="Composición recursiva 2 → 4 → 8 bits a partir de bloques descubiertos por el agente, donde los métodos tabulares saturan desde los 6 bits.",
         f="Corregir 1–2 operaciones por bloque baja el MAE de <b>3.612</b> a 2.709 y <b>1.543</b> (producto máx. 65.025)."),
    dict(l="l1 l2", st="Activo", t="Ax-INT4 en visión",
         d="El multiplicador aproximado de 4 bits hallado por el agente, traducido a Verilog, sintetizado con LibreLane y evaluado en filtros de imagen frente a UDM, BAM y DRUM.",
         f="Desenfoque gaussiano 5×5: <b>PSNR 38,0 dB</b> · SSIM 0,99. Sobel 3×3: <b>43,9 dB</b> · 0,97."),
    dict(l="l2", st="Fabricado", t="brUNo · ASIC grises + Sobel",
         d="Arquitectura streaming de dos etapas para imágenes RGB de 320 × 240 recibidas por SPI, con LFSR de estímulo y lógica de selección de modo integradas para prueba.",
         f="Grises: <b>F1 de bordes 0,953</b> · IoU 0,910 frente a la referencia ideal."),
    dict(l="l2", st="Activo", t="Banco de pruebas post-silicio",
         d="Medición de función, potencia y throughput del chip real para contrastar las estimaciones del EDA abierto y depurar fallos que la simulación RTL no captura.",
         f="La fuga medida <b>supera la estimada</b>: OpenLane no modela las celdas header de power-gating."),
]

# ---------------- piezas ----------------
def photo(p, cls=""):
    line = "l1" if p.get("line") == "l1" else ""
    pos = f' style="object-position:{p["pos"]}"' if p.get("pos") else ""  # encuadre si la cara no está centrada
    return (f'<div class="photo {line} {cls}"><span class="ini" aria-hidden="true">{p["ini"]}</span>'
            f'<img src="img/personas/{p["slug"]}.jpg" alt="Foto de {html.escape(p["name"])}" loading="lazy"{pos}></div>')

def pills(l):
    out = []
    if "l1" in l.split(): out.append('<span class="pill l1">Línea 1</span>')
    if "l2" in l.split(): out.append('<span class="pill l2">Línea 2</span>')
    return "".join(out)

def project_card(p):
    st = '<span class="pill ok">Activo</span>' if p["st"] == "Activo" else f'<span class="pill">{p["st"]}</span>'
    return (f'<article class="proj" data-l="{p["l"]}"><div class="meta">{pills(p["l"])}{st}</div>'
            f'<h3>{p["t"]}</h3><p>{p["d"]}</p><div class="fig">{p["f"]}</div></article>')

def pub_item(p):
    return (f'<article class="pub" data-l="{p["l"]}"><span class="yr">{p["yr"]}</span><div>'
            f'<h3>{p["t"]}</h3><p class="au">{p["au"]}</p><p class="venue">{p["v"]}</p></div>'
            f'<div class="side">{pills(p["l"])}</div></article>')

def header(cur):
    cur_attr = ' aria-current="page"'
    links = "".join(
        '<a href="%s"%s>%s</a>' % (href, cur_attr if href == cur else "", label)
        for href, label in NAV if href != "index.html")
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="ChipLabUN, inicio">
      <img src="img/logo.jpg" alt="" width="85" height="42">
      <span class="sep" aria-hidden="true"></span>
      <img class="unal" src="img/unal-logo-blanco.png" alt="" width="94" height="40">
    </a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="nav">Menú</button>
    <nav class="nav" id="nav" aria-label="Principal">{links}</nav>
  </div>
</header>'''

FOOTER = '''<footer>
  <div class="wrap">
    <div>
      <img class="foot-unal" src="img/unal-logo-blanco.png" alt="Universidad Nacional de Colombia" width="151" height="64" loading="lazy">
      <h4>Semillero ChipLabUN</h4>
      <p style="font-size:15px;max-width:44ch">Investigación en diseño de circuitos integrados. IA para diseñar chips · Chips para ejecutar IA. Departamento de Ingeniería Eléctrica y Electrónica, Sede Bogotá.</p>
    </div>
    <div>
      <h4>Explorar</h4>
      <ul><li><a href="conocenos.html">Conócenos</a></li><li><a href="proyectos.html">Proyectos</a></li><li><a href="personas.html">Personas</a></li><li><a href="publicaciones.html">Publicaciones</a></li></ul>
    </div>
    <div>
      <h4>Contacto</h4>
      <ul><li>jseslavag@unal.edu.co</li><li>rruedam@unal.edu.co</li><li><a href="https://github.com/DarkSpartan345" target="_blank" rel="noopener">GitHub · DarkSpartan345</a></li></ul>
    </div>
    <div class="legal"><span>© 2026 ChipLabUN · Universidad Nacional de Colombia</span><span>Herramientas abiertas: Sky130 · OpenLane · TinyTapeout</span></div>
  </div>
</footer>
<script src="js/main.js"></script>'''

def page_head(title, lead):
    return f'''<section class="page-head"><div class="wrap">
  <p class="crumbs"><a href="index.html">Inicio</a> / {title}</p>
  <h1>{title}</h1><p>{lead}</p></div></section>'''

def doc(fname, title, body, full=True):
    head = f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Semillero ChipLabUN · Universidad Nacional de Colombia. IA para diseñar chips · Chips para ejecutar IA.">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png">
<link rel="apple-touch-icon" href="favicon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Exo+2:wght@500;600;700;800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="css/estilo.css">'''
    inner = f"{header(fname)}\n<main id=\"contenido\">\n{body}\n</main>\n{FOOTER}\n"
    if not full:
        return head + "\n" + inner
    return (f'<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{head}\n</head>\n<body>\n{inner}</body>\n</html>\n')

# ---------------- páginas ----------------
STATS = '''<div class="wrap stats-wrap"><div class="stats">
  <div><b>4</b><span>artículos en 2026</span></div>
  <div><b>1</b><span>ASIC fabricado y medido</span></div>
  <div><b>2</b><span>líneas de investigación</span></div>
  <div><b>7</b><span>integrantes</span></div>
</div></div>'''

LINE1_CHIPS = '''<div class="kv">
  <div class="chip"><b>&lt; 5 %</b><span>error de peor caso a 4 bits (SARSA de 30 pasos)</span></div>
  <div class="chip"><b>0,0039</b><span>NMAE del mejor multiplicador de 4 bits</span></div>
  <div class="chip"><b>50 M</b><span>episodios sobre 512 entornos paralelos en GPU</span></div>
  <div class="chip"><b>2 → 8 bits</b><span>escalamiento por composición recursiva</span></div></div>'''
LINE2_CHIPS = '''<div class="kv">
  <div class="chip"><b>0,036 mm²</b><span>área en Sky130 · 2.183 celdas · 2 tiles</span></div>
  <div class="chip"><b>2,91 mW</b><span>potencia total medida a 1,8 V</span></div>
  <div class="chip"><b>SSIM 0,983</b><span>fidelidad de la conversión a grises aproximada</span></div>
  <div class="chip"><b>100 % / 42 %</b><span>coincidencia en grises / discrepancia en Sobel</span></div></div>'''

def lines_block(detail):
    l1 = ('<p>El espacio de diseño de un multiplicador crece de forma combinatoria con el ancho de operando. Modelamos el diseño como un problema de decisión secuencial: un agente tabular coloca términos booleanos sobre la grilla de productos parciales, sin reglas de multiplicación predefinidas, y descubre multiplicadores aproximados fuera de las plantillas clásicas (array, Booth, Dadda, Wallace).</p>'
          if detail else '<p>Aprendizaje por refuerzo que explora automáticamente el espacio de diseño de la aritmética digital y descubre multiplicadores aproximados fuera de las plantillas clásicas.</p>')
    l2 = ('<p>Muchas tareas de visión parten de un sensor que entrega un flujo continuo de píxeles y repiten la misma operación sobre cada uno. Diseñamos, implementamos, fabricamos y medimos ASIC de código abierto que ejecutan ese front-end en silicio: escala de grises y detección de bordes Sobel, solo con sumas, restas y desplazamientos.</p>'
          if detail else '<p>Diseño, implementación, fabricación y medición de ASIC de código abierto que ejecutan en silicio el front-end de visión por computador: escala de grises y detección de bordes Sobel.</p>')
    f1 = '<div class="flow" aria-label="Flujo de la línea 1"><span>Agente tabular</span><i>→</i><span>Entorno CUDA ×512</span><i>→</i><span>Verilog</span><i>→</i><span>Yosys · OpenROAD</span><i>→</i><span>PPA Sky130</span></div>'
    f2 = '<div class="flow" aria-label="Flujo de la línea 2"><span>SystemVerilog</span><i>→</i><span>Yosys</span><i>→</i><span>OpenLane 2</span><i>→</i><span>DRC/LVS</span><i>→</i><span>TinyTapeout</span><i>→</i><span>Medición</span></div>'
    x1 = f1 + LINE1_CHIPS if detail else '<a class="more line-link" href="proyectos.html#l1">Ver proyectos de la Línea 1 →</a>'
    x2 = f2 + LINE2_CHIPS if detail else '<a class="more line-link" href="proyectos.html#l2">Ver proyectos de la Línea 2 →</a>'
    return f'''<div class="lines">
  <article class="line" id="linea-1"><header><h3>Línea 1 · IA para diseñar chips</h3><code>IA → CHIPS</code></header><div class="body">{l1}{x1}</div></article>
  <article class="line" id="linea-2"><header><h3>Línea 2 · Chips que ejecutan IA</h3><code>CHIPS → IA</code></header><div class="body">{l2}{x2}</div></article>
</div>'''

def sec(eyebrow, title, inner, aside="", sid=""):
    return f'''<section class="block"{f' id="{sid}"' if sid else ""}><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><span class="bar"></span></div>{aside}</div>
  {inner}
</div></section>'''

CTA = '''<section class="block"><div class="wrap"><div class="cta">
  <div><span class="eyebrow" style="color:#e3a07a">Posgrado</span>
    <h2>¿Quieres hacer tu posgrado diseñando chips?</h2>
    <p>En ChipLabUN puedes desarrollar tu tesis de maestría o doctorado en exploración de espacios de diseño con aprendizaje por refuerzo, aritmética aproximada, flujos de EDA abiertos y diseño físico de ASIC en Sky130.</p></div>
  <div class="contact">
    <div><code>jseslavag@unal.edu.co</code><button type="button" data-copy="jseslavag@unal.edu.co">Copiar</button></div>
    <div><code>rruedam@unal.edu.co</code><button type="button" data-copy="rruedam@unal.edu.co">Copiar</button></div>
    <small>Departamento de Ingeniería Eléctrica y Electrónica · Facultad de Ingeniería · Sede Bogotá</small>
  </div></div></div></section>'''

MILESTONES = '''<div class="timeline">
  <article class="ms"><time>2026 · OPEN DAY</time><h3>Open Day de Posgrados</h3><p>Presentamos las dos líneas del semillero y abrimos cupos para tesis de maestría y doctorado.</p><a href="contacto.html">Postúlate →</a></article>
  <article class="ms"><time>2026 · IEEE LASCAS</time><h3>brUNo en el 17th IEEE LASCAS</h3><p>Diseño, implementación y verificación post-silicio del ASIC de escala de grises y Sobel.</p><a href="publicaciones.html">Ver artículo →</a></article>
  <article class="ms"><time>2026 · ISCMI</time><h3>RL para multiplicadores en ISCMI</h3><p>Exploración del espacio de diseño de multiplicadores digitales potenciada con aprendizaje por refuerzo.</p><a href="publicaciones.html">Ver artículo →</a></article>
</div>'''

def p_index():
    faces = "".join(photo(p) for p in [DIRECTOR] + MEMBERS)
    hero = f'''<section class="hero" id="inicio"><div class="wrap">
  <div>
    <span class="eyebrow">Semillero de investigación · Diseño de circuitos integrados</span>
    <h1>Semillero ChipLabUN</h1>
    <p class="tag">IA para diseñar chips · Chips para ejecutar IA</p>
    <p class="lead">Somos el semillero del <strong>Departamento de Ingeniería Eléctrica y Electrónica</strong> de la Universidad Nacional de Colombia, Sede Bogotá. Usamos aprendizaje por refuerzo para descubrir aritmética digital y llevamos funciones de visión por computador al silicio con herramientas de código abierto, del RTL al chip medido.</p>
    <div class="btns"><a class="btn primary" href="conocenos.html">Conoce el semillero</a><a class="btn ghost" href="proyectos.html">Ver proyectos</a></div>
  </div>
  <figure class="die">
    <img src="img/brUNo-die.jpg" alt="Fotografía del die de TinyTapeout de 3,6 por 5,2 mm y detalle del bloque brUNo de 0,226 por 0,161 mm" width="739" height="559">
    <figcaption>Chip brUNo · die TinyTapeout 3,6 × 5,2 mm · bloque 0,226 × 0,161 mm · Sky130</figcaption>
  </figure>
</div>{STATS}</section>'''
    featured = "".join(project_card(PROJECTS[i]) for i in (0, 3, 4))
    team = f'''<div class="director-feature team-teaser">
  <div class="faces">{faces}</div>
  <div><p style="color:var(--ink)">Un director y seis investigadores de pregrado y posgrado trabajando entre el aprendizaje por refuerzo y el silicio.</p>
  <a class="more" href="personas.html">Conoce al equipo →</a></div></div>'''
    body = hero + sec("Investigación", "Líneas de investigación", lines_block(False),
                      '<p>Dos ejes que se alimentan entre sí: la aritmética que descubre la Línea 1 es el próximo bloque de los aceleradores de la Línea 2.</p>')
    body += sec("Portafolio", "Proyectos destacados", f'<div class="grid3">{featured}</div>', '<a class="more" href="proyectos.html">Catálogo completo →</a>')
    body += sec("Equipo", "Personas", team)
    body += sec("Actualidad", "Hitos del semillero", MILESTONES)
    body += CTA
    return body

def p_conocenos():
    about = f'''<div class="about">
  <div class="text">
    <p>ChipLabUN es el semillero de investigación en diseño de circuitos integrados del Departamento de Ingeniería Eléctrica y Electrónica de la Universidad Nacional de Colombia. Su trabajo se ubica en la intersección entre la inteligencia artificial y la microelectrónica.</p>
    <p>Se organiza en dos líneas complementarias que recorren el mismo camino en sentidos opuestos: una usa la IA como herramienta para diseñar hardware; la otra lleva funciones de IA y visión por computador al silicio con herramientas de código abierto.</p>
    <p>Hoy contamos con un entorno de RL propio acelerado en GPU, un flujo RTL-a-GDSII con OpenLane/LibreLane sobre Sky130 y un banco de pruebas post-silicio.</p>
  </div>
  <aside class="director">
    {photo(DIRECTOR)}
    <span class="role">Dirección</span>
    <h3>{DIRECTOR["name"]}</h3>
    <p style="color:var(--muted);font-size:15.5px">{DIRECTOR["title"]}</p>
    <span class="mail">{DIRECTOR["mail"]}</span>
  </aside>
</div>'''
    goals = '''<div class="goal"><h3>Objetivo general</h3><p>Consolidar en la Universidad Nacional de Colombia una capacidad propia de diseño de circuitos integrados que use la inteligencia artificial como herramienta de diseño y que lleve funciones de inteligencia artificial al silicio, con flujos, resultados y publicaciones abiertos y verificables.</p></div>
<div class="goals">
  <div><b>1</b><p>Automatizar la exploración del espacio de diseño de aritmética digital mediante aprendizaje por refuerzo, sin reglas de multiplicación predefinidas.</p></div>
  <div><b>2</b><p>Escalar las arquitecturas descubiertas de 2 a 8 bits y sintetizarlas en el PDK Sky130 con flujos de EDA abiertos.</p></div>
  <div><b>3</b><p>Diseñar, implementar y verificar ASIC de procesamiento de imagen con un flujo RTL-a-GDSII enteramente de código abierto.</p></div>
  <div><b>4</b><p>Validar en silicio función, potencia y throughput; formar estudiantes y publicar los resultados en conferencias IEEE.</p></div>
</div>'''
    synergy = '''<div class="synergy">
  <div><small>PASO 1 · LÍNEA 1</small><p>El agente descubre aritmética aproximada.</p></div>
  <div><small>PASO 2</small><p>Traducción a Verilog y síntesis en Sky130.</p></div>
  <div><small>PASO 3 · LÍNEA 2</small><p>Un ASIC de visión ejecuta esa aritmética.</p></div>
  <div><small>PASO 4</small><p>Medición en silicio: área, potencia y error reales.</p></div>
  <p class="synergy-foot">↺ Las medidas reales realimentan la función de recompensa del agente.</p>
</div>'''
    impact = '''<div class="impact-wrap"><table class="impact">
  <thead><tr><th></th><th>Medioambientales</th><th>Sociales</th></tr></thead>
  <tbody>
  <tr class="pos"><th>Positivos</th>
    <td>La computación aproximada y la aritmética de sumas y desplazamientos reducen área, conmutación y energía por píxel: menor consumo en dispositivos de borde alimentados por batería. La evaluación vectorizada sin simulación de hardware ahorra miles de horas-CPU.</td>
    <td>Las herramientas y el PDK abiertos (Sky130, OpenLane, TinyTapeout) bajan la barrera de entrada al diseño de chips en Colombia y forman talento local. Estudiantes de pregrado y posgrado publican en conferencias IEEE, con código y resultados públicos.</td></tr>
  <tr class="neg"><th>Negativos</th>
    <td>El entrenamiento de los agentes (decenas de millones de episodios en GPU) y las campañas de síntesis son intensivos en energía. La fabricación de silicio, aun en oblea multiproyecto, implica huella material, química e hídrica.</td>
    <td>El error controlado de la computación aproximada no es admisible en aplicaciones críticas sin una caracterización rigurosa. La línea depende de plataformas y PDK externos, y el acceso a equipos de medición sigue siendo desigual entre instituciones.</td></tr>
  </tbody></table></div>'''
    body = page_head("Conócenos", "Investigación en diseño de circuitos integrados en la intersección entre la inteligencia artificial y la microelectrónica.")
    body += sec("El semillero", "Quiénes somos", about)
    body += sec("Propósito", "Objetivos", goals)
    body += sec("Ciclo cerrado", "Sinergia entre líneas", synergy)
    body += sec("Responsabilidad", "Impactos", impact)
    body += CTA
    return body

def p_proyectos():
    filt = '''<div class="filters" role="group" aria-label="Filtrar proyectos por línea">
  <button type="button" data-f="all" aria-pressed="true">Todos</button>
  <button type="button" data-f="l1" aria-pressed="false">Línea 1</button>
  <button type="button" data-f="l2" aria-pressed="false">Línea 2</button></div>'''
    cards = "".join(project_card(p) for p in PROJECTS)
    body = page_head("Proyectos", "Las dos líneas de investigación y los proyectos activos de cada una, con sus resultados principales.")
    body += sec("Investigación", "Líneas de investigación", lines_block(True))
    body += sec("Portafolio", "Catálogo de proyectos", f'<div class="grid3" id="projGrid">{cards}</div>', filt)
    return body

def p_resultados():
    figs = '''<div class="results">
  <figure class="fig-card wide"><img src="img/axint4-vision.jpg" alt="Comparación entre filtro exacto y filtro con el multiplicador Ax-INT4, con mapa de error absoluto, para desenfoque gaussiano y Sobel" width="1143" height="820" loading="lazy">
    <figcaption><strong>Línea 1.</strong> El multiplicador Ax-INT4 hallado por el agente conserva alta fidelidad visual (PSNR 38,0 dB y SSIM 0,99 en desenfoque gaussiano; 43,9 dB y 0,97 en Sobel) con menor complejidad lógica de productos parciales.</figcaption></figure>
  <figure class="fig-card wide"><img src="img/brUNo-mariposa.jpg" alt="Imagen RGB de entrada, salida en escala de grises y mapa de bordes Sobel generados por el chip brUNo" width="1479" height="415" loading="lazy">
    <figcaption><strong>Línea 2.</strong> Validación post-silicio: imagen RGB de 320 × 240 transmitida al ASIC, salida en escala de grises y mapa de bordes Sobel generados por el chip.</figcaption></figure>
  <figure class="fig-card"><img src="img/brUNo-die.jpg" alt="Die de TinyTapeout y detalle del bloque brUNo" width="739" height="559" loading="lazy">
    <figcaption><strong>Chip brUNo.</strong> Die de TinyTapeout (3,6 × 5,2 mm) y detalle del bloque implementado (0,226 × 0,161 mm).</figcaption></figure>
  <div class="fig-card" style="justify-content:center">''' + LINE2_CHIPS + '''</div>
</div>'''
    lessons = '''<div class="lessons">
  <div class="lesson"><h4>Capacidad instalada</h4><p>Entorno de RL propio en GPU, flujo RTL-a-GDSII sobre Sky130 y banco de pruebas post-silicio en la UNAL.</p></div>
  <div class="lesson"><h4>El silicio corrige al modelo</h4><p>La etapa Sobel de brUNo presentó 42,01 % de discrepancia que la verificación RTL no detectó.</p></div>
  <div class="lesson"><h4>Potencia medida, no estimada</h4><p>El reloj representa cerca del 27,8 % de la potencia dinámica, y la fuga medida supera la estimada por OpenLane.</p></div>
</div>'''
    body = page_head("Resultados", "Medir en silicio es parte del método, no un trámite final.")
    body += sec("Evidencia", "Figuras", figs)
    body += sec("Conclusiones", "Lo que aprendimos", lessons)
    return body

def member_card(p):
    mail = f'<span class="mail">{p["mail"]}</span>' if p["mail"] else ""
    return (f'<article class="member">{photo(p)}<div class="info"><h4>{p["name"]}</h4>'
            f'<span class="r">{p["role"]}</span>{mail}</div></article>')

def p_personas():
    d = DIRECTOR
    director = f'''<div class="director-feature">
  {photo(d)}
  <div><span class="eyebrow">Director del semillero</span>
    <h2>{d["name"]}</h2>
    <p>Ph.D., M.Sc. Profesor del Departamento de Ingeniería Eléctrica y Electrónica de la Facultad de Ingeniería, Universidad Nacional de Colombia, Sede Bogotá. Dirige las dos líneas de ChipLabUN: exploración de aritmética digital con aprendizaje por refuerzo y diseño de ASIC de código abierto.</p>
    <span class="mail">{d["mail"]}</span></div>
</div>'''
    l1 = "".join(member_card(p) for p in MEMBERS if p["line"] == "l1")
    l2 = "".join(member_card(p) for p in MEMBERS if p["line"] == "l2")
    join = '''<article class="member" style="border-style:dashed;background:transparent">
  <div class="photo" style="background:var(--copper-soft)"><span class="ini" style="color:var(--copper)">+</span></div>
  <div class="info"><h4>Tu tesis aquí</h4><span class="r">Maestría o doctorado en diseño de chips</span><a class="more" href="contacto.html">Escríbenos →</a></div></article>'''
    inner = director + f'''<div class="group-title"><h3>Línea 1 · IA para diseñar chips</h3><span>Aprendizaje por refuerzo y aritmética aproximada</span></div>
<div class="members">{l1}</div>
<div class="group-title"><h3>Línea 2 · Chips que ejecutan IA</h3><span>Diseño, fabricación y medición de ASIC</span></div>
<div class="members">{l2}{join}</div>'''
    return page_head("Personas", "El equipo de ChipLabUN: dirección e investigadores de las dos líneas.") + sec("Equipo", "Integrantes", inner)

def p_publicaciones():
    filt = '''<div class="filters" role="group" aria-label="Filtrar publicaciones por línea">
  <button type="button" data-p="all" aria-pressed="true">Todas</button>
  <button type="button" data-p="l1" aria-pressed="false">Línea 1</button>
  <button type="button" data-p="l2" aria-pressed="false">Línea 2</button></div>'''
    items = "".join(pub_item(p) for p in PUBS)
    inner = f'''<div class="pubs" id="pubList">{items}</div>
<div class="profiles">
  <a href="https://ieeexplore.ieee.org/author/491224199951815" target="_blank" rel="noopener">Perfil de autor en IEEE Xplore ↗</a>
  <a href="https://ieeexplore.ieee.org/author/907075812378910" target="_blank" rel="noopener">Perfil de autor en IEEE Xplore ↗</a>
  <a href="https://github.com/DarkSpartan345" target="_blank" rel="noopener">Código y resultados en GitHub ↗</a>
</div>'''
    return page_head("Publicaciones", "Artículos del semillero en conferencias IEEE y producción académica.") + sec("Producción", "Artículos", inner, filt)

def p_contacto():
    cards = '''<div class="contact-grid">
  <div class="contact-card"><h3>Ubicación</h3><p>Departamento de Ingeniería Eléctrica y Electrónica, Facultad de Ingeniería. Universidad Nacional de Colombia, Sede Bogotá.</p></div>
  <div class="contact-card"><h3>Código abierto</h3><p>El código y los resultados del semillero están en repositorios públicos.</p><a href="https://github.com/DarkSpartan345" target="_blank" rel="noopener">github.com/DarkSpartan345 ↗</a></div>
  <div class="contact-card"><h3>Publicaciones</h3><p>Consulta los artículos del grupo y los perfiles de autor en IEEE Xplore.</p><a href="publicaciones.html">Ver publicaciones →</a></div>
</div>'''
    return page_head("Contáctanos", "Tesistas, semilleros e instituciones pueden escribirnos para proponer trabajo conjunto.") + CTA + f'<section class="block" style="padding-top:0"><div class="wrap">{cards}</div></section>'

PAGES = [
    ("index.html", "ChipLabUN", p_index),
    ("conocenos.html", "Conócenos · ChipLabUN", p_conocenos),
    ("proyectos.html", "Proyectos · ChipLabUN", p_proyectos),
    ("resultados.html", "Resultados · ChipLabUN", p_resultados),
    ("personas.html", "Personas · ChipLabUN", p_personas),
    ("publicaciones.html", "Publicaciones · ChipLabUN", p_publicaciones),
    ("contacto.html", "Contáctanos · ChipLabUN", p_contacto),
]

if __name__ == "__main__":
    for fname, title, fn in PAGES:
        body = fn()
        with open(os.path.join(OUT, fname), "w") as f:
            f.write(doc(fname, title, body))
        if fname == "index.html" and OUT != _HERE:  # versión para la vista previa en Claude (sin <html>/<head>)
            with open(os.path.join(os.path.dirname(OUT), "preview-index.html"), "w") as f:
                f.write(doc(fname, title, body, full=False))
    print("ok")
