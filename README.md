# Transcripteur Audio Français Ultra-léger

Ce logiciel permet de transcrire des fichiers audio (mp3, wav, m4a) en français en utilisant le modèle `LeBenchmark/wav2vec2-FR-7k-large`. Il est optimisé pour tourner sur CPU et utilise le découpage par morceaux (chunking) pour économiser la RAM.

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

Lancez l'application avec :
```bash
python main.py
```

## Création de l'exécutable (.exe)

Pour transformer ce script en un seul fichier exécutable pour Windows, utilisez la commande suivante après avoir installé `pyinstaller` :

```bash
pyinstaller --onefile --windowed --name "TranscripteurFR" --collect-all customtkinter --collect-all transformers --collect-all torch main.py
```

*Note : L'utilisation de `--collect-all` peut être nécessaire pour s'assurer que toutes les données des bibliothèques (modèles, thèmes GUI) sont incluses.*

## Fonctionnalités
- Sélection de fichiers audio.
- Transcription optimisée pour le français.
- Barre de progression en temps réel.
- Zone de texte pour copier le résultat.
- Fonctionnement 100% local sur CPU.
