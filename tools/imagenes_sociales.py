# Genera la imagen para compartir (og:image, 1200x630) y los favicons en docs/img/.
# Requiere Playwright y las fuentes Barlow / Barlow Condensed instaladas.
import asyncio, os
from playwright.async_api import async_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, "docs", "img")

CSS = """*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0a0a;color:#F0EDE8;font-family:'Barlow',sans-serif;overflow:hidden;position:relative}
.c{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase}.o{color:#C9982A}"""

def og(eyebrow, l1, l2, pie):
    return f"""<div style="position:absolute;inset:0;border:10px solid #C9982A"></div>
<div style="position:absolute;left:80px;top:78px;right:80px">
<div style="font-weight:700;font-size:24px;letter-spacing:.22em;color:#C9982A;text-transform:uppercase">{eyebrow}</div>
<div class="c" style="font-size:118px;line-height:.92;margin-top:30px">{l1}<br><span class="o">{l2}</span></div></div>
<div style="position:absolute;left:80px;bottom:70px;font-weight:600;font-size:26px;letter-spacing:.06em;color:#A39D92">{pie}</div>"""

PIEZAS = {
 "og-profesional.png": (1200, 630, og("Rigging Artist · Technical Director", "Eduardo", "Ramírez Gracia", "Secret Level · Marathon · Zeri · 30 Monedas · eduardoramirezgracia.com")),
 "og-docencia.png": (1200, 630, og("Seminarios de rigging · Escuelas y universidades", "Rigging como se", "trabaja en estudio.", "Eduardo Ramírez Gracia · eduardoramirezgracia.com")),
}
ICONO = """<div style="position:absolute;inset:0;background:#0a0a0a"></div><div style="position:absolute;inset:{b}px;border:{bw}px solid #C9982A"></div>
<div class="c o" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:{fs}px;line-height:1;padding-top:{pt}px">E</div>"""
for nombre, tam in (("favicon-32.png", 32), ("favicon-192.png", 192), ("apple-touch-icon.png", 180)):
    PIEZAS[nombre] = (tam, tam, ICONO.format(b=round(tam*.06), bw=max(2, round(tam*.06)), fs=round(tam*.78), pt=round(tam*.06)))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for nombre, (w, h, cuerpo) in PIEZAS.items():
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.set_content(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='width:{w}px;height:{h}px'>{cuerpo}</body></html>")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=os.path.join(IMG, nombre))
            await pg.close()
            print(nombre)
        await b.close()

asyncio.run(main())
