# Generated by Django 3.1.7 on 2021-05-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210516_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, '1 - Very bad'), (2, '2 - Bad'), (3, '3 - Okay'), (4, '4 - Great'), (5, '5 - Excellent')], default=4),
        ),
    ]