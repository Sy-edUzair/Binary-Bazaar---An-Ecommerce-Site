# Generated by Django 5.0.1 on 2024-08-20 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_rating_alter_review_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.AlterField(
            model_name='vendor',
            name='v_rating',
            field=models.IntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')], default=1),
        ),
    ]
