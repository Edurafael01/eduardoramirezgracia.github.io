# Web profesional de Eduardo Ramírez Gracia
# Genera la web estática bilingüe en docs/ (español en la raíz, inglés en docs/en/).
# Para cambiar contenido: edita PROYECTOS, SEMINARIOS, CENTROS o los textos de T y ejecuta:  python3 build.py
# Cada texto visible tiene versión "es" y "en".
import html, os, re, unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(RAIZ, "docs")  # GitHub Pages publica esta carpeta
DOMINIO = "eduardoramirezgracia.com"
URL = "https://" + DOMINIO
EMAIL = "eduardoramirezgracia@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/eduardoramirezgracia"
INSTAGRAM = "https://www.instagram.com/edu_madrigs"
NOMBRE = "Eduardo Ramírez Gracia"
REEL = dict(yt="hT5Q2sQDEmU", img="036cf3_a8b0a880144844d78cb128b8602cf3df~mv2.jpg")
RETRATO = "img/retrato.jpg"
DOSSIER = "dossier-seminarios-rigging.pdf"
IDIOMAS = ("es", "en")

def src(img):
    # Los ids de Wix se sirven desde la copia local en docs/img/ (descargada con tools/traer_imagenes.py)
    if img.startswith(("img/", "http")):
        return img
    return "img/" + img.split("~")[0] + ".jpg"

def L(es, en):
    return {"es": es, "en": en}

