# Web profesional de Eduardo Ramírez Gracia
# Genera la web estática en docs/ a partir de los datos de este archivo.
# Para cambiar contenido: edita PROYECTOS, SEMINARIOS o CENTROS y ejecuta:  python3 build.py
import html, os, re, unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(RAIZ, "docs")  # GitHub Pages publica esta carpeta
DOMINIO = None  # poner "eduardoramirezgracia.com" cuando el dominio apunte a GitHub
EMAIL = "eduardoramirezgracia@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/eduardoramirezgracia"
INSTAGRAM = "https://www.instagram.com/edu_madrigs"
NOMBRE = "Eduardo Ramírez Gracia"
REEL = dict(yt="hT5Q2sQDEmU", img="036cf3_a8b0a880144844d78cb128b8602cf3df~mv2.jpg")

# Imágenes: de momento siguen en el gestor de medios de Wix.
# Un valor que empieza por "img/" apunta a un archivo dentro del repositorio.
WIX = "https://static.wixstatic.com/media/"

def src(img):
    return img if img.startswith(("img/", "http")) else WIX + img

# Proyectos, del más reciente al más antiguo. Diddl va el último.
# f = ficha en orden Cliente, Estudio, Rig. video = (id de YouTube, segundo de inicio, etiqueta).
PROYECTOS = [
    dict(t="TotalEnergies", t1="TotalEnergies", t2="Publicidad", a="2026", img="036cf3_2a972a8c4c0744e58cf43abc2b1551ee~mv2.jpg",
         d="Rig del personaje principal de una pieza publicitaria para TotalEnergies.",
         f=[("Cliente", "TotalEnergies"), ("Estudio", "Miopia"), ("Rig", "Character rig")], video=("6LG45b-x8TI", 0, "Anuncio")),
    dict(t="El Fantasma de la Quinta", t1="El Fantasma", t2="de la Quinta", a="2025", img="036cf3_4dc6122ad3f64b78bf977e5394cb2394~mv2.jpeg",
         d="Rig corporal de Goya y rigs corporales y faciales de Saturno y del pájaro.",
         f=[("Cliente", "Illusorium & Martirio Films"), ("Estudio", "Illusorium"), ("Rig", "Goya · Saturno · pájaro")], video=("UC2GJT3PUS0", 0, "Trailer")),
    dict(t="Marathon · Cinematic Trailer", s="marathon-cinematic-trailer", t1="Marathon", t2="Cinematic Trailer", a="2025", img="036cf3_ae6ea901d7984047b9acf65915a10507~mv2.jpg",
         d="Rig de personaje de Man para el trailer cinemático de Marathon, dirigido por Alberto Mielgo.",
         f=[("Cliente", "Bungie"), ("Estudio", "Illusorium"), ("Rig", "Man · character rig")], video=("fvbEnWLRo1s", 101, "Trailer")),
    dict(t="Secret Level · PAC-MAN", t1="Secret Level", t2="PAC-MAN", a="2024", img="036cf3_a6c7a423f1394cb1ab3cd644ed6e6dec~mv2.jpg",
         d="Rig de criatura de Beast para el episodio PAC-MAN de la serie antológica Secret Level.",
         f=[("Cliente", "Blur Studio · Amazon"), ("Estudio", "Illusorium"), ("Rig", "Beast · creature rig")], video=("1hsuOFv5hRk", 0, "Trailer")),
    dict(t="Secret Level · Spelunky", t1="Secret Level", t2="Spelunky", a="2024", img="036cf3_95df628c1bf74ee6b5681fbf396b8cc2~mv2.jpg",
         d="Rig de personaje de Young Girl y rig mecánico para el episodio Spelunky.",
         f=[("Cliente", "Blur Studio · Amazon"), ("Estudio", "Illusorium"), ("Rig", "Young Girl · rig mecánico")], video=("1hsuOFv5hRk", 0, "Trailer")),
    dict(t="Secret Level · Mega Man", t1="Secret Level", t2="Mega Man", a="2024", img="036cf3_f31ee0c1ead641fb85c59ea661e05eee~mv2.png",
         d="Rigs corporales de Mega Man y Doctor Light, y rig de araña, para el episodio Mega Man.",
         f=[("Cliente", "Blur Studio · Amazon"), ("Estudio", "Illusorium"), ("Rig", "Mega Man · Doctor Light · araña")], video=("1hsuOFv5hRk", 0, "Trailer")),
    dict(t="Dungeon Fighter", t1="Dungeon", t2="Fighter", a="2023", img="036cf3_dd67386ff4814f1e994085acaba9cf18~mv2.jpg",
         d="Rigs de personaje de Shadow y Armour.",
         f=[("Estudio", "Illusorium"), ("Rig", "Shadow · Armour")], video=None),
    dict(t="Sky: The Two Embers", t1="Sky", t2="The Two Embers", a="2023", img="036cf3_e0c779c3e34245ac8d815bab85742039~mv2.jpg",
         d="Rigs de múltiples personajes para Sky: The Two Embers.",
         f=[("Cliente", "That Game Company"), ("Estudio", "Illusorium · Orchid"), ("Rig", "Múltiples rigs")], video=("FWepS03YbFU", 0, "Trailer")),
    dict(t="Zeri: The Spark of Zaun", t1="Zeri", t2="The Spark of Zaun", a="2022", img="036cf3_08cbb93d717d4c8582eb321037d043f3~mv2.png",
         d="Rig de Son of Urgoth para Zeri: The Spark of Zaun.",
         f=[("Cliente", "Riot Games"), ("Estudio", "Illusorium"), ("Rig", "Son of Urgoth")], video=("YW2mAg9w7Vw", 0, "Trailer")),
    dict(t="Ark Encounter", t1="Ark", t2="Encounter", a="2021", img="036cf3_164ae5db46ac4e48935d3082ab246462~mv2.jpg",
         d="Rigs de criatura de una llama y un canguro.",
         f=[("Cliente", "Ark Encounter"), ("Estudio", "Illusorium"), ("Rig", "Llama · canguro")], video=("P2fVPLn3rTg", 0, "Trailer")),
    dict(t="Dislyte: Ready to Awake", s="dislyte", t1="Dislyte", t2="Ready to Awake", a="2021", img="036cf3_b806ef56640645b88b770fba50f7c971~mv2.jpg",
         d="Rigs de múltiples personajes para Dislyte: Ready to Awake.",
         f=[("Cliente", "Dislyte"), ("Estudio", "Illusorium"), ("Rig", "Múltiples personajes")], video=("F0hGORCEd9s", 0, "Trailer")),
    dict(t="30 Monedas", t1="30", t2="Monedas", a="2021", img="036cf3_0ec4be564bb94b00953a2bacce5a040b~mv2.jpg",
         d="Rig de Beast para la serie 30 Monedas.",
         f=[("Cliente", "HBO"), ("Estudio", "Illusorium"), ("Rig", "Beast")], video=("8WO2GFnS6UU", 0, "Trailer")),
    dict(t="My Universe", t1="My", t2="Universe", a="2021", img="036cf3_1c077fdc2d9f467aa19f77a7309d1dc1~mv2.jpg",
         d="Rig de ojos para My Universe.",
         f=[("Cliente", "BTS & Coldplay"), ("Estudio", "Illusorium"), ("Rig", "Eye rig")], video=("3YqPKLZF_WU", 0, "Videoclip")),
    dict(t="Treasure Trekkers", t1="Treasure", t2="Trekkers", a="2021", img="036cf3_ebe7641ef25c41639391e4a0b095bcb0~mv2.jpg",
         d="Rig corporal y facial del mono y rigs de múltiples personajes, con AdvancedSkeleton.",
         f=[("Estudio", "B-Water Animation Studios"), ("Rig", "Mono · múltiples personajes")], video=("IOtM-InsCmA", 0, "Trailer")),
    dict(t="Diddl", t1="Diddl", t2="", a="2020", img="036cf3_6c1696523d4643899d9dc1fe80989238~mv2.jpg",
         d="Rigs de múltiples personajes para Diddl en B-Water Animation Studios.",
         f=[("Estudio", "B-Water Animation Studios"), ("Rig", "Múltiples personajes")], video=("I0tvjOpWpJ8", 0, "Trailer")),
]

