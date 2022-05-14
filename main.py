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
        self.prompt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.init_sizers()


        self.SetBackgroundColour("Green")

    def init_sizers(self):
        self.write_prompt_text("butts")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(0, 50, 0)
        vbox.Add(self.prompt_sizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(vbox)

    def write_prompt_text(self, text: str):
        self.prompt_sizer.Clear()
        for char in text:
            prompt_char = wx.StaticText(self, label=char, style=wx.ALIGN_CENTER)
            prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
            prompt_char.SetFont(prompt_font)
            self.prompt_sizer.Add(prompt_char)


if __name__=="__main__":
    app = App()
    app.MainLoop()