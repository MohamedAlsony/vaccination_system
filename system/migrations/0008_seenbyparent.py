# Generated by Django 3.2 on 2021-05-27 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_alter_vaccine_child_age_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeenByParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.parent')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.vaccine')),
            ],
        ),
    ]
