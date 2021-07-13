# PyTrie
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


# Comamndline example
## Search
```
python pytrie.py search -d dict.txt -q ตัวแปล
```
Should produce
```
search
query 'ตัวแปล' || closest 'ตัวแปร', distance 1
```

## Approximate search
```
python pytrie.py approx_search -d dict.txt -q ตัวแปล
```
Should produce
```
approx_search
query 'ตัวแปล' || closest 'ตัวแปร', distance 1
```

## Spell correction
```
python pytrie.py spell -d dict -q การปับฅ่าตัสแปฮ
```
Should produce
```
spell
การปรับค่าตัวแปร
```

We can also insert word segmentation separator, for example '|' by
```
python pytrie.py spell -d dict -q การปับฅ่าตัสแปฮ --sep '|'
```
Should produce
```
spell
การ|ปรับ|ค่า|ตัวแปร
```



# Contributor
- [https://github.com/peune](Sanparith Marukatat)
