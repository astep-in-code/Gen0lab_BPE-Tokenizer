# Gen0lab - BPE Tokenizer From Scratch

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ce dépôt contient une implémentation éducative du tokenizer **Byte Pair Encoding (BPE)**, développée pas à pas pour démystifier la manière dont les Large Language Models (LLMs) traitent le texte. 

> Ce projet accompagne mon article détaillé sur la tokenisation à retrouver sur [Gen0lab.com](https://gen0lab.com).

## Pourquoi ce projet ?

L'objectif ici était de reconstruire l'algorithme de tokenisation utilisé par GPT-4 en partant d'une page blanche, afin de comprendre :
1. Pourquoi les modèles ne lisent pas des lettres mais des **IDs**.
2. Comment la compression BPE optimise la **fenêtre de contexte**.
3. L'importance de la **priorité chronologique** des fusions lors de l'encodage.

## Crédits & César

Ce travail est une implémentation personnelle fortement inspirée par le cours "Let's build the GPT Tokenizer" d'**Andrej Karpathy** et son dépôt [minbpe](https://github.com/karpathy/minbpe). Ce repo documente mon propre cheminement technique et les ajustements logiques nécessaires pour aboutir à un système fonctionnel.

## Fonctionnalités

### Step 1 : BasicTokenizer (Terminé)
* **Entraînement** : Identification des paires d'octets les plus fréquentes et création de règles de fusion.
* **Encodage** : Transformation d'un texte brut en IDs en respectant la hiérarchie des fusions apprises.
* **Décodage** : Reconstruction fidèle du texte original via une Lookup Table (LUT) d'octets.
* **Sans perte** : Garantie que `decode(encode(text)) == text`.

### Step 2 : RegexTokenizer (En cours)
* Intégration du pattern Regex officiel de GPT-4.
* Prévention des fusions illogiques (ex: ne pas fusionner une lettre et un signe de ponctuation).