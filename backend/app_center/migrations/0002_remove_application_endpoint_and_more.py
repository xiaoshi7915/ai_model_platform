# Generated by Django 4.2.7 on 2025-04-20 01:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('training_center', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_center', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='endpoint',
        ),
        migrations.RemoveField(
            model_name='application',
            name='resource_usage',
        ),
        migrations.AddField(
            model_name='application',
            name='api_endpoint',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='API端点'),
        ),
        migrations.AddField(
            model_name='application',
            name='plugins',
            field=models.ManyToManyField(blank=True, related_name='applications', to='app_center.plugin', verbose_name='插件'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='entry_point',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='入口点'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='status',
            field=models.CharField(choices=[('active', '激活'), ('inactive', '未激活'), ('deprecated', '已弃用')], default='active', max_length=20, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='application',
            name='config',
            field=models.JSONField(blank=True, default=dict, verbose_name='配置信息'),
        ),
        migrations.AlterField(
            model_name='application',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_applications', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='application',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='training_center.model', verbose_name='模型'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('created', '已创建'), ('running', '运行中'), ('stopped', '已停止'), ('error', '错误')], default='created', max_length=20, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_plugins', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='version',
            field=models.CharField(max_length=20, verbose_name='版本号'),
        ),
        migrations.CreateModel(
            name='ApplicationMetric',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cpu_usage', models.FloatField(default=0.0, verbose_name='CPU使用率')),
                ('memory_usage', models.FloatField(default=0.0, verbose_name='内存使用率')),
                ('total_requests', models.IntegerField(default=0, verbose_name='总请求数')),
                ('avg_response_time', models.FloatField(default=0.0, verbose_name='平均响应时间')),
                ('error_rate', models.FloatField(default=0.0, verbose_name='错误率')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='时间戳')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='app_center.application', verbose_name='应用')),
            ],
            options={
                'verbose_name': '应用指标',
                'verbose_name_plural': '应用指标',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ApplicationLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.CharField(choices=[('debug', 'DEBUG'), ('info', 'INFO'), ('warning', 'WARNING'), ('error', 'ERROR'), ('critical', 'CRITICAL')], default='info', max_length=10, verbose_name='日志级别')),
                ('message', models.TextField(verbose_name='日志信息')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='时间戳')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='app_center.application', verbose_name='应用')),
            ],
            options={
                'verbose_name': '应用日志',
                'verbose_name_plural': '应用日志',
                'ordering': ['-timestamp'],
            },
        ),
    ]
