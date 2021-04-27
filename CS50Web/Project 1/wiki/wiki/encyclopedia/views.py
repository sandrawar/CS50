import markdown2
from django.shortcuts import redirect
from django.shortcuts import render

from . import util
from django import forms
from random import randrange

class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, widget=forms.HiddenInput())
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    display = util.get_entry(entry)
    if display == None:
        raise Http404("Entry with this title does not exist.")
    htmlDisplay = markdown2.markdown(display)
    return render(request, "encyclopedia/entry.html", {
        "entry": htmlDisplay,
        "title": entry
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) != None: 
                raise Http404("Entry with this title does not exist.")
            util.save_entry(title, content)
            return redirect('entry', entry = title)

    else:
        form = CreateForm()
        return render(request, "encyclopedia/create.html", {
            "form": form
            })

def search(request):
    form = request.POST
    display = util.get_entry(form["p"])
    if display == None:
        query = set()
        for entry in util.list_entries():
            if form["p"] in entry:
                query.add(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": query
    })
    return redirect('entry', entry = form["p"])
    
def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) == None: 
                raise Http404("Entry with that title does not exist.")
            util.save_entry(title, content)
            return redirect('entry', entry=entry)

    else:
        data = util.get_entry(entry)
        if data == None:
            raise Http404("Entry with this title does not exist.") 
        form = EditForm({
            "title": entry,
            "content": data
        })
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": entry
            })
   
def random(request):
    entryList = util.list_entries()
    title = entryList[randrange(len(entryList))]
    if util.get_entry(title) == None:
        raise Http404("Entry with this title does not exist.")
    return redirect('entry', entry = title)