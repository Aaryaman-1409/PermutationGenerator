# Generated by Django 4.0.2 on 2022-02-09 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0005_alter_answersmodel_orderanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersmodel',
            name='orderAnswer',
            field=models.IntegerField(verbose_name=''),
        ),
    ]
