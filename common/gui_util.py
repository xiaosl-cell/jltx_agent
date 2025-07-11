import win32gui
import win32ui
from PIL import Image
from ctypes import windll
import ctypes
import time
from ctypes import wintypes

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

def get_window_dpi_scale(hwnd):
    """获取窗口的DPI缩放比例"""
    try:
        # 尝试使用GetDpiForWindow (Windows 10 1607+)
        dpi = windll.user32.GetDpiForWindow(hwnd)
        if dpi > 0:
            return dpi / 96.0  # 96 DPI是100%缩放
    except:
        pass
    
    try:
        # 备用方法：使用GetWindowDC获取设备上下文的DPI
        hdc = win32gui.GetWindowDC(hwnd)
        dpi = windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
        win32gui.ReleaseDC(hwnd, hdc)
        return dpi / 96.0
    except:
        pass
    
    # 如果都失败，返回1.0（无缩放）
    return 1.0

def capture_window(hwnd):
    """
    截取窗口图像，处理DPI缩放问题
    """
    print(f"开始截取窗口 (hwnd: {hwnd})")
    
    # 先将窗口切换到前台
    try:
        # 检查窗口是否最小化
        if win32gui.IsIconic(hwnd):
            print("窗口处于最小化状态，正在还原...")
            win32gui.ShowWindow(hwnd, 9)  # SW_RESTORE
            time.sleep(0.5)
        # 将窗口设置为可见
        win32gui.ShowWindow(hwnd, 5)  # SW_SHOW
        time.sleep(0.5)
        
        # 将窗口置于最前面
        win32gui.SetForegroundWindow(hwnd)
        
        # 等待一下让窗口完全切换到前台
        time.sleep(0.5)
        
        print("窗口已切换到前台")
        
    except Exception as e:
        print(f"切换窗口到前台时出错: {e}")
        # 继续尝试截图，即使切换失败
    
    # 获取窗口的DPI缩放比例
    dpi_scale = get_window_dpi_scale(hwnd)
    
    # 首先尝试获取客户区尺寸
    client_rect = win32gui.GetClientRect(hwnd)
    left, top, right, bottom = client_rect
    client_width = right - left
    client_height = bottom - top
    
    print(f"客户区尺寸: {client_width}x{client_height}")
    
    # 如果客户区尺寸为0或太小，使用窗口完整尺寸
    if client_width <= 0 or client_height <= 0 or client_width < 50 or client_height < 50:
        print("客户区尺寸无效，使用窗口完整尺寸")
        window_rect = win32gui.GetWindowRect(hwnd)
        win_left, win_top, win_right, win_bottom = window_rect
        width = win_right - win_left
        height = win_bottom - win_top
        use_window_rect = True
    else:
        width = client_width
        height = client_height
        use_window_rect = False
    
    print(f"使用尺寸: {width}x{height}")
    
    # 根据DPI缩放调整实际尺寸
    actual_width = int(width * dpi_scale)
    actual_height = int(height * dpi_scale)
    
    print(f"DPI缩放比例: {dpi_scale:.2f}")
    print(f"实际截图尺寸: {actual_width}x{actual_height}")
    
    # 最终检查尺寸是否有效
    if actual_width <= 0 or actual_height <= 0:
        print("错误：计算出的截图尺寸无效")
        return None
    
    # 获取设备上下文
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # 创建位图对象 - 使用实际尺寸
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, actual_width, actual_height)
    save_dc.SelectObject(bitmap)

    # 方法1：使用PrintWindow (推荐)
    result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)  # 使用PW_RENDERFULLCONTENT标志
    
    if result != 1:
        print("PrintWindow失败，尝试使用BitBlt方法")
        # 方法2：使用BitBlt作为备用
        if use_window_rect:
            # 使用窗口坐标
            window_rect = win32gui.GetWindowRect(hwnd)
            window_left, window_top, window_right, window_bottom = window_rect
        else:
            # 使用客户区坐标，需要转换为屏幕坐标
            client_point = win32gui.ClientToScreen(hwnd, (0, 0))
            window_left, window_top = client_point
        
        # 获取屏幕设备上下文
        screen_dc = win32gui.GetDC(0)
        screen_mfc_dc = win32ui.CreateDCFromHandle(screen_dc)
        
        # 使用BitBlt复制屏幕内容
        result = windll.gdi32.BitBlt(
            save_dc.GetSafeHdc(),
            0, 0, actual_width, actual_height,
            screen_mfc_dc.GetSafeHdc(),
            window_left, window_top,
            0x00CC0020  # SRCCOPY
        )
        
        print(f"BitBlt从屏幕位置 ({window_left}, {window_top}) 复制 {actual_width}x{actual_height} 像素")
        
        # 清理屏幕设备上下文
        screen_mfc_dc.DeleteDC()
        win32gui.ReleaseDC(0, screen_dc)
        
        if result == 0:
            print("BitBlt也失败了，尝试最后一种方法")
            # 清理资源
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            
            # 最后尝试使用alternative方法
            return capture_window_alternative(hwnd)

    # 转换为 PIL 图像格式
    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)
    
    print(f"位图信息: {bmpinfo['bmWidth']}x{bmpinfo['bmHeight']}")
    
    # 检查是否有足够的图像数据
    expected_size = bmpinfo['bmWidth'] * bmpinfo['bmHeight'] * 4  # BGRX格式，每像素4字节
    if len(bmpstr) < expected_size:
        print(f"图像数据不足: 期望{expected_size}字节，实际{len(bmpstr)}字节")
        # 清理资源
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        return None
    
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

    print("截图完成！")
    return image

def capture_window_alternative(hwnd):
    """
    替代的窗口截图方法，使用GetWindowRect而不是GetClientRect
    """
    # 获取窗口的完整矩形区域（包括标题栏）
    window_rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = window_rect
    width = right - left
    height = bottom - top
    
    print(f"窗口完整尺寸: {width}x{height}")
    
    # 获取屏幕设备上下文
    screen_dc = win32gui.GetDC(0)
    mfc_dc = win32ui.CreateDCFromHandle(screen_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # 创建位图对象
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)

    # 使用BitBlt从屏幕复制内容
    result = windll.gdi32.BitBlt(
        save_dc.GetSafeHdc(),
        0, 0, width, height,
        mfc_dc.GetSafeHdc(),
        left, top,
        0x00CC0020  # SRCCOPY
    )

    if result == 0:
        print("截图失败")
        # 清理资源
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(0, screen_dc)
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
    win32gui.ReleaseDC(0, screen_dc)

    return image

if __name__ == "__main__":
    result = get_game_windows()
    print(result)