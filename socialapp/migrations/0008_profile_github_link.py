# Generated by Django 4.1.4 on 2023-12-28 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0007_rename_homepage_link_profile_website_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]