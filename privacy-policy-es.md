---
layout: legal
lang: es
title: Política de privacidad
permalink: /es/privacy/
---

# Política de privacidad

**Nombre de la app: Sheet Widget (la «App»)**
**Fecha de entrada en vigor: 21 de junio de 2026 / Última actualización: 17 de julio de 2026**

> Esta es una traducción de cortesía. En caso de discrepancia entre esta traducción y la versión original en japonés, prevalecerá la versión japonesa.

---

`Sheet Widget` («nosotros») establece la presente Política de privacidad (la «Política») sobre el tratamiento de la información personal y los datos de los usuarios en la App. Al usar la App, usted acepta esta Política.

## 1. Principio básico

La App **no transmite ni almacena sus datos en ningún servidor operado por nosotros**. No operamos ningún servidor propio: el procesamiento de datos se realiza principalmente en su dispositivo o directamente entre su cuenta de Google y los servicios de Google. (Solo si activa la sincronización con iCloud en los ajustes, la configuración de sus widgets pasa por su propio iCloud; consulte la Sección 4.) **La App no muestra anuncios ni realiza ningún seguimiento (p. ej., IDFA); no incorpora SDK de publicidad ni de analítica de terceros.**

## 2. Información que tratamos

La App trata la siguiente información únicamente en la medida necesaria para ofrecer sus funciones.

### (1) Información de la cuenta de Google
- Dirección de correo electrónico y datos de perfil de su cuenta de Google
- Tokens de autenticación OAuth (token de acceso y token de actualización)

### (2) Información de las hojas de cálculo
- Datos de configuración, como el identificador de la hoja de cálculo de Google, el nombre de la hoja y el rango de celdas que seleccione
- Valores de celda e información de formato obtenidos de la hoja de cálculo para su visualización
- La definición del gráfico que seleccione para mostrar (tipo, rangos referenciados, colores) y sus datos referenciados
- Imágenes referenciadas por fórmulas IMAGE() en celdas (su dispositivo las obtiene directamente del host de la URL y las almacena en caché solo en su dispositivo)

### (3) Información de compras
- El estado de sus compras dentro de la app (compra única y suscripciones). Todos los pagos se procesan a través de Apple (App Store). No recopilamos ni almacenamos datos de pago como números de tarjeta.

## 3. Finalidades de uso

Utilizamos la información únicamente para:
1. Obtener y mostrar datos de hojas de cálculo de Google en widgets, etc.
2. Guardar y restaurar sus configuraciones de widgets
3. Renovar el token de acceso mediante el token de actualización cuando caduque
4. Proporcionar y desbloquear funciones mediante compras dentro de la app

## 4. Dónde y cómo se almacenan los datos

| Datos | Ubicación | Notas |
|---|---|---|
| Tokens de acceso/actualización | Keychain y contenedor compartido de App Group del dispositivo | Nunca salen del dispositivo |
| Configuración y datos de visualización | Contenedor compartido de App Group del dispositivo (y iCloud si la sincronización está activada) | Ver «Sincronización con iCloud» abajo |
| Estado de compra | En el dispositivo | Según la información de compra de Apple |

La App nunca envía estos datos a ningún servidor operado por nosotros. Los datos de las hojas de cálculo se solicitan directamente a los servidores de Google mediante HTTPS usando su token.

### Sincronización con iCloud (opcional)

Solo si activa «Sincronizar con tus otros dispositivos (iCloud)» en los ajustes, la **configuración de tus widgets (el identificador de la hoja, el nombre de la hoja, el rango de celdas, el tamaño, los colores y otros ajustes de visualización)** se sincroniza entre dispositivos con el mismo Apple ID a través de tu propio iCloud (el almacén iCloud Key-Value de Apple).

- Solo se sincroniza la **configuración** anterior. **Tus tokens de OAuth y los valores, el formato y las imágenes de tus hojas no se sincronizan.**
- Los datos sincronizados se guardan en tu propio iCloud y se gestionan según la política de privacidad de Apple. **Nosotros no tenemos acceso a ellos.**
- Esta función está desactivada de forma predeterminada. Mientras esté desactivada, tu configuración nunca sale del dispositivo.

## 5. Comunicación a terceros

Salvo obligación legal, no proporcionamos ni vendemos su información a terceros. Para su funcionamiento, la App se comunica con:

- **Google LLC**: autenticación (Google Sign-In) y obtención de datos de hojas de cálculo (Google Sheets API)
- **Apple Inc.**: procesamiento de compras dentro de la app

## 6. Tratamiento de datos de usuario de Google (Google API Services User Data Policy)

El uso y la transferencia de la información recibida de las API de Google se ajustan a la [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), incluidos los requisitos de Uso Limitado (Limited Use).

- Permisos (scopes) solicitados por la App:
  - `https://www.googleapis.com/auth/drive.file` (acceso a los archivos que el usuario seleccione)
- Solo es accesible el archivo que usted seleccione expresamente mediante el selector oficial de Google (Google Picker). La App no lista ni examina los archivos de su Google Drive y no puede acceder a archivos que no haya seleccionado.
- Aunque `drive.file` permite ver y editar el archivo seleccionado, la App realiza un acceso de **solo lectura** para la visualización y nunca modifica ni elimina sus archivos.
- Los datos de las hojas de cálculo se utilizan **exclusivamente para la función principal de la App: mostrárselos a usted**.
- Nunca usamos dichos datos con fines publicitarios ni los vendemos o transferimos a terceros.
- No permitimos la lectura humana de dichos datos (salvo con su consentimiento explícito, por motivos de seguridad, para cumplir la ley u otras excepciones permitidas por la política).

## 7. Conservación y eliminación de datos

- Al cerrar sesión en la App se eliminan los tokens de autenticación almacenados en el dispositivo.
- Al **desinstalar** la App se eliminan todos los datos relacionados almacenados en el dispositivo (configuración, caché, tokens).
- Puede revocar el acceso de la App en cualquier momento desde la [configuración de seguridad de su cuenta de Google](https://myaccount.google.com/permissions).

## 8. Publicidad y seguimiento

La App **no muestra anuncios**. **No** recopila identificadores de seguimiento (como el IDFA) y no utiliza SDK de publicidad ni de analítica de terceros. Tampoco se muestra el diálogo de App Tracking Transparency.

## 9. Privacidad de los menores

La App no está dirigida a menores de 13 años y no recopilamos deliberadamente información personal de menores de 13 años.

## 10. Seguridad

Los tokens de autenticación se almacenan en el dispositivo mediante los mecanismos de protección del sistema, como el Keychain de iOS. No obstante, ningún método de transmisión por Internet o de almacenamiento electrónico es completamente seguro.

## 11. Transferencias internacionales de datos

Dado que la App utiliza servicios de Google, los datos pueden procesarse en servidores de Google en distintos países. Dicho procesamiento se rige por la política de privacidad de Google.

## 12. Cambios en esta Política

Podemos revisar esta Política cuando sea necesario. En caso de cambios sustanciales, lo notificaremos en la App o en una página pública. El uso continuado de la App tras dichos cambios constituye la aceptación de la Política revisada.

## 13. Contacto

Para consultas sobre esta Política:

- Operador: `Sheet Widget`
- Contacto: `sheetwidget@gmail.com`
- Soporte: `sheetwidget@gmail.com`

---

Esta Política se rige por `la legislación de Japón (con el Tribunal de Distrito de Tokio como tribunal de primera instancia de jurisdicción exclusiva)`.
