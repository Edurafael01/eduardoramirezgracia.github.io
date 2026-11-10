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

# Datos: vienen del kit de marca (repositorio madrigs_kit, carpeta datos/), única fuente de verdad.
# Se usa ../madrigs_kit/datos si existe (y se copia aquí); si no, la copia local datos/.
import json, shutil
KIT_DATOS = os.path.join(os.path.dirname(RAIZ), "madrigs_kit", "datos")
DATOS = os.path.join(RAIZ, "datos")
if os.path.isdir(KIT_DATOS):
    os.makedirs(DATOS, exist_ok=True)
    for f in ("perfil.json", "proyectos.json", "seminarios.json", "centros.json", "alumnos.json"):
        shutil.copy(os.path.join(KIT_DATOS, f), os.path.join(DATOS, f))

def _cargar(nombre):
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as fh:
        return json.load(fh)

def _img(ruta):
    return ruta  # en los datos ya viene como img/...

PERFIL = _cargar("perfil.json")
PROYECTOS = [dict(s=p["id"], t=p["titulo"], t1=p["portada_texto"][0], t2=p["portada_texto"][1], a=p["anio"],
                  img=p["imagen_web"], d=p["descripcion"], f=[(x["campo"], x["valor"]) for x in p["ficha"]],
                  video=(None if not p["video"] else (p["video"]["youtube"], p["video"]["inicio"],
                                                       p["video"]["etiqueta"]["es"], p["video"]["etiqueta"]["en"])))
             for p in _cargar("proyectos.json")["proyectos"]]
SEMINARIOS = [dict(t1=x["portada_texto"][0], t2=x["portada_texto"][1], dur=x["duracion"], img=x["imagen_web"],
                   titulo=x["titulo"], desc=x["descripcion"], lista=x["resultados"],
                   datos=[(y["campo"], y["valor"]) for y in x["ficha"]])
              for x in _cargar("seminarios.json")["seminarios"]]
# (nombre, archivo del logo sin extensión o None)
CENTROS = [(c["nombre"], (os.path.splitext(os.path.basename(c["logo"]))[0] if c["logo"] else None))
           for c in _cargar("centros.json")["centros"]]

# Antiguos alumnos (carrusel de Docencia). Solo los marcados para publicar y con todo lo necesario.
def _alumnos():
    nombres_centros = {n for n, _ in CENTROS}
    lista = []
    for a in _cargar("alumnos.json")["alumnos"] if os.path.exists(os.path.join(DATOS, "alumnos.json")) else []:
        if not a.get("publicar"):
            continue
        faltan = [c for c in ("nombre", "foto", "reel", "permiso") if not a.get(c)]
        if faltan:
            raise SystemExit(f"alumnos.json · {a['id']}: para publicar faltan {', '.join(faltan)}")
        if not os.path.exists(os.path.join(OUT, a["foto"])):
            raise SystemExit(f"alumnos.json · {a['id']}: no existe docs/{a['foto']} (usa tools/foto_alumno.py)")
        if a.get("centro") and a["centro"] not in nombres_centros:
            raise SystemExit(f"alumnos.json · {a['id']}: el centro «{a['centro']}» no está en centros.json")
        lista.append(a)
    return lista
ALUMNOS = _alumnos()
HUECOS_ALUMNOS = _cargar("alumnos.json").get("huecos", 0) if os.path.exists(os.path.join(DATOS, "alumnos.json")) else 0

