import streamlit as st
import sqlite3
import pandas as pd
import key
from dotenv import load_dotenv
import os

with open('questions_encrypted.db', 'rb') as f:
    encrypted_data = f.read()

# 解密数据
# 加载.env文件
load_dotenv()

# 从环境变量中获取DB_KEY
db_key = os.getenv('DB_KEY')

decrypted_data = key.SQLiteEncryptor.aes_decrypt(encrypted_data, db_key)

with open("questions_decrypted.db", 'wb') as f:
    f.write(decrypted_data)

# 数据库连接
conn = sqlite3.connect("questions_decrypted.db", timeout=10000)

# 页面配置
st.set_page_config(page_title='入党题库练习系统', layout='centered',
                   menu_items={'Get Help': 'https://github.com/Maicarons/streamlit-template/issues',
                               'Report a bug': "https://github.com/Maicarons/streamlit-template/issues",
                               'About': "Maicarons"})
# 侧边栏导航
page = st.sidebar.selectbox('选择模式', ['主页', '筛选模式', '难题模式', '搜索模式', '练习模式'])

# 主页
if page == '主页':
    st.title('入党题库练习系统')
    total = pd.read_sql('SELECT COUNT(*) FROM questions', conn).iloc[0, 0]
    st.metric('总题数', total)

    # 题型分布
    type_dist = pd.read_sql('SELECT question_type, COUNT(*) as count FROM questions GROUP BY question_type', conn)
    st.bar_chart(type_dist.set_index('question_type'))

# 筛选模式
elif page == '筛选模式':
    st.title('题目筛选')
    # 筛选条件
    col1, col2, col3 = st.columns(3)
    with col1:
        types = pd.read_sql('SELECT DISTINCT question_type FROM questions', conn)['question_type'].tolist()
        selected_type = st.multiselect('题型', types)
    with col2:
        min_rate, max_rate = st.slider('易错率范围', 0.0, 100.0, (0.0, 100.0))
    with col3:
        knowledge = pd.read_sql('SELECT DISTINCT knowledge_point FROM questions', conn)['knowledge_point'].tolist()
        selected_knowledge = st.multiselect('知识点', knowledge)

    # 构建查询
    query = 'SELECT * FROM questions WHERE 1=1'
    params = []

    if selected_type:
        query += f" AND question_type IN ({','.join(['?'] * len(selected_type))})"
        params.extend(selected_type)
    query += " AND error_rate BETWEEN ? AND ?"
    params.extend([min_rate, max_rate])
    if selected_knowledge:
        query += f" AND knowledge_point IN ({','.join(['?'] * len(selected_knowledge))})"
        params.extend(selected_knowledge)

    results = pd.read_sql(query, conn, params=params)
    st.dataframe(results, height=500)

# 难题模式
elif page == '难题模式':
    st.title('高频易错题')
    page_size = 20
    page_num = st.number_input('页码', min_value=1, value=1) - 1

    df = pd.read_sql('SELECT * FROM questions ORDER BY error_rate DESC LIMIT ? OFFSET ?',
                     conn, params=(page_size, page_num * page_size))

    for _, row in df.iterrows():
        with st.expander(f"[{row['question_type']}] {row['content']}"):
            options_text = row["options"].replace("A", "\nA").replace("B", "\nB").replace("C", "\nC").replace("D",
                                                                                                              "\nD")
            st.markdown(f'选项：\n{options_text}')
            st.write(f'正确答案：{row["answer"]}  易错率：{row["error_rate"]}%')
            st.write(f'知识点：{row["knowledge_point"]}')

# 搜索模式
elif page == '搜索模式':
    st.title('题目搜索')
    search_term = st.text_input('输入搜索关键词')
    if search_term:
        query = """
        SELECT * FROM questions 
        WHERE content LIKE ? 
        OR options LIKE ?
        """
        params = [f'%{search_term}%', f'%{search_term}%']
        results = pd.read_sql(query, conn, params=params)

        for _, row in results.iterrows():
            st.markdown(f"**{row['content']}**")
            st.write(row['options'].replace('¶', '\n'))
            st.caption(f"正确答案：{row['answer']} | 知识点：{row['knowledge_point']}")

# 练习模式
elif page == '练习模式':
    st.title('单题练习模式')
    # 初始化或刷新题目
    if 'current_question' not in st.session_state or st.button('下一题'):
        st.session_state.current_question = pd.read_sql(
            'SELECT * FROM questions ORDER BY RANDOM() LIMIT 1', conn
        ).iloc[0]
        st.session_state.user_answer = None
    row = st.session_state.current_question
    st.markdown(f"**题目**: {row['content']}")
    options = row['options'].split("\n")
    if row['question_type'] == '多选题':
        selected = st.multiselect("请选择答案（可多选）", options)
        submitted = st.button('提交')
    elif row['question_type'] == '判断题':
        selected = st.radio("请判断 A正确 B错误", ["A", "B"])
        submitted = st.button('提交')
    else:  # 单选题
        selected = st.radio("请选择答案", options)
        submitted = st.button('提交')
    if submitted:
        st.session_state.user_answer = selected
        st.divider()
        correct_ans = list(row['answer'])
        if isinstance(selected, list):
            user_ans = [s[0] for s in selected]
        else:
            user_ans = [selected[0]]
        if set(user_ans) == set(correct_ans):
            st.success('✅ 回答正确！')
        else:
            st.error(f'❌ 正确答案：{", ".join(correct_ans)}')
        st.markdown(f"**解析**:")
        st.caption(f"知识点：{row['knowledge_point']}")
        st.caption(f"易错率：{row['error_rate']}%")