# Proyectos, del más reciente al más antiguo. Diddl va el último.
# f = ficha en orden Cliente, Estudio, Rig. video = (id de YouTube, segundo de inicio, etiqueta es, etiqueta en).
PROYECTOS = [
    dict(s="blacksad", t=L("Blacksad", "Blacksad"), t1="Blacksad", t2="Fan Animation", a="2026",
         img="036cf3_47cc1c6251a0418faa9f6e503dd5d1a2~mv2.jpg",
         d=L("Múltiples rigs para una animación fan de Blacksad.", "Multiple rigs for a Blacksad fan animation."),
         f=[("estudio", "Illusorium"), ("rig", L("Múltiples rigs", "Multiple rigs"))],
         video=("t3qnuVscDes", 0, "Vídeo", "Video")),
    dict(s="totalenergies", t=L("TotalEnergies", "TotalEnergies"), t1="TotalEnergies", t2=L("Publicidad", "Commercial"), a="2026",
         img="036cf3_2a972a8c4c0744e58cf43abc2b1551ee~mv2.jpg",
         d=L("Rig del personaje principal de una pieza publicitaria para TotalEnergies.",
             "Rig of the main character for a TotalEnergies commercial."),
         f=[("cliente", "TotalEnergies"), ("estudio", "Miopia"), ("rig", L("Character rig", "Character Rig"))],
         video=("6LG45b-x8TI", 0, "Anuncio", "Commercial")),
    dict(s="el-fantasma-de-la-quinta", t=L("El Fantasma de la Quinta", "The Quinta's Ghost"), t1=L("El Fantasma", "The Quinta's"), t2=L("de la Quinta", "Ghost"), a="2025",
         img="036cf3_4dc6122ad3f64b78bf977e5394cb2394~mv2.jpeg",
         d=L("Rig corporal de Goya y rigs corporales y faciales de Saturno y del pájaro.",
             "Body rig for Goya, and body and facial rigs for Saturn and the bird."),
         f=[("cliente", "Illusorium & Martirio Films"), ("estudio", "Illusorium"),
            ("rig", L("Goya · Saturno · pájaro", "Goya · Saturn · Bird"))],
         video=("UC2GJT3PUS0", 0, "Trailer", "Trailer")),
    dict(s="marathon-cinematic-trailer", t=L("Marathon · Cinematic Trailer", "Marathon · Cinematic Trailer"), t1="Marathon", t2="Cinematic Trailer", a="2025",
         img="036cf3_ae6ea901d7984047b9acf65915a10507~mv2.jpg",
         d=L("Rig de personaje de Man para el trailer cinemático de Marathon, dirigido por Alberto Mielgo.",
             "Character rig for Man in the Marathon cinematic trailer, directed by Alberto Mielgo."),
         f=[("cliente", "Bungie"), ("estudio", "Illusorium"), ("rig", L("Man · character rig", "Man, Character Rig"))],
         video=("fvbEnWLRo1s", 101, "Trailer", "Trailer")),
    dict(s="secret-level-pac-man", t=L("Secret Level · PAC-MAN", "Secret Level · PAC-MAN"), t1="Secret Level", t2="PAC-MAN", a="2024",
         img="036cf3_a6c7a423f1394cb1ab3cd644ed6e6dec~mv2.jpg",
         d=L("Rig de criatura de Beast para el episodio PAC-MAN de la serie antológica Secret Level.",
             "Creature rig for the Beast in the PAC-MAN episode of the anthology series Secret Level."),
         f=[("cliente", "Blur Studio · Amazon"), ("estudio", "Illusorium"),
            ("rig", L("Beast · creature rig", "Beast, Creature Rig (simulation not included)"))],
         video=("1hsuOFv5hRk", 0, "Trailer", "Trailer")),
    dict(s="secret-level-spelunky", t=L("Secret Level · Spelunky", "Secret Level · Spelunky"), t1="Secret Level", t2="Spelunky", a="2024",
         img="036cf3_95df628c1bf74ee6b5681fbf396b8cc2~mv2.jpg",
         d=L("Rig de personaje de Young Girl y rig mecánico para el episodio Spelunky.",
             "Character rig for the Young Girl and a mechanical rig for the Spelunky episode."),
         f=[("cliente", "Blur Studio · Amazon"), ("estudio", "Illusorium"),
            ("rig", L("Young Girl · rig mecánico", "Young Girl, Character Rig · Mechanical Rig"))],
         video=("1hsuOFv5hRk", 0, "Trailer", "Trailer")),
    dict(s="secret-level-mega-man", t=L("Secret Level · Mega Man", "Secret Level · Mega Man"), t1="Secret Level", t2="Mega Man", a="2024",
         img="036cf3_f31ee0c1ead641fb85c59ea661e05eee~mv2.png",
         d=L("Rigs corporales de Mega Man y Doctor Light, y rig de araña, para el episodio Mega Man.",
             "Body rigs for Mega Man and Doctor Light, plus a spider rig, for the Mega Man episode."),
         f=[("cliente", "Blur Studio · Amazon"), ("estudio", "Illusorium"),
            ("rig", L("Mega Man · Doctor Light · araña", "Mega Man · Doctor Light · Spider"))],
         video=("1hsuOFv5hRk", 0, "Trailer", "Trailer")),
    dict(s="dungeon-fighter", t=L("Dungeon Fighter", "Dungeon Fighter"), t1="Dungeon", t2="Fighter", a="2023",
         img="036cf3_dd67386ff4814f1e994085acaba9cf18~mv2.jpg",
         d=L("Rigs de personaje de Shadow y Armour.", "Character rigs for Shadow and Armour."),
         f=[("estudio", "Illusorium"), ("rig", L("Shadow · Armour", "Shadow & Armour, Character Rig"))],
         video=None),
    dict(s="sky-the-two-embers", t=L("Sky: The Two Embers", "Sky: The Two Embers"), t1="Sky", t2="The Two Embers", a="2023",
         img="036cf3_e0c779c3e34245ac8d815bab85742039~mv2.jpg",
         d=L("Rigs de múltiples personajes para Sky: The Two Embers.", "Rigs for multiple characters in Sky: The Two Embers."),
         f=[("cliente", "That Game Company"), ("estudio", "Illusorium · Orchid"), ("rig", L("Múltiples rigs", "Multiple rigs"))],
         video=("FWepS03YbFU", 0, "Trailer", "Trailer")),
    dict(s="zeri-the-spark-of-zaun", t=L("Zeri: The Spark of Zaun", "Zeri: The Spark of Zaun"), t1="Zeri", t2="The Spark of Zaun", a="2022",
         img="036cf3_08cbb93d717d4c8582eb321037d043f3~mv2.png",
         d=L("Rig de Son of Urgoth para Zeri: The Spark of Zaun.", "Rig for the Son of Urgoth in Zeri: The Spark of Zaun."),
         f=[("cliente", "Riot Games"), ("estudio", "Illusorium"), ("rig", "Son of Urgoth")],
         video=("YW2mAg9w7Vw", 0, "Trailer", "Trailer")),
    dict(s="ark-encounter", t=L("Ark Encounter", "Ark Encounter"), t1="Ark", t2="Encounter", a="2021",
         img="036cf3_164ae5db46ac4e48935d3082ab246462~mv2.jpg",
         d=L("Rigs de criatura de una llama y un canguro.", "Creature rigs for a llama and a kangaroo."),
         f=[("cliente", "Ark Encounter"), ("estudio", "Illusorium"), ("rig", L("Llama · canguro", "Llama & Kangaroo, Creature Rig"))],
         video=("P2fVPLn3rTg", 0, "Trailer", "Trailer")),
    dict(s="dislyte", t=L("Dislyte: Ready to Awake", "Dislyte: Ready to Awake"), t1="Dislyte", t2="Ready to Awake", a="2021",
         img="036cf3_b806ef56640645b88b770fba50f7c971~mv2.jpg",
         d=L("Rigs de múltiples personajes para Dislyte: Ready to Awake.", "Rigs for multiple characters in Dislyte: Ready to Awake."),
         f=[("cliente", "Dislyte"), ("estudio", "Illusorium"), ("rig", L("Múltiples personajes", "Multiple characters"))],
         video=("F0hGORCEd9s", 0, "Trailer", "Trailer")),
    dict(s="30-monedas", t=L("30 Monedas", "30 Coins"), t1="30", t2=L("Monedas", "Coins"), a="2021",
         img="036cf3_0ec4be564bb94b00953a2bacce5a040b~mv2.jpg",
         d=L("Rig de Beast para la serie 30 Monedas.", "Rig for the Beast in the series 30 Coins."),
         f=[("cliente", "HBO"), ("estudio", "Illusorium"), ("rig", "Beast")],
         video=("8WO2GFnS6UU", 0, "Trailer", "Trailer")),
    dict(s="my-universe", t=L("My Universe", "My Universe"), t1="My", t2="Universe", a="2021",
         img="036cf3_1c077fdc2d9f467aa19f77a7309d1dc1~mv2.jpg",
         d=L("Rig de ojos para My Universe.", "Eye rig for My Universe."),
         f=[("cliente", "BTS & Coldplay"), ("estudio", "Illusorium"), ("rig", "Eye rig")],
         video=("3YqPKLZF_WU", 0, "Videoclip", "Music video")),
    dict(s="treasure-trekkers", t=L("Treasure Trekkers", "Treasure Trekkers"), t1="Treasure", t2="Trekkers", a="2021",
         img="036cf3_ebe7641ef25c41639391e4a0b095bcb0~mv2.jpg",
         d=L("Rig corporal y facial del mono y rigs de múltiples personajes, con AdvancedSkeleton.",
             "Body and facial rig for the monkey and rigs for multiple characters, built with AdvancedSkeleton."),
         f=[("estudio", "B-Water Animation Studios"), ("rig", L("Mono · múltiples personajes", "Monkey · multiple characters"))],
         video=("IOtM-InsCmA", 0, "Trailer", "Trailer")),
    dict(s="diddl", t=L("Diddl", "Diddl"), t1="Diddl", t2="", a="2020",
         img="036cf3_6c1696523d4643899d9dc1fe80989238~mv2.jpg",
         d=L("Rigs de múltiples personajes para Diddl en B-Water Animation Studios.",
             "Rigs for multiple characters for Diddl at B-Water Animation Studios."),
         f=[("estudio", "B-Water Animation Studios"), ("rig", L("Múltiples personajes", "Multiple characters"))],
         video=("I0tvjOpWpJ8", 0, "Trailer", "Trailer")),
]

