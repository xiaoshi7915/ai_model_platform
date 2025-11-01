# Generated manually on 2025-11-01 to add missing fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_center', '0002_remove_application_endpoint_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='endpoint',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='应用端点'),
        ),
        migrations.AddField(
            model_name='application',
            name='resource_usage',
            field=models.JSONField(blank=True, default=dict, verbose_name='资源使用情况'),
        ),
    ]
