from agent.menus.exit_task_menu import ExitTaskMenu
from agent.menus.conquer_city_menu import ConquerCityMenu
from common.utils import print_box, print_menu_item, Colors

class MainMenu:
    def __init__(self):
        self.menu_items = [
            ExitTaskMenu(),
            ConquerCityMenu()
        ]

    def display(self):
        menu_text = []
        for i, item in enumerate(self.menu_items, start=1):
            menu_text.append(print_menu_item(i, item.name))
        menu_text.append("")
        menu_text.append(f"{Colors.YELLOW}请输入您的选择...{Colors.ENDC}")
        
        print_box(menu_text, title="主菜单", width=60)
        
        choice = input(f"\n{Colors.GREEN}>>> {Colors.ENDC}")
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.menu_items):
                selected_item = self.menu_items[choice - 1]
                selected_item.execute()
            else:
                print(f"\n{Colors.RED}无效的选择，请重新输入。{Colors.ENDC}")
        except ValueError:
            print(f"\n{Colors.RED}无效的输入，请输入一个数字。{Colors.ENDC}")
    
