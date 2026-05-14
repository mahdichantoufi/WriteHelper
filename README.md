# WriteHelper - Outil de rédaction médico-légale

## Utilisation

1. Double-cliquer sur `writehelper.py`
2. Entrer les codes séparés par des tirets (ex: `ID6-ID7-F1-TC4-ITT3-C1`)
3. Le texte est copié dans le presse-papier et sauvegardé dans un fichier horodaté

## Modifier le dictionnaire

[📝 Ouvrir le dictionnaire dans le Bloc-notes](dictionary.py)

Ou directement via l'Explorateur Windows : clic droit sur `dictionary.py` → Ouvrir avec → Bloc-notes

Format des entrées :
```
"CODE": "Phrase associée",
```

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

## Prérequis

```
pip install pyperclip
```
