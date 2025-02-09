# Generated by Django 4.2 on 2024-09-23 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='カテゴリ')),
            ],
            options={
                'verbose_name_plural': 'カテゴリ',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='タグ')),
            ],
            options={
                'verbose_name_plural': 'タグ',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='タイトル')),
                ('url', models.URLField(verbose_name='URL')),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('favicon_url', models.URLField(blank=True, max_length=255, null=True)),
                ('og_title', models.CharField(blank=True, max_length=200, null=True)),
                ('og_description', models.TextField(blank=True, null=True)),
                ('og_image', models.URLField(blank=True, max_length=255, null=True)),
                ('og_type', models.CharField(blank=True, max_length=50, null=True)),
                ('og_site_name', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bookmark.category', verbose_name='カテゴリ')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='bookmark.tag', verbose_name='タグ')),
            ],
            options={
                'verbose_name_plural': 'アイテム',
            },
        ),
    ]
