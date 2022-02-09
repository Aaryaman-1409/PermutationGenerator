from django.db import models
from django.forms import ModelForm
import django
import re


class StorePermutation(models.Model):
    permutation = models.JSONField('Two Line Dict', primary_key=True)


class SetSizeModel(models.Model):
    size_options = [
        ('2', "2"),
        ('3', "3"),
        ('4', "4"),
        ('5', "5"),
        ('6', "6"),
        ('7', "7"),
        ('8', "8"),
        ('9', "9"),
        ('10', "10"),
        ('11', "11"),
        ('12', "12")
    ]
    size = models.CharField(max_length=2, choices=size_options)


class AnswersModel(models.Model):
    orderAnswer = models.IntegerField('')
    signAnswer = models.IntegerField('')
    cyclicAnswer = models.CharField('', max_length=50)


class SetSize(ModelForm):
    class Meta:
        model = SetSizeModel
        fields = ['size']


class Answers(ModelForm):
    class Meta:
        model = AnswersModel
        fields = ['orderAnswer', 'signAnswer', 'cyclicAnswer']

    def clean(self):
        cleaned_data = self.cleaned_data
        cyclicAnswer = cleaned_data['cyclicAnswer']
        cyclicAnswer = cyclicAnswer.strip()
        separate = re.findall(r'[(]\d+[)]', cyclicAnswer)
        s = ''
        cyclic_list = []
        for x in separate:
            s += x
            cyclic_list.append(str(re.sub("[()]", '', x)))
        if s != cyclicAnswer:
            raise django.forms.ValidationError("Invalid Cycle Notation")

        self.cleaned_data['cyclicAnswer'] = cyclic_list

        return self.cleaned_data

