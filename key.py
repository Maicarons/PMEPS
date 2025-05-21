import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256


class SQLiteEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite 文件加密解密工具")

        # 设置窗口大小和位置
        window_width = 500
        window_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # 密码输入
        self.password_label = tk.Label(root, text="密码:")
        self.password_label.pack(pady=(20, 5))

        self.password_entry = tk.Entry(root, show="*", width=40)
        self.password_entry.pack()

        # 文件选择按钮
        self.file_button = tk.Button(root, text="选择 SQLite 文件", command=self.select_file)
        self.file_button.pack(pady=20)

        # 文件路径显示
        self.file_path = tk.StringVar()
        self.file_label = tk.Label(root, textvariable=self.file_path, wraplength=400)
        self.file_label.pack()

        # 加密解密按钮
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.encrypt_button = tk.Button(self.button_frame, text="加密文件", command=self.encrypt_file)
        self.encrypt_button.pack(side=tk.LEFT, padx=10)

        self.decrypt_button = tk.Button(self.button_frame, text="解密文件", command=self.decrypt_file)
        self.decrypt_button.pack(side=tk.LEFT, padx=10)

        # 状态标签
        self.status = tk.StringVar()
        self.status_label = tk.Label(root, textvariable=self.status, fg="blue")
        self.status_label.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择 SQLite 文件",
            filetypes=[("SQLite 数据库", "*.db *.sqlite *.sqlite3"), ("所有文件", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            self.status.set("已选择文件: " + os.path.basename(file_path))

    @staticmethod
    def aes_encrypt(data, key):

        key_hash = SHA256.new(key.encode()).digest()
        cipher = AES.new(key_hash, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        return cipher.iv + ct_bytes

    @staticmethod
    def aes_decrypt(data, key):

        key_hash = SHA256.new(key.encode()).digest()
        iv = data[:16]
        cipher = AES.new(key_hash, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(data[16:]), AES.block_size)
        return pt

    def encrypt_file(self):
        if not self.validate_input():
            return

        input_file = self.file_path.get()
        password = self.password_entry.get()
        output_file = os.path.splitext(input_file)[0] + "_encrypted.db"

        try:
            # 读取原始文件
            with open(input_file, 'rb') as f:
                original_data = f.read()

            # 加密数据
            encrypted_data = self.aes_encrypt(original_data, password)

            # 写入加密文件
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)

            self.status.set(f"文件加密成功，保存为: {os.path.basename(output_file)}")
            messagebox.showinfo("成功", "文件加密成功!")
        except Exception as e:
            messagebox.showerror("错误", f"加密失败: {str(e)}")

    def decrypt_file(self):
        if not self.validate_input():
            return

        input_file = self.file_path.get()
        password = self.password_entry.get()

        # 判断是否是加密文件（简单通过文件名判断）
        if "_encrypted" not in os.path.basename(input_file):
            output_file = os.path.splitext(input_file)[0] + "_decrypted.db"
        else:
            output_file = input_file.replace("_encrypted", "_decrypted")

        try:
            # 读取加密文件
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()

            # 解密数据
            decrypted_data = self.aes_decrypt(encrypted_data, password)

            # 写入解密文件
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)

            # 验证解密后的文件是否是有效的SQLite数据库
            try:
                conn = sqlite3.connect(output_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()

                if not tables:
                    raise ValueError("解密后的文件不是有效的SQLite数据库")

                self.status.set(f"文件解密成功，保存为: {os.path.basename(output_file)}")
                messagebox.showinfo("成功", "文件解密成功!")
            except sqlite3.DatabaseError:
                os.remove(output_file)
                raise ValueError("解密失败 - 密码错误或文件损坏")
        except Exception as e:
            messagebox.showerror("错误", f"解密失败: {str(e)}")

    def validate_input(self):
        if not self.file_path.get():
            messagebox.showwarning("警告", "请先选择SQLite文件")
            return False
        if not self.password_entry.get():
            messagebox.showwarning("警告", "请输入密码")
            return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLiteEncryptor(root)
    root.mainloop()
