from django.apps import AppConfig

class BigModelAppConfig(AppConfig):
    name = 'big_model_app'
    verbose_name = "大型模型构建管理平台"
    
    def ready(self):
        """
        当Django应用准备就绪时执行的函数
        用于初始化应用和执行启动任务
        """
        # 导入UUID修复函数
        from utils.uuid_helper import auto_fix_uuids
        
        # 自动修复UUID格式问题
        auto_fix_uuids()
        
        print("BigModelApp 应用初始化完成！") 