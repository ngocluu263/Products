# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_txt', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'created_at')),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'created_at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'modified_at')),
                ('likes', models.ManyToManyField(to='product.Like', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('comment', models.ForeignKey(to='product.Comments')),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(to='product.User'),
        ),
        migrations.AddField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(to='product.Product'),
        ),
    ]