# Seminarios (contenido del dossier de seminarios, 30/10/2026)
SEMINARIOS = [
    dict(t1=L("Fundamentos", "Rigging"), t2=L("del Rigging", "Fundamentals"), dur="3 h", img="036cf3_7013a77583954fd3b14b3cfd0d9e8526~mv2.jpg",
         titulo=L("Fundamentos del Rigging en Producción", "Rigging Fundamentals for Production"),
         desc=L("Rig de props en Maya: jerarquías, constraints, control rig y pipeline.",
                "Prop rigging in Maya: hierarchies, constraints, control rig and pipeline."),
         lista=L(["Entiende la estructura jerárquica del rigging aplicado a producción",
                  "Crea un rig funcional de prop con el flujo de trabajo de un estudio",
                  "Aplica la nomenclatura y la organización de escena de un pipeline real"],
                 ["Understand the hierarchical structure of production rigging",
                  "Build a working prop rig following a studio workflow",
                  "Apply the naming and scene organisation of a real pipeline"]),
         datos=[("nivel", L("Básico", "Beginner")), ("software", "Autodesk Maya"), ("impartido", "CEU San Pablo")]),
    dict(t1="Maya", t2="+ Unreal Engine", dur="3 h", img="036cf3_96946e13c4564668ac88b6eddca3f33a~mv2.jpg",
         titulo=L("Rigging en Maya + Unreal Engine", "Rigging in Maya + Unreal Engine"),
         desc=L("Rigging para videojuegos: exportación, IK Rig, Modular Rig y Control Rig.",
                "Rigging for games: export, IK Rig, Modular Rig and Control Rig."),
         lista=L(["Sabe qué viaja de Maya a Unreal Engine 5 y prepara esqueleto y geometría para exportar",
                  "Trabaja dentro del motor con IK Rig, Modular Rig y Control Rig",
                  "Comprende las restricciones técnicas del pipeline de videojuegos"],
                 ["Know what travels from Maya to Unreal Engine 5 and prepare skeleton and geometry for export",
                  "Work inside the engine with IK Rig, Modular Rig and Control Rig",
                  "Understand the technical constraints of a game pipeline"]),
         datos=[("nivel", L("Básico", "Beginner")), ("software", "Autodesk Maya · Unreal Engine 5"), ("impartido", "CEU San Pablo")]),
    dict(t1=L("Automatización", "Rigging"), t2=L("de Rigging", "Automation"), dur="6 h", img="036cf3_d30c10bd89504689acc9b432f0bc4241~mv2.jpg",
         titulo=L("Automatización de Rigging en Entornos Profesionales", "Rigging Automation in Professional Environments"),
         desc=L("Rigging con AdvancedSkeleton: rig corporal y facial, herramientas y pipeline.",
                "Rigging with AdvancedSkeleton: body and facial rig, tools and pipeline."),
         lista=L(["Construye el rig corporal y facial de un personaje con AdvancedSkeleton",
                  "Itera sobre el rig cuando el modelo cambia, sin rehacer el trabajo",
                  "Muestra el rig en movimiento para su demoreel"],
                 ["Build a character's body and facial rig with AdvancedSkeleton",
                  "Iterate on the rig when the model changes, without redoing the work",
                  "Show the rig in motion for their demo reel"]),
         datos=[("nivel", L("Inicial-intermedio", "Beginner to intermediate")), ("software", "Autodesk Maya · AdvancedSkeleton"),
                ("impartido", L("CEU San Pablo · UNIR (laboratorio online)", "CEU San Pablo · UNIR (online lab)"))]),
    dict(t1=L("Criaturas", "Quadruped"), t2=L("Cuadrúpedas", "Creatures"), dur="3 h · 6 h", img=None,
         titulo=L("Rigging de Criaturas Cuadrúpedas", "Quadruped Creature Rigging"),
         desc=L("Laboratorio práctico: el alumnado construye desde cero el rig de un caballo, del esqueleto a los controles de animación.",
                "Hands-on lab: students build a horse rig from scratch, from the skeleton to the animation controls."),
         lista=L(["3 h: patas con control del corvejón y del casco, columna, cuello y cabeza",
                  "6 h: todo lo anterior, más criaturas aladas, skinning, cola y rig facial sobre el rig de referencia"],
                 ["3 h: legs with hock and hoof control, spine, neck and head",
                  "6 h: all of the above, plus winged creatures, skinning, tail and facial rig on the reference rig"]),
         datos=[("nivel", L("Intermedio", "Intermediate")), ("software", "Autodesk Maya"), ("impartido", L("Novedad 2027", "New in 2027"))]),
]

