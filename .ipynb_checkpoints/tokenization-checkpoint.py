#!/usr/bin/env python
# coding: utf-8

# TODO next step
# 
# ### 1. Initialisation
# * **Liste de travail** : `tokens` = mon texte converti en liste d'octets (0-255).
# * **Cible** : `nb_fusions` = (Taille vocabulaire visée) - 256.
# * **Registre** : `merges = {}` (Dictionnaire pour stocker : `(id1, id2): nouvel_id`).
# 
# ---
# 
# ### 2. BOUCLE PRINCIPALE : L'Entraînement
# *Répéter `nb_fusions` fois (pour créer les tokens de 256 à X) :*
# 
# #### A. BOUCLE DE COMPTAGE (Fréquences)
# * Parcourir la liste `tokens` de l'indice `0` à `len(tokens) - 1`.
# * Pour chaque paire adjacente `(tokens[i], tokens[i+1])` :
#     * L'ajouter ou l'incrémenter dans un dictionnaire de statistiques.
# * **Fin de boucle** : Identifier la paire la plus fréquente (la "gagnante").
# 
# #### B. ENREGISTREMENT
# * Créer un `nouvel_id` (256, puis 257, etc.).
# * Enregistrer dans `merges` : `gagnante -> nouvel_id`.
# 
# #### C. BOUCLE DE FUSION (Remplacement)
# * Créer une `nouvelle_liste` vide.
# * Parcourir la liste `tokens` actuelle :
#     * **SI** l'élément actuel et le suivant forment la paire gagnante :
#         * Ajouter `nouvel_id` à `nouvelle_liste`.
#         * Sauter l'élément suivant (avancer de 2 rangs).
#     * **SINON** :
#         * Ajouter l'élément actuel à `nouvelle_liste`.
#         * Avancer de 1 rang.
# * **Mise à jour** : `tokens = nouvelle_liste` (la liste est maintenant plus courte).
# 
# ---
# 
# ### 3. Résultat final
# * `tokens` : Le texte compressé.
# * `merges` : Le dictionnaire de règles permettant d'encoder/décoder.

# In[ ]:


import io

with open('example.txt', 'r', encoding='utf-8') as f:
    rawText = f.read()

ByteText = rawText.encode("utf-8", "replace")
raw_tokens = ByteText


# In[ ]:


DictSize = 280
def encode(tokens) :
    merges = {}
    vocab = {}
    v = 0 
    while v < 255:
        vocab[v] = bytes(v)
        v +=1

    d = 0
    while d <= (DictSize - 256) :
        d += 1
        mydict = {}
        for i in range(len(tokens) - 1) :
            currentTuple = (tokens[i], tokens[i + 1])
            if currentTuple in mydict :
                mydict[currentTuple] += 1
            else :
                mydict[currentTuple] = 1
        if not mydict:
            break
        top_pair = max(mydict, key=mydict.get)
        merges[top_pair] = 255 + d
        new_tokens = list()
        t = 0
        while t < len(tokens) - 1:
            if t < len(tokens) -1 and tokens[t] == top_pair[0] and tokens[t + 1] == top_pair[1]:
                    new_tokens.append(merges[top_pair])
                    vocab[255 + d] = vocab[top_pair[0]] + vocab[top_pair[1]] 
                    t += 2
            else:
                new_tokens.append(tokens[t])

            t += 1
        tokens = new_tokens
    #print(vocab)
    return tokens, vocab


returnedtokens = encode(raw_tokens)
bpe_tokens = returnedtokens[0]
vocab = returnedtokens[1]

print(bpe_tokens[0])


# # Plan d'Action : Décodage BPE
# 
# L'objectif est de transformer notre liste de `tokens` compressés (ex: `[77, 259, ...]`) en texte lisible, en utilisant le dictionnaire `merges` que nous avons construit à l'entraînement.
# 
# ## 1. Reconstruction du Vocabulaire (`vocab`)
# Le dictionnaire `merges` contient les règles de fusion, mais pour décoder, nous avons besoin d'un dictionnaire qui associe chaque **ID** à sa séquence d'**octets** d'origine.
# 
# * **Initialisation** : Créer un dictionnaire `vocab` contenant les 256 octets de base.
#     * *Clé* : l'entier (0 à 255).
#     * *Valeur* : l'octet correspondant (ex: `bytes([i])`).
# * **Expansion** : Parcourir le dictionnaire `merges` dans l'ordre d'insertion.
#     * Pour chaque paire `(p1, p2)` associée à un nouvel ID `v` :
#     * `vocab[v] = vocab[p1] + vocab[p2]` (on concatène les deux séquences d'octets).
# 
# ## 2. Traduction des Tokens
# Une fois le `vocab` complet, le décodage devient une simple lecture.
# 
# 1.  Créer une liste vide `b_parts`.
# 2.  Parcourir chaque `idx` de la liste `tokens` compressée.
# 3.  Récupérer la séquence d'octets correspondante : `vocab[idx]`.
# 4.  L'ajouter à `b_parts`.
# 
# ## 3. Recomposition Finale
# 1.  Fusionner toutes les séquences d'octets de `b_parts` en un seul objet `bytes` (utiliser `b"".join()`).
# 2.  Décoder cet objet en chaîne de caractères UTF-8.
#     * Utiliser `.decode("utf-8", errors="replace")` pour éviter les crashs si une séquence est mal formée.

# In[44]:


def decode(tokens, vocab) :
    b_parts = []
    for i in range(len(tokens)) :
        b_parts.append(vocab[tokens[i]])

    full_bytes = b"".join(b_parts)
    return full_bytes.decode("utf-8", errors="replace")

print(decode(bpe_tokens, vocab))



# In[ ]:




