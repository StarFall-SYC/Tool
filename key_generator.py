import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class KeyGeneratorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("密钥生成工具")
        self.window.geometry("500x500")
        
        # 创建主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 长度输入区域
        length_frame = ttk.LabelFrame(main_frame, text="密钥长度设置")
        length_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(length_frame, text="密钥长度:").pack(side='left', padx=5)
        self.length_var = tk.StringVar(value="16")
        ttk.Entry(length_frame, textvariable=self.length_var, width=10).pack(side='left', padx=5)
        
        # 字符类型选择区域
        char_frame = ttk.LabelFrame(main_frame, text="字符类型选择")
        char_frame.pack(fill='x', padx=5, pady=5)
        
        self.use_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(char_frame, text="数字", variable=self.use_digits).pack(side='left', padx=5)
        
        self.use_lowercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(char_frame, text="小写字母", variable=self.use_lowercase).pack(side='left', padx=5)
        
        self.use_uppercase = tk.BooleanVar(value=False)
        ttk.Checkbutton(char_frame, text="大写字母", variable=self.use_uppercase).pack(side='left', padx=5)
        
        self.use_special = tk.BooleanVar(value=False)
        ttk.Checkbutton(char_frame, text="特殊字符", variable=self.use_special).pack(side='left', padx=5)
        
        # 分组设置区域
        group_frame = ttk.LabelFrame(main_frame, text="分组设置")
        group_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(group_frame, text="每组字符数:").pack(side='left', padx=5)
        self.group_size_var = tk.StringVar(value="4")
        ttk.Entry(group_frame, textvariable=self.group_size_var, width=5).pack(side='left', padx=5)
        
        ttk.Label(group_frame, text="连字符:").pack(side='left', padx=5)
        self.separator_var = tk.StringVar(value="-")
        ttk.Entry(group_frame, textvariable=self.separator_var, width=5).pack(side='left', padx=5)
        
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
        if length < 1:
            raise ValueError("密钥长度必须大于0")
        
        # 构建字符集
        chars = ''
        if self.use_digits.get():
            chars += string.digits
        if self.use_lowercase.get():
            chars += string.ascii_lowercase
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_special.get():
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        if not chars:
            raise ValueError("请至少选择一种字符类型")
        
        # 生成随机字符串
        raw_key = ''.join(random.choices(chars, k=length))
        
        try:
            # 获取分组大小
            group_size = int(self.group_size_var.get())
            if group_size <= 0:
                raise ValueError
            
            # 获取分隔符
            separator = self.separator_var.get()
            
            # 按指定大小分组
            groups = [raw_key[i:i+group_size] for i in range(0, len(raw_key), group_size)]
            formatted_key = separator.join(groups)
            return formatted_key
        except ValueError:
            # 如果分组设置无效，直接返回未分组的密钥
            return raw_key
    
    def generate(self):
        try:
            length = int(self.length_var.get())
            key = self.generate_key(length)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', key)
        except ValueError as e:
            if str(e) == "密钥长度必须大于0" or str(e) == "请至少选择一种字符类型":
                messagebox.showerror("错误", str(e))
            else:
                messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"生成密钥时出错：{str(e)}")

    
    def copy_key(self):
        key = self.result_text.get('1.0', tk.END).strip()
        if key:
            pyperclip.copy(key)
            messagebox.showinfo("成功", "密钥已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "请先生成密钥！")

if __name__ == '__main__':
    KeyGeneratorGUI()