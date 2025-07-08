import win32gui
import win32ui
from PIL import Image
from ctypes import windll

def enum_windows_callback(hwnd, windows):
    window_title = win32gui.GetWindowText(hwnd)
    if window_title:
        windows.append((hwnd, window_title))

def get_all_windows():
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def get_game_windows():
    all_windows = get_all_windows()
    game_windows = []
    for hwnd, title in all_windows:
        if title.startswith("联想模拟器"):
            game_windows.append((hwnd, title))
    return game_windows

def capture_window(hwnd):
    # 获取窗口位置和大小
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top

    # 获取设备上下文
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # 创建位图对象
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)

    # 使用 BitBlt 拷贝屏幕内容到 bitmap 中
    result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)

    if result != 1:
        print("截图失败")
        return None

    # 转换为 PIL 图像格式
    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)
    image = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    # 清理资源
    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return image

if __name__ == "__main__":
    result = get_game_windows()
    print(result)