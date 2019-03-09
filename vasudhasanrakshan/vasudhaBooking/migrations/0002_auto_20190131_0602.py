# Generated by Django 2.1.5 on 2019-01-31 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vasudhaBooking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratebycity',
            name='ratelist',
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Rate List'},
        ),
        migrations.AlterModelOptions(
            name='homepageimage',
            options={'verbose_name_plural': 'Home Page Image'},
        ),
        migrations.AddField(
            model_name='ratelist',
            name='product_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ratelist',
            name='rate',
            field=models.PositiveIntegerField(default=1, help_text='rate of product per kg'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RateByCity',
        ),
    ]
