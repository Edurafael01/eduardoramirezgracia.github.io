# Prepara la foto de un antiguo alumno para la web: recorte cuadrado centrado, 480x480, JPEG.
# Uso: python tools/foto_alumno.py <foto original> <id del alumno>   (el id es el de datos/alumnos.json)
# Resultado: docs/img/alumnos/<id>.jpg
import os, sys
from PIL import Image, ImageOps

origen, ident = sys.argv[1], sys.argv[2]
im = ImageOps.exif_transpose(Image.open(origen)).convert("RGB")
lado = min(im.size)
x, y = (im.width - lado) // 2, max(0, (im.height - lado) // 3)  # algo por encima del centro: deja sitio a la cara
im = im.crop((x, y, x + lado, y + lado)).resize((480, 480), Image.LANCZOS)
destino = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "img", "alumnos", ident + ".jpg")
os.makedirs(os.path.dirname(destino), exist_ok=True)
im.save(destino, "JPEG", quality=86, optimize=True, progressive=True)
print("ok:", destino)
