# Generated by Django 4.1.5 on 2023-01-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], default='pending', max_length=20),
        ),
    ]
