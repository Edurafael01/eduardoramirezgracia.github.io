# eduardoramirezgracia.github.io

Web profesional de Eduardo Ramírez Gracia, Rigging Artist y Technical Director.

- **Profesional**: demoreel y proyectos, para estudios.
- **Docencia**: centros y seminarios, para escuelas y universidades.

## Cómo está montada

| Ruta | Qué es |
|---|---|
| `build.py` | Genera toda la web. Aquí están los datos: `PROYECTOS`, `SEMINARIOS`, `CENTROS`. |
| `styles.css` | Estilos (negro, dorado, Barlow). Se copia a `docs/` al generar. |
| `logos_svg/` | Logos de los centros en SVG blanco. |
| `docs/` | **La web publicada.** GitHub Pages sirve esta carpeta. No se edita a mano: se regenera con `build.py`. |

## Cambiar algo

1. Edita los datos en `build.py` (por ejemplo, añade un proyecto a `PROYECTOS`).
2. Ejecuta `python3 build.py`.
3. Haz commit y push. GitHub Pages publica en uno o dos minutos.

Cada proyecto genera su página `docs/proyecto-<nombre>.html` con ficha, portada y trailer de YouTube.

## Imágenes

Las portadas están todavía en el gestor de medios de Wix (`static.wixstatic.com`). Para independizarse de Wix, sube cada imagen a `docs/img/` y cambia su valor en `build.py` por `img/nombre.jpg`.

## Dominio

Cuando `eduardoramirezgracia.com` apunte a GitHub Pages, pon `DOMINIO = "eduardoramirezgracia.com"` en `build.py` y regenera: se crea `docs/CNAME`.
