# Generated by Django 3.2.4 on 2021-12-22 14:35

from django.db import migrations, models
import django.db.models.deletion
import system.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('date_of_birth', models.DateField()),
                ('nationalid', models.CharField(default='', max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('password', models.CharField(default='', max_length=50)),
                ('nationalid', models.CharField(default='', max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('vaccine_for', models.CharField(blank=True, default='', max_length=100)),
                ('child_age_from', system.models.IntegerRangeField()),
                ('child_age_to', system.models.IntegerRangeField()),
                ('additional_information', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='SeenByParent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.parent')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.vaccine')),
            ],
        ),
        migrations.CreateModel(
            name='ChildVaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.child')),
                ('vaccine', models.ManyToManyField(blank=True, to='system.Vaccine')),
            ],
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.parent'),
        ),
    ]
