# Generated by Django 5.0.6 on 2024-06-06 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_imagewithtext_slide_delete_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImageWithText',
        ),
        migrations.DeleteModel(
            name='Slide',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='product',
            name='technologies',
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='products/'),
        ),
    ]