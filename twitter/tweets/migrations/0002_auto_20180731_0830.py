# Generated by Django 2.0.7 on 2018-07-31 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['created']},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='tag',
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default='old', max_length=30, unique=True, verbose_name='tag name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tweet',
            name='tags',
            field=models.ManyToManyField(related_name='associated_tweets', to='tweets.Tag', verbose_name='list of tags'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tweets', to=settings.AUTH_USER_MODEL, verbose_name='creator of tweet'),
        ),
    ]