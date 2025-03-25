import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import re

class RenameConfig:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文件夹重命名配置")
        self.window.geometry("800x600")
        
        # 创建左右分栏
        self.left_frame = ttk.Frame(self.window)
        self.left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        self.right_frame = ttk.Frame(self.window)
        self.right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # 创建预览列表
        self.preview_frame = ttk.LabelFrame(self.right_frame, text="重命名预览")
        self.preview_frame.pack(fill='both', expand=True)
        
        # 创建预览列表的滚动条
        preview_scroll = ttk.Scrollbar(self.preview_frame)
        preview_scroll.pack(side='right', fill='y')
        
        # 创建预览列表
        self.preview_list = ttk.Treeview(
            self.preview_frame,
            columns=('old_name', 'new_name'),
            show='headings',
            yscrollcommand=preview_scroll.set
        )
        self.preview_list.heading('old_name', text='原文件名')
        self.preview_list.heading('new_name', text='新文件名')
        self.preview_list.pack(fill='both', expand=True)
        
        preview_scroll.config(command=self.preview_list.yview)
        
        # 创建配置选项
        ttk.Label(self.left_frame, text="命名规则配置").pack(pady=10)
        
        # 前缀
        prefix_frame = ttk.Frame(self.left_frame)
        prefix_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(prefix_frame, text="前缀:").pack(side='left')
        self.prefix = tk.StringVar(value="")
        prefix_entry = ttk.Entry(prefix_frame, textvariable=self.prefix)
        prefix_entry.pack(side='left', fill='x', expand=True)
        prefix_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 数字起始值
        start_frame = ttk.Frame(self.left_frame)
        start_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(start_frame, text="起始数字:").pack(side='left')
        self.start_num = tk.StringVar(value="1")
        start_entry = ttk.Entry(start_frame, textvariable=self.start_num)
        start_entry.pack(side='left', fill='x', expand=True)
        start_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 数字位数
        digits_frame = ttk.Frame(self.left_frame)
        digits_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(digits_frame, text="数字位数:").pack(side='left')
        self.digits = tk.StringVar(value="1")
        digits_entry = ttk.Entry(digits_frame, textvariable=self.digits)
        digits_entry.pack(side='left', fill='x', expand=True)
        digits_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 后缀
        suffix_frame = ttk.Frame(self.left_frame)
        suffix_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(suffix_frame, text="后缀:").pack(side='left')
        self.suffix = tk.StringVar(value="")
        suffix_entry = ttk.Entry(suffix_frame, textvariable=self.suffix)
        suffix_entry.pack(side='left', fill='x', expand=True)
        suffix_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 添加保留原文件名选项
        keep_name_frame = ttk.Frame(self.left_frame)
        keep_name_frame.pack(fill='x', padx=20, pady=5)
        self.keep_original = tk.BooleanVar(value=False)
        ttk.Checkbutton(keep_name_frame, text="保留原文件名", variable=self.keep_original, command=self.update_preview).pack(side='left')
        
        # 添加自定义分隔符
        separator_frame = ttk.Frame(self.left_frame)
        separator_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(separator_frame, text="分隔符:").pack(side='left')
        self.separator = tk.StringVar(value="_")
        separator_entry = ttk.Entry(separator_frame, textvariable=self.separator)
        separator_entry.pack(side='left', fill='x', expand=True)
        separator_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 日期格式
        date_frame = ttk.Frame(self.left_frame)
        date_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(date_frame, text="日期格式:").pack(side='left')
        self.date_format = tk.StringVar(value="")
        date_entry = ttk.Entry(date_frame, textvariable=self.date_format)
        date_entry.pack(side='left', fill='x', expand=True)
        date_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        ttk.Label(date_frame, text="例如: %Y%m%d").pack(side='left')
        
        # 添加正则表达式替换
        regex_frame = ttk.LabelFrame(self.left_frame, text="正则表达式替换")
        regex_frame.pack(fill='x', padx=20, pady=5)
        
        # 匹配模式
        pattern_frame = ttk.Frame(regex_frame)
        pattern_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(pattern_frame, text="匹配:").pack(side='left')
        self.regex_pattern = tk.StringVar(value="")
        pattern_entry = ttk.Entry(pattern_frame, textvariable=self.regex_pattern)
        pattern_entry.pack(side='left', fill='x', expand=True)
        pattern_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 替换文本
        replace_frame = ttk.Frame(regex_frame)
        replace_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(replace_frame, text="替换为:").pack(side='left')
        self.regex_replace = tk.StringVar(value="")
        replace_entry = ttk.Entry(replace_frame, textvariable=self.regex_replace)
        replace_entry.pack(side='left', fill='x', expand=True)
        replace_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 排序选项
        sort_frame = ttk.LabelFrame(self.left_frame, text="排序方式")
        sort_frame.pack(fill='x', padx=20, pady=5)
        self.sort_method = tk.StringVar(value="name")
        ttk.Radiobutton(sort_frame, text="按名称", variable=self.sort_method, value="name", command=self.update_preview).pack(side='left')
        ttk.Radiobutton(sort_frame, text="按修改时间", variable=self.sort_method, value="mtime", command=self.update_preview).pack(side='left')
        ttk.Radiobutton(sort_frame, text="按大小", variable=self.sort_method, value="size", command=self.update_preview).pack(side='left')
        
        # 按钮框架
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(fill='x', padx=20, pady=20)
        
        # 预览按钮
        ttk.Button(button_frame, text="更新预览", command=self.update_preview).pack(side='left', padx=5)
        
        # 确认按钮
        ttk.Button(button_frame, text="开始重命名", command=self.start_rename).pack(side='left', padx=5)
        
        # 选择文件夹按钮
        ttk.Button(button_frame, text="选择文件夹", command=self.select_folder).pack(side='left', padx=5)
        
        # 撤销按钮
        ttk.Button(button_frame, text="撤销上次重命名", command=self.undo_rename).pack(side='left', padx=5)
        
        # 初始化文件列表和历史记录
        self.folders: List[str] = []
        self.folder_path = ""
        self.rename_history: List[Dict] = []
        
        # 绑定预览列表双击事件
        self.preview_list.bind('<Double-1>', self.edit_preview_item)
        
        self.config = None
        self.window.mainloop()
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="请选择包含要重命名文件夹的目录")
        if folder_path:
            self.folder_path = folder_path
            self.folders = []
            self.files = []
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    self.folders.append(item)
                elif os.path.isfile(item_path):
                    self.files.append(item)
            self.sort_items()
            self.update_preview()
    
    def sort_items(self):
        if not self.folders and not self.files:
            return
            
        if self.sort_method.get() == "name":
            self.folders.sort()
            self.files.sort()
        elif self.sort_method.get() == "mtime":
            self.folders.sort(key=lambda x: os.path.getmtime(os.path.join(self.folder_path, x)))
            self.files.sort(key=lambda x: os.path.getmtime(os.path.join(self.folder_path, x)))
        elif self.sort_method.get() == "size":
            self.folders.sort(key=lambda x: os.path.getsize(os.path.join(self.folder_path, x)))
            self.files.sort(key=lambda x: os.path.getsize(os.path.join(self.folder_path, x)))
    
    def update_preview(self, event=None):
        # 清空预览列表
        for item in self.preview_list.get_children():
            self.preview_list.delete(item)
        
        if not self.folders and not self.files:
            return
            
        try:
            start_num = int(self.start_num.get())
            digits = int(self.digits.get())
        except ValueError:
            messagebox.showerror("错误", "起始数字和位数必须是整数！")
            return
            
        current_num = start_num
        date_str = ""
        if self.date_format.get():
            date_str = datetime.now().strftime(self.date_format.get())
        
        # 处理文件夹
        for folder in self.folders:
            new_name = self.generate_new_name(folder, current_num, digits, date_str)
            self.preview_list.insert('', 'end', values=(folder, new_name))
            current_num += 1
            
        # 处理文件
        for file in self.files:
            new_name = self.generate_new_name(file, current_num, digits, date_str)
            self.preview_list.insert('', 'end', values=(file, new_name))
            current_num += 1
            
    def generate_new_name(self, original_name, number, digits, date_str):
        # 如果有正则表达式，先进行替换
        if self.regex_pattern.get() and self.regex_replace.get():
            try:
                original_name = re.sub(self.regex_pattern.get(), self.regex_replace.get(), original_name)
            except re.error:
                pass
        
        # 获取文件名和扩展名
        name_parts = os.path.splitext(original_name)
        base_name = name_parts[0]
        extension = name_parts[1] if len(name_parts) > 1 else ""
        
        # 构建新名称
        parts = []
        
        # 添加前缀
        if self.prefix.get():
            parts.append(self.prefix.get())
            
        # 添加日期
        if date_str:
            parts.append(date_str)
            
        # 添加数字
        parts.append(str(number).zfill(digits))
        
        # 添加原文件名
        if self.keep_original.get():
            parts.append(base_name)
            
        # 添加后缀
        if self.suffix.get():
            parts.append(self.suffix.get())
            
        # 使用分隔符连接所有部分
        new_name = self.separator.get().join(parts)
        
        # 添加扩展名（如果有）
        if extension:
            new_name += extension
            
        return new_name
    
    def edit_preview_item(self, event):
        # 获取选中的项
        item = self.preview_list.selection()[0]
        if not item:
            return
            
        # 获取当前值
        old_name, new_name = self.preview_list.item(item, 'values')
        
        # 创建编辑对话框
        dialog = tk.Toplevel(self.window)
        dialog.title("编辑文件名")
        dialog.geometry("400x100")
        
        # 添加输入框
        ttk.Label(dialog, text="新文件名:").pack(pady=5)
        name_var = tk.StringVar(value=new_name)
        entry = ttk.Entry(dialog, textvariable=name_var, width=50)
        entry.pack(pady=5)
        
        def update_name():
            # 更新预览列表中的名称
            self.preview_list.set(item, 'new_name', name_var.get())
            dialog.destroy()
        
        # 添加确认按钮
        ttk.Button(dialog, text="确认", command=update_name).pack(pady=5)
        
        # 设置对话框为模态
        dialog.transient(self.window)
        dialog.grab_set()
        self.window.wait_window(dialog)
    
    def start_rename(self):
        if not self.folders and not self.files:
            messagebox.showwarning("警告", "请先选择要重命名的文件或文件夹！")
            return
            
        # 获取预览列表中的新旧文件名对应关系
        rename_pairs = []
        for item in self.preview_list.get_children():
            old_name, new_name = self.preview_list.item(item)['values']
            if old_name != new_name:  # 只处理名称发生变化的项
                rename_pairs.append((old_name, new_name))
                
        if not rename_pairs:
            messagebox.showinfo("提示", "没有需要重命名的项目！")
            return
            
        # 检查是否有重复的新文件名
        new_names = [pair[1] for pair in rename_pairs]
        if len(new_names) != len(set(new_names)):
            messagebox.showerror("错误", "检测到重复的新文件名，请修改后重试！")
            return
            
        # 执行重命名操作
        success_count = 0
        rename_history = []
        
        for old_name, new_name in rename_pairs:
            old_path = os.path.join(self.folder_path, old_name)
            new_path = os.path.join(self.folder_path, new_name)
            
            try:
                os.rename(old_path, new_path)
                success_count += 1
                rename_history.append({
                    'old_path': old_path,
                    'new_path': new_path
                })
            except Exception as e:
                messagebox.showerror("错误", f"重命名 {old_name} 失败：{str(e)}")
                
        # 保存重命名历史记录
        if rename_history:
            self.rename_history.append(rename_history)
            
        # 更新文件列表
        self.folders = []
        self.files = []
        for item in os.listdir(self.folder_path):
            item_path = os.path.join(self.folder_path, item)
            if os.path.isdir(item_path):
                self.folders.append(item)
            elif os.path.isfile(item_path):
                self.files.append(item)
        
        self.sort_items()
        self.update_preview()
        
        messagebox.showinfo("成功", f"成功重命名 {success_count} 个项目！")
    
    def undo_rename(self):
        if not self.rename_history:
            messagebox.showinfo("提示", "没有可撤销的重命名操作")
            return
            
        last_operation = self.rename_history.pop()
        try:
            for old_name, new_name in last_operation.items():
                old_path = os.path.join(self.folder_path, old_name)
                new_path = os.path.join(self.folder_path, new_name)
                if os.path.exists(new_path):
                    os.rename(new_path, old_path)
            messagebox.showinfo("成功", "已撤销上次重命名操作")
            self.folders = [f for f in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, f))]
            self.sort_folders()
            self.update_preview()
        except Exception as e:
            messagebox.showerror("错误", f"撤销操作失败：{str(e)}")

