# Generated by Django 4.2 on 2023-05-23 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_tweet_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='parent',
        ),
    ]
