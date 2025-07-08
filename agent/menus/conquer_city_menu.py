from agent.menus.menu_item_base import MenuItemBase
from agent.tasks.conquer_city_task import ConquerCityTask

class ConquerCityMenu(MenuItemBase):
    def __init__(self):
        super().__init__("攻城掠地", "执行工程掠地", "task")
        self.task = ConquerCityTask()
        
    def display_submenu(self):
        """显示子菜单的方法，子类应该重写这个方法"""
        return None

    def execute(self):
        """执行退出系统任务"""
        self.task.execute()