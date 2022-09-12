# Docso renderer

import markdown,yaml
import codecs,os,re
import shutil

SIDEE={}
styPATH=__file__[:-9]+"themes\\"
HTMLsc="<link rel='stylesheet' href='%s' /><script src='js/scrolling.js'></script><article class='main-post'><h1 class='title-name'>%s</h1>%s<title>%s</title>%s</article><script>document.getElementsByClassName('main-post')[0].style.left=document.getElementById('sidebar-nav').clientWidth;document.getElementsByClassName('main-post')[0].style.width=document.body.clientWidth-42-document.getElementById('sidebar-nav').clientWidth;</script>"
with open(__file__[:-17]+"__config__.yml","r",encoding="utf-8") as f:
    global CONF
    CONF=yaml.safe_load(f)
with open(__file__[:-17]+"docs\\sidebar.yml","r",encoding="utf-8") as fi:
    global SIDE
    SIDE=yaml.safe_load(fi)
print(SIDE)
STYLE=CONF["theme"]
SCROLLTIME=CONF["scrolltime"]
TITLE=CONF["title"]

if not os.path.isdir(__file__[:-17]+"public"):
    os.system("mkdir "+__file__[:-17]+"public")

titlist={}
_titlist={}

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
    #print(murs)
    st[-1]=st[-1].replace("_"," ")
    et[-1]=et[-1].replace("_"," ")
    RTVAL=markdown.markdown(rr)
    titlist[st[-1].title()]=os.path.splitext(r)[0]+".html"
    #RTVAL=RTVAL.replace("\n","<br>\n")
    ##print(RTVAL)
    
    RTVAL=HTMLsc%(STYLE+'.css',st[-1].title(),'',et[-1],RTVAL)
        #f"<div id='{i}'>"+i+"</div>"
        ##print([i.strip()],end='\n')
    RTVAL="</aside>"+RTVAL
    _murs=list(murs)
    _murs.sort(reverse=True)
    #print(_murs,murs)
    for iii in _murs:
        #print(RTVAL.find(ii.strip()))
        RTVAL=RTVAL.replace(iii.strip(),f"<div id='{iii.strip().replace(' ','_')}'>"+iii+"</div>")   
    murs.reverse()
    for i,j in SIDEE.items():
        if type(j)==str:
            ww,rr=os.path.split(j)
            if rr==r:
                for ii in murs:
                    
                    RTVAL=f"&nbsp&nbsp&nbsp&nbsp- <a href=\"#{ii.strip().replace(' ','_')}\" class='linkr'>{ii.strip().title()}</a><br>"+RTVAL                
                RTVAL=f" <a class='linkr homepage' href='{os.path.splitext(rr)[0]+'.html'}'><b>{i.strip()}</b></a><br>"+RTVAL   
            else:
                RTVAL=f" <a class='linkr homepage' href='{os.path.splitext(rr)[0]+'.html'}'><b>{i.strip()}</b></a><br>"+RTVAL         
        elif type(j)==dict:
            for k,m in j.items():
                ww,rr=os.path.split(m)
                if rr==r:
                    for ii in murs:
                        
                        RTVAL=f"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp- <a href=\"#{ii.strip().replace(' ','_')}\" class='sub'>{ii.strip().title()}</a><br>"+RTVAL                
                    RTVAL=f"&nbsp&nbsp&nbsp&nbsp <a class='reg' href='{os.path.splitext(rr)[0]+'.html'}'><b>{k.strip()}</b></a><br>"+RTVAL    
                else:
                    RTVAL=f"&nbsp&nbsp&nbsp&nbsp <a class='linkr' href='{os.path.splitext(rr)[0]+'.html'}'>{k.strip()}</a><br>"+RTVAL            
            RTVAL=f" <a class='linkr homepage' href='#'><b>{i.strip()}</b></a><br>"+RTVAL    

    RTVAL=f"<link rel='stylesheet' href='{STYLE+'.css'}'/><aside id='sidebar-nav'>"+RTVAL
    ##print(RTVAL,RTVAL.find("hello"))
    #print(RTVAL)
    f=codecs.open(__file__[:-17]+"public\\"+os.path.splitext(r)[0]+".html",mode="w+",encoding="utf-8",errors="xmlcharrefreplace")
    f.write(RTVAL)
    f.close()

