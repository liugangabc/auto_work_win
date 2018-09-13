# -*- coding: utf-8 -*- # 

# by oldj http://oldj.net/ #

import pythoncom
import pyHook


def onMouseEvent(event):
    # 监听鼠标事件
    print {
        "MessageName:": event.MessageName,
        "Message:": event.Message,
        "Time:": event.Time,
        "Window:": event.Window,
        "WindowName:": event.WindowName,
        "Position:": event.Position,
        "Wheel:": event.Wheel,
        "Injected:": event.Injected,
    }
    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True


def onKeyboardEvent(event):
    # 监听键盘事件
    print {
        "MessageName:": event.MessageName,
        "Message:": event.Message,
        "Time:": event.Time,
        "Window:": event.Window,
        "WindowName:": event.WindowName,
        "Ascii:": (event.Ascii, chr(event.Ascii)),
        "Key:": event.Key,
        "KeyID:": event.KeyID,
        "ScanCode:": event.ScanCode,
        "Extended:": event.Extended,
        "Injected:": event.Injected,
        "Alt": event.Alt,
        "Transition": event.Transition,
    }
    # 同鼠标事件监听函数的返回值
    return True


def main():
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
    # 监听所有鼠标事件
    hm.MouseAllButtonsDown = onMouseEvent
    # 设置鼠标“钩子”
    hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()
