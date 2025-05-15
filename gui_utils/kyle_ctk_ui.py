
# https://customtkinter.tomschimansky.com/documentation/widgets/


import threading
from tkinter import font
import customtkinter as ctk
import tkinter as tk
import os  # 用于检查文件是否存在
import ctypes


from gui_utils.kyle_ui_font import dky_fonts
from gui_utils.kyle_ui_size import *
from gui_utils.command_funcs import *
from gui_utils.global_indexes import *
from text_translation_func.translate_win import TranslatorWindow

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
    # 仅 Windows 下有效,# 不然会获取不到真实的数据， 但是Linux mac不行
    # SetProcessDpiAwareness(1) 表示“系统感知 DPI”（可让 tkinter 得到真实分辨率）

# 禁用 DPI 自动适配（一般不建议），是否使用系统 DPI 缩放设置（比如 125%、150%）来自动放大界面
ctk.deactivate_automatic_dpi_awareness()

def ctk_ui( ):
    indexes_all= {
        "org_language": "None", # du, en, fr ,zh, yue, ja, all, not
        "dest_language": "None",
        "translate_model": "tiny",
        "audio_source" :"MP3",
        "translate_status": -1, # -1:end, 0 stop, 1 : start/running
        "org_text": True,
        "translate_text": False,
        "save_text": "None", # path if has
        "edit":True,
    }
    # # 创建主窗口
    ctk_ui_root = ctk.CTk()
    ctk_ui_root.title("DUAN_Translating")
    ctk_ui_root.attributes('-alpha', 1)  # 设置透明度
    # ctk_ui_root.attributes('-topmost', 1)  # 置顶窗口
    ctk_ui_root.resizable(False, False)  # 禁止允许用户用鼠标拖动改变大小（宽、高）resize

    # 放置调用的时候出现问题，比如路径找不到
    old_dir = os.getcwd()  # 1. 记住当前工作目录
    os.chdir(os.path.dirname(__file__))

    icon_path = r"../img/plane_icon_128.ico"
    if os.path.exists(icon_path):
        ctk_ui_root.iconbitmap(icon_path)
    else:
        exit("icon_path not exists")

    os.chdir(old_dir)

    ctk_ui_root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")  # 2048x360+256+900
    print(f"{window_width}x{window_height}+{x_position}+{y_position}")

    ################################################################################################
    ######################### # main two frames 的 size   ###########################################
    ################################################################################################

    frame1 = ctk.CTkFrame(ctk_ui_root, width=text_frame1_w, height=text_frame1_h, corner_radius=0, )
    frame1.pack_propagate(False)
    frame1.place(x=frame1_place_x, y=frame1_place_y)  # 基于root

    frame2 = ctk.CTkFrame(ctk_ui_root, width=text_frame2_w, height=text_frame2_h, corner_radius=0)
    frame2.pack_propagate(False)

    frame2.place(x=frame2_place_x, y=frame2_place_y)  # 基于root

    frame3 = ctk.CTkFrame(ctk_ui_root,
                          width=text_frame3_w,
                          height=text_frame3_h,
                          corner_radius=0)
    # frame3.place(x=frame3_place_x, y=frame3_place_y ) # 基于root

    ############################################################################
    ######################### frame1 ###########################################
    ############################################################################
    textbox = ctk.CTkTextbox(master=frame1,
                             font=dky_fonts["Times_25"],
                             activate_scrollbars=False, wrap="word",  # wrap="char"：按字符（宽度）换行，none 不自动换行
                             width=textbox_w,
                             height=textbox_h,
                             )
    textbox.place(x=gap_frame1_textbox, y=gap_frame1_textbox)

    # 添加垂直滚动条到textbox
    textbox_scrollbar_vertical = ctk.CTkScrollbar(master=frame1, orientation="vertical", command=textbox.yview,
                                                  width=scrollbar_text_width,  # 滚动条宽度
                                                  height=text_frame1_h - gap_frame1_textbox * 2,
                                                  # fg_color = "#DDDDDD",  # 背景轨道颜色
                                                  button_color="#CCCCCC",  # 滚动条按钮颜色
                                                  button_hover_color="#DDDDDD",  # #DDDDDD",  # 悬停颜色gold
                                                  corner_radius=25
                                                  )
    textbox_scrollbar_vertical.place(relx=1.0, anchor="ne")  # 右对齐
    textbox.configure(yscrollcommand=textbox_scrollbar_vertical.set)

    ############################################################################
    ######################### frame2 #### width=350 ############################
    ############################################################################
    label_arrows = ctk.CTkLabel(frame2, text="⇄", font=dky_fonts["Segoe_45"],
                                width=label_arrows_width,
                                height=label_arrows_height, )
    label_arrows.place(x=label_place_x,
                       y=-6, anchor="nw")

    # 创建 OptionMenu_1
    option_menu_1 = ctk.CTkOptionMenu(
        master=frame2,
        dynamic_resizing=False,  # 文本太大而无法容纳时自动调整 optionmenu 的大小
        values=list(model_languages_main.keys()),
        variable=selected_option_1,
        command=lambda value: on_select_1(value, selected_option_1, selected_option_2, indexes_all),
        font=dky_fonts["Times_20"],
        dropdown_font=dky_fonts["Times_20"],
        width=option_menu_width,
        height=option_menu_height,
    )
    option_menu_1.place(x=option_menu_1_place_x, y=option_menu_1_place_y, anchor="nw")

    # 创建 OptionMenu_2
    option_menu_2 = ctk.CTkOptionMenu(
        master=frame2,
        dynamic_resizing=False,  # 文本太大而无法容纳时自动调整 optionmenu 的大小
        values=list(model_languages_main.keys())[:-2] + list(model_languages_main.keys())[-1:],
        variable=selected_option_2,
        command=lambda value: on_select_2(value, selected_option_2, selected_option_1,indexes_all),
        font=dky_fonts["Times_20"],
        dropdown_font=dky_fonts["Times_20"],
        width=option_menu_width,
        height=option_menu_height,
    )
    option_menu_2.place(x=option_menu_2_place_x, y=option_menu_2_place_y, anchor="nw")

    ##################################################################################
    tabview = ctk.CTkTabview(master=frame2,
                             width=tabview_w,
                             height=tabview_h)
    # tabview._segmented_button 是内部变量，非官方 API, 虽然这样做在目前版本有效，但未来 customtkinter 更新可能变动
    tabview._segmented_button.configure(font=dky_fonts["Times_25"])
    tabview.pack_propagate(False)
    tabview.place(x=tabview_place_x, y=tabview_place_y)

    tabview.add("Model")  # add tab at the end
    tabview.add("Source")  # add tab at the end
    tabview.add("Theme")  # add tab at the end

    ####################################################################################
    ####################Model_tab = tabview.tab("Model")################################
    ####################################################################################
    # # 加载不同的模型
    # https://github.com/openai/whisper
    # 前面四个适用于英文
    # model_tiny = whisper.load_model("tiny")
    # model_base = whisper.load_model("base")
    # model_small = whisper.load_model("small")
    # model_medium = whisper.load_model("medium")
    #
    # # 适合多语言
    # model_large = whisper.load_model("large")
    # model_large = whisper.load_model("turbo") # large-v3-turbo	large-v3  large-v2

    frame2_1 = ctk.CTkFrame(master=tabview.tab("Model"),
                            # fg_color="green",
                            corner_radius=15,
                            width=frame2_1_w,
                            height=frame2_1_y,
                            )
    frame2_1.pack_propagate(False)
    frame2_1.pack(expand=False, fill="none", padx=0, pady=0)

    # 滚动框（固定尺寸 + 圆角 + 滚动条按钮颜色）
    Model_tab_scroll_frame = ctk.CTkScrollableFrame(master=frame2_1,
                                                    corner_radius=15,
                                                    width=Model_tab_scroll_frame_w,
                                                    )
    Model_tab_scroll_frame.pack_propagate(False)
    Model_tab_scroll_frame.pack(expand=False, fill="none", padx=2, pady=3)

    ########################## add model radio button #####################3
    for i in range(0, 6):  # create
        rb_num = ctk.CTkRadioButton(master=Model_tab_scroll_frame,
                                    text=model_names[i],
                                    variable=Model_radio_var,
                                    value=model_names[i].split(".")[1],
                                    font=dky_fonts["Times_20"],
                                    command=lambda: model_radiobutton_event(Model_radio_var,indexes_all),
                                    )
        model_rb.append(rb_num)
    for i in range(0, 6):  # place
        model_rb[i].grid(row=i, column=0, padx=15, pady=8, sticky="w")

    ####################################################################################
    ####################Audio_tab = tabview.tab("Audio")################################
    ####################################################################################
    frame2_2 = ctk.CTkFrame(master=tabview.tab("Source"),
                            width=frame2_2_w,
                            height=frame2_2_y,
                            corner_radius=15,
                            )
    frame2_2.pack_propagate(False)
    frame2_2.pack(expand=False, fill="none", padx=0, pady=0)

    Audio_tab_scroll_frame = ctk.CTkScrollableFrame(master=frame2_2,
                                                    corner_radius=15,
                                                    width=Audio_tab_scrollframe_w,
                                                    )
    Audio_tab_scroll_frame.pack_propagate(False)
    Audio_tab_scroll_frame.pack(expand=False, fill="none", padx=2, pady=3)


    text_translate = ctk.CTkRadioButton(master=Audio_tab_scroll_frame,
                                   font=dky_fonts["Times_20"],
                                   text="TEXT translate",
                                   command=lambda :create_toplevel_with_icon(ctk_ui_root)
                                   )
    audio_btn.append(text_translate)
    # 单选框
    for i in range(0, 6):
        btn_num = ctk.CTkRadioButton(master=Audio_tab_scroll_frame,
                                     font=dky_fonts["Times_20"],
                                     text=audio_radio_options[i],
                                     value=audio_radio_options[i].split(" ")[0],
                                     variable=Audio_radio_var,
                                     command=lambda: audio_radiobutton_event(Audio_radio_var,indexes_all,textbox),
                                     )
        audio_btn.append(btn_num)

    for i in range(0, 7):
        audio_btn[i].grid(row=i, column=0, padx=15, pady=8, sticky="w")

    ####################################################################################
    ####################Theme_tab = tabview.tab("Theme")################################
    ####################################################################################
    frame2_3 = ctk.CTkFrame(master=tabview.tab("Theme"),
                            width=frame2_3_w,
                            height=frame2_3_y,
                            corner_radius=15,
                            )
    frame2_3.pack_propagate(False)
    frame2_3.pack(expand=False, fill="none", padx=0, pady=0)

    Theme_tab_scroll_frame = ctk.CTkScrollableFrame(master=frame2_3,
                                                    corner_radius=15,
                                                    width=Audio_tab_scrollframe_w,
                                                    )
    Theme_tab_scroll_frame.pack_propagate(False)
    Theme_tab_scroll_frame.pack(expand=False, fill="none", padx=2, pady=3)

    group = ExclusiveSwitchGroup()
    for i in range(0, 6):
        sw = ctk.CTkSwitch(master=Theme_tab_scroll_frame,
                           text=theme_app[i],
                           font=dky_fonts["Times_20"]
                           )
        if theme_app[i] == "System":  # default option
            sw.select()
        sw.grid(row=i // 2, column=i % 2, padx=15, pady=8, sticky="w")
        group.add(sw)

    ##################################################################################################################
    ########################################  P4  ####################################################################
    ##################################################################################################################

    segemented_button = ctk.CTkSegmentedButton(master=frame2,
                                               font=dky_fonts["Times_25"],
                                               dynamic_resizing=False,
                                               width=segemented_button_w,
                                               height=segemented_button_h,
                                               values=bottom_button_values,
                                               command=lambda value:
                                               segmented_button_callback(value, ctk_ui_root, frame2, frame3,
                                                                         segemented_button, bottom_button_values,
                                                                         indexes_all),
                                               )
    segemented_button.set(" End ")
    segemented_button.place(x=segemented_button_place_x,
                            y=segemented_button_place_y,
                            )

    ##################################################################################################################
    ########################################  frame3  ####################################################################
    ##################################################################################################################

    # Python 是动态语言,可以随时向任何对象添加属性
    frame3.checkbox_values = ["Original",
                              "Translate",
                              "Save",
                              "Edit",
                              ]
    frame3_1 = ctk.CTkScrollableFrame(master=frame3, corner_radius=15,
                                      width=frame3_1_w, height=frame3_1_h,
                                      )  #
    frame3_1.place(x=frame3_1_place_x, y=frame3_1_place_y, )  # anchor="nw")

    button_AIchat = ctk.CTkButton(master=frame3,
                                  width=button_AIchat_w,
                                  height=button_AIchat_h,
                                  text="AI chat",
                                  font=dky_fonts["Times_30"],
                                  command=lambda :button_aichat(root_main=ctk_ui_root)
                                  )
    button_AIchat.place(x=button_AIchat_place_x, y=button_AIchat_place_y, anchor="nw")

    # 循环创建复选框
    frame3.check_vars= {}
    for i, name in enumerate(frame3.checkbox_values):
        if i == 0:
            var = tk.IntVar(value=1)
        else:
            var = tk.IntVar(value=0)
        frame3.check_vars[name] = var
        cb = ctk.CTkCheckBox(
            master=frame3_1,
            text=name,
            font=dky_fonts["Times_15"],
            variable=var,
            onvalue=1,
            offvalue=0,
            command=lambda: combobox_callback(frame3,indexes_all),
            width=80,
            height=50
        )
        cb.grid(row=i + 2, column=0, padx=5, pady=8, sticky="w")


    button_more = ctk.CTkButton(master=frame3,
                                width=button_more_w,
                                height=button_more_h,
                                text="☰☰",
                                font=dky_fonts["Times_30"],
                                command=lambda: add_frame2(ctk_ui_root, frame2, frame3),
                                )
    button_more.place(x=button_more_place_x, y=button_more_place_y, anchor="nw")
    #
    # segmented_button_callback(" Hide ", ctk_ui_root, frame2, frame3, segemented_button, bottom_button_values)
    return ctk_ui_root


def on_close():

    # destory widgets
    xx = root_main.winfo_children()
    for x in xx:
        x.destroy()
    try:
        print(f"{__file__}: {on_close.__name__}")
        index_win2.destroy()  ######################
        index_win.destroy()  #############very important

    except tk.TclError as e:
        print(f"An error occurred: {e}")

    try:
        root_main.destroy()
    except tk.TclError as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    root_main = ctk_ui()
    root_main.protocol("WM_DELETE_WINDOW", on_close)
    root_main.mainloop()

#
# #
# def do_work_in_thread(name :str="xxx", count :int=5)->None:
#     # 这里是你后台要做的工作，比如调用 API
#     for i in range(0,10000,10):
#         sleep(3)
#         print(f"后台执行中:  {name} 工作中... {count}")
#         if break_flag[0] == False:
#             break
#     # result = some_long_task()
#     # print("后台完成：", result)
#
# #
# threads = []
# break_flag = [True,True,True]
# t1 = threading.Thread(target=do_work_in_thread,args=("线程A", 5), daemon=True)
# t1.start()
# threads.append(t1)
# t2 = threading.Thread(target=do_work_in_thread, daemon=True)
# t2.start()
#
# threads.append(t2)
# t3 = threading.Thread(target=do_work_in_thread, daemon=True)
# t3.start()
# threads.append(t3)
#
#
# def on_close():
#
#
#
#     # destory widgets
#     xx = root.winfo_children()
#     for x in xx:
#         x.destroy()
#     try:
#         print("111")
#         root.update()
#     except tk.TclError as e:
#         print(f"An error occurred: {e}")
#     try:
#          print("222")
#          index_win2.destroy()  ######################
#          index_win.destroy()   #############very important
#          root.destroy()
#     except tk.TclError as e:
#          print(f"An error occurred: {e}")
#
#     # kill threads
#     for i in range(len(threads)):
#          break_flag[i] = False
#     for t in threads:
#         t.join()
#
# root.protocol("WM_DELETE_WINDOW", on_close)
#
#

#
# segmented_button_callback( " Hide ", root, frame2, frame3,  segemented_button, bottom_button_values)
# root.mainloop()


