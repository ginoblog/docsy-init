# Docso renderer

import markdown,yaml
import codecs,os,re
import shutil

styPATH=__file__[:-9]+"themes\\"
HTMLsc="<link rel='stylesheet' href='%s' /><script src='js/scrolling.js'></script><div class='main-post'><h1 class='title-name'>%s</h1>%s<title>%s</title>%s</div>"
with open(__file__[:-17]+"__config__.yml","r",encoding="utf-8") as f:
    global CONF
    CONF=yaml.safe_load(f)

STYLE=CONF["theme"]
SCROLLTIME=CONF["scrolltime"]
    
if not os.path.isdir(__file__[:-17]+"public"):
    os.system("mkdir "+__file__[:-17]+"public")

titlist={}

def openf(fname):
    
    w,r=os.path.split(fname)
    
    if r=="index.md":
        titlist["Home"]="index.html"
        return 0
    
    f=codecs.open(fname,mode="r",encoding="utf-8")
    _rr=f.read()
    f.close()
    
    st=re.findall("<!--\s*title:\s*([ \S]+)\s*-->",_rr)
    
    if st==[]:
        st=["Post"]
    
    et=re.findall("<!--\s*name:\s*([ \S]+)\s*-->",_rr)
    if et==[]:
        et=["Post"]  
        
    rr=_rr
    murs=re.findall("<!--\s*menu\s*-->\s*#*\s*([ \S]*)\s*\n",_rr)
    
    st[-1]=st[-1].replace("_"," ")
    et[-1]=et[-1].replace("_"," ")
    RTVAL=markdown.markdown(rr)
    titlist[st[-1].title()]=os.path.splitext(r)[0]+".html"
    #RTVAL=RTVAL.replace("\n","<br>\n")
    #print(RTVAL)
    
    RTVAL=HTMLsc%(STYLE+'.css',st[-1].title(),'',et[-1],RTVAL)
    for i in murs:
        RTVAL=RTVAL.replace(i.strip(),f"<div id='{i.strip()}'>"+i+"</div>")
        #f"<div id='{i}'>"+i+"</div>"
        #print([i.strip()],end='\n')
    RTVAL="</div>"+RTVAL
    for i in murs:
        RTVAL=f"- <a href=\"#{i.strip()}\">{i.strip()}</a><br>"+RTVAL
    RTVAL="<div id='sidebar-nav'>"+RTVAL
    #print(RTVAL,RTVAL.find("hello"))
    f=codecs.open(__file__[:-17]+"public\\"+os.path.splitext(r)[0]+".html",mode="w+",encoding="utf-8",errors="xmlcharrefreplace")
    f.write(RTVAL)
    f.close()

def init():
    RTVAL=""
    
    stname=CONF["sitename"]
    sub=CONF["subtitle"]
    #print(stname)
    
    fname=__file__[:-17]+"docs\\index.md"
    f=codecs.open(fname,mode="r",encoding="utf-8")
    _rr=f.read()
    f.close() 
    
        
    rr=_rr
    
    RTVAL=markdown.markdown(rr)
    #RTVAL=RTVAL.replace("\n","<br>\n")
    #print(RTVAL)
    if sub!="":
        RTVAL=HTMLsc%(STYLE+'.css',stname,f"<h2 class='subtitle-top'>{sub}</h2>",'',RTVAL)
    else:
        RTVAL=HTMLsc%(STYLE+'.css',stname,"",'',RTVAL)
    RTVAL="</div>"+RTVAL
    titr=list(titlist.keys())
    titv=list(titlist.values())
    titv.reverse()
    titr.reverse()
    _titlist=dict(zip(titr,titv))
    for i,j in _titlist.items():
        RTVAL=f"- <a href='{j.strip()}'>{i.strip()}</a><br>"+RTVAL
    RTVAL="<div id='sidebar-nav'>"+RTVAL
    #print(RTVAL,RTVAL.find("hello"))
    w,r=os.path.split(fname)
    f=codecs.open(__file__[:-17]+"public\\"+os.path.splitext(r)[0]+".html",mode="w+",encoding="utf-8",errors="xmlcharrefreplace")
    f.write(RTVAL)
    f.close()
    
import glob

flist=glob.glob(__file__[:-17]+"docs/*.*")
shutil.copyfile(styPATH+STYLE+'.css',__file__[:-17]+"public\\"+STYLE+'.css')
try:
    shutil.rmtree(__file__[:-17]+"public\\js\\")
except:
    pass
try:
    shutil.copytree(__file__[:-9]+"js\\",__file__[:-17]+"public\\js\\")
except:
    pass
for i in flist:
    temp,j=os.path.split(i)
    print(os.path.splitext(j)[1])
    if os.path.splitext(j)[1]!=".md" and os.path.splitext(j)[1]!=".html" and os.path.splitext(j)[1]!=".yml":
        shutil.copyfile(i,__file__[:-17]+"public\\"+j)
    elif os.path.splitext(j)[1]!=".yml":
        openf(i)
print(titlist)
init()
    