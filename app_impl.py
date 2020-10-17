import inspect
import sqlite3
from collections import namedtuple
from operator import attrgetter, itemgetter
from pprint import pprint
import re
Cache={}
class DB_item():
    SQL = []
    def __init__(self,sql,chk,ix=-1,cols=None):
        self.chk=chk
        if ix ==0 :
            self.SQL.insert(0,self)
        else:
            self.SQL.append(self)
        self.sql=sql
        self.args=re.findall("#\w+",sql)
        self.cols=cols
    @property
    def ix(self):
        return self.SQL.index(self)
    def __int__(self):
       return self.ix
    def __index__(self):
       return self.ix
    def exec(self,vals):
        sql=self.sql
        for a in self.args:
            sql = sql.replace("#"+a, vals.get(a))
        sql=sql.strip()
        db = sqlite3.connect("./surah.sqlite")
        c = db.cursor()
        c.execute(sql)
        if not self.cols:
            self.cols=[column[0] for column in c.description]
        res = c.fetchall()

        allres = []
        for row in res:
            d = {}
            for i, c in enumerate(self.cols):
                d[c] = row[i]
            allres.append(d)
        c.close()
        return allres



def do_search(txt):
    db = sqlite3.connect("./surah.sqlite")
    c = db.cursor()
    c.execute("select * from surah where \"text\" LIKE '%"+str(txt) +"%'")
    res=c.fetchall()
    allres=[]
    for row in res:
        allres.append({"surah":row[0],"section":row[1],"text":row[2]})
    c.close()
    return allres
def get_categories():
    allres=Cache.get("categories")
    if allres is None:
        db = sqlite3.connect("./surah.sqlite")

        allres=[]
        c = db.cursor()
        c.execute("select * from sections")
        res=c.fetchall()
        for row in res:
            allres.append({"surah":row[0],"label":row[1]})
        Cache["categories"]=allres
        c.close()
    return allres
def get_surah_in_categorie(surah):
    allres=Cache.get("categories_"+str(surah))
    if allres is None:
        db = sqlite3.connect("./surah.sqlite")

        c = db.cursor()
        c.execute("select * from surah where surah="+str(surah))
        res=c.fetchall()
        allres=[]
        for row in res:
            allres.append({"surah":row[0],"section":row[1],"text":row[2]})
        Cache["categories_"+str(surah)]=allres
        c.close()

    return allres
#pprint(get_surah_in_categorie( 1))


"""
rom nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sent = "This is a sample sentence, showing off the stop words filtration."
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(example_sent)

filtered_sentence = [w for w in word_tokens if not w in stop_words]
print(filtered_sentence)
"""