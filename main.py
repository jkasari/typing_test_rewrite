import wx
import random
import time
import json


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
        self.import_json_data()
        self.init_data_members()
        self.init_panel(size)
        self.init_sizer()
        self.func_panel.init_actions()
        self.action_control("START_GAME")
        self.frame_sizer.Layout()

    def init_panel(self, size: tuple):
        self.func_panel = FuncPanel(self, size)
    
    # Displays the restart button and hides the rest of the widgets
    def restart_display(self):
        self._time_limit = (self._time_limit + self.calc_average_response()) / 2
        print(self._time_limit)
        self.update_score_board(self._time_limit)
        self.live_prompt = str(round(self._time_limit, 4)) # Calc the final average of all the response times
        self.func_panel.restart_display()
        self.init_data_members()

    def update_score_board(self, score: int):
        record_score = self.text_dict["HIGH_SCORE_NUM"]
        if record_score:
            record_score = int(record_score)
        else:
            record_score = 100
        new_score = round(score, 4)
        if new_score < record_score:
            self.text_dict["HIGH_SCORE_NUM"] = str(new_score)
        with open("text.json", 'w') as i:
            json.dump(self.text_dict, i, indent=2)

    # This hides the restart button and starts the actual game by displaying the input box
    def start_game(self):
        if self._round == 1:
            self.live_prompt = self.text_dict["ROUND_ONE"]
        elif self._round == 2:
            self.live_prompt = self.text_dict["ROUND_TWO"]
        self.func_panel.start_game_display()

    # Each time the text is matched, this updates the prompt.
    def generate_new_prompt(self):
        self.live_prompt = random.choice(self._prompt_list)
        self.func_panel.generate_new_prompt_display()

    # calibrates the prompts for the second round
    def calibrate_round_two(self):
        big_list = []
        self._time_limit = self.calc_average_response()
        for char in self.response_times:
            for _ in range(int(self.response_times[char] * 4)):
                big_list.append(char)
        for i in range(5):
            random.shuffle(big_list)
            temp_str = ''.join(big_list[0: i+2])
            print(temp_str)
            self._prompt_list.append(temp_str)
        random.shuffle(self._prompt_list)
        
    def calc_average_response(self):
        temp = 1
        for i in self.response_times:
            temp += self.response_times[i]
        return temp / len(self.response_times)

    # Handles the logic when a round is done. Adding up times for round one and finishing the game after round 2.
    def finish_round(self):
        if self._round == 1:
            self.calibrate_round_two()
            self._round = 2
            self.start_game()
        else:
            self.action_control("RESTART_DISPLAY")

    # Everytime there is a text match, this function gets called and manages what to do while the game is running.
    def run_game(self):
        time_diff = self.check_time()
        print(time_diff)
        if self.live_prompt != self.text_dict["ROUND_ONE"] and self.live_prompt != self.text_dict["ROUND_TWO"]: 
            if time_diff < self._time_limit * len(self.live_prompt):
                self.func_panel.turn_green()
                self._prompt_list.remove(self.live_prompt)
                self.count_response_time(time_diff)
            else:
                self.func_panel.turn_red()
        if self._prompt_list:
            self.generate_new_prompt()
        else:
            self.finish_round()

    def count_response_time(self, time_diff: int):
        if self._round == 1:
            self.response_times[self.live_prompt] = time_diff
        else:
            self.response_times[self.live_prompt] = time_diff / len(self.live_prompt)

    # imports all the strings from the json file and puts them into a python dict object.
    def import_json_data(self):
        json_obj = open("text.json")
        content_str = json_obj.read()
        self.text_dict = json.loads(content_str)

    # This controls all actions that require a widget to change on the panel.
    def action_control(self, action: str):
        if action == "RESTART_DISPLAY":
            self.restart_display()
        elif action == "CHECK_INPUT":
            self.func_panel.update_prompt_text()
        elif action == "START_GAME":
            self.start_game()
        elif action == "TEXT_MATCH":
            self.run_game()
        self.frame_sizer.Layout()

    # Creates the main sizer for the Frame.
    def init_sizer(self):
        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer.Add(self.func_panel, 1, wx.EXPAND)
        self.SetSizer(self.frame_sizer)
        self.Fit()
        self.Show()

    # Declares all the data members for the Frame.
    def init_data_members(self):
        self._round = 1
        self.live_prompt = " "
        self._prompt_list = list(self.text_dict["PROMPTS"])
        self.start = 0
        self.response_times = {}
        self._time_limit = 5

    # Retrun the difference between the current time and the self.start variable. 
    def check_time(self):
        time_diff = time.time()-self.start
        self.start = time.time()
        return time_diff
        


