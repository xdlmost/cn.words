import json
# -*- coding: utf-8 -*- 

word_dict=[]
level_1_3500={}
#with open("word.json","r",encoding='utf-8') as f:
#    word_dict = json.load(f)

index=10000
with open("1.csv","r",encoding='utf-8') as f:
    for  line in  f.readlines():
        level_1_3500[line]=index
        index+=1

index=1
fre={}
with open("fre.csv","r",encoding='utf-8') as f:
    for  line in  f.readlines():
        fre[line]=index
        index+=1

for f in fre:
    if f in level_1_3500:
        level_1_3500[f]=fre[f]

sortedWordsTemp=[]
for w in level_1_3500:
    sortedWordsTemp.append({
        'index':level_1_3500[w],
        'word':w
    })

sortedWords=sorted(sortedWordsTemp, key=lambda record: record['index'])

sql=""" INSERT INTO words.word (id,word,pinyin,`level`) VALUES \n"""

for i in sortedWords:
    a=False
    for w in load_dict:
        if (i==w['word']):
            level=(index%10)+1
            sql+="(%d,\"%s\",\"%s\",%d)\n,"%(indexs[level],w['word'],w['pinyin'],level)
            indexs[level]+=1
            index+=1
            a=True
            break
    if not a :
        print ("(%d,%s,%d)\n,"%(index,i,level))
        print (i)


with open("word.sql","w",encoding='utf-8') as f:
    f.write(sql)