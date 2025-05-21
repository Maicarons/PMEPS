f='error_rate'
e='练习模式'
d='搜索模式'
c='难题模式'
b='筛选模式'
a='https://github.com/Maicarons/streamlit-template/issues'
Z='入党题库练习系统'
Y='questions_decrypted.db'
T='提交'
S='answer'
R='options'
Q='content'
J='knowledge_point'
I='question_type'
import streamlit as A,sqlite3 as g,pandas as C,key
from dotenv import load_dotenv as h
import os
with open('questions_encrypted.db','rb')as K:i=K.read()
h()
j=os.getenv('DB_KEY')
k=key.SQLiteEncryptor.aes_decrypt(i,j)
with open(Y,'wb')as K:K.write(k)
D=g.connect(Y,timeout=10000)
A.set_page_config(page_title=Z,layout='centered',menu_items={'Get Help':a,'Report a bug':a,'About':'Maicarons'})
H=A.sidebar.selectbox('选择模式',['主页',b,c,d,e])
if H=='主页':A.title(Z);l=C.read_sql('SELECT COUNT(*) FROM questions',D).iloc[0,0];A.metric('总题数',l);m=C.read_sql('SELECT question_type, COUNT(*) as count FROM questions GROUP BY question_type',D);A.bar_chart(m.set_index(I))
elif H==b:
	A.title('题目筛选');n,o,p=A.columns(3)
	with n:q=C.read_sql('SELECT DISTINCT question_type FROM questions',D)[I].tolist();L=A.multiselect('题型',q)
	with o:r,s=A.slider('易错率范围',.0,1e2,(.0,1e2))
	with p:t=C.read_sql('SELECT DISTINCT knowledge_point FROM questions',D)[J].tolist();M=A.multiselect('知识点',t)
	E='SELECT * FROM questions WHERE 1=1';F=[]
	if L:E+=f" AND question_type IN ({','.join(['?']*len(L))})";F.extend(L)
	E+=' AND error_rate BETWEEN ? AND ?';F.extend([r,s])
	if M:E+=f" AND knowledge_point IN ({','.join(['?']*len(M))})";F.extend(M)
	N=C.read_sql(E,D,params=F);A.dataframe(N,height=500)
elif H==c:
	A.title('高频易错题');U=20;u=A.number_input('页码',min_value=1,value=1)-1;v=C.read_sql('SELECT * FROM questions ORDER BY error_rate DESC LIMIT ? OFFSET ?',D,params=(U,u*U))
	for(w,B)in v.iterrows():
		with A.expander(f"[{B[I]}] {B[Q]}"):x=B[R].replace('A','\nA').replace('B','\nB').replace('C','\nC').replace('D','\nD');A.markdown(f"选项：\n{x}");A.write(f"正确答案：{B[S]}  易错率：{B[f]}%");A.write(f"知识点：{B[J]}")
elif H==d:
	A.title('题目搜索');O=A.text_input('输入搜索关键词')
	if O:
		E='\n        SELECT * FROM questions \n        WHERE content LIKE ? \n        OR options LIKE ?\n        ';F=[f"%{O}%",f"%{O}%"];N=C.read_sql(E,D,params=F)
		for(w,B)in N.iterrows():A.markdown(f"**{B[Q]}**");A.write(B[R].replace('¶','\n'));A.caption(f"正确答案：{B[S]} | 知识点：{B[J]}")
elif H==e:
	A.title('单题练习模式')
	if'current_question'not in A.session_state or A.button('下一题'):A.session_state.current_question=C.read_sql('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1',D).iloc[0];A.session_state.user_answer=None
	B=A.session_state.current_question;A.markdown(f"**题目**: {B[Q]}");V=B[R].split('\n')
	if B[I]=='多选题':G=A.multiselect('请选择答案（可多选）',V);P=A.button(T)
	elif B[I]=='判断题':G=A.radio('请判断 A正确 B错误',['A','B']);P=A.button(T)
	else:G=A.radio('请选择答案',V);P=A.button(T)
	if P:
		A.session_state.user_answer=G;A.divider();W=list(B[S])
		if isinstance(G,list):X=[A[0]for A in G]
		else:X=[G[0]]
		if set(X)==set(W):A.success('✅ 回答正确！')
		else:A.error(f"❌ 正确答案：{', '.join(W)}")
		A.markdown(f"**解析**:");A.caption(f"知识点：{B[J]}");A.caption(f"易错率：{B[f]}%")