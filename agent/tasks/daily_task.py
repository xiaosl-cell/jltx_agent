import time

from agent.tasks.task_base import TaskBase
from common.gui_util import get_game_windows
from common.coordinate_converter import CoordinateConverter
from common.image_finder import ImageFinder


def sign_in(coord_converter: CoordinateConverter):
    """签到"""
    # 点击侧边栏
    coord_converter.find_and_click_icon(
        icon_path="./img/template/cebianlan_zhankai.png",
        description="侧边栏",
        confidence_threshold=0.8,
        delay=1.0
    )

    # 进入军团
    coord_converter.find_and_click_icon(
        icon_path="./img/template/legion.png",
        description="进入军团",
        confidence_threshold=0.8,
        delay=1.0
    )

    # 军团签到
    coord_converter.find_and_click_icon(
        icon_path="./img/template/legion_sign_in.png",
        description="军团签到",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/close.png",
        description="关闭",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/cebianlan_shouqi.png",
        description="侧边栏",
        confidence_threshold=0.8,
        delay=1.03
    )


def competition_among_warlords(coord_converter: CoordinateConverter, image_finder: ImageFinder):
    """群雄争霸"""
    # 群雄争霸
    coord_converter.find_and_click_icon(
        icon_path="./img/template/military_affairs.png",
        description="军事事务图标",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/qunxiongzhengba.png",
        description="群雄争霸",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/jiangli.png",
        description="奖励",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/lingjiang.png",
        description="群雄争霸-领奖",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/close.png",
        description="关闭",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/qunxiong-attack.png",
        description="开始战斗",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/attack.png",
        description="进攻",
        confidence_threshold=0.8,
        delay=1.5
    )

    while True:
        time.sleep(10)
        # 游戏窗口左边最中间鼠标左键不放手
        window_center_x, window_center_y = coord_converter.get_window_center()

        # 计算左边位置：窗口中心x坐标减去窗口宽度的一半，再加一点偏移避免在边界
        coord_converter._update_window_info()
        left_margin = 50  # 距离左边界50像素的位置
        left_x = coord_converter.client_screen_pos[0] + left_margin
        center_y = window_center_y

        print(f"准备在窗口左边中间位置按住鼠标: ({left_x}, {center_y})")

        # 移动鼠标到目标位置
        import win32api
        import win32con
        win32api.SetCursorPos((left_x, center_y))
        # 按下鼠标左键20秒
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        print("鼠标左键已按下，将保持20秒...")

        # 保持按下20秒
        time.sleep(10)

        # 松开鼠标左键
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        print("鼠标左键已松开")

        # 检查是否出现“下一场”按钮
        while True:
            image_finder = ImageFinder(0.8)
            results = image_finder.find_icon_in_game("./img/template/qunxiong-xiayichang.png")
            if results:
                print("下一场按钮已出现，等待5秒后点击")
                time.sleep(10)
                break
        # 点击下一场
        coord_converter.find_and_click_icon(
            icon_path="./img/template/qunxiong-xiayichang.png",
            description="下一场",
            confidence_threshold=0.8,
            delay=1.0
        )

        over = image_finder.find_icon_in_game("./img/template/goumaitili.png")
        if over:
            coord_converter.find_and_click_icon(
                icon_path="./img/template/cancel.png",
                description="取消",
                confidence_threshold=0.8,
                delay=1.0
            )
            coord_converter.find_and_click_icon(
                icon_path="./img/template/huiying.png",
                description="回营",
                confidence_threshold=0.8,
                delay=1.0
            )


def songxin(coord_converter: CoordinateConverter):
    coord_converter.find_and_click_icon(
        icon_path="./img/template/shejiao.png",
        description="社交",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/friend.png",
        description="好友",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/yijiansongxin.png",
        description="好友",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/close.png",
        description="关闭",
        confidence_threshold=0.8,
        delay=1.0
    )


def yangqi(coord_converter: CoordinateConverter):
    coord_converter.find_and_click_icon(
        icon_path="./img/template/chengzhang.png",
        description="成长",
        confidence_threshold=0.8,
    )
    coord_converter.find_and_click_icon(
        icon_path="./img/template/zhugong.png",
        description="主公",
        confidence_threshold=0.8,
    )
    coord_converter.find_and_click_icon(
        icon_path="./img/template/zhanqi.png",
        description="战旗",
        confidence_threshold=0.8,
    )
    coord_converter.find_and_click_icon(
        icon_path="./img/template/yangqi.png",
        description="战旗",
        confidence_threshold=0.8,
    )
    coord_converter.find_and_click_icon(
        icon_path="./img/template/close.png",
        description="关闭",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/close.png",
        description="关闭",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/shiwei.png",
        description="侍卫",
        confidence_threshold=0.8,
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/tianjige.png",
        description="天玑阁",
        confidence_threshold=0.8,
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/yangua.png",
        description="单次演卦",
        confidence_threshold=0.8,
    )

    # 随意点击鼠标
    import win32api
    import win32con
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    coord_converter.find_and_click_icon(
        icon_path="./img/template/fanhui.png",
        description="返回",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/close.png",
        description="关闭",
        confidence_threshold=0.8,
        delay=1.0
    )

    coord_converter.find_and_click_icon(
        icon_path="./img/template/shiwei-huiying.png",
        description="回营",
        confidence_threshold=0.8,
        delay=1.0
    )




class DailyTask(TaskBase):
    def __init__(self):
        super().__init__('日常任务', '日常琐事')

    def execute(self):
        try:
            game_windows = get_game_windows()
            titles = [title for hwnd, title in game_windows]
            print(f"检测到{len(game_windows)}个游戏窗口：{titles}")

            for game_window in game_windows:
                hwnd, title = game_window
                print(f"正在处理窗口：{title}")

                # 创建坐标转换器
                coord_converter = CoordinateConverter(hwnd)

                image_finder = ImageFinder(0.8)

                sign_in(coord_converter)

                competition_among_warlords(coord_converter, image_finder)

                songxin(coord_converter)

                yangqi(coord_converter)



        except Exception as e:
            print(e)
