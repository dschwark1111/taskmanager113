# Generated by Django 4.2.5 on 2023-09-30 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_auto_20230927_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='issues.status'),
            preserve_default=False,
        ),
    ]