class FuncPanel(wx.Panel):
    def __init__(self, parent, size: tuple):
        super().__init__(parent=parent, size=size)
        self.parent = parent
        self.init_restart_button()
        self.init_input()
        self.init_final_score()
        self.init_sizers()
        self.SetBackgroundColour("Green")

        self.test_count = 0

    #creates the actual restart button
    def init_restart_button(self):
        self.restart_button = wx.Button(self, label=self.parent.text_dict["RESTART_BUTTON"], size=(90, 30))
        self.restart_button.Hide()

    def init_final_score(self):
        self.final_score = wx.StaticText(self, label=self.parent.text_dict["FINAL_SCORE"], size=(100, 30))
        self.final_score.Hide()

    #creats the input box.
    def init_input(self):
        prompt_font = wx.Font(pointSize= 40, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL)
        self.input_box = wx.TextCtrl(self, value="", size=(180, 80))
        self.input_box.SetFont(prompt_font)

    # Inits the dong show that is the panel sizers. LOOK AT ALL OF THEM
    def init_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.prompt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.high_score_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(0, 30, 0)
        self.main_sizer.Add(self.final_score, 0, wx.ALIGN_CENTER)
        self.main_sizer.Add(0, 20, 0)
        self.main_sizer.Add(self.prompt_sizer, 0, wx.ALIGN_CENTER)
        self.main_sizer.Add(0, 30, 0)
        self.main_sizer.Add(self.high_score_sizer, 0, wx.ALIGN_CENTER)
        self.main_sizer.Add(0, 30, 0)
        self.main_sizer.Add(self.restart_button, 0, wx.ALIGN_CENTER)
        self.main_sizer.Add(self.input_box, 0, wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)
  
    # Python was giving me a bug if I inited these in the constructor. Now the parent can init them, I plan on fixing this. 
    def init_actions(self):
        self.Bind(wx.EVT_BUTTON, self.restart_pushed, self.restart_button)
        self.Bind(wx.EVT_TEXT, self.text_entered, self.input_box)

    # Tell action control it needs to potentially update the prompt.
    def text_entered(self, e):
        self.parent.action_control("CHECK_INPUT")

    # Tell action control to restart the app.
    def restart_pushed(self, e):
        self.parent.action_control("START_GAME")
    
    def update_high_score(self):
        if not self.high_score_sizer.IsEmpty():
            self.clear_high_score()
        text_label = self.parent.text_dict["HIGH_SCORE"]
        score_label = self.parent.text_dict["HIGH_SCORE_NUM"]
        score_font = wx.Font(pointSize=70, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_BOLD)
        dc = wx.ScreenDC()
        dc.SetFont(score_font)
        text = wx.StaticText(self, label=text_label)
        score = wx.StaticText(self, label=score_label, size=dc.GetTextExtent(score_label))
        score.SetFont(score_font)
        self.high_score_sizer.Add(text)
        self.high_score_sizer.Add(score)

    def clear_high_score(self):
        for i in reversed(range(len(self.high_score_sizer.GetChildren()))):
            self.high_score_sizer.Hide(i)
            self.high_score_sizer.Remove(i)

    # Takes a string and displays it as the prompt. Everytime it is called it checks the input box and either color codes the prompt or asks for it to be changed. 
    def update_prompt_text(self):
        if not self.prompt_sizer.IsEmpty():
            self.clear_prompt()
        input = ""
        if self.input_box.GetValue():
            input = self.input_box.GetValue()
        if input == self.parent.live_prompt:
            self.parent.action_control("TEXT_MATCH")
        else:
            self.write_prompt_text(input)

    # Takes in a string for the prompt and for the input. It then fills the prompt sizer with color coded characters based on which ones match the input string.
    def write_prompt_text(self, input: str):
        for int, char in enumerate(self.parent.live_prompt):
            prompt_font = wx.Font(pointSize= 60, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_MAX,  weight=wx.FONTWEIGHT_NORMAL)
            dc = wx.ScreenDC()
            dc.SetFont(prompt_font)
            prompt_char = wx.StaticText(self, label=char, style=wx.ALIGN_CENTER, size=dc.GetTextExtent(char))
            prompt_char.SetFont(prompt_font)
            if int < len(input):
                if input[int] != char:
                    prompt_char.SetForegroundColour((255, 0, 0))
            self.prompt_sizer.Add(prompt_char)

    # A helper function that clears the prompt of all its chilren
    def clear_prompt(self):
        for i in reversed(range(len(self.prompt_sizer.GetChildren()))):
            self.prompt_sizer.Hide(i)
            self.prompt_sizer.Remove(i)

    def turn_red(self):
        self.SetBackgroundColour("Grey")

    def turn_green(self):
        self.SetBackgroundColour("Green")

    # Adjust the displays for the game to start
    def start_game_display(self):
        self.update_prompt_text()
        self.clear_high_score()
        self.input_box.SetValue("")
        self.restart_button.Hide()
        self.final_score.Hide()
        self.input_box.Show()
        
    # Sets the displays for the restart button and page
    def restart_display(self):
        self.update_high_score()
        self.final_score.Show()
        self.input_box.SetValue("")
        self.restart_button.Show()
        self.input_box.Hide()
        self.update_prompt_text()

    # Adjust the displays needed to allow a new prompt to exist
    def generate_new_prompt_display(self):
        self.input_box.SetValue("")
        self.update_prompt_text()

        


if __name__=="__main__":
    app = App()
    app.MainLoop()