def init():
    global titlist,_titlist
    RTVAL=""
    
    stname=CONF["sitename"]
    sub=CONF["subtitle"]
    ##print(stname)
    
    fname=__file__[:-17]+"docs\\index.md"
    f=codecs.open(fname,mode="r",encoding="utf-8")
    _rr=f.read()
    f.close() 
    
        
    rr=_rr
    
    RTVAL=markdown.markdown(rr)
    #RTVAL=RTVA#printlace("\n","<br>\n")
    ###print(RTVAL)
    if sub!="":
        RTVAL=HTMLsc%(STYLE+'.css',stname,f"<h2 class='subtitle-top'>{sub}</h2>",'',RTVAL)
    else:
        RTVAL=HTMLsc%(STYLE+'.css',stname,"",'',RTVAL)
    RTVAL="</aside>"+RTVAL
    titr=list(titlist.keys())
    titv=list(titlist.values())
    titv.reverse()
    titr.reverse()
    _titlist=dict(zip(titr,titv))
    titr=list(SIDE.keys())
    titv=list(SIDE.values())
    titv.reverse()
    titr.reverse()
    global SIDEE
    SIDEE=dict(zip(titr,titv))    
    for i,j in SIDEE.items():
        if type(j)==str:
            ww,rr=os.path.split(j)
            RTVAL=f" <a class='linkr homepage' href='{os.path.splitext(rr)[0]+'.html'}'><b>{i.strip()}</b></a><br>"+RTVAL
        elif type(j)==dict:
            for k,m in j.items():
                ww,rr=os.path.split(m)          
                RTVAL=f"&nbsp&nbsp&nbsp&nbsp <a class='linkr' href='{os.path.splitext(rr)[0]+'.html'}'>{k.strip()}</a><br>"+RTVAL            
            RTVAL=f" <a class='linkr homepage' href='#'><b>{i.strip()}</b></a><br>"+RTVAL
    RTVAL=f"<link rel='stylesheet' href='{STYLE+'.css'}'/><aside id='sidebar-nav'>"+RTVAL
    ###print(RTVAL,RTVAL.find("hello"))
    w,r=os.path.split(fname)
    f=codecs.open(__file__[:-17]+"public\\"+os.path.splitext(r)[0]+".html",mode="w+",encoding="utf-8",errors="xmlcharrefreplace")
    f.write(RTVAL)
    
    f.close()

def main():
    import glob
    
    try:
        flist=glob.glob(__file__[:-17]+"docs/*.*")
        shutil.copyfile(styPATH+STYLE+'.css',__file__[:-17]+"public\\"+STYLE+'.css')
    except:
        print("DOCSY: Docs folder does not exist!")
        return 0
    try:
        shutil.rmtree(__file__[:-17]+"public\\js\\")
    except:
        print("DOCSY: Clearing js folder")
    try:
        shutil.copytree(__file__[:-9]+"js\\",__file__[:-17]+"public\\js\\")
    except:
        print("DOCSY: Tryed to create public/js, but it already exists!")
    try:
        for i in flist:
            temp,j=os.path.split(i)
            ##print(os.path.splitext(j)[1])
            if os.path.splitext(j)[1]!=".md" and os.path.splitext(j)[1]!=".html" and os.path.splitext(j)[1]!=".yml":
                shutil.copyfile(i,__file__[:-17]+"public\\"+j)
            elif os.path.splitext(j)[1]!=".yml":
                openf(i)
        init()
        ##print(_titlist)
        for i in flist:
            temp,j=os.path.split(i)
            ##print(os.path.splitext(j)[1])
            if os.path.splitext(j)[1]!=".md" and os.path.splitext(j)[1]!=".html" and os.path.splitext(j)[1]!=".yml":
                shutil.copyfile(i,__file__[:-17]+"public\\"+j)
            elif os.path.splitext(j)[1]!=".yml":
                openf(i)
        ##print(titlist)
        init()
    except Exception as e:
        print("DOCSY: Unknown error ",e)

main()