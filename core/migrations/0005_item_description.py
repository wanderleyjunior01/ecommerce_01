# Generated by Django 2.2.13 on 2021-07-20 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]