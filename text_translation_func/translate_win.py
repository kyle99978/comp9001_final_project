import customtkinter as ctk
from tkinter import messagebox
from translate_deepl_API.deep_api_in import translate_text

# init CTk
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
# 禁用 DPI 自动适配（一般不建议），是否使用系统 DPI 缩放设置（比如 125%、150%）来自动放大界面
# Disable DPI auto-adaptation (generally not recommended),
# whether to use system DPI zoom settings (e.g. 125%, 150%) to automatically zoom the interface
ctk.deactivate_automatic_dpi_awareness()

class TranslatorWindow(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("DUAN_translating")
        self.attributes('-topmost', 1)  # 置顶窗口

        # 计算居中并偏下的位置
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.root = root

        window_width = 1000
        window_height = 500
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2) + 50  # 向下偏移50像素/// Offset 50 pixels down
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.minsize(800, 500)
        self.configure(padx=20, pady=20)

        self.language_mode = "中文"

        self.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(2, weight=1)

        # 顶部控制区
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        self.top_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.source_lang_menu = ctk.CTkOptionMenu(
            self.top_frame, width=150,  command=self.check_language_selection ,
            values=["中文/Chinese(ZH)", "英语/English(EN)", "日语/Japanese(JA)", "韩语/Korean(KO)", "法语/French(FR)",
                    "德语/German(DU)"],
        )
        self.source_lang_menu.set("源语言")
        self.source_lang_menu.grid(row=0, column=0, sticky="ws", pady=(15,0),padx=(5, 0),columnspan=2)

        self.tip_label = ctk.CTkLabel(self.top_frame, text="按 Shift+Enter 翻译", font=("Times New Roman", 14))
        self.tip_label.grid(row=0, column=1, sticky="s", padx=(25, 0))

        self.target_lang_menu = ctk.CTkOptionMenu(
            self.top_frame, width=150, command=self.check_language_selection ,
            values=["中文/Chinese(ZH)", "英语/English(EN)", "日语/Japanese(JA)", "韩语/Korean(KO)", "法语/French(FR)",
                    "德语/German(DU)"],
        )
        self.target_lang_menu.set("目标语言")
        self.target_lang_menu.grid(row=0, column=3, sticky="ws", pady=(15, 0),padx=(25, 0),columnspan=2,)

        self.lang_switch = ctk.CTkSwitch(self.top_frame, text="英文/中文", command=self.toggle_language, switch_width=60, switch_height=30)
        self.lang_switch.grid(row=0, column=4, sticky="se", padx=(5, 15))

        self.theme_switch = ctk.CTkSwitch(self.top_frame, text="切换主题", command=self.toggle_theme, switch_width=60, switch_height=30)
        self.theme_switch.grid(row=0, column=5, sticky="se", padx=(5, 15))

        # 顶部分隔线
        self.separator = ctk.CTkFrame(self, height=2, fg_color="gray")
        self.separator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        # 输入输出文本框
        self.input_text = ctk.CTkTextbox(self, font=("Times New Roman", 14), wrap="word")
        self.input_text.grid(row=2, column=0, sticky="nsew", padx=(0, 1), pady=(0, 0))
        self.input_text.bind("<Shift-Return>", self.start_translation)

        self.output_text = ctk.CTkTextbox(self, font=("Times New Roman", 14), wrap="word")
        self.output_text.grid(row=2, column=1, sticky="nsew", padx=(1, 0), pady=(0, 0))


        # 统计栏
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        self.stats_frame.grid_columnconfigure((0,2), weight=1)

        # api options
        self.api_options = ctk.CTkOptionMenu(self.stats_frame, values=["deepl","baidu","google","microsoft"])
        self.api_options.set("API")
        self.api_options.grid(row=0, column=1, sticky="ew", )


        self.input_stats_label = ctk.CTkLabel(self.stats_frame, text="输入字数: 0", anchor="center")
        self.input_stats_label.grid(row=0, column=0, sticky="ew")

        self.output_stats_label = ctk.CTkLabel(self.stats_frame, text="输出字数: 0", anchor="center")
        self.output_stats_label.grid(row=0, column=2, sticky="ew")

        self.input_text.bind("<KeyRelease>", self.update_word_count)
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    def check_language_selection(self, event=None):
        source_lang = self.source_lang_menu.get()
        target_lang = self.target_lang_menu.get()

        # 提取标准语言代码
        source_lang_code = source_lang.split("(")[-1].strip(")")
        target_lang_code = target_lang.split("(")[-1].strip(")")

        if source_lang_code == target_lang_code:
            # 如果一致，设置目标语言为 None
            self.target_lang_menu.set("None")
        else:
            # 如果之前是 None 但现在不一致了，恢复原来选项
            if self.target_lang_menu.get() == "None":
                # 这里可以自动恢复默认提示，也可以不动，根据需要
                if self.language_mode == "中文":
                    self.target_lang_menu.set("目标语言")
                else:
                    self.target_lang_menu.set("Target Language")



    def update_word_count(self, event=None):
        input_text = self.input_text.get("1.0", "end-1c")
        output_text = self.output_text.get("1.0", "end-1c")
        self.input_stats_label.configure(text=f"{self.input_stats_label.cget('text').split(': ')[0]}: {len(input_text)}")
        self.output_stats_label.configure(text=f"{self.output_stats_label.cget('text').split(': ')[0]}: {len(output_text)}")

    def start_translation(self, event=None):
        source = self.source_lang_menu.get()[-3:-1]
        tar = self.target_lang_menu.get()[-3:-1]
        translate_api=self.api_options.get()
        print(source, tar)
        if source=="ZH" and tar=="EN" and translate_api=="deepl":
            source_text = self.input_text.get("1.0", "end-1c").strip()
            if not source_text:
                messagebox.showwarning("Error", "Invalid input !")
                return


            self.output_text.delete("1.0", "end")

            # translated_text = f"[翻译自 {source_lang} 到 {target_lang}]\n{source_text[::-1]}"
            translated_text = translate_text(source_text,target_lang="EN")

            self.output_text.insert("1.0", translated_text)

            self.update_word_count()
        else:
            messagebox.showwarning("Error", "Currently only support ZH to EN translation via deepl's api!")
            return

    def toggle_language(self):
        if self.language_mode == "中文":
            self.language_mode = "English"
            # self.title("Instant Translator")
            self.source_lang_menu.set("Source Language")
            self.target_lang_menu.set("Target Language")
            self.tip_label.configure(text="Press Shift+Enter to translate")
            self.input_stats_label.configure(text="Input Characters: 0")
            self.output_stats_label.configure(text="Output Characters: 0")
            self.update_word_count()
            self.lang_switch.configure(text="EN/ZH")
            self.theme_switch.configure(text="Switch Theme")
        else:
            self.language_mode = "中文"
            # self.title("即时翻译器")
            self.source_lang_menu.set("源语言")
            self.target_lang_menu.set("目标语言")
            self.tip_label.configure(text="按 Shift+Enter 翻译")
            self.input_stats_label.configure(text="输入字数: 0")
            self.output_stats_label.configure(text="输出字数: 0")
            self.update_word_count()
            self.lang_switch.configure(text="英文/中文")
            self.theme_switch.configure(text="切换主题")

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
    def _on_close(self):
        self.destroy()
        # self.master.deiconify()
        # self.master.destroy()
        # self.root.quit()


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    app = TranslatorWindow(root)
    app.mainloop()
