import threading
from time import sleep

from gui_utils.global_indexes import model_languages_main
# from global_indexes import *
from gui_utils.kyle_ui_size import *
from gui_utils.kyle_ui_font import dky_fonts
from tkinter import filedialog

import tkinter as tk

from kyle_whisper.kyle_faster_whisper import kyle_faster_whisper_1
from translate_AI_chat_API.ctk_AI_chat_beta import chat_with_gpt_api_kyle, chat_win_ui
from text_translation_func.translate_win import TranslatorWindow

# window
index_win2 = tk.Tk()
index_win2.withdraw()


#############################################################3
# 翻译语言选择
#############################################################3
# 互斥逻辑, 避免两边选择同样的语言
def on_select_1(value, selected_option_1, selected_option_2,indexes_all):
    val = str(value).split(" ")[0]
    print("你选择了（左）：", val)

    if val == selected_option_2.get():
        # if selected_option_1.get() != "None":
            selected_option_1.set("None")
            indexes_all["org_language"] = "None"
    else:
        # if selected_option_1.get() != val:
        selected_option_1.set(val)
        indexes_all["org_language"] = model_languages_main[value]


def on_select_2(value, selected_option_2, selected_option_1,indexes_all):
    val = str(value).split(" ")[0]
    print("你选择了（右）：", val)

    if val == selected_option_1.get():
        # if selected_option_2.get() != "None":
            selected_option_2.set("None")
            indexes_all["org_language"] = "None"
    else:
        # if selected_option_2.get() != val:
        selected_option_2.set(val)
        indexes_all["dest_language"] = model_languages_main[value]






#############################################################3
# 翻译语言选择
#############################################################3







############################# model ##############################################
def model_radiobutton_event(Model_radio_var,indexes_all):
    print("当前选择模型：", Model_radio_var.get())
    indexes_all["translate_model"] = Model_radio_var.get()

############################# audio ##############################################
def audio_radiobutton_event(Audio_radio_var,indexes_all,textbox):
    print("radiobutton toggled, current value:", Audio_radio_var.get())
    indexes_all["audio_source"] = Audio_radio_var.get()
    if Audio_radio_var.get() in {"MP3","MP4","WAV"}:
        filename = filedialog.askopenfilename(title="choosing file")
        indexes_all["audio_source"] = indexes_all["audio_source"] + " " + filename
        print(indexes_all["audio_source"])
        print("model:" + indexes_all["translate_model"])
        print("audio:" + indexes_all["audio_source"])

        print(indexes_all["audio_source"].split(" ")[0])
        print( indexes_all["audio_source"].split(" ")[1])

        print("---")
        print("org_language" +": "+ indexes_all["org_language"])
        print("dest_language" + ": "+ indexes_all["dest_language"])

    if indexes_all["audio_source"].split(" ")[0] == "MP3" \
            and indexes_all["org_language"] == "None" \
            and indexes_all["dest_language"] == "None":
        # try:
        #     a1, a2 = kyle_faster_whisper_1(model_type=indexes_all["translate_model"],
        #                                    abs_path=indexes_all["audio_source"].split(" ")[1],
        #                                    task="translate",
        #
        #                                    compute_type="float32",
        #                                    device="cuda", )
        #     print(a1)
        #     print(a2)
        #
        # except Exception as e:
        #     print(f"Error: {e}")
        try:
            a1, a2 = kyle_faster_whisper_1(model_type=indexes_all["translate_model"],
                                           abs_path=indexes_all["audio_source"].split(" ")[1],
                                           task="transcribe",
                                           compute_type="float32",
                                           device="cuda", )
            textbox.insert(tk.END, "\n")
            # for i in a1:
            #     textbox.insert(tk.END, i.strip())
            #     textbox.insert(tk.END, "\n")
            for i in a2:
                textbox.insert(tk.END, i)
                textbox.insert(tk.END, "\n")
            print(a1)
            print(a2)

        except Exception as e:
            print(f"Error: {e}")

