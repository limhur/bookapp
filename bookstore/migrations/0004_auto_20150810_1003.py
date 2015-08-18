# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_auto_20150810_0840'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pricerange',
            new_name='Author',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='pricerange',
            new_name='author',
        ),
    ]
