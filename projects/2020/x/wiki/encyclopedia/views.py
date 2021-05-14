from django.shortcuts import render
from django.http import HttpResponseRedirect
import random
from django.urls import reverse

from . import util
from .forms import EntryForm, Query

    
def index(request):
    form = Query(request.POST or None)
    
    context={
        "entries": util.list_entries(),
        "form":form
    }
    #query the database for entries with title posted
    if form.is_valid():
        title = form.cleaned_data.get("title")
        Title = title.capitalize()
        titlE = title.upper()
        
        Result = util.get_entry(Title)
        result = util.get_entry(title)
        resulT = util.get_entry(titlE)
        if result:
            return render(request,"encyclopedia/wiki.html", {
            "title":Title,
            "entry":result,
        })
        if Result:
            return render(request,"encyclopedia/wiki.html", {
            "title":Title,
            "entry":Result,
        })
        if resulT:
            return render(request,"encyclopedia/wiki.html", {
            "title":titlE,
            "entry":resulT,
        })  
        else:
            list=[]
            entries = util.list_entries()
            for entry in entries:
                if title.upper() in entry.upper():
                    list.append(entry)
            
            return render(request, "encyclopedia/index.html", {
	            "entries": list,
	            "title":title
            })
               
    return render(request, "encyclopedia/index.html", context)

    

def create(request):
    #add form            
    form2 = EntryForm(request.POST or None)
    
    context={
        "form2":form2
    }
    
    #save form and call save_entry function
    if form2.is_valid():
        instance = form2.save(commit = False)
       
        Title = instance.title.capitalize()
        title = instance.title
        titlE = instance.title.upper()
        
        #check is entry already exist
        entry = util.get_entry(title)
        Entry = util.get_entry(Title)
        entrY = util.get_entry(titlE)
                
        print(entry)
        if entry or Entry or entrY:
            return HttpResponseRedirect(reverse("wiki",args=(title,)))
            
        else:
            instance.save()
            util.save_entry(title, instance.text)
            return HttpResponseRedirect(reverse("wiki",args=(title,)))
        
    
    return render(request, "encyclopedia/createpage.html", context)

def wiki(request, title):
    Title = title.capitalize()
    titlE = title.upper()

    Entry = util.get_entry(Title)
    entrY = util.get_entry(titlE)
    entry = util.get_entry(title)
    
    if entry:
        return render(request,"encyclopedia/wiki.html", {
        "title":title,
        "entry":entry,
    })
    if Entry:
        return render(request,"encyclopedia/wiki.html", {
        "title":title,
        "entry":Entry,
    }) 
    if entrY:
        return render(request,"encyclopedia/wiki.html", {
        "title":titlE,
        "entry":entrY,
    })    
    if not (entry or Entry or entrY):
        return render(request, "encyclopedia/pagenotfound.html", {
            "title": Title,
        })
      
def edit(request, title): 
    form2 = EntryForm(request.POST or None)
    if request.method == "POST":
        instance = form2.save(commit = False)
        instance.save() 
        
        util.save_entry(title, instance.text)
        return HttpResponseRedirect(reverse("wiki", args=(title,)))
    
    else:
        entry = util.get_entry(title)
        
        if entry:
            form2.fields["title"].initial=title
            form2.fields["text"].initial=entry
            return render(request,"encyclopedia/edit.html", {
            "title":title,
            "form2": form2,
        })
 

def randompage(request):
    entries = util.list_entries()
    entry=random.choice(entries)
    return HttpResponseRedirect(reverse("wiki", args=(entry,)))
    