# (nombre, archivo del logo en docs/img/logos/ sin extensión, o None para mostrar el nombre en texto). Universidades primero.
CENTROS = [("CEU San Pablo", "ceu"), ("UNIR", "unir"), ("UFV", "ufv"), ("ECAM", "ecam"), ("Lightbox Academy", "lightbox"),
           ("CICE", "cice"), ("Trazos", "trazos"), ("Animworkshop", "animworkshop"), ("Movie School", None)]

# Textos de la interfaz
T = {
 "cliente": L("Cliente", "Client"), "estudio": L("Estudio", "Studio"), "rig": L("Rig", "Rig"),
 "nivel": L("Nivel", "Level"), "software": L("Software", "Software"), "impartido": L("Impartido en", "Taught at"),
 "profesional": L("Profesional", "Professional"), "docencia": L("Docencia", "Teaching"), "contacto": L("Contacto", "Contact"),
 "proyecto": L("Proyecto", "Project"), "seminario": L("Seminario", "Seminar"),
 "todos": L("← Todos los proyectos", "← All projects"), "ver_yt": L("Ver en YouTube", "Watch on YouTube"),
 "escribeme": L("Escríbeme", "Email me"),
 "cargo": L("Rigging Artist · Technical Director", "Rigging Artist · Technical Director"),
}

e = html.escape

def tr(v, lang):
    return v[lang] if isinstance(v, dict) else v

# Logos oficiales en PNG blanco (docs/img/logos/), a partir de los originales de cada centro.
LOGOS_CUADRADOS = {"cice", "trazos", "ecam"}

CSS = open(os.path.join(RAIZ, "styles.css")).read()

def pre(lang):
    """Prefijo de rutas hacia la raíz de docs/ desde la página de ese idioma."""
    return "" if lang == "es" else "../"

def head(lang, pagina, titulo, desc, desc_social, og_img):
    p = pre(lang)
    ruta_es = URL + "/" + (pagina if pagina != "index.html" else "")
    ruta_en = URL + "/en/" + (pagina if pagina != "index.html" else "")
    canon = ruta_es if lang == "es" else ruta_en
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="es" href="{ruta_es}">
<link rel="alternate" hreflang="en" href="{ruta_en}">
<link rel="alternate" hreflang="x-default" href="{ruta_es}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc_social)}">
<meta property="og:image" content="{URL}/img/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'es_ES' if lang == 'es' else 'en_GB'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{p}img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{p}img/favicon-192.png">
<link rel="apple-touch-icon" href="{p}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&family=Barlow+Condensed:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}styles.css">
</head>
<body>
<div class="marco" aria-hidden="true"></div>"""

def cabecera(lang, actual, pagina):
    def a(href, txt, clave):
        cur = ' aria-current="page"' if clave == actual else ""
        return f'<a href="{href}"{cur}>{txt}</a>'
    # Selector: misma página en el otro idioma
    es_href = ("" if lang == "es" else "../") + pagina
    en_href = ("en/" if lang == "es" else "") + pagina
    sel = (f'<span class="idioma" aria-label="Idioma / Language">'
           f'<a href="{es_href}" hreflang="es" lang="es"{" aria-current=true" if lang == "es" else ""}>ESP</a>|'
           f'<a href="{en_href}" hreflang="en" lang="en"{" aria-current=true" if lang == "en" else ""}>ENG</a></span>')
    return f"""<header><div class="wrap">
