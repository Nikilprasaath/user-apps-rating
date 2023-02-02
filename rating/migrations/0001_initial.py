# Generated by Django 4.1.5 on 2023-01-30 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='app',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=20)),
                ('app_link', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=20)),
                ('subcategory', models.CharField(max_length=20)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(null=True)),
                ('apps', models.ManyToManyField(to='rating.app')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(upload_to='scrn')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], max_length=20)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rating.app')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
