# Generated by Django 2.2 on 2020-03-31 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('url', models.TextField()),
                ('rating', models.DecimalField(decimal_places=5, max_digits=10)),
            ],
        ),
    ]
