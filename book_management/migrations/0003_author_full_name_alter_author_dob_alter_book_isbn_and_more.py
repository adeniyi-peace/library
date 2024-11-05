# Generated by Django 5.0.8 on 2024-10-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_management', '0002_alter_book_isbn_alter_book_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='DOB',
            field=models.DateField(max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='ISBN',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateField(max_length=50, null=True),
        ),
    ]