from agent.tasks.task_base import TaskBase
from common.utils import exit_program

class ExitTask(TaskBase):
    """退出系统任务"""

    def __init__(self):
        super().__init__("退出系统", "退出游戏Agent系统")

    def execute(self):
        """执行退出系统任务"""
        print("退出游戏Agent系统")
        exit_program()