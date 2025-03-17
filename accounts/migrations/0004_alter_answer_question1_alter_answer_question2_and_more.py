# Generated by Django 5.1.6 on 2025-03-16 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_reviewee_name_answer_reviewer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question1',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (None, 'わからない')]),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question2',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (None, 'わからない')]),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question3',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (None, 'わからない')], null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='reviewee_role',
            field=models.CharField(choices=[('general', '一般'), ('manager', 'マネージャー'), ('leader', 'リーダー')], max_length=10),
        ),
    ]
