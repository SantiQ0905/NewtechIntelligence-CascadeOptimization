# Generated by Django 5.1.1 on 2024-09-15 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_alter_task_description_alter_task_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='register_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
