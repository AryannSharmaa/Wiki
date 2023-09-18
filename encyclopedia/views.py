from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponse,HttpResponseRedirect

from . import util
from random import choice


def convert_md(title):
    content=util.get_entry(title)
    md=Markdown()
    if content ==None:
        return None
    else:
        return md.convert(content)


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def search(request):
    if request.method=="POST":
        search=request.POST['q']
        html=convert_md(search)
        if html!=None:
            return render(request,"encyclopedia/entry.html",{
            "title":search,
            "content":html
        })
            
        
        else:
            all_entries=util.list_entries()
            recom=[]
            for entry in all_entries:
                if search.lower() in entry.lower():
                    recom.append(entry)
            if len(recom)!=0:
                return render(request,"encyclopedia/search.html",{
                    "recom":recom            
                }) 
            else:
                return render(request,"encyclopedia/error.html",{
            "message":"This entry doesn't exist."
        })

        

def entry(request,title):
    content=convert_md(title)
    if content==None:
        return render(request,"encyclopedia/error.html",{
            "message":"This entry doesn't exist."
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":content
        })



def new_page(request):
    
    if request.method=="POST":
        title=request.POST['title']
        content=request.POST["content"]
        title_exist=util.get_entry(title)
        if title_exist:
            return render(request,"encyclopedia/error.html",{
                "message":"Title already exist"
            })
        else:

            util.save_entry(title,content)
            return entry(request,title)
    return render(request,"encyclopedia/new.html")



def edit(request):
    if request.method=="POST":
        title=request.POST['title']
        content=util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title":title,
            "content":content
        })

def save(request):
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]
        util.save_entry(title,content)
        return entry(request,title)
    

def random(request):
    all_entries=util.list_entries()
    
    ran=choice(all_entries)

    
    return entry(request,ran)
