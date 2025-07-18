from agent.main_menu import MainMenu
from common.utils import clear_screen, print_box, Colors


def main():
    """游戏Agent主函数"""
    clear_screen()
    welcome_text = [
        "",
        f"{Colors.BOLD}{Colors.YELLOW}游戏Agent{Colors.ENDC}",
        f"{Colors.BOLD}{Colors.GREEN}欢迎使用君临天下智能体{Colors.ENDC}",
        ""
    ]
    print_box(welcome_text, title="JXTX AGENT", width=60)
    print()
    menu = MainMenu()
    menu.display()


if __name__ == "__main__":
    main()
