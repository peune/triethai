# TrieThai
Trie for storing dictionary with search, approximate search, and spell correction functions. 
Designed for Thai language, in mind, but should be pretty generic for other languages :)

ทรัยสำหรับเก็บรายการคำศัพท์ พร้อมกับฟังก์ชันในการ ค้นคืน, ค้นคืน _โดยประมาณ_, การแก้การสะกดผิด

# Descriptions
Search returns the closest word in the dictionary, with respect to edit distance to the input query string.
If the query exists in the dictionary, the same string will be returned.
Approximate search also perform the same function but with heuristic that tries to reduce the memory during runtime.
This should make it faster for large dictionary.

Spell correction perform simultanously correction & word segmentation.
If there are no spelling error, it returns similar result as _maximal matching_ word segmentation.

# Usage
We need to load dictionary first into list of strings and Trie.
```
words,root = load_dictionary(dictionary_filename)
```

Then we may choose which operation to perform 
### Search
```
idx, score = nn_search(root, query)
print('query \'%s\' || closest \'%s\', distance %.2f' % (query, words[idx], score))
```

### Approximate search
```
idx, score = approx_nn_search(root, query, 3)
print('query \'%s\' || closest \'%s\', distance %.2f' % (query, words[idx], score))
```

### Spelling correction
```
res = spell_correction(words, root, beam, transit_cost, separator, query)
print(res)
```


# Comamnd line example
## Search
```
python triethai.py search -d dict.txt -q ตัวแปล
```
Should produce
```
search
query 'ตัวแปล' || closest 'ตัวแปร', distance 1
```

## Approximate search
```
python triethai.py approx_search -d dict.txt -q ตัวแปล
```
Should produce
```
approx_search
query 'ตัวแปล' || closest 'ตัวแปร', distance 1
```

## Spell correction
```
python triethai.py spell -d dict -q การปับฅ่าตัสแปฮ
```
Should produce
```
spell
การปรับค่าตัวแปร
```

We can also insert word segmentation separator, for example '|' by
```
python triethai.py spell -d dict -q การปับฅ่าตัสแปฮ --sep '|'
```
Should produce
```
spell
การ|ปรับ|ค่า|ตัวแปร
```



# Contributor
- [Sanparith Marukatat](https://github.com/peune)
