# Party Member Exam Practice System - README  

# 入党题库练习系统 - 使用说明  

## Overview / 概述  

This is an interactive Streamlit web application designed to help users prepare for the Party Member Exam (入党考试). It features multiple practice modes with a secure encrypted question database.  
这是一个基于Streamlit的交互式入党考试练习系统，提供多种练习模式并采用加密题库保护数据安全。  

---

## Key Features / 核心功能  

### 1. Secure Database / 安全数据库  

- Encrypted SQLite database with AES-256 protection  
- 采用AES-256加密保护的SQLite题库  
- Automatic decryption on launch using environment variables  
- 通过环境变量自动解密运行  

### 2. Practice Modes / 练习模式  

| Mode | 功能 | Description |  
|------|------|-------------|  
| **Home** | 主页 | Displays question statistics and distribution |  
| **Filter Mode** | 筛选模式 | Filter questions by type/difficulty/knowledge point |  
| **Challenge Mode** | 难题模式 | Practice high-error-rate questions with pagination |  
| **Search Mode** | 搜索模式 | Full-text search across all questions |  
| **Practice Mode** | 练习模式 | Randomized single-question practice with instant feedback |  

### 3. Interactive Features / 交互功能  

- Real-time answer validation  
- 实时答题验证  
- Error rate indicators  
- 题目易错率显示  
- Knowledge point tagging  
- 知识点标记系统  
- Responsive design for all devices  
- 全设备响应式设计  

---

## Setup Instructions / 安装说明  

### Requirements / 环境要求  

```bash
Python 3.8+
pip install streamlit sqlite3 pandas python-dotenv
```

### Configuration / 配置  

1. Create `.env` file:  

```env
DB_KEY=your_encryption_key_here
```

### Launch / 启动  

```bash
streamlit run app.py
```

---

## Usage Guide / 使用指南  

### For Candidates / 考生使用  

1. Start with **Practice Mode** for daily exercises  
   - 日常练习从"练习模式"开始  
2. Use **Challenge Mode** to focus on difficult questions  
   - "难题模式"专攻高频易错题  
3. Review mistakes using **Search Mode**  
   - 通过"搜索模式"查漏补缺  

### For Administrators / 管理员功能  

- Database encrypted with `SQLiteEncryptor` class  
- 数据库使用SQLiteEncryptor类加密  
- Environment variable based key management  
- 基于环境变量的密钥管理  
- Easy question bank updates via SQLite  
- 通过SQLite轻松更新题库  

---

## Security Notice / 安全声明  

⚠️ The question database is protected by AES-256 encryption. Never share your `.env` file or decrypted database.  
⚠️ 题库采用AES-256加密保护，请勿分享.env文件或解密后的数据库  

---

## Support / 技术支持  

Contact 问题反馈: <https://github.com/Maicarons/streamlit-template/issues>  

AGPL-3.0  License
