# Descarga las imágenes que build.py todavía toma de Wix y las guarda optimizadas en docs/img/.
# Se ejecuta en GitHub Actions (tiene acceso a internet). Nombre: <id de Wix sin ~mv2>.jpg
import os, re, io, urllib.request
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "docs", "img")
os.makedirs(DEST, exist_ok=True)
texto = open(os.path.join(RAIZ, "build.py"), encoding="utf-8").read()
ids = sorted(set(re.findall(r"(036cf3_[0-9a-f]+~mv2\.(?:jpg|jpeg|png))", texto)))
print(len(ids), "imágenes")
for mid in ids:
    destino = os.path.join(DEST, mid.split("~")[0] + ".jpg")
    if os.path.exists(destino):
        continue
    datos = urllib.request.urlopen("https://static.wixstatic.com/media/" + mid, timeout=60).read()
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    if im.width > 1920:
        im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
    im.save(destino, "JPEG", quality=84, optimize=True, progressive=True)
    print(mid, im.size, os.path.getsize(destino) // 1024, "KB")