############################## theme ##########################################3
import customtkinter as ctk
class ExclusiveSwitchGroup:

    def __init__(self):
        self.switches = []
        self.labels = ["System", "Blue", "Dark", "DarkBlue", "Light", "Green"]

    def add(self, switch):
        self.switches.append(switch)
        switch.configure(command=lambda s=switch: self._on_selected(s))
        # 当你点击一个开关，就会触发 _only_keep_selected，它会关掉其他开关

    def _on_selected(self, selected):
        global root
        for sw in self.switches:
            if sw != selected:
                sw.deselect()
            elif sw == selected and selected.cget("text")==self.labels[0]:
                ctk.set_appearance_mode(selected.cget("text"))
            elif sw == selected and selected.cget("text")==self.labels[2]:
                ctk.set_appearance_mode(selected.cget("text"))
            elif sw == selected and selected.cget("text")==self.labels[4]:
                ctk.set_appearance_mode(selected.cget("text"))
            #
            # elif sw == selected and selected.cget("text")==self.labels[1]:
            #     ctk.set_default_color_theme("blue")
            #     print("111111")
            #     apply_theme_and_reload_ui(theme_name= "green", root= root, build_ui_function= lambda : self._on_selected(selected))
            #     root.update()
            # elif sw == selected and selected.cget("text")==self.labels[3]:
            #     ctk.set_default_color_theme("dark-blue")
            #     # Themes: "blue" (standard), "green", "dark-blue"
            #     print("3333333333")
            #     root.update()
            # elif sw == selected and selected.cget("text") == self.labels[5]:
            #     ctk.set_default_color_theme("green")
            #     print("55555555555555")
            #     root.update_idletasks()
            #     root.update()






###############################################################3
#####################################################################
def add_frame2(root, frame2,frame3):
    frame3.place_forget()
    sleep(0.01)

    root.geometry(f"{window_width}x{window_height}+{root.winfo_x()}+{root.winfo_y()}")
    frame2.place(x=frame2_place_x, y=frame2_place_y)


def combobox_callback(frame3,indexes_all):
    # 这里可以根据需要读取所有复选框状态
    for name, var in frame3.check_vars.items():
        print(f"{name} = {var.get()}")
    print("---")

    if frame3.check_vars["Original"].get() == 1:
        indexes_all["org_text"] = True
    if frame3.check_vars["Translate"].get() == 1:
        indexes_all["translate_text"] = True
    if frame3.check_vars["Save"].get() == 1:
        indexes_all["save_text"] = "None"
    if frame3.check_vars["Edit"].get() == 1:
        indexes_all["edit_text"] = True

def add_frame3(frame3):
    frame3.place(x=frame3_place_x, y=frame3_place_y, )


def create_toplevel_with_icon(root):

    app = TranslatorWindow(root)


def segmented_button_callback(value, root, frame2,frame3, segemented_button, bottom_button_values,indexes_all):
    print("segmented button clicked:", value)

    if value == bottom_button_values[0]:
        indexes_all["translate_status"] = 1
        print(indexes_all)

        # if indexes_all["audio_source"].splict(" ")[0] in  {"MP3","MP4","WAV"}:
        #     if indexes_all["audio_source"].splict(" ")[1]:
        #
        #




    elif value == bottom_button_values[1]:
        indexes_all["translate_status"] = 0

    elif value == bottom_button_values[2]:
        indexes_all["translate_status"] = -1

    elif value == bottom_button_values[3]:
        frame2.place_forget()
        root.geometry(f"{window_width - 200}x{window_height}+{root.winfo_x()}+{root.winfo_y()}")
        segemented_button.set("")
        add_frame3(frame3)


def button_aichat(root_main):
    print("button_aichat")
    root_main.withdraw()
    t4 = threading.Thread(target=chat_with_gpt_api_kyle,) #, daemon=True)
    t4.start()


    ai_chat_win = chat_win_ui(root_main)

    # return ai_chat_win


