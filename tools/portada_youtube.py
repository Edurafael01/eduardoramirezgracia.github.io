# Descarga la portada (miniatura) de vídeos de YouTube a docs/img/yt_<id>.jpg y muestra título y canal,
# para comprobar que es el vídeo oficial. Se ejecuta en GitHub Actions (tiene acceso a internet).
# Uso: IDS="id1 id2" python tools/portada_youtube.py
import os, io, json, urllib.request, urllib.error
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "docs", "img")
os.makedirs(DEST, exist_ok=True)

for vid in os.environ.get("IDS", "").split():
    try:
        meta = json.load(urllib.request.urlopen(
            f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json", timeout=30))
        print(f"{vid} · {meta.get('title')} · canal: {meta.get('author_name')} ({meta.get('author_url')})")
    except urllib.error.HTTPError as err:
        print(f"{vid} · sin datos ({err.code})")
        continue
    for calidad in ("maxresdefault", "sddefault", "hqdefault"):
        try:
            datos = urllib.request.urlopen(f"https://i.ytimg.com/vi/{vid}/{calidad}.jpg", timeout=30).read()
            break
        except urllib.error.HTTPError:
            continue
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    destino = os.path.join(DEST, f"yt_{vid}.jpg")
    im.save(destino, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"   {calidad} {im.size} -> docs/img/yt_{vid}.jpg")
