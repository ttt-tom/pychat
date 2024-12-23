### 🚀 **Docker + Python FAQ ChatBot 项目代码模板** 🚀  

---

## 📂 **项目结构**  

```
faq-chatbot/
├── app/
│   ├── main.py          # 核心后端服务
│   ├── chatbot.py       # ChatBot 逻辑
│   ├── database.py      # FAQ 数据库管理
│   ├── config.py        # 配置文件
│   └── requirements.txt # 依赖库
├── static/
│   ├── widget.html      # 嵌入 WordPress 的 HTML/JS 小部件
├── Dockerfile           # Docker 构建文件
├── docker-compose.yml   # Docker Compose 文件
└── README.md            # 项目文档
```

---

## 🐍 **1. Python 后端代码**

### **app/main.py**
```python
from fastapi import FastAPI
from chatbot import ChatBot
from database import FAQDatabase

app = FastAPI()
db = FAQDatabase()
chatbot = ChatBot(db)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FAQ ChatBot API!"}

@app.get("/ask/")
def ask_question(question: str):
    answer = chatbot.get_answer(question)
    return {"question": question, "answer": answer}
```

---

### **app/chatbot.py**
```python
class ChatBot:
    def __init__(self, database):
        self.db = database

    def get_answer(self, question: str) -> str:
        faq_data = self.db.get_faq_data()
        for item in faq_data:
            if question.lower() in item['question'].lower():
                return item['answer']
        return "Sorry, I don't have an answer for that question."
```

---

### **app/database.py**
```python
import json

class FAQDatabase:
    def __init__(self):
        self.faq_file = 'faq_data.json'

    def get_faq_data(self):
        with open(self.faq_file, 'r', encoding='utf-8') as f:
            return json.load(f)
```

---

### **app/config.py**
```python
class Config:
    APP_NAME = "FAQ ChatBot"
    VERSION = "1.0"
    DEBUG = True
```

---

### **app/requirements.txt**
```
fastapi==0.95.2
uvicorn==0.21.1
```

---

## 📦 **2. FAQ 数据文件**

### **faq_data.json**
```json
[
    {
        "question": "What is your return policy?",
        "answer": "You can return the product within 30 days."
    },
    {
        "question": "How can I contact support?",
        "answer": "You can email support@example.com."
    }
]
```

---

## 🐳 **3. Docker 文件**

### **Dockerfile**
```dockerfile
# 使用 Python 官方镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制文件
COPY ./app /app
COPY ./faq_data.json /app/faq_data.json

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 启动服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### **docker-compose.yml**
```yaml
version: '3.8'

services:
  chatbot:
    build: .
    container_name: faq_chatbot
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
      - ./faq_data.json:/app/faq_data.json
```

---

## 🌐 **4. WordPress 嵌入小部件**

### **static/widget.html**
```html
<div id="faq-chatbot">
  <input type="text" id="user-question" placeholder="Ask a question...">
  <button onclick="askFAQ()">Ask</button>
  <div id="faq-answer"></div>
</div>

<script>
async function askFAQ() {
    const question = document.getElementById('user-question').value;
    const response = await fetch(`http://your-server-ip:8000/ask/?question=${question}`);
    const data = await response.json();
    document.getElementById('faq-answer').innerText = data.answer;
}
</script>
```

---

## 📝 **5. 快速启动**

### 📦 **本地运行**
```bash
# 安装依赖
pip install -r app/requirements.txt

# 启动服务
uvicorn app.main:app --reload
```

### 🐳 **Docker 部署**
```bash
# 构建镜像
docker-compose up --build -d

# 访问服务
http://localhost:8000
```

### 🌐 **嵌入 WordPress**
1. 将 `widget.html` 代码粘贴到 WordPress 页面编辑器的 HTML 模式下。  
2. 将 `your-server-ip` 替换为实际服务器 IP 地址。  

---

## ✅ **6. API 测试**

- **根路径**：`GET /`  
   **返回**：`{"message": "Welcome to the FAQ ChatBot API!"}`  

- **查询 FAQ**：`GET /ask/?question=your-question`  
   **示例**：`/ask/?question=How can I contact support?`  
   **返回**：`{"question": "How can I contact support?", "answer": "You can email support@example.com."}`  

---

## 📤 **7. 提交指南**

1. Fork 项目到个人 GitHub。  
2. 完成开发并提交代码。  
3. 编写产品手册和开发文档。  
4. 提交 Pull Request。  

---

## 🚀 **8. 后续优化**

- 支持添加/删除 FAQ。  
- 添加管理员后台控制面板。  
- 优化前端交互效果。  

---

**🎓 期待你的优秀项目交付！** 💻🔥
