# Docso renderer

import markdown,yaml
import codecs,os,re
import shutil,json

with open(__file__[:-17]+"__config__.yml","r",encoding="utf-8") as f:
    global CONF
    CONF=yaml.safe_load(f)

searchdb={}    

def openf(fname):
    w,r=os.path.split(fname)
    
    f=codecs.open(fname,mode="r",encoding="utf-8")
    _rr=f.read()
    f.close()
    
    st=re.findall("<!--\s*title:\s*([ \S]+)\s*-->",_rr)
    if r=="index.md":
        st=[CONF["sitename"]+": "+CONF["subtitle"]]
    
    elif st==[]:
        st=["Post"]
    
    
    st[-1]=st[-1].replace("_"," ")
    
    searchdb[st[-1]]={}
    searchdb[st[-1]]["val"]=_rr
    searchdb[st[-1]]["title"]=st[-1]
    
    


import glob

flist=glob.glob(__file__[:-17]+"_docs/*.*")


for i in flist:
    temp,j=os.path.split(i)
    print(os.path.splitext(j)[1])
    if os.path.splitext(j)[1]!=".yml":
        openf(i)

strr=json.dumps(searchdb)
with open(__file__[:-17]+"public/search.json","w+") as rp:
    rp.write(strr)
