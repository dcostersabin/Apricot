# Generated by Django 3.1.5 on 2021-02-04 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('submission', '0001_initial'),
        ('benchmark', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchmark',
            name='submission_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.submission', verbose_name='submission_id'),
        ),
    ]