# Textos de la interfaz
T = {
 "cliente": L("Cliente", "Client"), "estudio": L("Estudio", "Studio"), "rig": L("Rig", "Rig"),
 "nivel": L("Nivel", "Level"), "software": L("Software", "Software"), "impartido": L("Impartido en", "Taught at"),
 "profesional": L("Profesional", "Professional"), "docencia": L("Docencia", "Teaching"), "contacto": L("Contacto", "Contact"),
 "proyecto": L("Proyecto", "Project"), "seminario": L("Seminario", "Seminar"),
 "todos": L("← Todos los proyectos", "← All projects"), "ver_yt": L("Ver en YouTube", "Watch on YouTube"),
 "escribeme": L("Escríbeme", "Email me"),
 "cargo": PERFIL["cargo"],
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

def alumnos(lang):
    huecos = max(0, HUECOS_ALUMNOS - len(ALUMNOS))
    if not ALUMNOS and not huecos:
        return ""  # la sección no aparece hasta que haya perfiles publicados o huecos
    es = lang == "es"
    def tarjeta(a):
        rol = f'<p class="rol">{e(a["rol"][lang])}</p>' if a.get("rol", {}).get(lang) else ""
        donde = " · ".join(x for x in (a.get("centro"), a.get("anio")) if x)
        donde = f'<p class="donde">{"Formación en" if es else "Trained at"} {e(donde)}</p>' if donde else ""
        li = (f'<a class="btn" href="{e(a["linkedin"])}" target="_blank" rel="noopener" '
              f'aria-label="LinkedIn · {e(a["nombre"])}">LinkedIn</a>') if a.get("linkedin") else ""
        return f"""<li class="alumno">
<img class="foto" src="{pre(lang)}{a["foto"]}" alt="{e(a["nombre"])}" width="800" height="1000" loading="lazy">
<h3>{e(a["nombre"])}</h3>
{rol}{donde}
<div class="enlaces"><a class="btn primario" href="{e(a["reel"])}" target="_blank" rel="noopener" aria-label="{"Ver el reel de" if es else "Watch the reel by"} {e(a["nombre"])}">{"Ver reel" if es else "Watch reel"}</a>{li}</div>
</li>"""
    hueco = f"""<li class="alumno vacio">
<svg class="silueta" viewBox="0 0 200 250" aria-hidden="true"><circle cx="100" cy="88" r="42"></circle><path d="M24 250c0-52 34-86 76-86s76 34 76 86"></path></svg>
<h3>{"[Sin nombre]" if es else "[No name]"}</h3>
</li>"""
    tarjetas = "\n".join([tarjeta(a) for a in ALUMNOS] + [hueco] * huecos)
    return f"""<section id="alumnos"><div class="wrap">
<div class="cab"><p class="eyebrow">{"Antiguos alumnos" if es else "Former students"}</p><h2>{"Su trabajo,<br><span>después del aula.</span>" if es else "Their work,<br><span>after class.</span>"}</h2></div>
<div class="carrusel" data-carrusel>
<button class="flecha prev" type="button" aria-label="{"Anterior" if es else "Previous"}">&#8249;</button>
<ul class="pista" tabindex="0" aria-label="{"Reels de antiguos alumnos" if es else "Former students' reels"}">
{tarjetas}
</ul>
<button class="flecha next" type="button" aria-label="{"Siguiente" if es else "Next"}">&#8250;</button>
</div>
</div></section>
<script>
/* Carrusel de alumnos: las flechas avanzan una tarjeta; al llegar al final vuelve al primero (y al revés). */
document.querySelectorAll("[data-carrusel]").forEach(function (c) {{
  var p = c.querySelector(".pista");
  var suave = matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
  function paso() {{ return p.querySelector(".alumno").getBoundingClientRect().width + parseFloat(getComputedStyle(p).columnGap || 0); }}
  function revisar() {{ c.classList.toggle("quieto", p.scrollWidth <= p.clientWidth + 4); }}
  c.querySelector(".next").addEventListener("click", function () {{
    var fin = p.scrollLeft + p.clientWidth >= p.scrollWidth - 4;
    p.scrollTo({{ left: fin ? 0 : p.scrollLeft + paso(), behavior: suave }});
  }});
  c.querySelector(".prev").addEventListener("click", function () {{
    var ini = p.scrollLeft <= 4;
    p.scrollTo({{ left: ini ? p.scrollWidth : p.scrollLeft - paso(), behavior: suave }});
  }});
  addEventListener("resize", revisar); revisar();
}});
</script>"""

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

{alumnos(lang)}

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
