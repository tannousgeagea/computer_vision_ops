# Generated by Django 4.2 on 2024-06-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='annotated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='mode',
            field=models.CharField(default='N/A', max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
