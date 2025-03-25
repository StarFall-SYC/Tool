import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pyautogui
import pyperclip
import time
import threading

class WeChatBoomGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("微信消息发送工具")
        self.window.geometry("600x500")
        
        # 创建主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 消息输入区域
        message_frame = ttk.LabelFrame(main_frame, text="消息内容")
        message_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 消息输入框
        self.message_text = scrolledtext.ScrolledText(message_frame, height=10)
        self.message_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="发送设置")
        settings_frame.pack(fill='x', padx=5, pady=5)
        
        # 发送次数设置
        count_frame = ttk.Frame(settings_frame)
        count_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(count_frame, text="发送次数:").pack(side='left')
        self.count_var = tk.StringVar(value="1")
        ttk.Entry(count_frame, textvariable=self.count_var, width=10).pack(side='left', padx=5)
        
        # 发送间隔设置
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(interval_frame, text="发送间隔(秒):").pack(side='left')
        self.interval_var = tk.StringVar(value="0.1")
        ttk.Entry(interval_frame, textvariable=self.interval_var, width=10).pack(side='left', padx=5)
        
        # 进度显示
        progress_frame = ttk.LabelFrame(main_frame, text="发送进度")
        progress_frame.pack(fill='x', padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', padx=5, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="就绪")
        self.progress_label.pack(padx=5, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="导入文件", command=self.load_file).pack(side='left', padx=5)
        ttk.Button(button_frame, text="开始发送", command=self.start_sending).pack(side='left', padx=5)
        ttk.Button(button_frame, text="停止发送", command=self.stop_sending).pack(side='left', padx=5)
        
        # 发送状态
        self.is_sending = False
        
        self.window.mainloop()
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="选择文本文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.message_text.delete('1.0', tk.END)
                self.message_text.insert('1.0', content)
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件：{str(e)}")
    
    def start_sending(self):
        if self.is_sending:
            return
        
        message = self.message_text.get('1.0', tk.END).strip()
        if not message:
            messagebox.showwarning("警告", "请输入要发送的消息内容！")
            return
        
        try:
            count = int(self.count_var.get())
            interval = float(self.interval_var.get())
            if count <= 0 or interval < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "请输入有效的发送次数和间隔时间！")
            return
        
        # 开始发送
        self.is_sending = True
        threading.Thread(target=self.send_messages, args=(message, count, interval)).start()
    
    def stop_sending(self):
        self.is_sending = False
        self.progress_label.config(text="已停止")
    
    def send_messages(self, message, count, interval):
        try:
            # 复制消息到剪贴板
            pyperclip.copy(message)
            
            for i in range(count):
                if not self.is_sending:
                    break
                
                # 发送消息
                pyautogui.hotkey("ctrl", "v")
                pyautogui.press("enter")
                
                # 更新进度
                progress = (i + 1) / count * 100
                self.progress_var.set(progress)
                self.progress_label.config(text=f"正在发送: {i + 1}/{count}")
                
                # 等待间隔时间
                time.sleep(interval)
            
            if self.is_sending:
                self.progress_label.config(text="发送完成")
        except Exception as e:
            messagebox.showerror("错误", f"发送过程中出错：{str(e)}")
        finally:
            self.is_sending = False

if __name__ == "__main__":
    WeChatBoomGUI()