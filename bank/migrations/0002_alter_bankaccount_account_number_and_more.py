# Generated by Django 4.1.2 on 2022-10-20 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='account_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='card_number',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='iin',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=500)),
                ('data_time', models.DateTimeField()),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.bankaccount')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
