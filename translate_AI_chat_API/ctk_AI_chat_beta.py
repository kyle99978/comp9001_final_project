import os
from time import sleep

import tkinterweb as TKweb
import threading

from gui_utils.kyle_ui_font import dky_fonts
from translate_AI_chat_API.check_available_models import get_available_models
from translate_AI_chat_API.ctk_AI_funcs import *
from translate_AI_chat_API.muti_chat import chat_with_gpt

user_input ="kyle_825"
ai_answer = ""
lock_ai_respond = threading.Lock()
model_name_thisfile = "gpt-3.5-turbo"
answer_isok = False
off_chat=False

def chat_with_gpt_api_kyle():

    api_key = 'your key'  # Replace it with your API key
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    try:
        while True:
            sleep(1)
            with ((lock_ai_respond)):
                if off_chat:
                    print("T-4 thread is killed")
                    break
                print("t4 is alive")
                global user_input,ai_answer,answer_isok
                if  user_input != "kyle_825":
                    print("sending to ai")
                    user_input = (f"你好，请按照markdown格式给我回复,而且回答的每一行的字符不要超过80字符，如果超过请换行。\
                                   （你不需要特意回复这句话，但是必须记住而且严格执行。\
                                  着重的是我后面的,回答的语言也是和我这句无关,你应该根据后面的内容判断。）这句和这句话之前都是我的AI提示词。\n\n")\
                                 + user_input

                    messages.append({"role": "user", "content": user_input})
                    global model_name_thisfile
                    response = chat_with_gpt(messages, api_key,model_name_thisfile)
                    if "error" in response:
                        print(response)
                        assistant_reply = str(response["error"]["message"]) + "\n您也可以选择使用其他它模型。\nYou can choose other model."
                        print(f"Assistant: {assistant_reply}")
                    else:
                        assistant_reply = response['choices'][0]['message']['content']
                        print(f"Assistant: {assistant_reply}")
                    ai_answer = assistant_reply
                    answer_isok = True
                    messages.append({"role": "assistant", "content": assistant_reply})
                    user_input = "kyle_825"
                else:
                    pass

    except Exception as e:
        print(f"Exception in thread: {e}")



