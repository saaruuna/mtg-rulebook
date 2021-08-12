from django.shortcuts import render, redirect
import urllib.request
from .models import Section
from django.db.models import Q

def homeView(request):
    url = 'https://media.wizards.com/2021/downloads/MagicCompRules%2020210419.txt'
    sections = Section.objects.all()

    if not sections.exists():
        create_db(url)

    chapters = Section.objects.filter(is_chapter=True)
    rules = Section.objects.filter(is_rule=True)

    return render(request, 'rules/index.html', {'chapters':chapters, 'rules': rules})

def chapterView(request, sectionid):
    chapter = Section.objects.get(pk=sectionid)

    rules = Section.objects.filter(Q(is_rule=True), Q(address__istartswith=str(chapter.address)))
    chapters = Section.objects.filter(is_chapter=True)

    return render(request, 'rules/chapter.html', {'chapters':chapters, 'rules': rules, 'chapter': chapter})

def searchView(request):
    keyword = request.GET.get('search')
    if len(keyword) == 0:
        return redirect('/')
    rules = Section.objects.filter(Q(content__icontains=keyword), Q(is_rule=True))
    chapters = Section.objects.filter(is_chapter=True)

    return render(request, 'rules/search.html', {'chapters':chapters, 'rules': rules, 'keyword':keyword})

def create_db(url):
    contents = urllib.request.urlopen(url).read()
    results = contents.splitlines( )

    for result in results:
        line = result.decode('utf8')
        if len(line) > 3 and line[0].isdigit() and line[3]=='.':
            rule = line.split(" ", 1)
            if len(rule[0]) == 4:
                Section.objects.get_or_create(address=rule[0], content=rule[1], is_chapter=True, is_rule=False)
            if len(rule[0]) > 4:
                Section.objects.get_or_create(address=rule[0], content=rule[1], is_chapter=False, is_rule=True)
