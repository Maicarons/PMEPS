L='选择 SQLite 文件'
K=ValueError
J=Exception
I=staticmethod
E=open
import sqlite3 as H,tkinter as B
from tkinter import filedialog as M,messagebox as C
import os as A
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES as D
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256 as F
class N:
	def __init__(A,root):C=root;A.root=C;A.root.title('SQLite 文件加密解密工具');D=500;E=300;F=C.winfo_screenwidth();G=C.winfo_screenheight();H=int(F/2-D/2);I=int(G/2-E/2);A.root.geometry(f"{D}x{E}+{H}+{I}");A.password_label=B.Label(C,text='密码:');A.password_label.pack(pady=(20,5));A.password_entry=B.Entry(C,show='*',width=40);A.password_entry.pack();A.file_button=B.Button(C,text=L,command=A.select_file);A.file_button.pack(pady=20);A.file_path=B.StringVar();A.file_label=B.Label(C,textvariable=A.file_path,wraplength=400);A.file_label.pack();A.button_frame=B.Frame(C);A.button_frame.pack(pady=20);A.encrypt_button=B.Button(A.button_frame,text='加密文件',command=A.encrypt_file);A.encrypt_button.pack(side=B.LEFT,padx=10);A.decrypt_button=B.Button(A.button_frame,text='解密文件',command=A.decrypt_file);A.decrypt_button.pack(side=B.LEFT,padx=10);A.status=B.StringVar();A.status_label=B.Label(C,textvariable=A.status,fg='blue');A.status_label.pack()
	def select_file(C):
		B=M.askopenfilename(title=L,filetypes=[('SQLite 数据库','*.db *.sqlite *.sqlite3'),('所有文件','*.*')])
		if B:C.file_path.set(B);C.status.set('已选择文件: '+A.path.basename(B))
	@I
	def aes_encrypt(data,key):B=F.new(key.encode()).digest();A=D.new(B,D.MODE_CBC);C=A.encrypt(pad(data,D.block_size));return A.iv+C
	@I
	def aes_decrypt(data,key):A=F.new(key.encode()).digest();B=data[:16];C=D.new(A,D.MODE_CBC,iv=B);E=unpad(C.decrypt(data[16:]),D.block_size);return E
	def encrypt_file(B):
		if not B.validate_input():return
		F=B.file_path.get();H=B.password_entry.get();G=A.path.splitext(F)[0]+'_encrypted.db'
		try:
			with E(F,'rb')as D:I=D.read()
			K=B.aes_encrypt(I,H)
			with E(G,'wb')as D:D.write(K)
			B.status.set(f"文件加密成功，保存为: {A.path.basename(G)}");C.showinfo('成功','文件加密成功!')
		except J as L:C.showerror('错误',f"加密失败: {str(L)}")
	def decrypt_file(B):
		M='_encrypted'
		if not B.validate_input():return
		F=B.file_path.get();N=B.password_entry.get()
		if M not in A.path.basename(F):D=A.path.splitext(F)[0]+'_decrypted.db'
		else:D=F.replace(M,'_decrypted')
		try:
			with E(F,'rb')as G:O=G.read()
			P=B.aes_decrypt(O,N)
			with E(D,'wb')as G:G.write(P)
			try:
				I=H.connect(D);L=I.cursor();L.execute("SELECT name FROM sqlite_master WHERE type='table';");Q=L.fetchall();I.close()
				if not Q:raise K('解密后的文件不是有效的SQLite数据库')
				B.status.set(f"文件解密成功，保存为: {A.path.basename(D)}");C.showinfo('成功','文件解密成功!')
			except H.DatabaseError:A.remove(D);raise K('解密失败 - 密码错误或文件损坏')
		except J as R:C.showerror('错误',f"解密失败: {str(R)}")
	def validate_input(A):
		B=False
		if not A.file_path.get():C.showwarning('警告','请先选择SQLite文件');return B
		if not A.password_entry.get():C.showwarning('警告','请输入密码');return B
		return True
if __name__=='__main__':G=B.Tk();O=N(G);G.mainloop()