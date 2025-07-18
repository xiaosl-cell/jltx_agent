from agent.menus.menu_item_base import MenuItemBase
from agent.tasks.daily_task import DailyTask


class DailyMenu(MenuItemBase):
    def __init__(self):
        super().__init__('日常任务', '每日常规任务', 'task')
        self.task = DailyTask()

    def display_submenu(self):
        """显示子菜单的方法，子类应该重写这个方法"""
        return None

    def execute(self):
        """执行退出系统任务"""
        self.task.execute()
