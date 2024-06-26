# Generated by Django 5.0.4 on 2024-05-29 01:37

import file.validations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0007_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='file/documents/', validators=[file.validations.document_file_validation]),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
