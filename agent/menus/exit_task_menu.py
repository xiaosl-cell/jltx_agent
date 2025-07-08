from agent.tasks.exit_task import ExitTask
from agent.menus.menu_item_base import MenuItemBase

class ExitTaskMenu(MenuItemBase):
    """退出系统任务"""

    def __init__(self):
        super().__init__("退出系统", "退出游戏Agent系统", "task")
        self.task = ExitTask()

    def display_submenu(self):
        """显示子菜单的方法，子类应该重写这个方法"""
        return None

    def execute(self):
        """执行退出系统任务"""
        print("退出游戏Agent系统")
        self.task.execute()