SEMINARIOS = [
    dict(t1="Fundamentos", t2="del Rigging", dur="3 h", img="036cf3_7013a77583954fd3b14b3cfd0d9e8526~mv2.jpg",
         titulo="Fundamentos del Rigging en Producción",
         desc="Principios de rigging aplicados a producción en Autodesk Maya: organización de la escena, jerarquías, constraints y criterios de control pensados para animación.",
         datos=[("Software", "Autodesk Maya"), ("Impartido en", "CEU San Pablo")]),
    dict(t1="Rigging en Maya", t2="+ Unreal Engine", dur="3 h", img="036cf3_96946e13c4564668ac88b6eddca3f33a~mv2.jpg",
         titulo="Rigging en Maya + Unreal Engine",
         desc="Del rig en Maya a Unreal Engine: cómo preparar un personaje para que funcione en motor.",
         datos=[("Software", "Autodesk Maya · Unreal Engine"), ("Impartido en", "CEU San Pablo")]),
    dict(t1="Automatización", t2="de Rigging", dur="6 h", img="036cf3_d30c10bd89504689acc9b432f0bc4241~mv2.jpg",
         titulo="Automatización de Rigging en Entornos Profesionales",
         desc="Cómo se trabaja con autorigs en el sector: qué automatizar, qué no y cómo encaja en el pipeline de un estudio.",
         datos=[("Software", "Autodesk Maya"), ("Impartido en", "CEU San Pablo · UNIR")]),
]

