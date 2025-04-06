# 🕊️ Saint of the Day – Home Assistant Integration

Affiche le saint du jour selon le calendrier français (et bientôt d'autres langues) dans Home Assistant, sous forme de capteur simple.

![Home Assistant logo](https://img.shields.io/badge/Powered%20by-Home%20Assistant-41BDF5?style=flat-square)

---

## 📦 Installation (via HACS)

1. Ouvrez **HACS > Intégrations** dans Home Assistant
2. Cliquez sur les **trois points** en haut à droite → *Dépôts personnalisés*
3. Ajoutez ce dépôt :  https://github.com/trollix/ha-sotd-int

Type : **Intégration**
4. Recherchez **Saint of the Day** dans HACS et installez-la
5. Redémarrez Home Assistant

---

## ⚙️ Configuration

Une fois installée, ajoutez une nouvelle intégration via l’interface Home Assistant (UI) :

- Entrez un **nom personnalisé** pour le capteur
- Choisissez une **langue** (actuellement : `fr`, `en`, `es`)

Le capteur sera créé avec un nom comme :  
`sensor.saint_du_jour` (ou autre selon le nom choisi)

---

## 📐 Exemple de capteur

```yaml
sensor.saint_du_jour:
state: "Irène"
icon: mdi:church

