from os import remove
import wx
import random
import time


class App(wx.App):
    def __init__(self):
        super().__init__()
        self.init_frame()

    def init_frame(self):
        frame = MainFrame(parent=None, title="Main Frame", pos=(100, 100), size=(500, 350))
        frame.Show()


class MainFrame(wx.Frame):
    def __init__(self, parent: wx.App, title: str, pos: tuple, size: tuple):
        super().__init__(parent= parent, title=title, pos=pos, size=size)
        self.init_panel(size)
        self.init_sizer()
        self.func_panel.init_actions()
        self.func_panel.change_prompt("BUTTS")
        self.frame_sizer.Layout()

    def init_panel(self, size: tuple):
        self.func_panel = FuncPanel(self, size)

    def action_control(self, action: str):
        if action == "test":
            self.func_panel.change_prompt("BUTTS")
        self.frame_sizer.Layout()

    def init_sizer(self):
        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer.Add(self.func_panel, 1, wx.EXPAND)
        self.SetSizer(self.frame_sizer)
        self.Fit()
        self.Show()

        


class FuncPanel(wx.Panel):
    def __init__(self, parent, size: tuple):
        super().__init__(parent=parent, size=size)
        self.parent = parent
        self.init_restart_button()
        self.init_sizers()

        self.SetBackgroundColour("Green")

        self.test_count = 0

    def init_restart_button(self):
        self.restart_button = wx.Button(self, label='', pos=(270, 370), size=(90, 30))
        #self.restart_button.Hide()


    def init_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.prompt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(0, 50, 0)
        self.main_sizer.Add(self.prompt_sizer, 0, wx.ALIGN_CENTER)
        self.main_sizer.Add(0, 50, 0)
        self.main_sizer.Add(self.restart_button, 0, wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)
  

    def init_actions(self):
        self.Bind(wx.EVT_BUTTON, self.restart_pushed)

    def restart_pushed(self, e):
        self.parent.action_control("test")

    def write_prompt_text(self, text: str):
        for int, char in enumerate(text):
            prompt_char = wx.StaticText(self, label=char, style=wx.ALIGN_CENTER)
            #prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL)
            #prompt_char.SetFont(prompt_font)
            if int == self.test_count:
                prompt_char.SetForegroundColour((255, 0, 0))
            self.prompt_sizer.Add(prompt_char)
        self.test_count += 1
        if self.test_count > len(text):
            self.test_count = 0

    def clear_prompt(self):
        for i in reversed(range(len(self.prompt_sizer.GetChildren()))):
            self.prompt_sizer.Hide(i)
            self.prompt_sizer.Remove(i)

    def change_prompt(self, text: str):
        if self.prompt_sizer.GetChildren():
            self.clear_prompt()
        self.write_prompt_text(text)
        


if __name__=="__main__":
    app = App()
    app.MainLoop()