# (nombre, archivo del logo en logos_svg/ o None para mostrar el nombre en texto)
CENTROS = [("CICE", "cice"), ("Trazos", "trazos"), ("Movie School", None), ("Lightbox Academy", "lightbox"),
           ("CEU San Pablo", "ceu"), ("UNIR", "unir"), ("UFV", "ufv"), ("Animworkshop", "animworkshop"), ("ECAM", "ecam")]

e = html.escape

def slug(p):
    if p.get("s"):
        return p["s"]
    t = unicodedata.normalize("NFKD", p["t"]).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def url_proyecto(p):
    return "proyecto-" + slug(p) + ".html"

def logo_svg(clave):
    return open(os.path.join(RAIZ, "logos_svg", clave + ".svg")).read().strip()

CSS = open(os.path.join(RAIZ, "styles.css")).read()

def head(titulo, desc):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&family=Barlow+Condensed:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="marco" aria-hidden="true"></div>"""

def cabecera(actual):
    def a(href, txt, clave):
        cur = ' aria-current="page"' if clave == actual else ""
        return f'<a href="{href}"{cur}>{txt}</a>'
    return f"""<header><div class="wrap">
<a class="marca" href="index.html">Eduardo <span class="largo">Ramírez </span><span>Gracia</span></a>
<nav aria-label="Principal">
{a("index.html", "Profesional", "pro")}
{a("docencia.html", "Docencia", "doc")}
<a class="nav-sec" href="#contacto">Contacto</a>
</nav></div></header>"""

def portada(t1, t2, eyebrow, img, alt):
    if img:
        return f'<div class="cover"><img src="{e(src(img))}" alt="{e(alt)}" loading="lazy"></div>'
    t2h = f"<span>{e(t2)}</span>" if t2 else ""
    return f'<div class="cover tipo" aria-hidden="true"><span class="ce">{e(eyebrow)}</span><span class="ct">{e(t1)}{t2h}</span></div>'

def datos(lst):
    return "<dl>" + "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in lst) + "</dl>"

def contacto(titulo_b, titulo_g, texto, asunto):
    mail = f"mailto:{EMAIL}?subject={asunto.replace(' ', '%20')}"
    return f"""<section id="contacto" class="contacto"><div class="wrap">