<a class="marca" href="index.html">Eduardo <span class="largo">Ramírez </span><span>Gracia</span></a>
<nav aria-label="{'Principal' if lang == 'es' else 'Main'}">
{a("index.html", T["profesional"][lang], "pro")}
{a("docencia.html", T["docencia"][lang], "doc")}
<a class="nav-sec" href="#contacto">{T["contacto"][lang]}</a>
{sel}
</nav></div></header>"""

def portada(lang, t1, t2, eyebrow, img, alt):
    if img:
        return f'<div class="cover"><img src="{pre(lang)}{e(src(img))}" alt="{e(alt)}" loading="lazy"></div>'
    t1, t2 = tr(t1, lang), tr(t2, lang)
    t2h = f"<span>{e(t2)}</span>" if t2 else ""
    return f'<div class="cover tipo" aria-hidden="true"><span class="ce">{e(eyebrow)}</span><span class="ct">{e(t1)}{t2h}</span></div>'

def datos(lang, lst):
    return "<dl>" + "".join(f"<dt>{e(T[k][lang])}</dt><dd>{e(tr(v, lang))}</dd>" for k, v in lst) + "</dl>"

def mailto(asunto, cuerpo=""):
    from urllib.parse import quote
    q = "subject=" + quote(asunto)
    if cuerpo:
        q += "&amp;body=" + quote(cuerpo)
    return f"mailto:{EMAIL}?{q}"

def contacto(lang, titulo_b, titulo_g, texto, asunto, cuerpo="", extra_btn=""):
    return f"""<section id="contacto" class="contacto"><div class="wrap">
<p class="eyebrow">{T["contacto"][lang]}</p>
<h2>{e(titulo_b)}<br><span>{e(titulo_g)}</span></h2>
<p class="lead">{e(texto)}</p>
<div class="btns"><a class="btn primario" href="{mailto(asunto, cuerpo)}">{T["escribeme"][lang]}</a>{extra_btn}<a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></div>
<div class="redes"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></div>
</div></section>"""

def pie(lang):
    return f"""<footer><div class="wrap">{e(NOMBRE)} · {T["cargo"][lang]}</div></footer>
</body></html>"""

TXT_ESTUDIO = L("Para incorporaciones a estudio o proyectos de rigging, escríbeme y te respondo.",
                "For studio positions or rigging projects, drop me a line and I'll get back to you.")
ASUNTO_ESTUDIO = L("Rigging para estudio", "Rigging for your studio")

def url_proyecto(p):
    return "proyecto-" + p["s"] + ".html"

def tarjeta_proyecto(lang, p):
    t = tr(p["t"], lang)
    return f"""<article class="card">{portada(lang, p['t1'], p['t2'], T['proyecto'][lang], p['img'], t)}
<div class="h"><span class="meta">{e(p['a'])}</span><h3><a class="enlace" href="{url_proyecto(p)}">{e(t)}</a></h3></div><p class="tx">{e(tr(p['d'], lang))}</p><div class="dt">{datos(lang, p['f'])}</div></article>"""

def bloque_video(lang, p):
    if not p.get("video"):
        return ""
    vid, ini, et_es, et_en = p["video"]
    etiqueta = et_es if lang == "es" else et_en
    emb = f"https://www.youtube-nocookie.com/embed/{vid}?rel=0" + (f"&amp;start={ini}" if ini else "")
    ver = f"https://www.youtube.com/watch?v={vid}" + (f"&amp;t={ini}s" if ini else "")
    de = "de" if lang == "es" else "for"
    return f"""
<section class="trailer"><div class="wrap">
<p class="eyebrow">{e(etiqueta)}</p>
<div class="video"><iframe src="{emb}" title="{e(etiqueta)} {de} {e(tr(p['t'], lang))}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
<p class="yt"><a href="{ver}" target="_blank" rel="noopener">{T["ver_yt"][lang]}</a></p>
</div></section>"""

def pagina_proyecto(lang, i):
    p = PROYECTOS[i]
    t = tr(p["t"], lang)
    ant = PROYECTOS[i - 1] if i > 0 else None
    sig = PROYECTOS[i + 1] if i < len(PROYECTOS) - 1 else None
    nav = ""
    if ant: nav += f'<a class="btn" href="{url_proyecto(ant)}">← {e(tr(ant["t"], lang))}</a>'
    if sig: nav += f'<a class="btn" href="{url_proyecto(sig)}">{e(tr(sig["t"], lang))} →</a>'
    d = tr(p["d"], lang)
    social = (f"{d} Proyecto de {NOMBRE}, Rigging Artist." if lang == "es" else f"{d} A project by {NOMBRE}, Rigging Artist.")
    return f"""{head(lang, url_proyecto(p), t + " · " + NOMBRE, d, social, "og-profesional.png")}
{cabecera(lang, "pro", url_proyecto(p))}
<main>
<section class="hero"><div class="wrap">
<a class="volver" href="index.html#proyectos">{T["todos"][lang]}</a>
<p class="eyebrow" style="margin-top:28px">{e(p['a'])} · {T["proyecto"][lang]}</p>
<h1>{e(t)}</h1>
<p class="lead">{e(d)}</p>
<div class="ficha">{datos(lang, p['f'])}</div>
</div></section>
<section><div class="wrap">{portada(lang, p['t1'], p['t2'], T['proyecto'][lang], p['img'], t)}</div></section>{bloque_video(lang, p)}
<div class="wrap puente">{nav}</div>
{contacto(lang, *(("¿Hablamos", "de tu proyecto?") if lang == "es" else ("Shall we talk", "about your project?")), TXT_ESTUDIO[lang], ASUNTO_ESTUDIO[lang])}
</main>
{pie(lang)}"""

def tarjeta_seminario(lang, s):
    titulo = tr(s["titulo"], lang)
    lista = "".join(f"<li>{e(x)}</li>" for x in tr(s["lista"], lang))
    return f"""<article class="card">{portada(lang, s['t1'], s['t2'], T['seminario'][lang], s.get('img'), titulo)}
