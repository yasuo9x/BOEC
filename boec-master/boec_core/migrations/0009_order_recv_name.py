# Generated by Django 3.1.7 on 2021-06-02 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boec_core', '0008_auto_20210602_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='recv_name',
            field=models.CharField(blank=True, db_column='rcv_name', max_length=255, null=True),
        ),
    ]
