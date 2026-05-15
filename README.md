# WriteHelper - Outil de rédaction médico-légale

## Prérequis

- Python 3.x → https://www.python.org/downloads/ (cocher "Add to PATH")
- `pip install pyperclip`

Ou lancer `installer.bat`.

## Notice utilisateur

[Guide pas-à-pas pour les utilisateurs](./NOTICE_UTILISATEUR.md)

## Fichiers

| Fichier | Rôle |
|---------|------|
| `gui.py` | Interface graphique (point d'entrée) |
| `dictionary.py` | Dictionnaire des codes et phrases |
| `installer.bat` | Installe les dépendances |
| `NOTICE_UTILISATEUR.md` | Guide pas-à-pas pour les utilisateurs |

## Architecture

- `dictionary.py` expose un dict `PHRASES` : clé = code, valeur = phrase (str) ou groupe (list de codes)
- `gui.py` : 3 onglets tkinter (consultation, édition, génération avec prévisualisation)

## Codes disponibles

| Préfixe | Catégorie |
|---------|-----------|
| ID | Identité et contexte |
| F | Faits déclarés |
| EG | État général |
| TC | Tête et cou |
| MS | Membres supérieurs |
| TR | Tronc |
| MI | Membres inférieurs |
| L | Description des lésions |
| PSY | Retentissement psychologique |
| EC | Examens complémentaires |
| ITT | Incapacité totale de travail |
| C | Conclusions |
| VS | Violences sexuelles |
| ENF | Enfants / mineurs |
| ML | Formules médico-légales |

## Groupes

Un code peut référencer une liste de sous-codes (paragraphe) :
```python
"INTRO": ["ID6", "ID7", "EG1", "EG2"],
```