<p class="eyebrow">Contacto</p>
<h2>{e(titulo_b)}<br><span>{e(titulo_g)}</span></h2>
<p class="lead">{e(texto)}</p>
<div class="btns"><a class="btn primario" href="{mail}">Escríbeme</a><a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></div>
<div class="redes"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></div>
</div></section>"""

def pie():
    return f"""<footer><div class="wrap">{e(NOMBRE)} · Rigging Artist · Technical Director</div></footer>
</body></html>"""

TXT_ESTUDIO = "Para incorporaciones a estudio o proyectos de rigging, escríbeme y te respondo."

def tarjeta_proyecto(p):
    return f"""<article class="card">{portada(p['t1'], p['t2'], "Proyecto", p['img'], p['t'])}
<div class="h"><span class="meta">{e(p['a'] or 'Proyecto')}</span><h3><a class="enlace" href="{url_proyecto(p)}">{e(p['t'])}</a></h3></div><p class="tx">{e(p['d'])}</p><div class="dt">{datos(p['f'])}</div></article>"""

def bloque_video(p):
    if not p.get("video"):
        return ""
    vid, ini, etiqueta = p["video"]
    emb = f"https://www.youtube-nocookie.com/embed/{vid}?rel=0" + (f"&amp;start={ini}" if ini else "")
    ver = f"https://www.youtube.com/watch?v={vid}" + (f"&amp;t={ini}s" if ini else "")
    return f"""
<section class="trailer"><div class="wrap">
<p class="eyebrow">{e(etiqueta)}</p>
<div class="video"><iframe src="{emb}" title="{e(etiqueta)} de {e(p['t'])}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
<p class="yt"><a href="{ver}" target="_blank" rel="noopener">Ver en YouTube</a></p>
</div></section>"""

def pagina_proyecto(i):
    p = PROYECTOS[i]
    ant = PROYECTOS[i - 1] if i > 0 else None
    sig = PROYECTOS[i + 1] if i < len(PROYECTOS) - 1 else None
    nav = ""
    if ant: nav += f'<a class="btn" href="{url_proyecto(ant)}">← {e(ant["t"])}</a>'
    if sig: nav += f'<a class="btn" href="{url_proyecto(sig)}">{e(sig["t"])} →</a>'
    anio = f"{p['a']} · " if p['a'] else ""
    return f"""{head(p['t'] + " · " + NOMBRE, p['d'])}
{cabecera("pro")}
<main>
<section class="hero"><div class="wrap">
<a class="volver" href="index.html#proyectos">← Todos los proyectos</a>
<p class="eyebrow" style="margin-top:28px">{e(anio)}Proyecto</p>
<h1>{e(p['t'])}</h1>
<p class="lead">{e(p['d'])}</p>
<div class="ficha">{datos(p['f'])}</div>
</div></section>
<section><div class="wrap">{portada(p['t1'], p['t2'], "Proyecto", p['img'], p['t'])}</div></section>{bloque_video(p)}
<div class="wrap puente">{nav}</div>
{contacto("¿Hablamos", "de tu proyecto?", TXT_ESTUDIO, "Rigging para estudio")}
</main>
{pie()}"""

def tarjeta_seminario(s):
    return f"""<article class="card">{portada(s['t1'], s['t2'], "Seminario", s.get('img'), s['titulo'])}
