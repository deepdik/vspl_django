# Generated by Django 2.1.5 on 2019-02-10 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vasudhaBooking', '0004_auto_20190210_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTotalPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField()),
                ('sell', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='vasudhaBooking.SellDemand')),
            ],
            options={
                'verbose_name_plural': 'Product List Details',
            },
        ),
        migrations.RenameModel(
            old_name='ProductList',
            new_name='ProductListDetail',
        ),
        migrations.AlterModelOptions(
            name='productlistdetail',
            options={'verbose_name_plural': 'Product List Details'},
        ),
    ]