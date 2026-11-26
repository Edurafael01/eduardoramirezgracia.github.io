/**
 * Formulario de mentorías de eduardoramirezgracia.com
 *
 * Recibe las inscripciones del formulario de mentorias.html, las añade como fila en esta hoja
 * y avisa por email a Edu. Se pega en la hoja "Inscripciones mentorías"
 * (Extensiones > Apps Script) y se publica como aplicación web. Instrucciones en INSTRUCCIONES.md.
 */
const AVISAR_A = 'eduardoramirezgracia@gmail.com';
const CABECERA = ['Fecha', 'Nombre', 'Email', 'Qué estudia y dónde', 'Reel', 'Modalidad', 'Disponibilidad', 'Consentimiento'];
const DISPONIBILIDAD = { manana: 'Mañana', tarde: 'Tarde', finde: 'Fin de semana' };

function doPost(e) {
  const p = (e && e.parameter) || {};
  // Campo trampa: las personas no lo ven; si viene relleno es un bot. Se contesta OK sin guardar nada.
  if (p.web) return respuesta_(true);

  const faltan = ['nombre', 'email', 'estudios', 'modalidad'].filter(function (c) { return !String(p[c] || '').trim(); });
  if (faltan.length) return respuesta_(false, 'faltan: ' + faltan.join(', '));
  if (p.consentimiento !== 'si') return respuesta_(false, 'sin consentimiento');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(p.email)) return respuesta_(false, 'email no válido');
  if (['individual', 'grupo'].indexOf(p.modalidad) < 0) return respuesta_(false, 'modalidad no válida');

  const disponibilidad = ((e.parameters && e.parameters.disponibilidad) || [])
    .map(function (d) { return DISPONIBILIDAD[d]; }).filter(Boolean).join(', ');
  const fila = [new Date(), limpia_(p.nombre), limpia_(p.email), limpia_(p.estudios), limpia_(p.reel),
                p.modalidad === 'grupo' ? 'En grupo' : 'Individual', disponibilidad, 'Sí'];

  // Bloqueo para que dos envíos a la vez no se pisen
  const bloqueo = LockService.getScriptLock();
  bloqueo.waitLock(10000);
  try {
    const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (hoja.getLastRow() === 0) hoja.appendRow(CABECERA);
    hoja.appendRow(fila);
  } finally {
    bloqueo.releaseLock();
  }

  MailApp.sendEmail({
    to: AVISAR_A,
    replyTo: limpia_(p.email),
    subject: 'Mentoría · nueva solicitud de ' + limpia_(p.nombre),
    body: CABECERA.slice(1, 7).map(function (c, i) { return c + ': ' + fila[i + 1]; }).join('\n') +
          '\n\nResponde a este correo para escribirle directamente.\nTodas las solicitudes: ' +
          SpreadsheetApp.getActiveSpreadsheet().getUrl()
  });
  return respuesta_(true);
}

// Recorta y evita que un texto que empiece por = + - @ se interprete como fórmula en la hoja
function limpia_(v) {
  v = String(v || '').trim().slice(0, 500);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function respuesta_(ok, error) {
  return ContentService.createTextOutput(JSON.stringify({ ok: ok, error: error || null }))
    .setMimeType(ContentService.MimeType.JSON);
}
