# Generated by Django 3.2 on 2021-05-25 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_alter_vacsine_additional_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childvaccine',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.child'),
        ),
    ]
