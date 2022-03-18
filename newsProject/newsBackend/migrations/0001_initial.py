# Generated by Django 4.0.3 on 2022-03-18 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sourceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.SlugField(unique=True)),
                ('source_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NewsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('news_url', models.URLField()),
                ('img_url', models.URLField()),
                ('publishedAt', models.DateTimeField(blank=True, null=True)),
                ('content', models.TextField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsBackend.sourcemodel')),
            ],
        ),
    ]
