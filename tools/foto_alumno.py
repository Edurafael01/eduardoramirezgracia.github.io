# Prepara la foto de un antiguo alumno para la web: recorte vertical 4:5 (la foto es el fondo de la tarjeta), 800x1000, JPEG.
# Uso: python tools/foto_alumno.py <foto original> <id del alumno>   (el id es el de datos/alumnos.json)
# Resultado: docs/img/alumnos/<id>.jpg
import os, sys
from PIL import Image, ImageOps

origen, ident = sys.argv[1], sys.argv[2]
im = ImageOps.exif_transpose(Image.open(origen)).convert("RGB")
# Recorte 4:5 lo más grande posible; en vertical se toma algo por encima del centro para dejar sitio a la cara
if im.width / im.height > 4 / 5:
    w, h = round(im.height * 4 / 5), im.height
else:
    w, h = im.width, round(im.width * 5 / 4)
x, y = (im.width - w) // 2, max(0, (im.height - h) // 3)
if im.width < 800:
    print("aviso: la foto tiene menos de 800 px de ancho; se verá blanda en pantallas grandes")
im = im.crop((x, y, x + w, y + h)).resize((800, 1000), Image.LANCZOS)
destino = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "img", "alumnos", ident + ".jpg")
os.makedirs(os.path.dirname(destino), exist_ok=True)
im.save(destino, "JPEG", quality=86, optimize=True, progressive=True)
print("ok:", destino)
