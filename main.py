
import customtkinter as ctk
import tkinter as tk
from gui_utils.kyle_ctk_ui import ctk_ui, index_win2, index_win

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
        root_main.quit()
    except tk.TclError as e:
        print(f"An error occurred: {e}")


if __name__=="__main__":
    root_main = ctk_ui()
    root_main.protocol("WM_DELETE_WINDOW", on_close)
    root_main.mainloop()


