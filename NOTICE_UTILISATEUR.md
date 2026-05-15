# 📖 Notice d'utilisation - WriteHelper

---

## Installation (une seule fois)

1. Télécharger et installer Python depuis https://www.python.org/downloads/
   - **Cocher la case "Add Python to PATH"** lors de l'installation
2. Double-cliquer sur le fichier `installer.bat` fourni avec l'outil

C'est prêt !

---

## Lancer l'outil

Double-cliquer sur **`gui.py`**

Une fenêtre s'ouvre avec 3 onglets en haut :

- 📋 Dictionnaire
- ✏️ Éditeur
- ⚡ Générateur

---

## Usage 1 : Consulter les codes disponibles

1. Cliquer sur l'onglet **📋 Dictionnaire**
2. La liste complète des codes et phrases s'affiche
3. Faire défiler pour trouver le code souhaité

---

## Usage 2 : Générer un compte rendu

1. Cliquer sur l'onglet **⚡ Générateur**
2. Dans le champ de saisie, taper les codes séparés par des tirets
   - Exemple : `ID6-ID7-F1-TC4-ITT3-C1`
3. La prévisualisation s'affiche automatiquement en dessous
4. Cliquer sur **Copier** pour copier le texte dans le presse-papier
   - Il suffit ensuite de faire Ctrl+V dans votre logiciel
5. Cliquer sur **Sauvegarder** pour enregistrer dans un fichier texte horodaté

💡 **Astuce** : Vous pouvez utiliser des codes de groupe (ex: `INTRO`) qui génèrent automatiquement plusieurs phrases d'un coup.

---

## Usage 3 : Ajouter ou modifier une phrase

1. Cliquer sur l'onglet **✏️ Éditeur**
2. Remplir le champ **Code** (ex: `TC19`) et le champ **Phrase** (ex: `Plaie de la lèvre`)
3. Cliquer sur **Ajouter / Modifier**
4. Si le code existe déjà, une confirmation sera demandée avant écrasement

⚠️ Les caractères suivants sont interdits dans les phrases : `"  '  \  {  }  ```

---

## Usage 4 : Supprimer une phrase

1. Cliquer sur l'onglet **✏️ Éditeur**
2. Cliquer sur la ligne à supprimer dans la liste (les champs se remplissent automatiquement)
3. Cliquer sur **Supprimer**
4. Confirmer la suppression

---

## Usage 5 : Créer un groupe (paragraphe type)

Un groupe permet de regrouper plusieurs codes sous un seul nom.

Pour créer un groupe, ouvrir le fichier `dictionary.py` avec le Bloc-notes et ajouter une ligne comme :

```
"INTRO": ["ID6", "ID7", "EG1", "EG2"],
```

Ensuite, taper simplement `INTRO` dans le générateur pour obtenir les 4 phrases d'un coup.

---

## En cas de problème

- **L'outil ne se lance pas** → Vérifier que Python est installé (taper `python --version` dans l'invite de commandes)
- **"Module not found"** → Double-cliquer sur `installer.bat`
- **Un code affiche "[Code inconnu]"** → Vérifier l'orthographe du code dans l'onglet Dictionnaire
