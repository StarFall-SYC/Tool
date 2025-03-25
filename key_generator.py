import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class KeyGeneratorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("密钥生成工具")
        self.window.geometry("400x300")
        
        # 创建主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 长度输入区域
        length_frame = ttk.LabelFrame(main_frame, text="密钥长度设置")
        length_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(length_frame, text="密钥长度(必须是4的倍数):").pack(side='left', padx=5)
        self.length_var = tk.StringVar(value="16")
        ttk.Entry(length_frame, textvariable=self.length_var, width=10).pack(side='left', padx=5)
        
        # 生成按钮
        ttk.Button(main_frame, text="生成密钥", command=self.generate).pack(pady=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="生成结果")
        result_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.result_text = tk.Text(result_frame, height=3, wrap='word')
        self.result_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 复制按钮
        ttk.Button(main_frame, text="复制密钥", command=self.copy_key).pack(pady=10)
        
        self.window.mainloop()
    
    def generate_key(self, length):
        if length % 4 != 0:
            raise ValueError("密钥长度必须是4的倍数")
        
        def generate_valid_group():
            # 确保每组包含至少一个数字和一个字母
            digits = ''.join(random.choices(string.digits, k=2))
            letters = ''.join(random.choices(string.ascii_lowercase, k=2))
            combined = list(digits + letters)
            random.shuffle(combined)
            return ''.join(combined)
        
        # 生成所需数量的有效分组
        groups = [generate_valid_group() for _ in range(length // 4)]
        raw_key = ''.join(groups)
        
        # 每4位插入连字符
        formatted_key = '-'.join([raw_key[i:i+4] for i in range(0, length, 4)])
        return formatted_key
    
    def generate(self):
        try:
            length = int(self.length_var.get())
            key = self.generate_key(length)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', key)
        except ValueError as e:
            messagebox.showerror("错误", str(e))
    
    def copy_key(self):
        key = self.result_text.get('1.0', tk.END).strip()
        if key:
            pyperclip.copy(key)
            messagebox.showinfo("成功", "密钥已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "请先生成密钥！")

if __name__ == '__main__':
    KeyGeneratorGUI()