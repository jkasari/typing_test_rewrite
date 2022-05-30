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
        self.prompt_string = ""
        self.action_control("RESTART_DISPLAY")
        self.frame_sizer.Layout()

    def init_panel(self, size: tuple):
        self.func_panel = FuncPanel(self, size)
    
    def restart_display(self):
        self.func_panel.input_box.Hide()
        self.func_panel.restart_button.Show()

    def start_game(self):
        self.func_panel.restart_button.Hide()
        self.func_panel.input_box.Show()
        self.func_panel.update_prompt_text(self.prompt_string)

    # This controls all actions that require a widget to change on the panel.
    def action_control(self, action: str):
        if action == "RESTART_DISPLAY":
            self.restart_display()
        if action == "CHECK_INPUT":
            self.func_panel.update_prompt_text(self.prompt_string)
        if action == "START_GAME":
            self.prompt_string = "Start"
            self.start_game()
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
        self.init_input()
        self.init_sizers()
        self.SetBackgroundColour("Green")

        self.test_count = 0

    def init_restart_button(self):
        self.restart_button = wx.Button(self, label='Restart', pos=(270, 370), size=(90, 30))
        self.restart_button.Hide()

    
    def init_input(self):
        self.input_box = wx.TextCtrl(self, value="", size=(90, 30))

    def init_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.prompt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(0, 50, 0)
        self.main_sizer.Add(self.prompt_sizer, 0, wx.ALIGN_CENTER)
        self.main_sizer.Add(0, 50, 0)
        self.main_sizer.Add(self.restart_button, 0, wx.ALIGN_CENTER)
        self.main_sizer.Add(self.input_box, 0, wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)
  

    def init_actions(self):
        self.Bind(wx.EVT_BUTTON, self.restart_pushed, self.restart_button)
        self.Bind(wx.EVT_TEXT, self.text_entered, self.input_box)

    # Tell action control it needs to potentially update the prompt.
    def text_entered(self, e):
        #self.parent.action_control("CHECK_INPUT")
        self.parent.action_control("RESTART_DISPLAY")

    # Tell action control to restart the app.
    def restart_pushed(self, e):
        self.parent.action_control("START_GAME")

    # Takes a string and displays it as the prompt. Everytime it is called it checks the input box and either color codes the prompt or asks for it to be changed. 
    def update_prompt_text(self, text: str):
        if self.prompt_sizer.GetChildren():
            self.clear_prompt()
        input = ""
        if self.input_box.GetValue():
            input = self.input_box.GetValue()
        if input == text:
            self.parent.action_control("RESTART_DISPLAY")
        else:
            self.write_prompt_text(text, input)

    # Takes in a string for the prompt and for the input. It then fills the prompt sizer with color coded characters based on which ones match the input string.
    def write_prompt_text(self, text: str, input: str):
        for int, char in enumerate(text):
            prompt_char = wx.StaticText(self, label=char, style=wx.ALIGN_CENTER)
            #prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL)
            #prompt_char.SetFont(prompt_font)
            #if text[char]:
            #    prompt_char.SetForegroundColour((255, 0, 0))
            if int < len(input):
                if input[int] != char:
                    prompt_char.SetForegroundColour((255, 0, 0))
            self.prompt_sizer.Add(prompt_char)

    # A helper function that clears the prompt of all its chilren
    def clear_prompt(self):
        for i in reversed(range(len(self.prompt_sizer.GetChildren()))):
            self.prompt_sizer.Hide(i)
            self.prompt_sizer.Remove(i)

        


if __name__=="__main__":
    app = App()
    app.MainLoop()