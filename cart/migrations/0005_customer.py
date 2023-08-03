# Generated by Django 4.2 on 2023-07-31 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_orderproduct_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('country', models.CharField(choices=[('us', 'United States'), ('uk', 'United Kingdom'), ('ger', 'Germany'), ('fra', 'France'), ('ind', 'India'), ('aus', 'Australia'), ('bra', 'Brazil'), ('cana', 'Canada')], max_length=50)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
    ]
