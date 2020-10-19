from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect , HttpResponse
import random

markdowner = Markdown()



class NewPage(forms.Form):
    pageTitle = forms.CharField(label = "Name")
    markdownText = forms.CharField(label = "Markdown text", widget = forms.Textarea)

    def clean_pageTitle(self, *args, **kwargs):
        title = self.cleaned_data.get("pageTitle")
        allTitles = util.list_entries()
        for t in allTitles:
            if t.lower() == title.lower():
                raise forms.ValidationError("a page with this name already exists")
            else:
                return title

class editPage(forms.Form):

    mdcontent = forms.CharField(label = "", widget = forms.Textarea , initial="Error loading content")
    
    def __init__(self,*args,**kwargs):
        getContent = kwargs.pop('content')
        super(editPage, self).__init__(*args, **kwargs)
        self.fields['mdcontent'].initial = getContent
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):

    isThereEntry = util.get_entry(name)

    if isThereEntry == None:
        return render(request , "encyclopedia/error.html")
    else:
        ent = markdowner.convert(isThereEntry)
        return render(request , "encyclopedia/entry.html", {"entry":ent , "title":name})

def search(request):
    SearchField = request.GET.get('q')
    result = util.get_entry(SearchField)
    if result == None:
        filteredList = util.list_entries()
        filterResults = [s for s in filteredList if SearchField.casefold() in s.casefold()]
        return render(request, "encyclopedia/search.html", {"entries": filterResults})
    else:
        ent = markdowner.convert(util.get_entry(SearchField))
        return render(request , "encyclopedia/entry.html", {"entry":ent , "title":SearchField})
        
def newPage(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pageTitle"]
            mdText = form.cleaned_data["markdownText"]
            util.save_entry(title , mdText)
            return render(request , "encyclopedia/entry.html", {"entry": markdowner.convert(mdText) , "title":title})
        else:
            return render(request,"encyclopedia/new_page.html", {"form": form})

    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPage()
        })    
    

def randomPage(request):
    randomPage = random.choice(util.list_entries())
    ent = markdowner.convert(util.get_entry(randomPage))
    return render(request , "encyclopedia/entry.html", {"entry":ent , "title":randomPage})

def edit(request,name):
    if request.method == "POST":
        form = editPage(request.POST,content="nnn")
        if form.is_valid():
            content = form.cleaned_data["mdcontent"]
            util.save_entry(name,content)
            contentHTML = markdowner.convert(content)
            return render(request , "encyclopedia/entry.html", {"entry": contentHTML , "title":name})
    else:
        return render(request, "encyclopedia/edit.html" , {"form":editPage(content=util.get_entry(name)) , "title":name})
