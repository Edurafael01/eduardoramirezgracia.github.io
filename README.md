# eduardoramirezgracia.github.io

Web profesional de Eduardo Ramírez Gracia, Rigging Artist y Technical Director.

- **Profesional**: demoreel y proyectos, para estudios.
- **Docencia**: centros y seminarios, para escuelas y universidades.

## Cómo está montada

| Ruta | Qué es |
|---|---|
| `build.py` | Genera toda la web. Aquí están los datos: `PROYECTOS`, `SEMINARIOS`, `CENTROS`. |
| `styles.css` | Estilos (negro, dorado, Barlow). Se copia a `docs/` al generar. |
| `docs/` | **La web publicada.** Español en la raíz, inglés en `docs/en/`. GitHub Pages sirve esta carpeta. No se edita a mano: se regenera con `build.py`. |
| `docs/img/` | Portadas, retrato, imagen para compartir y favicons. Logos de los centros en `docs/img/logos/` (PNG blanco a partir de los originales). |
| `tools/` | `traer_imagenes.py` (copió las imágenes de Wix, vía GitHub Actions) e `imagenes_sociales.py` (genera og:image y favicons). |

## Cambiar algo

1. Edita los datos en `build.py` (por ejemplo, añade un proyecto a `PROYECTOS`).
2. Ejecuta `python3 build.py`.
3. Haz commit y push. GitHub Pages publica en uno o dos minutos.

Cada proyecto genera su página `docs/proyecto-<nombre>.html` con ficha, portada y trailer de YouTube.

## Idiomas

Cada texto tiene versión `es` y `en` (función `L(es, en)` en `build.py`). El selector ESP | ENG de la cabecera enlaza con la misma página en el otro idioma.

## Imágenes

Todas las imágenes están en `docs/img/`. Para una nueva, guárdala ahí y usa `img/nombre.jpg` en `build.py`.

## Dominio

`eduardoramirezgracia.com`, con DNS en Cloudflare apuntando a GitHub Pages (`docs/CNAME`).
