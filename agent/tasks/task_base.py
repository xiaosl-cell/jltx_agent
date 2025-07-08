class TaskBase:
    """任务基类，所有具体任务都应该继承这个类"""
    
    def __init__(self, name, description):
        self.name = name
        self.type = "base"
        self.description = description
    
    def execute(self):
        """执行任务的方法，子类应该重写这个方法"""
        raise NotImplementedError("子类必须实现execute方法")
    
    def pre_execute(self):
        """任务执行前的准备工作"""
        print(f"准备执行任务: {self.name}")
    
    def post_execute(self):
        """任务执行后的清理工作"""
        print(f"任务 {self.name} 执行完成")