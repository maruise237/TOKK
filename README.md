# Transcripteur Audio Français Ultra-léger

Ce logiciel permet de transcrire des fichiers audio (mp3, wav, m4a) en français en utilisant le modèle `LeBenchmark/wav2vec2-FR-7k-large`. Il est optimisé pour tourner sur CPU et utilise le découpage par morceaux (chunking) pour économiser la RAM.

## Prérequis

Pour lire les fichiers compressés (MP3, M4A), ce logiciel s'appuie sur FFmpeg. Si vous rencontrez une erreur lors de l'ouverture d'un fichier audio, assurez-vous que FFmpeg est installé sur votre système et ajouté à votre PATH.

## Installation des dépendances

Si la commande `pip` ou `python` n'est pas reconnue, essayez d'utiliser le lanceur Windows `py` :

```bash
py -m pip install -r requirements.txt
```

Si `pip` n'est pas installé du tout, vous pouvez l'installer avec :
```bash
py -m ensurepip --default-pip
```

## Utilisation

Lancez l'application avec :
```bash
py main.py
```

## Création de l'exécutable (.exe)

Pour transformer ce script en un seul fichier exécutable pour Windows, utilisez la commande suivante :

```bash
py -m PyInstaller --onefile --windowed --name "TranscripteurFR" --collect-all customtkinter --collect-all transformers --collect-all torch main.py
```

*Note : L'utilisation de `--collect-all` est nécessaire pour s'assurer que toutes les données des bibliothèques (modèles, thèmes GUI) sont incluses dans l'exécutable.*

## Résolution des problèmes courants (Windows)

### Erreur : "Le terme 'pip' n'est pas reconnu"
Cela signifie que Python n'est pas dans votre PATH Windows ou que pip n'est pas installé.
1. Essayez d'utiliser `py -m pip` au lieu de `pip`.
2. Si cela échoue, réparez votre installation de Python ou installez pip avec `py -m ensurepip`.

### Erreur lors du lancement de `main.py`
Assurez-vous d'avoir bien installé toutes les dépendances. Si une erreur persiste, vérifiez que votre version de Python est 3.8 ou plus.

## Fonctionnalités
- Sélection de fichiers audio (mp3, wav, m4a).
- Transcription optimisée pour le français via LeBenchmark.
- Barre de progression en temps réel.
- Zone de texte pour copier le résultat.
- Fonctionnement 100% local sur CPU pour la confidentialité et la portabilité.
