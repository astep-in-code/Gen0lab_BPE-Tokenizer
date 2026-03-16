#!/usr/bin/env python
# coding: utf-8

# In[67]:


import regex as re
from basicTokenizer import BasicTokenizer

class RegexTokenizer(BasicTokenizer):
    def __init__(self):
        super().__init__()
        self.pattern = r"""(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
        self.compiled_pattern = re.compile(self.pattern)

    def train(self, text, vocab_size):
        # 1. Découper le texte en morceaux (chunks)
        chunked_text = self.compiled_pattern.findall(text)
        # 2. Transformer chaque morceau en liste d'octets (liste de listes)
        token_list = []
        for chunk in chunked_text:
            bytes_list = chunk.encode("utf-8")
            token_list.append(list(bytes_list))
        # 3. Boucle de fusion (num_merges) :
        num_merges = vocab_size - 256
        i = 0
        while i <= num_merges:
            dict_stats = {}
            for token in token_list:
                stats = super().get_stats(token)
                for stat in stats:
                    if stat in dict_stats:
                        dict_stats[stat] += stats[stat]
                    else :
                        dict_stats[stat] = stats[stat]

            if not dict_stats:
                break    
            top_pair = max(dict_stats, key=dict_stats.get)
            new_id = 256 + i 

            self.merges[top_pair] = new_id
            self.vocab[new_id] = self.vocab[top_pair[0]] + self.vocab[top_pair[1]]
            for idx in range(len(token_list)) :
                acutal_chunk = token_list[idx]
                new_chunk = self.merge(acutal_chunk, top_pair, new_id)
                token_list[idx] = new_chunk

            i += 1

        return token_list

    def encode(self, text):
        chunked_text = self.compiled_pattern.findall(text)
        token_list = []
        for chunk in chunked_text:
            bytes_list = chunk.encode("utf-8")
            token_list.append(list(bytes_list))

        for pair, new_id in self.merges.items():
            for idx in range(len(token_list)):
                chunk = token_list[idx]
                token_list[idx] = self.merge(chunk, pair, new_id)

        final_tokens = []
        for chunk in token_list:
            final_tokens.extend(chunk)

        return final_tokens

    def decode(self, ids):
        parts = []
        for idx in ids:
            if idx in self.vocab:
                parts.append(self.vocab[idx])

        text_bytes = b"".join(parts)
        return text_bytes.decode("utf-8", errors="replace")


# In[68]:


# Test
if __name__ == "__main__":
    tokenizer = RegexTokenizer()
    rawText = tokenizer.load()
    tokenizer.train(rawText, 276)

    #encode & decode
    tokens = tokenizer.encode(rawText)
    print("Tokens compressés :", tokens[:10])

    texte_reconstruit = tokenizer.decode(tokens)
    print("Succès ?", rawText == texte_reconstruit)



# In[ ]:




