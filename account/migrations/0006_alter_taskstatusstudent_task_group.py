# Generated by Django 4.2.3 on 2023-08-03 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_studentcv_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstatusstudent',
            name='task_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.taskstudent', verbose_name='Задача студента'),
        ),
    ]
