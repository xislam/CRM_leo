# Generated by Django 4.2.3 on 2023-07-31 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_student_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название группы')),
                ('students', models.ManyToManyField(blank=True, to='account.student', verbose_name='Студенты')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
    ]
