# Generated by Django 3.0.3 on 2020-05-22 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200518_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='kakao_id',
            field=models.IntegerField(max_length=250, null=True),
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, null=True)),
                ('is_default', models.BooleanField(null=True, verbose_name=False)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'db_table': 'shipping_addresses',
            },
        ),
    ]
