# Generated by Django 3.2.5 on 2021-08-14 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_pose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
