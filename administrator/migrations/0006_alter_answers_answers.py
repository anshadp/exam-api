# Generated by Django 4.2.4 on 2023-09-09 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_alter_answers_is_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='answers',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