# 初始化CustomTkinter应用   Initialising the CustomTkinter application
ctk.set_appearance_mode("System")  # Appearance: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Theme color: "blue", "dark-blue", "green"
def chat_win_ui(root_main):

    root_top = ctk.CTkToplevel(root_main)
    root_top.title("AI chat window")

    icon_path = r"./img/plane_icon_128.ico"
    root_top=create_toplevel_with_icon(root_top,icon_path)
    root_top.update()


    screen_width = root_top.winfo_screenwidth()
    screen_height = root_top.winfo_screenheight()
    wid=1200
    hei=500
    x = (screen_width - wid) // 2
    y = (screen_height - hei) // 2
    root_top.geometry(f"{wid}x{hei}+{x}+{y}")

    root_top.grid_rowconfigure(0, weight=1)
    root_top.grid_rowconfigure(1, weight=1)
    root_top.grid_rowconfigure(2, weight=1)
    root_top.grid_columnconfigure(0, weight=1)



    # 回答窗口 answer window
    output_frame = ctk.CTkFrame(root_top, corner_radius=10, fg_color="#999999")
    output_frame.grid(row=0,  rowspan=2,column=0, columnspan=8, sticky="nsew", padx=10, pady=10)

    output_html_frame = TKweb.HtmlFrame(output_frame, messages_enabled = False, # fetch_external_styles=False,
                                        vertical_scrollbar="auto",
                                        )
    # 默认用 CSS 控制溢出行为，必须显式指定 overflow-x: auto 才有效果
    # 没有水平滚动条，内部机制的问题,horizontal_scrollbar="auto" 这个参数目前 没有被 HtmlFrame 真正实现
    # Overflow behaviour is controlled by CSS by default, overflow-x: auto must be explicitly specified to have any effect.
    # No horizontal scrollbar, internal mechanism, horizontal_scrollbar="auto" parameter is not implemented by HtmlFrame.

    output_html_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # 回答窗口2 answer window2
    output_frame2 = ctk.CTkTextbox(root_top, corner_radius=10,height=380,)
    # output_frame2.grid(row=0, column=0, columnspan=8, sticky="nsew", padx=10, pady=10)





    # 发送窗口
    input_text = ctk.CTkTextbox(root_top, wrap="none", )
    input_text.grid(row=2, rowspan=1, column=0, columnspan=8, sticky="nsew", padx=10, pady=0)

    # initial
    convert_markdown(root_top,output_html_frame,output_frame2, ai_answer=" ", index=1)
    root_top.update()

    def select_model_on_click(val):
        with lock_ai_respond:
            global model_name_thisfile,switch_model
            print(f"your model is : {val}")
            model_name_thisfile = str(val)
            # print(f"your model is : {model_name_thisfile}")
            switch_model=True

    # model select
    models = get_available_models()
    models = list(set(models))
    models.sort()
    option_model = ctk.CTkOptionMenu(root_top, values=models, font=dky_fonts["Times_15"],
                                     command=lambda val: select_model_on_click(val),
                                     width=220, height=30,
                                     )
    option_model.grid(row=4, column=0,   sticky="w", padx=5, pady=10)
    option_model.set("gpt-3.5-turbo")



    # 修改复选框  # 添加两个变量
    # Modify the checkbox # Add two variables
    var1 = ctk.IntVar()
    var2 = ctk.IntVar()
    def _button1_command():
        text_or_mdtext1(root_top, output_frame,output_frame2,var2)

    def _button2_command():
        text_or_mdtext2(root_top, output_frame,output_frame2,var1)
        pass
    _button1 = ctk.CTkCheckBox(root_top, text="TEXT", variable=var1, font=dky_fonts["Times_20"],
                                      command=_button1_command ,
                                      width=50, height=50)
    _button1.grid(row=4, column=1, padx=5, pady=10)

    _button2 = ctk.CTkCheckBox(root_top, text="MD VIEW", variable=var2, font=dky_fonts["Times_20"],
                                      command=_button2_command,
                                 width=50, height=50)
    _button2.grid(row=4, column=2, padx=5, pady=10)
    _button2.select()






    # 中部：转换按钮
    # Centre: changeover button
    convert_button = ctk.CTkButton(root_top, text="SAVE", font=dky_fonts["Times_20"],
                                   width=80, height=50)
    # convert_button.grid(row=3, column=5, padx=10, pady=10)

    def update_web():
        print("get answer, doing update web")
        num_res=1
        while True:
            sleep(0.01)
            with lock_ai_respond:
                global ai_answer
                if ai_answer != "":
                    convert_markdown(root_top,output_html_frame,output_frame2, ai_answer, index=2)
                    root_top.update()
                    ai_answer = ""
                    break
                else:
                    pass



    # send button
    def send_button_on_click():
        print("send button clicked")
        get_text = get_text_from_user(root_top, input_text)
        print("had got input text")
        if get_text !="":
            convert_markdown(root_top, output_html_frame, output_frame2, ai_answer="#AI responding....", index=2)
            root_top.update()
            with lock_ai_respond:
                global user_input
                user_input = get_text
            print("xxxxxxxxxxx")
            update_web()
        else:
            convert_markdown(root_top, output_html_frame, output_frame2, ai_answer="#Invalid input", index=2)
            root_top.update()

    send_button = ctk.CTkButton(root_top, text="  ⮝  ", font=("Times New Roman",40,"bold"),
                                   command=send_button_on_click,
                                   width=80, height=50)
    send_button.grid(row=4, column=6, padx=10, pady=10,sticky="nswe")

    root_top.bind("<Return>", lambda event: send_button.invoke())


    def on_close():
        global lock_ai_respond
        with lock_ai_respond:
           global off_chat
           off_chat = True
        # destory widgets
        xx = root_top.winfo_children()
        for x in xx:
            x.destroy()
        root_top.destroy()
        # root_top.quit()
        # 在 Tkinter 里：
        # quit() 是用来终止整个 Tkinter 事件循环的！
        # 无论 top.quit() 还是 root.quit()，都会结束整个 root.mainloop()，导致整个应用退出。
        # In Tkinter:
        # quit() is used to terminate the entire Tkinter event loop!
        # Either top.quit() or root.quit() will end the entire root.mainloop(), causing the entire application to exit.
        root_top.master.deiconify()





    root_top.protocol("WM_DELETE_WINDOW", on_close)
    return root_top




def root_top_close():
    global lock_ai_respond
    with lock_ai_respond:
       global off_chat
       off_chat = True

    root_top.destroy()
    # root_top.quit()
    print("root0 quit")

if __name__ == "__main__":
    #
    t4 = threading.Thread(target=chat_with_gpt_api_kyle, daemon=True)
    t4.start()
    # # 创建主窗口
    root0 = ctk.CTk()
    root0.withdraw()

    root_top =  chat_win_ui(root0)


    root_top.protocol("WM_DELETE_WINDOW", root_top_close)
    root_top.mainloop()


