# Transcripteur Audio Français Ultra-léger

Ce logiciel permet de transcrire des fichiers audio (mp3, wav, m4a) en français en utilisant le modèle `LeBenchmark/wav2vec2-FR-7k-large`. Il est optimisé pour tourner sur CPU et utilise le découpage par morceaux (chunking) pour économiser la RAM.

## Prérequis

Pour lire les fichiers compressés (MP3, M4A), ce logiciel s'appuie sur FFmpeg. Si vous rencontrez une erreur lors de l'ouverture d'un fichier audio, assurez-vous que FFmpeg est installé sur votre système et ajouté à votre PATH.

## Installation des dépendances

Si la commande `pip` n'est pas reconnue, utilisez `python -m pip` :

```bash
python -m pip install -r requirements.txt
```

## Utilisation

Lancez l'application avec :
```bash
python main.py
```

## Création de l'exécutable (.exe)

Pour transformer ce script en un seul fichier exécutable pour Windows, utilisez la commande suivante. Si `pyinstaller` n'est pas reconnu directement, utilisez `python -m PyInstaller` :

```bash
python -m PyInstaller --onefile --windowed --name "TranscripteurFR" --collect-all customtkinter --collect-all transformers --collect-all torch main.py
```

*Note : L'utilisation de `--collect-all` est nécessaire pour s'assurer que toutes les données des bibliothèques (modèles, thèmes GUI) sont incluses dans l'exécutable.*

## Résolution des problèmes courants (Windows)

### Erreur : "Le terme 'pip' n'est pas reconnu"
Cela signifie que Python n'est pas dans votre PATH Windows. Vous pouvez :
1. Utiliser `python -m pip` au lieu de `pip`.
2. Réinstaller Python en cochant la case **"Add Python to PATH"**.

### Erreur lors du lancement de `main.py`
Assurez-vous d'avoir bien installé toutes les dépendances. Si une erreur persiste, vérifiez que votre version de Python est 3.8 ou plus.

## Fonctionnalités
- Sélection de fichiers audio (mp3, wav, m4a).
- Transcription optimisée pour le français via LeBenchmark.
- Barre de progression en temps réel.
- Zone de texte pour copier le résultat.
- Fonctionnement 100% local sur CPU pour la confidentialité et la portabilité.
