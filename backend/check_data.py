#!/usr/bin/env python
import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'big_model_app.settings')
django.setup()

# 导入模型
from data_center.models import Dataset, KnowledgeBase
from training_center.models import Model, TrainingJob, DockerImage
from app_center.models import Application, Plugin
from evaluation_center.models import EvaluationTask, EvaluationReport, ModelComparison

def check_data():
    print("=== 数据库数据检查 ===")
    
    print("\n1. 数据集 (Dataset):")
    datasets = Dataset.objects.all()
    print(f"   总数: {datasets.count()}")
    for dataset in datasets[:5]:  # 显示前5个
        print(f"   - {dataset.id}: {dataset.name}")
    
    print("\n2. 知识库 (KnowledgeBase):")
    knowledge_bases = KnowledgeBase.objects.all()
    print(f"   总数: {knowledge_bases.count()}")
    for kb in knowledge_bases[:5]:
        print(f"   - {kb.id}: {kb.name}")
    
    print("\n3. 模型 (Model):")
    models = Model.objects.all()
    print(f"   总数: {models.count()}")
    for model in models[:5]:
        print(f"   - {model.id}: {model.name} (状态: {model.status})")
    
    print("\n4. 训练任务 (TrainingJob):")
    jobs = TrainingJob.objects.all()
    print(f"   总数: {jobs.count()}")
    for job in jobs[:5]:
        print(f"   - {job.id}: {job.model.name if job.model else 'N/A'} (状态: {job.status})")
    
    print("\n5. Docker镜像 (DockerImage):")
    images = DockerImage.objects.all()
    print(f"   总数: {images.count()}")
    for image in images[:5]:
        print(f"   - {image.id}: {image.name}:{image.tag}")
    
    print("\n6. 应用 (Application):")
    applications = Application.objects.all()
    print(f"   总数: {applications.count()}")
    for app in applications[:5]:
        print(f"   - {app.id}: {app.name} (状态: {app.status})")
    
    print("\n7. 插件 (Plugin):")
    plugins = Plugin.objects.all()
    print(f"   总数: {plugins.count()}")
    for plugin in plugins[:5]:
        print(f"   - {plugin.id}: {plugin.name} v{plugin.version}")
    
    print("\n8. 评测任务 (EvaluationTask):")
    eval_tasks = EvaluationTask.objects.all()
    print(f"   总数: {eval_tasks.count()}")
    for task in eval_tasks[:5]:
        print(f"   - {task.id}: {task.name} (状态: {task.status})")
    
    print("\n9. 评测报告 (EvaluationReport):")
    reports = EvaluationReport.objects.all()
    print(f"   总数: {reports.count()}")
    for report in reports[:5]:
        print(f"   - {report.id}: {report.name}")
    
    print("\n10. 模型比较 (ModelComparison):")
    comparisons = ModelComparison.objects.all()
    print(f"   总数: {comparisons.count()}")
    for comp in comparisons[:5]:
        print(f"   - {comp.id}: {comp.name}")

if __name__ == '__main__':
    check_data() 