<div class="h"><span class="meta">{e(s['dur'])}</span><h3>{e(titulo)}</h3></div><div class="tx"><p>{e(tr(s['desc'], lang))}</p><ul class="lista">{lista}</ul></div><div class="dt">{datos(lang, s['datos'])}</div></article>"""

def hero_retrato(lang, eyebrow, h1, lead, botones):
    alt = "Retrato de " + NOMBRE if lang == "es" else "Portrait of " + NOMBRE
    return f"""<section class="hero"><div class="wrap hero-grid">
<div>
<p class="eyebrow">{eyebrow}</p>
<h1>{h1}</h1>
<p class="lead">{e(lead)}</p>
<div class="btns">{botones}</div>
</div>
<img class="retrato" src="{pre(lang)}{RETRATO}" alt="{e(alt)}" width="260" height="260">
</div></section>"""

def profesional(lang):
    es = lang == "es"
    cards = "\n".join(tarjeta_proyecto(lang, p) for p in PROYECTOS)
    titulo = NOMBRE + " · Rigging Artist"
    desc = ("Rigging Artist y Technical Director en Madrid. Rigs corporales, faciales y de criaturas para series, cinemáticas y publicidad." if es else
            "Rigging Artist and Technical Director based in Madrid. Body, facial and creature rigs for series, cinematics and commercials.")
    social = ("Demoreel y proyectos de rigging: Secret Level, Marathon, Zeri, 30 Monedas y más. Disponible para estudios." if es else
              "Demo reel and rigging projects: Secret Level, Marathon, Zeri, 30 Coins and more. Available for studios.")
    lead = ("Rigs corporales, faciales y de criaturas para series, cinemáticas y publicidad. Créditos en Secret Level (Blur Studio · Amazon) y en el trailer cinemático de Marathon." if es else
            "Body, facial and creature rigs for series, cinematics and commercials. Credits on Secret Level (Blur Studio · Amazon) and the Marathon cinematic trailer.")
    botones = (f'<a class="btn primario" href="#demoreel">{"Ver demoreel" if es else "Watch demo reel"}</a>'
               f'<a class="btn" href="#contacto">{"Contactar" if es else "Get in touch"}</a>')
    h1 = "Rigs para<br><span>producción.</span>" if es else "Rigs built for<br><span>production.</span>"
    ver = "Ver demoreel" if es else "Watch demo reel"
    return f"""{head(lang, "index.html", titulo, desc, social, "og-profesional.png")}
{cabecera(lang, "pro", "index.html")}
<main>
{hero_retrato(lang, T["cargo"][lang] + " · Madrid", h1, lead, botones)}

<section id="demoreel"><div class="wrap">
<div class="cab"><p class="eyebrow">{"Demoreel 2026" if es else "Demo reel 2026"}</p><h2>{"Mi trabajo<br><span>en 1 minuto.</span>" if es else "My work<br><span>in one minute.</span>"}</h2></div>
<a class="video reel" href="https://www.youtube.com/watch?v={REEL['yt']}" target="_blank" rel="noopener" aria-label="{ver} (YouTube)"><img src="{pre(lang)}{e(src(REEL['img']))}" alt="{'Demoreel 2026 de' if es else 'Demo reel 2026 by'} {e(NOMBRE)}" loading="lazy"><span class="play" aria-hidden="true"></span><span class="ver">{ver}</span></a>
</div></section>

<section id="proyectos"><div class="wrap">
<div class="cab"><p class="eyebrow">{"Proyectos" if es else "Projects"}</p><h2>{"Trabajo<br><span>en producción.</span>" if es else "Production<br><span>work.</span>"}</h2></div>
<div class="grid">
{cards}
</div></div></section>

{contacto(lang, *(("¿Necesitas rigger", "para tu estudio?") if es else ("Need a rigger", "for your studio?")), TXT_ESTUDIO[lang], ASUNTO_ESTUDIO[lang])}

