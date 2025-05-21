L='content'
K=float
I='knowledge'
H='question_type'
G='error_rate'
F='answer'
E='options'
D='number'
import sqlite3 as J,re as A
from typing import List,Dict
M=A.compile('^(\\d+)、【(.*?)】(.*?)$')
N=A.compile('^([A-D]、.*)')
O=A.compile('正确答案：([A-D]+)(?:易错率|$)')
P=A.compile('正确答案：([A-D]+)易错率：(\\d+\\.?\\d*)%')
Q=A.compile('易错率：(\\d+\\.?\\d*)%')
R=A.compile('知识点：(.*)')
def C(file_path):
	J=[];A={}
	with open(file_path,'r',encoding='utf-8')as S:
		for C in S:
			C=C.strip()
			if not C:
				if A and D in A:J.append(A);A={}
				continue
			if(B:=M.match(C)):
				A={D:B.group(1),H:B.group(2),L:B.group(3).strip(),E:[],F:'',G:None,I:''}
				if A[H]=='判断题':A[E]=['A、正确','B、错误']
			elif(B:=N.match(C)):
				if not A:continue
				A.setdefault(E,[]).append(B.group(1))
			elif(B:=P.search(C)):A[F]=B.group(1);A[G]=K(B.group(2))
			elif(B:=O.search(C)):A[F]=B.group(1)
			elif(B:=Q.search(C)):A[G]=K(B.group(1))
			elif(B:=R.search(C)):A[I]=B.group(1)
	if A and D in A:J.append(A)
	return J
def S(questions,db_path):
	B=J.connect(db_path);B.execute('DELETE FROM questions');C=B.cursor();C.execute('CREATE TABLE IF NOT EXISTS questions\n                 (id INTEGER PRIMARY KEY AUTOINCREMENT,\n                  number TEXT,\n                  question_type TEXT,\n                  content TEXT,\n                  options TEXT,\n                  answer TEXT,\n                  error_rate REAL,\n                  knowledge_point TEXT)')
	for A in questions:C.execute('INSERT INTO questions \n                     (number, question_type, content, options, answer, error_rate, knowledge_point)\n                     VALUES (?, ?, ?, ?, ?, ?, ?)',(A[D],A[H],A[L],'\n'.join(A[E]),A[F],A[G],A[I]))
	B.commit();B.close()
if __name__=='__main__':import os;T='questions.db';B=C('tiku.txt');S(B,T);print(f"成功导入{len(B)}道题目到数据库（已清除旧数据）")