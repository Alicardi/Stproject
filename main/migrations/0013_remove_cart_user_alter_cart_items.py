# Generated by Django 5.0.6 on 2024-06-12 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_cart_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(related_name='items', to='main.cartitem'),
        ),
    ]