<div class="wrap puente"><p>{"¿Eres un centro <span>educativo?</span>" if es else "Are you a <span>school?</span>"}</p><a class="btn" href="docencia.html">{"Ver seminarios" if es else "See seminars"}</a></div>
</main>
{pie(lang)}"""

def como_trabajo(lang):
    es = lang == "es"
    formatos = [
        (L("Masterclass", "Masterclass"), L("Hasta 3 h", "Up to 3 h"),
         L("Sesión expositiva con demostración en vivo. Ideal como actividad puntual, jornada o foro.",
           "Lecture with a live demo. Ideal as a one-off activity, event day or forum.")),
        (L("Seminario", "Seminar"), L("3 a 6 h", "3 to 6 h"),
         L("Teoría aplicada y práctica guiada con archivos de producción. Cada alumno sale con su entregable.",
           "Applied theory and guided practice with production files. Every student leaves with a deliverable.")),
        (L("Laboratorio práctico", "Hands-on lab"), L("3 h", "3 h"),
         L("El alumnado construye el rig desde cero, paso a paso, con un rig de referencia completo como guía.",
           "Students build the rig from scratch, step by step, with a complete reference rig as a guide.")),
        (L("A medida", "Tailored"), L("Según necesidad", "As needed"),
         L("Bloques de varios seminarios o contenido diseñado con el coordinador académico según el perfil del alumnado.",
           "Several seminars combined, or content designed with the academic coordinator for the student profile.")),
    ]
    f_html = "\n".join(f'<div class="formato"><h3>{e(n[lang])}</h3><span class="meta">{e(d[lang])}</span><p>{e(t[lang])}</p></div>' for n, d, t in formatos)
    cond = [
        (L("Modalidad", "Format"), L("Presencial en Madrid, en el aula del centro con un puesto por alumno, u online en directo en la plataforma del centro (España y Latinoamérica).",
                                     "In person in Madrid, in the school's classroom with one workstation per student, or live online on the school's platform (Spain and Latin America).")),
        (L("Encaje", "Fit"), L("Se adapta al nivel del grupo y se plantea como complemento al programa del centro, no como sustituto. Materiales y archivos de trabajo incluidos.",
                               "Adapted to the group's level and designed to complement the school's programme, not replace it. Materials and working files included.")),
    ]
    c_html = "\n".join(f'<div class="condicion"><strong>{e(n[lang])}</strong>{e(t[lang])}</div>' for n, t in cond)
    return f"""<section id="formatos"><div class="wrap">
<div class="cab"><p class="eyebrow">{"Cómo trabajo" if es else "How I work"}</p><h2>{"Cuatro formas<br><span>de trabajar.</span>" if es else "Four ways<br><span>to work together.</span>"}</h2></div>
<div class="formatos">
{f_html}
</div>
<div class="condiciones">
{c_html}
</div>
</div></section>"""

SESION_YT = "tzMgbhzYOzA"  # Foro UNIR, 27/10/2026

def sesion(lang):
    es = lang == "es"
    pie_ = ("Foro «Rigging artist ante la IA: así se crean los personajes 3D» · UNIR · 27 de octubre de 2026" if es else
            "Forum \u201cRigging artist ante la IA: así se crean los personajes 3D\u201d · UNIR · 27 October 2026")
    return f"""<section id="sesion" class="trailer"><div class="wrap">
