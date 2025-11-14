# Generated migration for hierarchical categories/collections

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_product_new_arrival_and_more'),
    ]

    operations = [
        # Remove unique constraint on name
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        # Add slug field
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, blank=True, default=''),
            preserve_default=False,
        ),
        # Add parent field for hierarchies
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                help_text='Parent category (for sub-collections)',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='subcategories',
                to='api.category'
            ),
        ),
        # Add is_collection field
        migrations.AddField(
            model_name='category',
            name='is_collection',
            field=models.BooleanField(default=False, help_text='Mark as top-level collection'),
        ),
        # Add display_order field
        migrations.AddField(
            model_name='category',
            name='display_order',
            field=models.IntegerField(default=0, help_text='Order in which to display (lower numbers first)'),
        ),
        # Update Meta options
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['display_order', 'name'], 'verbose_name_plural': 'categories'},
        ),
        # Add unique together constraint
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'name')},
        ),
    ]
