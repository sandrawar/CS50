from django.shortcuts import render

from . import util
from django import forms

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    display = util.get_entry(entry)
    if display == None:
        return ("Error")
    return render(request, "encyclopedia/entry.html", {
        "entry": display
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if util.get_entry(form[title]) != None:
            return ("Error")
        util.save_entry(form["title"], form["content"])
    else:
        form = CreateForm()
        return render(request, "encyclopedia/create.html", {
            "form": form
            })

def search(request):
    display = util.get_entry(form.request.POST["p"])
    if display == None:
        return ("Error")
    return render(request, "encyclopedia/entry.html", {
        "entry": display
    })
    