<p class="eyebrow">{"Así es una sesión" if es else "What a session looks like"}</p>
<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{SESION_YT}?rel=0" title="{e(pie_)}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
<p class="yt">{e(pie_)} · <a href="https://www.youtube.com/watch?v={SESION_YT}" target="_blank" rel="noopener">{T["ver_yt"][lang]}</a></p>
</div></section>"""

def docencia(lang):
    es = lang == "es"
    cards = "\n".join(tarjeta_seminario(lang, s) for s in SEMINARIOS)
    centros = "\n".join(
        f'<div class="centro"><img class="{"cuadrado" if l in LOGOS_CUADRADOS else ""}" src="{pre(lang)}img/logos/{l}.png" alt="{e(n)}" loading="lazy"></div>' if l else f'<div class="centro"><span>{e(n)}</span></div>'
        for n, l in CENTROS)
    titulo = ("Seminarios de rigging · " if es else "Rigging seminars · ") + NOMBRE
    desc = ("Seminarios de rigging de producción para escuelas y universidades, impartidos por un Rigging Artist y Technical Director en activo." if es else
            "Production rigging seminars for schools and universities, taught by a working Rigging Artist and Technical Director.")
    social = ("Seminarios, laboratorios y masterclasses de rigging para grados, másteres y escuelas. Presencial en Madrid u online." if es else
              "Rigging seminars, labs and masterclasses for degrees, master's programmes and schools. In person in Madrid or online.")
    lead = ("Rigging Artist y Technical Director con créditos en Secret Level (Blur Studio · Amazon) y en el tráiler cinemático de Marathon. Seminarios y laboratorios prácticos para grados, másteres y escuelas, en presencial (Madrid) u online." if es else
            "Rigging Artist and Technical Director with credits on Secret Level (Blur Studio · Amazon) and the Marathon cinematic trailer. Seminars and hands-on labs for degrees, master's programmes and schools, in person (Madrid) or online.")
    botones = (f'<a class="btn primario" href="#seminarios">{"Ver seminarios" if es else "See seminars"}</a>'
               f'<a class="btn" href="{pre(lang)}{DOSSIER}" target="_blank" rel="noopener">{"Descargar dossier (PDF)" if es else "Download brochure (PDF, Spanish)"}</a>')
    h1 = "Rigging como se<br><span>trabaja en estudio.</span>" if es else "Rigging the way<br><span>studios do it.</span>"
    extra = ('<p class="extra"><strong>También:</strong> desarrollo de herramientas con Python y la API de Maya, herramientas internas con PyQt y rigging cartoon. Pregúntame.</p>' if es else
             '<p class="extra"><strong>Also available:</strong> tool development with Python and the Maya API, in-house tools with PyQt, and cartoon rigging. Just ask.</p>')
    texto_contacto = ("Cuéntame tu centro y titulación, el nivel y el número de alumnos, si lo buscas presencial u online y unas fechas aproximadas. Te respondo con una propuesta." if es else
                      "Tell me about your school and programme, the students' level and group size, whether you need it in person or online, and rough dates. I'll reply with a proposal.")
    cuerpo = ("Centro y titulación:\nNivel del alumnado:\nNúmero de alumnos:\nPresencial u online:\nFechas aproximadas:\nSeminario o formato que os interesa:\n" if es else
              "School and programme:\nStudents' level:\nGroup size:\nIn person or online:\nRough dates:\nSeminar or format you're interested in:\n")
    btn_dossier = f'<a class="btn" href="{pre(lang)}{DOSSIER}" target="_blank" rel="noopener">{"Dossier (PDF)" if es else "Brochure (PDF)"}</a>'
    return f"""{head(lang, "docencia.html", titulo, desc, social, "og-docencia.png")}
{cabecera(lang, "doc", "docencia.html")}
<main>
{hero_retrato(lang, "Docencia · Formación técnica en rigging" if es else "Teaching · Technical rigging training", h1, lead, botones)}

<section id="centros"><div class="wrap">
<div class="cab"><p class="eyebrow">{"Centros" if es else "Schools"}</p><h2>{"Centros donde he<br><span>impartido formación.</span>" if es else "Where I have<br><span>taught.</span>"}</h2></div>
<div class="centros">
{centros}
</div></div></section>

{sesion(lang)}

{como_trabajo(lang)}

<section id="seminarios"><div class="wrap">
<div class="cab"><p class="eyebrow">{"Seminarios" if es else "Seminars"}</p><h2>{"Seminarios<br><span>especializados.</span>" if es else "Specialised<br><span>seminars.</span>"}</h2></div>
<div class="grid">
{cards}
</div>
{extra}
</div></section>

{contacto(lang, *(("Seminarios", "para tu centro.") if es else ("Seminars", "for your school.")), texto_contacto, "Seminarios de rigging" if es else "Rigging seminars", cuerpo, btn_dossier)}

<div class="wrap puente"><p>{"¿Eres un <span>estudio?</span>" if es else "Are you a <span>studio?</span>"}</p><a class="btn" href="index.html">{"Ver proyectos" if es else "See projects"}</a></div>
</main>
{pie(lang)}"""

def no_encontrada():
    return f"""{head("es", "404.html", "Página no encontrada · " + NOMBRE, "Esta página no existe.", "Esta página no existe.", "og-profesional.png").replace('href="styles.css"', 'href="/styles.css"').replace('href="img/', 'href="/img/')}
<header><div class="wrap"><a class="marca" href="/">Eduardo <span class="largo">Ramírez </span><span>Gracia</span></a></div></header>
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Error 404</p>
<h1>Esta página<br><span>no existe.</span></h1>
<p class="lead">This page does not exist.</p>
<div class="btns"><a class="btn primario" href="/">Ir al inicio</a><a class="btn" href="/en/">Go to home page</a></div>
</div></section>
</main>
{pie("es")}"""

def escribir(nombre, texto):
    ruta = os.path.join(OUT, nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write(texto)

if __name__ == "__main__":
    for carpeta in (OUT, os.path.join(OUT, "en")):
        if os.path.isdir(carpeta):
            for f in os.listdir(carpeta):
                if f.endswith(".html"):
                    os.remove(os.path.join(carpeta, f))
    escribir("styles.css", CSS.strip() + "\n")
    for lang in IDIOMAS:
        base = "" if lang == "es" else "en/"
        escribir(base + "index.html", profesional(lang))
        escribir(base + "docencia.html", docencia(lang))
        for i, p in enumerate(PROYECTOS):
            escribir(base + url_proyecto(p), pagina_proyecto(lang, i))
    escribir("404.html", no_encontrada())
    if DOMINIO:
        escribir("CNAME", DOMINIO + "\n")
    escribir(".nojekyll", "")
    print("ok:", len(PROYECTOS), "proyectos ×", len(IDIOMAS), "idiomas")
