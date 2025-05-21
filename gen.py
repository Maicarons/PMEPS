import sqlite3
import re
from typing import List, Dict

# 定义正则表达式模式
QUESTION_PATTERN = re.compile(r'^(\d+)、【(.*?)】(.*?)$')
OPTION_PATTERN = re.compile(r'^([A-D]、.*)')
CORRECT_ANSWER_PATTERN = re.compile(r'正确答案：([A-D]+)(?:易错率|$)')
COMBINED_CORRECT_ERROR_PATTERN = re.compile(r'正确答案：([A-D]+)易错率：(\d+\.?\d*)%')
ERROR_RATE_PATTERN = re.compile(r'易错率：(\d+\.?\d*)%')
KNOWLEDGE_PATTERN = re.compile(r'知识点：(.*)')


def parse_questions(file_path: str) -> List[Dict]:
    questions = []
    current = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                if current and 'number' in current:
                    questions.append(current)
                    current = {}
                continue

            # 匹配题目头
            if match := QUESTION_PATTERN.match(line):
                current = {
                    'number': match.group(1),
                    'question_type': match.group(2),
                    'content': match.group(3).strip(),
                    'options': [],  # Initialize options list for all question types
                    'answer': '',
                    'error_rate': None,
                    'knowledge': ''
                }
                # Handle special cases where options might be missing
                if current['question_type'] == '判断题':
                    current['options'] = ['A、正确', 'B、错误']
            elif match := OPTION_PATTERN.match(line):
                if not current:
                    continue  # Skip orphaned options
                current.setdefault('options', []).append(match.group(1))
            elif match := COMBINED_CORRECT_ERROR_PATTERN.search(line):
                current['answer'] = match.group(1)
                current['error_rate'] = float(match.group(2))
            elif match := CORRECT_ANSWER_PATTERN.search(line):
                current['answer'] = match.group(1)
            elif match := ERROR_RATE_PATTERN.search(line):
                current['error_rate'] = float(match.group(1))
            elif match := KNOWLEDGE_PATTERN.search(line):
                current['knowledge'] = match.group(1)

    # Validate and add the last question
    if current and 'number' in current:
        questions.append(current)
    return questions


def create_database(questions: List[Dict], db_path: str):
    # 清空表数据
    conn = sqlite3.connect(db_path)
    conn.execute('DELETE FROM questions')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  number TEXT,
                  question_type TEXT,
                  content TEXT,
                  options TEXT,
                  answer TEXT,
                  error_rate REAL,
                  knowledge_point TEXT)''')

    for q in questions:
        c.execute('''INSERT INTO questions 
                     (number, question_type, content, options, answer, error_rate, knowledge_point)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (q['number'], q['question_type'], q['content'],
                   '\n'.join(q['options']), q['answer'], q['error_rate'], q['knowledge']))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    import os

    db_path = 'questions.db'

    questions = parse_questions('tiku.txt')
    create_database(questions, db_path)
    print(f'成功导入{len(questions)}道题目到数据库（已清除旧数据）')
