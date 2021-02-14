# Generated by Django 3.1.6 on 2021-02-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(verbose_name='details')),
                ('inputs', models.TextField(verbose_name='inputs')),
                ('output', models.TextField(verbose_name='output')),
            ],
        ),
    ]