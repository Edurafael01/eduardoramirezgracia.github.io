# Formulario de mentorías: puesta en marcha (una sola vez)

Lo hace Edu con su cuenta de Google. Unos 15 minutos.

1. **Crear la hoja.** En Google Drive: Nuevo › Hojas de cálculo. Llamarla `Inscripciones mentorías`. Dejarla vacía.
2. **Pegar el script.** En la hoja: Extensiones › Apps Script. Borrar lo que haya en `Código.gs` y pegar el contenido de `Code.gs` (esta carpeta). Guardar (icono del disquete).
3. **Publicar como aplicación web.** Botón **Implementar › Nueva implementación**. En el engranaje, elegir **Aplicación web**.
   - Descripción: `Formulario mentorías`
   - Ejecutar como: **Yo** (tu cuenta)
   - Quién tiene acceso: **Cualquier usuario**
   - Pulsar **Implementar**.
4. **Dar permisos.** Google pide autorizar el acceso a la hoja y al envío de correo. Como el script es tuyo y no está verificado por Google, aparece un aviso: **Configuración avanzada › Ir a … (no seguro)** y **Permitir**. Solo puede escribir en esta hoja y mandarte correos a ti.
5. **Copiar la dirección.** Google da una "URL de la aplicación web" que termina en `/exec`. Esa dirección se la pasas a DISEÑADOR, que la pone en `datos/perfil.json` (`formulario_mentorias`) del kit y regenera la web.

Para probarlo: rellenar el formulario de la web. Tiene que aparecer una fila en la hoja y llegarte un correo.

Si cambias el script más adelante: Implementar › Gestionar implementaciones › editar › Versión: nueva. Así la dirección no cambia.