<div class="h"><span class="meta">{e(s['dur'])}</span><h3>{e(s['titulo'])}</h3></div><p class="tx">{e(s['desc'])}</p><div class="dt">{datos(s['datos'])}</div></article>"""

def profesional():
    cards = "\n".join(tarjeta_proyecto(p) for p in PROYECTOS)
    return f"""{head(NOMBRE + " · Rigging Artist", "Rigging Artist y Technical Director en Madrid. Rigs corporales, faciales y de criaturas para series, cinemáticas y publicidad.")}
{cabecera("pro")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Rigging Artist · Technical Director · Madrid</p>
<h1>Rigs para<br><span>producción.</span></h1>
<p class="lead">Rigs corporales, faciales y de criaturas para series, cinemáticas y publicidad. Créditos en Secret Level (Blur Studio · Amazon) y en el trailer cinemático de Marathon.</p>
<div class="btns"><a class="btn primario" href="#demoreel">Ver demoreel</a><a class="btn" href="#contacto">Contactar</a></div>
</div></section>

<section id="demoreel"><div class="wrap">
<div class="cab"><p class="eyebrow">Demoreel 2026</p><h2>Mi trabajo<br><span>en 1 minuto.</span></h2></div>
<a class="video reel" href="https://www.youtube.com/watch?v={REEL['yt']}" target="_blank" rel="noopener" aria-label="Ver la demoreel 2026 en YouTube"><img src="{e(src(REEL['img']))}" alt="Demoreel 2026 de {e(NOMBRE)}" loading="lazy"><span class="play" aria-hidden="true"></span><span class="ver">Ver demoreel</span></a>
</div></section>

<section id="proyectos"><div class="wrap">
<div class="cab"><p class="eyebrow">Proyectos</p><h2>Trabajo<br><span>en producción.</span></h2></div>
<div class="grid">
{cards}
</div></div></section>

{contacto("¿Necesitas rigger", "para tu estudio?", TXT_ESTUDIO, "Rigging para estudio")}

<div class="wrap puente"><p>¿Eres un centro <span>educativo?</span></p><a class="btn" href="docencia.html">Ver seminarios</a></div>
</main>
{pie()}"""

def docencia():
    cards = "\n".join(tarjeta_seminario(s) for s in SEMINARIOS)
    centros = "\n".join(
        f'<div class="centro" role="img" aria-label="{e(n)}">{logo_svg(l)}</div>' if l else f'<div class="centro"><span>{e(n)}</span></div>'
        for n, l in CENTROS)
    return f"""{head("Seminarios de rigging · " + NOMBRE, "Seminarios de rigging de producción para escuelas y universidades, impartidos por un Rigging Artist y Technical Director en activo.")}
{cabecera("doc")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Docencia · Formación técnica en rigging</p>
<h1>Rigging como se<br><span>trabaja en estudio.</span></h1>
<p class="lead">Seminarios prácticos para escuelas y universidades, impartidos por un rigger en activo en producción.</p>
<div class="btns"><a class="btn primario" href="#seminarios">Ver seminarios</a><a class="btn" href="#contacto">Contactar</a></div>
</div></section>

<section id="centros"><div class="wrap">
<div class="cab"><p class="eyebrow">Centros</p><h2>Centros con los que<br><span>he colaborado.</span></h2></div>
<div class="centros">
{centros}
</div></div></section>

<section id="seminarios"><div class="wrap">
<div class="cab"><p class="eyebrow">Seminarios</p><h2>Seminarios<br><span>especializados.</span></h2></div>
<div class="grid">
{cards}
</div></div></section>

{contacto("Seminarios", "para tu centro.", "Cuéntame el nivel de tu alumnado y el formato que buscas, y te propongo el seminario que encaja.", "Seminarios de rigging")}

<div class="wrap puente"><p>¿Eres un <span>estudio?</span></p><a class="btn" href="index.html">Ver proyectos</a></div>
</main>
{pie()}"""

def no_encontrada():
    return f"""{head("Página no encontrada · " + NOMBRE, "Esta página no existe.")}
{cabecera("")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Error 404</p>
<h1>Esta página<br><span>no existe.</span></h1>
<div class="btns"><a class="btn primario" href="index.html">Ir a proyectos</a><a class="btn" href="docencia.html">Ir a docencia</a></div>
</div></section>
</main>
{pie()}"""

def escribir(nombre, texto):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as fh:
        fh.write(texto)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".html"):
            os.remove(os.path.join(OUT, f))
    escribir("styles.css", CSS.strip() + "\n")
    escribir("index.html", profesional())
    escribir("docencia.html", docencia())
    escribir("404.html", no_encontrada())
    for i, p in enumerate(PROYECTOS):
        escribir(url_proyecto(p), pagina_proyecto(i))
    if DOMINIO:
        escribir("CNAME", DOMINIO + "\n")
    escribir(".nojekyll", "")
    print("ok:", len(PROYECTOS), "proyectos")
