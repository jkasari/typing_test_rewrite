import wx
import random
import time


class App(wx.App):
    def __init__(self):
        super().__init__()
        self.InitFrame()

    def InitFrame(self):
        frame = MainFrame(parent=None, title="Main Frame", pos=(100, 100), size=(500, 350))
        frame.Show()


class MainFrame(wx.Frame):
    def __init__(self, parent: wx.App, title: str, pos: tuple, size: tuple):
        super().__init__(parent= parent, title=title, pos=pos, size=size)
        self.InitPanel()

    def InitPanel(self):
        self.func_panel = FuncPanel(self)

class FuncPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.SetBackgroundColour("Green")


if __name__=="__main__":
    app = App()
    app.MainLoop()