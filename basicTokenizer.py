#!/usr/bin/env python
# coding: utf-8

# In[43]:


import io

class BasicTokenizer:
    def __init__(self):
        self.merges= {}
        self.vocab = {}
        v = 0 
        while v <= 255:
            self.vocab[v] = bytes([v])
            v +=1

    def get_stats(self, tokens):
        mydict = {}
        for i in range(len(tokens) - 1) :
            currentTuple = (tokens[i], tokens[i + 1])
            if currentTuple in mydict :
                mydict[currentTuple] += 1
            else :
                mydict[currentTuple] = 1
        return mydict

    def merge(self, tokens, top_pair, new_id):
        new_tokens=[]
        t=0
        while t < len(tokens):
            if t < len(tokens) -1 and tokens[t] == top_pair[0] and tokens[t + 1] == top_pair[1]:
                    new_tokens.append(new_id)
                    t += 2
            else:
                new_tokens.append(tokens[t])
                t += 1
        return new_tokens

    def train(self, text, vocab_size):
        tokens = list(text.encode("utf-8"))
        num_merges = vocab_size - 256
        i = 0
        while i <= num_merges :
            mydict = self.get_stats(tokens)
            if not mydict: break
            top_pair = max(mydict, key=mydict.get)
            new_id = 256 + i 

            self.merges[top_pair] = new_id
            self.vocab[new_id] = self.vocab[top_pair[0]] + self.vocab[top_pair[1]]
            tokens = self.merge(tokens, top_pair, new_id)
            i += 1
        return tokens

    def encode(self, text):
        tokens = list(text.encode("utf-8"))
        while len(tokens) >=2:
            stats = self.get_stats(tokens)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            tokens = self.merge(tokens, pair, idx)
        return tokens


    def decode(self, ids):
        b_parts = []
        for i in range(len(ids)) :
            b_parts.append(self.vocab[ids[i]])

        full_bytes = b"".join(b_parts)
        return full_bytes.decode("utf-8", errors="replace")

    def load(self):
        with open('example.txt', 'r', encoding='utf-8') as f:
            rawText = f.read()
        return __str__.rawText

if __name__ == "__main__":
    tokenizer = BasicTokenizer()
    rawText = tokenizer.load()
    tokenizer.train(rawText, 276)
    
    #encode & decode
    tokens = tokenizer.encode(rawText)
    print("Tokens compressés :", tokens[:10])
    
    texte_reconstruit = tokenizer.decode(tokens)
    print("Succès ?", rawText == texte_reconstruit)


# In[ ]:




