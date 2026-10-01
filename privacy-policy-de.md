---
layout: legal
lang: de
title: Datenschutzrichtlinie
permalink: /de/privacy/
---

# Datenschutzrichtlinie

**App-Name: Sheet Widget (die „App")**
**Inkrafttreten: 21. Juni 2026 / Zuletzt aktualisiert: 17. Juli 2026**

> Dies ist eine unverbindliche Übersetzung. Bei Abweichungen zwischen dieser Übersetzung und dem japanischen Original ist das japanische Original maßgeblich.

---

`Sheet Widget` („wir") legt in dieser Datenschutzrichtlinie (die „Richtlinie") fest, wie die App mit personenbezogenen Daten und Nutzerdaten umgeht. Durch die Nutzung der App stimmen Sie dieser Richtlinie zu.

## 1. Grundprinzip

Die App **überträgt oder speichert Ihre Daten auf keinem von uns betriebenen Server**. Wir betreiben keinen Backend-Server; die Datenverarbeitung erfolgt überwiegend auf Ihrem Gerät oder direkt zwischen Ihrem eigenen Google-Konto und den Google-Diensten. (Nur wenn Sie die iCloud-Synchronisierung in den Einstellungen aktivieren, laufen Ihre Widget-Einstellungen über Ihr eigenes iCloud – siehe Abschnitt 4.) **Die App zeigt keine Werbung und führt kein Tracking durch (z. B. IDFA); es sind keine Werbe- oder Analyse-SDKs von Drittanbietern eingebunden.**

## 2. Verarbeitete Informationen

Die App verarbeitet die folgenden Informationen nur in dem Umfang, der für die Bereitstellung ihrer Funktionen erforderlich ist.

### (1) Google-Konto-Informationen
- E-Mail-Adresse und Profilinformationen Ihres Google-Kontos
- OAuth-Authentifizierungstoken (Access-Token und Refresh-Token)

### (2) Tabellen-Informationen
- Konfigurationsdaten wie die Kennung der Google-Tabelle, der Blattname und der von Ihnen gewählte Zellbereich
- Zellwerte und Formatierungsinformationen, die zur Anzeige aus der Tabelle abgerufen werden
- Die Definition eines von Ihnen zur Anzeige gewählten Diagramms (Typ, referenzierte Bereiche, Farben) und dessen referenzierte Daten
- Von IMAGE()-Formeln in Zellen referenzierte Bilder (Ihr Gerät ruft diese direkt vom Host der URL ab und speichert sie nur auf dem Gerät zwischen)

### (3) Kaufinformationen
- Ihr In-App-Kaufstatus (Einmalkäufe und Abonnements). Alle Zahlungen werden über Apple (App Store) abgewickelt. Wir erfassen oder speichern keine Zahlungsdaten wie Kreditkartennummern.

## 3. Verwendungszwecke

Wir verwenden die Informationen ausschließlich, um:
1. Daten aus Google-Tabellen abzurufen und in Widgets usw. anzuzeigen
2. Ihre Widget-Konfigurationen zu speichern und wiederherzustellen
3. Token bei Ablauf des Access-Tokens mit dem Refresh-Token zu erneuern
4. Funktionen über In-App-Käufe bereitzustellen und freizuschalten

## 4. Speicherort und -art der Daten

| Daten | Speicherort | Hinweise |
|---|---|---|
| Access-/Refresh-Token | Keychain und App-Group-Container auf dem Gerät | Verlassen das Gerät nie |
| Tabellen-Konfiguration & Anzeigedaten | App-Group-Container auf dem Gerät (und iCloud, wenn die Synchronisierung aktiviert ist) | Siehe „iCloud-Synchronisierung“ unten |
| Kaufstatus | Auf dem Gerät | Basierend auf Apples Kaufinformationen |

Die App sendet diese Daten niemals an einen von uns betriebenen Server. Tabellendaten werden mit Ihrem Token direkt per HTTPS von den Google-Servern angefordert.

### iCloud-Synchronisierung (optional)

Nur wenn Sie in den Einstellungen „Mit anderen Geräten synchronisieren (iCloud)“ aktivieren, werden Ihre **Widget-Einstellungen (die Kennung der Ziel-Tabelle, der Tabellenname, der Zellbereich, die Größe, die Farben und weitere Anzeigeeinstellungen)** über Ihr eigenes iCloud (Apples iCloud Key-Value-Speicher) zwischen Geräten mit derselben Apple-ID synchronisiert.

- Nur die oben genannten **Einstellungen** werden synchronisiert. **Ihre OAuth-Token sowie die Werte, die Formatierung und die Bilder Ihrer Tabellen werden nicht synchronisiert.**
- Die synchronisierten Daten werden in Ihrem eigenen iCloud gespeichert und gemäß Apples Datenschutzrichtlinie verwaltet. **Wir haben keinen Zugriff darauf.**
- Diese Funktion ist standardmäßig deaktiviert. Solange sie deaktiviert ist, verlassen Ihre Einstellungen das Gerät nicht.

## 5. Weitergabe an Dritte

Außer bei gesetzlicher Verpflichtung geben wir Ihre Informationen nicht an Dritte weiter und verkaufen sie nicht. Für ihre Funktionen kommuniziert die App mit:

- **Google LLC**: Authentifizierung (Google Sign-In) und Abruf von Tabellendaten (Google Sheets API)
- **Apple Inc.**: Abwicklung von In-App-Käufen

## 6. Umgang mit Google-Nutzerdaten (Google API Services User Data Policy)

Die Nutzung und Übertragung von Informationen aus Google-APIs durch die App entspricht der [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy) einschließlich der Limited-Use-Anforderungen.

- Von der App angeforderte Berechtigungen (Scopes):
  - `https://www.googleapis.com/auth/drive.file` (Zugriff auf vom Nutzer ausgewählte Dateien)
- Zugänglich ist nur die Datei, die Sie ausdrücklich über Googles eigene Dateiauswahl (Google Picker) auswählen. Die App listet oder durchsucht keine Dateien in Ihrem Google Drive und kann nicht auf Dateien zugreifen, die Sie nicht ausgewählt haben.
- Obwohl `drive.file` das Ansehen und Bearbeiten der ausgewählten Datei erlaubt, greift die App nur **lesend** zur Anzeige zu und verändert oder löscht Ihre Dateien niemals.
- Tabellendaten werden **ausschließlich für die Kernfunktion der App verwendet: sie Ihnen anzuzeigen**.
- Wir verwenden solche Daten niemals zu Werbezwecken und verkaufen oder übertragen sie nicht an Dritte.
- Eine menschliche Einsichtnahme in diese Daten findet nicht statt (außer mit Ihrer ausdrücklichen Zustimmung, aus Sicherheitsgründen, zur Einhaltung geltenden Rechts oder in sonstigen von der Policy erlaubten Fällen).

## 7. Aufbewahrung und Löschung von Daten

- Beim Abmelden in der App werden die auf dem Gerät gespeicherten Authentifizierungstoken gelöscht.
- Beim **Deinstallieren** der App werden alle auf dem Gerät gespeicherten App-Daten gelöscht (Einstellungen, Cache, Token).
- Sie können den Zugriff der App jederzeit in den [Sicherheitseinstellungen Ihres Google-Kontos](https://myaccount.google.com/permissions) widerrufen.

## 8. Werbung und Tracking

Die App **zeigt keine Werbung**. Sie erfasst **keine** Tracking-Kennungen (wie IDFA) und verwendet keine Werbe- oder Analyse-SDKs von Drittanbietern. Es erscheint auch kein App-Tracking-Transparency-Dialog.

## 9. Datenschutz von Kindern

Die App richtet sich nicht an Kinder unter 13 Jahren. Wir erheben wissentlich keine personenbezogenen Daten von Kindern unter 13 Jahren.

## 10. Sicherheit

Authentifizierungstoken werden mit den Schutzmechanismen des Betriebssystems, etwa dem iOS-Keychain, auf dem Gerät gespeichert. Gleichwohl ist keine Übertragung über das Internet und keine elektronische Speicherung vollkommen sicher.

## 11. Internationale Datenübermittlung

Da die App Google-Dienste nutzt, können Daten auf Google-Servern in verschiedenen Ländern verarbeitet werden. Diese Verarbeitung unterliegt der Datenschutzerklärung von Google.

## 12. Änderungen dieser Richtlinie

Wir können diese Richtlinie bei Bedarf überarbeiten. Über wesentliche Änderungen informieren wir in der App oder auf einer öffentlichen Seite. Die weitere Nutzung der App nach solchen Änderungen gilt als Zustimmung zur überarbeiteten Richtlinie.

## 13. Kontakt

Bei Fragen zu dieser Richtlinie wenden Sie sich bitte an:

- Betreiber: `Sheet Widget`
- Kontakt: `sheetwidget@gmail.com`
- Support: `sheetwidget@gmail.com`

---

Diese Richtlinie unterliegt `japanischem Recht (ausschließlicher Gerichtsstand erster Instanz ist das Bezirksgericht Tokio)`.
