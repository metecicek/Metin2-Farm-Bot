import numpy as np
import win32gui, win32ui, win32con


class ekranYakala:
    def __init__(self, window_name=None):
        self.hwnd = win32gui.FindWindow(None, window_name) if window_name else win32gui.GetDesktopWindow()

        if not self.hwnd:
            raise Exception("Window not found")

        rect = win32gui.GetWindowRect(self.hwnd)

        self.offset_x = rect[0]
        self.offset_y = rect[1]

        self.w = rect[2] - rect[0]
        self.h = rect[3] - rect[1]

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()

        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dcObj, self.w, self.h)

        cDC.SelectObject(bmp)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)

        img = np.frombuffer(bmp.GetBitmapBits(True), dtype=np.uint8)
        img = img.reshape((self.h, self.w, 4))
        img = img[..., :3]

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(bmp.GetHandle())

        return np.ascontiguousarray(img)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)