from django.contrib import messages
from django.shortcuts import render
from . import permClasses as pc
from .models import SetSize, Answers, StorePermutation


def home(request):
    if request.method == 'POST':
        if 'generate' in request.POST:
            form = SetSize(request.POST)
            form1 = Answers()
            if form.is_valid():
                return on_valid(request, form, form1)

        else:
            form = SetSize()
            form1 = Answers(request.POST)
            two_line_dict = {int(k): v for k, v in StorePermutation.objects.first().permutation.items()}
            twoLineObj = pc.TwoLine(len(two_line_dict), two_line_dict)

            if form1.is_valid():
                return on_valid(request, form, form1, twoLineObj)

            else:
                messages.error(request, 'Invalid Cycle Notation. Try again', extra_tags='cyclic')
                return render(request, 'qna/home.html',
                              {'form': form, 'form1': form1, 'twoline': twoLineObj.to_latex()})

    form = SetSize()
    return render(request, 'qna/home.html', {'form': form, 'form1': None, 'twoline': None})


def help_page(request):
    return render(request, 'qna/help.html')


################ Helper Functions ####################

def on_valid(request, form, form1, twoLineObj=None):
    if 'generate' in request.POST:
        size = form.cleaned_data['size']
        twoLineObj = pc.TwoLine(int(size))
        StorePermutation.objects.all().delete()
        obj = StorePermutation()
        obj.permutation = twoLineObj.permutation
        obj.save()
        return render(request, 'qna/home.html',
                      {'form': form, 'form1': form1, 'twoline': twoLineObj.to_latex()})

    else:
        solution_objs = [pc.Order(twoLineObj.permutation, form1.cleaned_data['orderAnswer']),
                         pc.Sign(twoLineObj.permutation, form1.cleaned_data['signAnswer']),
                         pc.Cyclic(twoLineObj.permutation, form1.cleaned_data['cyclicAnswer'])]

        for objs in solution_objs:
            objs.check_answer(request)

        return render(request, 'qna/home.html',
                      {'form': form, 'form1': form1, 'twoline': twoLineObj.to_latex()})
