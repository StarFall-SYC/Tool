import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import chardet
import os

class TextIndentTool:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文本缩进工具")
        self.window.geometry("800x600")
        
        # 创建主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 创建左侧选项区域
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # 文件选择按钮
        self.file_path = tk.StringVar()
        ttk.Button(left_frame, text="选择文件", command=self.select_file).pack(fill='x', pady=5)
        ttk.Button(left_frame, text="选择文件夹", command=self.select_folder).pack(fill='x', pady=5)
        
        # 缩进选项
        indent_frame = ttk.LabelFrame(left_frame, text="缩进选项")
        indent_frame.pack(fill='x', pady=5)
        
        # 缩进空格数
        self.indent_spaces = tk.IntVar(value=4)
        ttk.Label(indent_frame, text="缩进空格数:").pack(pady=2)
        ttk.Entry(indent_frame, textvariable=self.indent_spaces, width=10).pack(pady=2)
        
        # 保留空行选项
        self.keep_empty_lines = tk.BooleanVar(value=True)
        ttk.Checkbutton(indent_frame, text="保留空行", variable=self.keep_empty_lines).pack(pady=2)
        
        # 保存选项
        save_frame = ttk.LabelFrame(left_frame, text="保存选项")
        save_frame.pack(fill='x', pady=5)
        
        self.save_mode = tk.StringVar(value="original")
        ttk.Radiobutton(save_frame, text="保存到原文件", variable=self.save_mode, 
                       value="original").pack(pady=2)
        ttk.Radiobutton(save_frame, text="保存为新文件", variable=self.save_mode, 
                       value="new").pack(pady=2)
        
        # 创建右侧主要区域
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # 文件路径显示
        path_frame = ttk.Frame(right_frame)
        path_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(path_frame, text="当前文件:").pack(side='left')
        ttk.Label(path_frame, textvariable=self.file_path).pack(side='left', fill='x', expand=True)
        
        # 创建预览区域
        preview_frame = ttk.LabelFrame(right_frame, text="预览")
        preview_frame.pack(fill='both', expand=True)
        
        # 添加滚动条
        scroll = ttk.Scrollbar(preview_frame)
        scroll.pack(side='right', fill='y')
        
        # 文本预览框
        self.preview_text = tk.Text(preview_frame, wrap='word', yscrollcommand=scroll.set,
                                   font=('Consolas', 10), spacing1=2, spacing2=2,
                                   selectbackground='#0078D7', selectforeground='white',
                                   padx=5, pady=5)
        self.preview_text.pack(fill='both', expand=True)
        scroll.config(command=self.preview_text.yview)
        
        # 绑定缩进选项变更事件
        self.indent_spaces.trace_add('write', lambda *args: self.update_preview())
        self.keep_empty_lines.trace_add('write', lambda *args: self.update_preview())
        
        # 底部按钮区域
        bottom_frame = ttk.Frame(right_frame)
        bottom_frame.pack(fill='x', pady=(5, 0))
        
        # 处理按钮
        ttk.Button(bottom_frame, text="处理文本", command=self.process_text).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="撤销", command=self.undo).pack(side='left', padx=5)
        
        # 初始化历史记录
        self.history = []
        self.current_file = None
        self.batch_files = []
        
        self.window.mainloop()
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择文本文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            self.current_file = file_path
            self.batch_files = []
            self.load_preview(file_path)
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择文件夹")
        if folder_path:
            self.batch_files = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.txt'):
                        self.batch_files.append(os.path.join(root, file))
            if self.batch_files:
                self.current_file = self.batch_files[0]
                self.file_path.set(f"已选择 {len(self.batch_files)} 个文件")
                self.load_preview(self.current_file)
            else:
                messagebox.showinfo("提示", "所选文件夹中没有找到文本文件")
    
    def detect_encoding(self, file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    
    def load_preview(self, file_path):
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', content)
            self.history = [content]  # 初始化历史记录
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件：{str(e)}")
    
    def undo(self):
        if len(self.history) > 1:
            self.history.pop()  # 移除当前状态
            previous_content = self.history[-1]  # 获取上一个状态
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', previous_content)
    
    def process_text(self):
        if not self.current_file and not self.batch_files:
            messagebox.showwarning("警告", "请先选择文件！")
            return
        
        try:
            files_to_process = self.batch_files if self.batch_files else [self.current_file]
            processed_count = 0
            
            for file_path in files_to_process:
                # 读取文件内容
                encoding = self.detect_encoding(file_path)
                with open(file_path, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                
                # 处理文本
                processed_lines = []
                for line in lines:
                    line = line.rstrip()  # 移除行尾空白字符
                    if line or self.keep_empty_lines.get():  # 根据选项决定是否保留空行
                        processed_lines.append(' ' * self.indent_spaces.get() + line if line else '')
                
                # 合并处理后的文本
                processed_text = '\n'.join(processed_lines)
                
                # 根据保存模式选择保存路径
                if self.save_mode.get() == "new":
                    file_path_obj = Path(file_path)
                    new_path = file_path_obj.parent / f"{file_path_obj.stem}_processed{file_path_obj.suffix}"
                    if len(files_to_process) == 1:
                        save_path = filedialog.asksaveasfilename(
                            title="保存文件",
                            initialfile=new_path,
                            defaultextension=".txt",
                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                        )
                        if not save_path:
                            return
                    else:
                        save_path = str(new_path)
                else:
                    save_path = file_path
                
                # 保存处理后的文本
                with open(save_path, 'w', encoding=encoding) as f:
                    f.write(processed_text)
                processed_count += 1
                
                # 如果是当前预览的文件，更新预览和历史记录
                if file_path == self.current_file:
                    self.preview_text.delete('1.0', tk.END)
                    self.preview_text.insert('1.0', processed_text)
                    self.history.append(processed_text)
            
            # 显示处理完成消息
            if len(files_to_process) > 1:
                messagebox.showinfo("成功", f"已处理 {processed_count} 个文件！")
            else:
                messagebox.showinfo("成功", "文本处理完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"处理文件时出错：{str(e)}")

if __name__ == "__main__":
    TextIndentTool()