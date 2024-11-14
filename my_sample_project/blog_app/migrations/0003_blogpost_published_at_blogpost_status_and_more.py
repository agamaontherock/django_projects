# Generated by Django 5.1.1 on 2024-11-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_blogpost_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(unique_for_date='created_at'),
        ),
    ]
