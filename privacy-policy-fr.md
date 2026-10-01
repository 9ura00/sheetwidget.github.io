---
layout: legal
lang: fr
title: Politique de confidentialité
permalink: /fr/privacy/
---

# Politique de confidentialité

**Nom de l’app : Sheet Widget (l’« App »)**
**Date d’entrée en vigueur : 21 juin 2026 / Dernière mise à jour : 17 juillet 2026**


---

`Sheet Widget` (« nous ») publie la présente politique de confidentialité (la « Politique »), qui décrit la manière dont l’App traite vos informations personnelles et vos données d’utilisateur. En utilisant l’App, vous acceptez la présente Politique.

## 1. Principe fondamental

L’App **ne transmet ni ne stocke vos données sur aucun serveur que nous exploitons**. Nous n’exploitons aucun serveur dorsal. Le traitement des données a lieu principalement sur votre appareil, ou directement entre votre propre compte Google et les services de Google. (Vos configurations de widgets ne transitent par votre propre iCloud que si vous activez la synchronisation iCloud dans les réglages — voir la section 4.) **L’App n’affiche aucune publicité et n’effectue aucun pistage (IDFA, par exemple) ; elle n’intègre aucun SDK publicitaire ou d’analyse tiers.**

## 2. Informations traitées

L’App traite les informations suivantes, uniquement dans la mesure nécessaire au fonctionnement de ses fonctionnalités.

### (1) Informations de compte Google
- L’adresse e-mail et les informations de profil de votre compte Google
- Les jetons d’authentification OAuth (jeton d’accès et jeton d’actualisation)

### (2) Informations relatives aux feuilles de calcul
- Les données de configuration telles que l’identifiant de la feuille de calcul Google, le nom de la feuille et la plage de cellules que vous sélectionnez
- Les valeurs des cellules et les informations de mise en forme récupérées depuis la feuille de calcul en vue de leur affichage
- La définition de tout graphique que vous choisissez d’afficher (type, plages référencées, couleurs) ainsi que les données auxquelles il fait référence
- Les images référencées par des formules IMAGE() dans les cellules (votre appareil les récupère directement auprès de l’hôte de l’URL et les met en cache uniquement sur votre appareil)

### (3) Informations d’achat
- L’état de vos achats intégrés (achats uniques et abonnements). Tous les paiements sont traités par Apple (l’App Store). Nous ne collectons ni ne conservons de données de paiement telles que les numéros de carte bancaire.


## 3. Finalités d’utilisation

Nous utilisons ces informations uniquement aux fins suivantes :
1. Récupérer et afficher les données de vos feuilles de calcul Google, notamment dans des widgets
2. Enregistrer et restaurer vos configurations de widgets
3. Actualiser les jetons à l’aide du jeton d’actualisation lorsque le jeton d’accès expire
4. Fournir et débloquer des fonctionnalités par le biais d’achats intégrés

## 4. Lieu et modalités de conservation des données

| Données | Lieu de conservation | Remarques |
|---|---|---|
| Jetons d’accès / d’actualisation | Trousseau et conteneur partagé App Group, sur l’appareil | Ne quittent jamais l’appareil |
| Configurations et données d’affichage | Conteneur partagé App Group, sur l’appareil (et iCloud si la synchronisation est activée) | Voir « Synchronisation iCloud » ci-dessous |
| État des achats | Sur l’appareil | Établi à partir des informations d’achat Apple |

L’App n’envoie jamais ces données à un serveur que nous exploitons. Les données des feuilles de calcul sont demandées directement aux serveurs de Google via HTTPS, au moyen de votre jeton.


### Synchronisation iCloud (facultative)

Uniquement si vous activez « Synchroniser avec vos autres appareils (iCloud) » dans les réglages, vos **configurations de widgets (identifiant de la feuille cible, nom de la feuille, plage de cellules, taille, couleurs et autres réglages d’affichage)** sont synchronisées entre les appareils liés au même identifiant Apple, par l’intermédiaire de votre propre iCloud (le stockage clé-valeur iCloud d’Apple).