def rename_files():
    # 获取命名规则配置
    config_window = RenameConfig()
    if not config_window.config:
        return
        
    folder_path = config_window.config['folder_path']
    if not folder_path:
        return
    
    try:
        # 使用已排序的文件夹列表
        folders = config_window.config['folders']
        
        # 记录重命名的文件夹数量和历史记录
        count = 0
        rename_history = {}
        
        # 遍历所有文件夹进行重命名
        for index, foldername in enumerate(folders, start=1):
            # 生成新文件夹名
            number = str(index + config_window.config['start_num'] - 1).zfill(config_window.config['digits'])
            date_str = ''
            if config_window.config['date_format']:
                try:
                    date_str = datetime.now().strftime(config_window.config['date_format'])
                except ValueError as e:
                    messagebox.showerror("错误", f"日期格式无效: {str(e)}")
                    return
            
            # 构建新名称
            parts = []
            if config_window.config['prefix']:
                parts.append(config_window.config['prefix'])
            if date_str:
                parts.append(date_str)
            if config_window.config['keep_original']:
                parts.append(foldername)
            parts.append(number)
            if config_window.config['suffix']:
                parts.append(config_window.config['suffix'])
            
            # 使用分隔符连接所有部分
            new_name = config_window.config['separator'].join(filter(None, parts))
            
            # 构建完整的文件夹路径
            old_path = os.path.join(folder_path, foldername)
            new_path = os.path.join(folder_path, new_name)
            
            # 如果新文件夹名已存在，跳过该文件夹
            if os.path.exists(new_path) and old_path != new_path:
                print(f"跳过文件夹 {foldername}，因为 {new_name} 已存在")
                continue
            
            # 重命名文件夹
            os.rename(old_path, new_path)
            rename_history[foldername] = new_name
            count += 1
            print(f"已将文件夹 {foldername} 重命名为 {new_name}")
        
        # 保存重命名历史记录
        if rename_history:
            config_window.rename_history.append(rename_history)
        
        messagebox.showinfo("完成", f"成功重命名 {count} 个文件夹！")
        
    except Exception as e:
        messagebox.showerror("错误", f"重命名过程中发生错误：{str(e)}")

if __name__ == "__main__":
    rename_files()