class MenuItemBase:
    """菜单项基类，所有菜单项（子菜单或任务）都应该继承这个类"""
    
    def __init__(self, name, description, item_type):
        self.name = name
        self.description = description
        self.item_type = item_type  # "menu" 或 "task"
    
    def execute(self):
        """执行菜单项的方法，子类应该重写这个方法"""
        if self.item_type == "menu":
            self.display_submenu()
        elif self.item_type == "task":
            self.execute_task()

    def display_submenu(self):
        """显示子菜单的方法，子类应该重写这个方法"""
        raise NotImplementedError("子类必须实现display_submenu方法")

    def execute_task(self):
        """执行任务的方法，子类应该重写这个方法"""
        raise NotImplementedError("子类必须实现execute_task方法")