- Seules les **configurations** ci-dessus sont synchronisées. **Vos jetons OAuth ainsi que les valeurs, la mise en forme et les images de vos feuilles ne le sont pas.**
- Les données synchronisées restent dans votre propre iCloud et sont traitées conformément à la politique de confidentialité d’Apple. **Nous n’y avons aucun accès.**
- Cette fonctionnalité est désactivée par défaut. Tant qu’elle l’est, vos configurations ne quittent jamais l’appareil.
## 5. Communication à des tiers

Sauf obligation légale, nous ne communiquons ni ne vendons vos informations à des tiers. Pour son fonctionnement, l’App communique avec les services tiers suivants :

- **Google LLC** : authentification (connexion Google) et récupération des données des feuilles de calcul (API Google Sheets)
- **Apple Inc.** : traitement des achats intégrés

## 6. Traitement des données utilisateur Google (Google API Services User Data Policy)

L’utilisation et le transfert par l’App des informations reçues des API Google respectent la [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), y compris les exigences relatives à l’usage limité (Limited Use).

- Autorisations demandées par l’App :
  - `https://www.googleapis.com/auth/drive.file` (accès aux fichiers que l’utilisateur sélectionne)
- Vous choisissez une feuille de calcul via le sélecteur de fichiers de Google (Google Picker) ; seul le fichier que vous sélectionnez explicitement est accessible. L’App ne répertorie ni ne parcourt les fichiers de votre Google Drive et ne peut pas accéder aux fichiers que vous n’avez pas sélectionnés.
- Bien que `drive.file` autorise la consultation et la modification du fichier sélectionné, l’App effectue un accès **en lecture seule** à des fins d’affichage et ne modifie ni ne supprime jamais vos fichiers.
- Les données des feuilles de calcul sont utilisées **uniquement pour assurer la fonction principale de l’App, à savoir vous les afficher**.
- Nous n’utilisons jamais ces données à des fins publicitaires, et nous ne les vendons ni ne les transférons à des tiers.
- Nous n’autorisons aucune lecture humaine de ces données, sauf (a) avec votre consentement explicite, (b) à des fins de sécurité, (c) pour nous conformer à la loi applicable, ou (d) dans les autres cas permis par la politique.

## 7. Conservation et suppression des données

- La déconnexion depuis l’App supprime les jetons d’authentification stockés sur votre appareil.
- La **désinstallation** de l’App supprime toutes les données qui lui sont liées sur l’appareil (réglages, cache, jetons).
- Vous pouvez révoquer l’accès de l’App à tout moment depuis les [paramètres de sécurité de votre compte Google](https://myaccount.google.com/permissions).

## 8. Publicité et pistage

L’App **n’affiche aucune publicité**. Elle ne collecte **aucun** identifiant de pistage (tel que l’IDFA) et n’utilise aucun SDK publicitaire ou d’analyse tiers. Aucune demande App Tracking Transparency n’est présentée.


## 9. Protection des mineurs

L’App ne s’adresse pas aux enfants de moins de 13 ans. Nous ne collectons pas sciemment d’informations personnelles auprès d’enfants de moins de 13 ans.

## 10. Sécurité

Les jetons d’authentification sont stockés sur l’appareil au moyen des mécanismes de protection fournis par le système, tels que le trousseau iOS. Toutefois, aucune méthode de transmission sur Internet ou de stockage électronique n’est totalement sûre, et nous ne pouvons garantir une sécurité absolue.

## 11. Transferts internationaux de données

L’App faisant appel aux services de Google, vos données peuvent être traitées sur des serveurs de Google situés dans différents pays. Ces traitements sont régis par la politique de confidentialité de Google.

## 12. Modifications de la présente Politique

Nous pouvons réviser la présente Politique si nécessaire. En cas de modification substantielle, nous en informerons les utilisateurs dans l’App ou sur une page publique. La poursuite de l’utilisation de l’App après ces modifications vaut acceptation de la Politique révisée.

## 13. Contact

Pour toute question relative à la présente Politique :

- Exploitant : `Sheet Widget`
- Contact : `sheetwidget@gmail.com`
- Assistance : `sheetwidget@gmail.com`

---

La présente Politique est régie par `le droit japonais (le tribunal de district de Tokyo étant la juridiction de première instance)`.
