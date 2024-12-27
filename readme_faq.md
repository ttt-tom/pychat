# FAQ ChatBot 产品手册和开发文档

## 产品手册

### **1. 产品概述**

FAQ ChatBot 是一款轻量级的聊天机器人，能够从数据库中获取数据并快速回答相关问题，支持模糊匹配搜索功能。用户还可以通过提供的网站链接获取详细信息。

**核心功能**：

1. 快速匹配用户问题并返回答案。
2. 支持模糊匹配，推荐相关问题。
3. 提供 URL 链接，方便用户获取更多信息。

---

### **2. 部署指南**

#### **部署方式**：

##### 1.  本地部署:

在文件目录faq-chatbot下，通过终端输入 `uvicorn app.mainbd:app --reload`

你会看到类似输出：

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [59800] using StatReload
INFO:     Started server process [75152]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

这表明后端服务器已经启动，继续尝试在浏览器输入:`http://127.0.0.1:8000/`

浏览器会返回：

```
{
    "message": "Welcome to the FAQ ChatBot API!"
}
```

这表明Chatbot成功启动。

###### *本地测试：*

1. 直接测试：打开/static/widget.html

```
├── static/
│   ├── widget.html
```

在这里可以直接对Chatbot进行测试。

在对话框输入`What is Easy Supplier Discovery?`

得到输出:

`Bot: Discover businesses worldwide anytime, anywhere. Access company data online, shortlist active exporters, track competitors' shipments, and more. Create a qualified list of potential suppliers globally. Instantly search companies by location, trade information, and business partners through our dashboard.`

`Bot: You can find more details in this link: [Click here](https://www.tradeint.com/solution/importer/easy-supplier-discovery/)`

最终为:

```
ChatBot

You: What is Easy Supplier Discovery?

Bot: Discover businesses worldwide anytime, anywhere.
Access company data online, shortlist active exporters, track competitors' shipments, and more.
Create a qualified list of potential suppliers globally.
Instantly search companies by location, trade information, and business partners through our dashboard.
Bot: You can find more details in this link: Click here

Type your question here...    Send
```

2. 在浏览器进行测试：
   
   ```
   输入 :`http://127.0.0.1:8000/ask/?question=What%20is%20the%20Belt%20%26%20Road%20group%3F `
   ```
   
   得到输出:

```
{
    "question": "What is the Belt & Road group?",
    "answer": "The Belt & Road group covers trade data from countries involved in the Belt and Road Initiative.",
    "url": "https://www.tradeint.com/product/countries-covered/groups-import-export-trade-data/belt-&-road-trade-data/"
}
```

这说明Chatbot已经成功从数据库读取到数据，并且成功返回回答。

##### 2. Docker + WordPress 部署:

1. 在faq-chatbot文件夹下，通过终端输入 `docker-compose up --build -d`
2. 等待Docker拉取整个项目。（注意，如果Docker没有包含Wordpress，请在 `setting`-`Docker-Engine`中 添加合适的镜像加速服务器。)
3. 在浏览器中通过 `http://localhost:8080` 进入后台
4. **嵌入 WordPress**：

- 将 `widget.html` 文件内容粘贴到 WordPress 页面编辑器的 HTML 模式下。
- 在 `fetch()` 中的 API 地址替换为实际服务地址。(如果wordpress与项目部署在一个容器，则可以直接使用本地地址）

###### *Wordpress测试：*

1. 将widget.html的代码插入WordPress以后，保存并发布。在页面中输入 `What is the Belt & Road group?`
2. Chatbot将返回 `The Belt & Road group covers trade data from countries involved in the Belt and Road Initiativ`同时附带相关FAQ网页网址 `https://www.tradeint.com/product/countries-covered/groups-import-export-trade-data/belt-&-road-trade-data/`
3. 网站同时支持模糊输入,在输入框输入 `TradeInt's customer support`,这截取自 `What are the operating hours for TradeInt's customer support`
4. Chatbot将正确输出 `Our customer support team is available to assist you during regular business hours (GMT+8), Monday through Friday. The exact operating hours may vary based on your region. Please refer to our TradeInt website or contact us directly for specific information.`同时附带网站相关页面url

最后输出应该如下：

```
ChatBot

You: Which countries are covered in Asia?
Bot: Countries such as China, India, Japan, Singapore, South Korea, and many more are included.
Bot: You can find more details in this link: Click here

You: TradeInt`s customer support
Bot: Whether you want to inquire about the following: Our customer support team is available
to assist you during regular business hours (GMT+8), Monday through Friday. 
The exact operating hours may vary based on your region. 
Please refer to our TradeInt website or contact us directly for specific information.
Bot: You can find more details in this link: Click here

Type your question here...                                       Send
```

**访问服务**

- FAQ ChatBot 后端 API：`http://localhost:8000`或者`http://127.0.0.1:8000/`
- WordPress 前端页面：`http://localhost:8080`

## 

## 开发文档

### **1. 项目结构**

```
faq-chatbot/
├── app/
│   ├── main.py          # 核心后端服务 - Docker
│   ├── maindb.py        # 核心后端服务 - 直接运行后端
│   ├── chatbot.py       # ChatBot 逻辑
│   ├── database.py      # FAQ 数据库管理
│   ├── config.py        # 配置文件
│   ├── faq_data.json    # 查询数据库
│   └── requirements.txt # 依赖库
├── static/
│   ├── widget.html      # 嵌入 WordPress 的 HTML/JS 小部件
│   ├── widget_ori_style     # 嵌入 WordPress 的 HTML/JS 小部件_Ori版本
├── jsdb/
│   ├── database.json    # 储存的数据
├── Dockerfile           # Docker 构建文件
├── docker-compose.yml   # Docker Compose 文件
└── README.md            # 项目文档
```

---

### **2. 后端逻辑**

#### **核心模块说明**

1. **main.py**
   
   - 提供 API 接口，支持以下路径：
     - `GET /`：返回服务欢迎信息。
     - `GET /ask/`：根据用户问题返回答案。
   
   部分代码（添加报错）：
   
   ```python
   @app.get("/ask/")
   def ask_question(question: str):
       try:
           response = chatbot.get_answer(question)
           if not response:
               return {"question": question, "answer": "Sorry, I don't have an answer for that question."}
           return {
               "question": question,
               "answer": response["answer"],
               "url": response["url"]  
           }
       except Exception as e:
           return {"error": str(e), "message": "An error occurred while processing your question."}
   ```
2. **chatbot.py**
   
   - 核心逻辑：匹配用户问题并返回答案，支持模糊匹配。
   - 模糊匹配基于 Python 内置的 `difflib` 模块实现。
   
   ```
   questions = [faq["question"] for faq in faq_data]
   closest_matches = difflib.get_close_matches(question, questions, n=1, cutoff=0.6)
   
   if closest_matches:
             for item in faq_data:
                 if item["question"] == closest_matches[0]:
                     explanation = "Whether you want to inquire about the following: "
                     return {
                         "answer": explanation +"  "+ item["answer"],
                         "url": item.get("url", None)
                     }
   
   
         return {
             "answer": "Sorry, I don't have an answer for that question. Could you rephrase it?",
             "url": None
         }
   ```
3. **database.py**
   
   - 负责加载和管理 FAQ 数据（存储为 JSON 格式）。

#### **数据格式**

FAQ 数据存储在 `faq_data.json` 文件中，格式如下：

```json
{
    "categories": [
      {
        "category": "Country Coverage",
        "subcategories": [
          {
            "subcategory": "Groups",
            "faqs": [
              {
                "question": "What is the Belt & Road group?",
                "answer": "The Belt & Road group covers trade data from countries involved in the Belt and Road Initiative.",
                "url": "https://www.tradeint.com/product/countries-covered/groups-import-export-trade-data/belt-&-road-trade-data/"
              },
              {
                "question": "What is the Central America (Transit) group?",
                "answer": "This group covers transit trade data from Central American countries.",
                "url": "https://www.tradeint.com/product/countries-covered/groups-import-export-trade-data/central-america-(transit)-trade-data/"
              },
```

---

### **3. 前端逻辑**

#### **HTML 和 JavaScript 说明**

- **HTML**:
  - 提供一个简单的输入框和按钮，用户可以输入问题并发送。
- **JavaScript**:
  - 使用 `fetch` 调用后端 API，获取答案并显示在页面上。

示例代码：

```javascript
fetch('http://localhost:8000/ask/?question=' + encodeURIComponent(question))
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('p');
        botMessage.textContent = `Bot: ${data.answer}`;
        messages.appendChild(botMessage);
        if (data.url) {
            const botLink = document.createElement('p');
            botLink.innerHTML = `Bot: You can find more details in this link: <a href="${data.url}" target="_blank">Click here</a>`;
            messages.appendChild(botLink);
        }
    });
```

---

### **4. 部署指南**

#### **Dockerfile**

后端服务的 Dockerfile：

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY ./app /app
COPY ./faq_data.json /app/faq_data.json
RUN pip install --no-cache-dir -r /app/requirements.txt
# EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **docker-compose.yml**

完整的 Docker Compose 配置文件：

```yaml
version: '3.8'

services:
  faq_chatbot:
    build:
      context: .
    container_name: faq_chatbot
    ports:
      - "8000:8000"

  wordpress:
    image: wordpress:latest
    container_name: wordpress
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: example
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - db

  db:
    image: mysql:5.7
    container_name: wordpress_db
    environment:
      MYSQL_ROOT_PASSWORD: example
      MYSQL_DATABASE: wordpress
```

输入`docker-compose up --build -d`直接拉取整个项目，直接在Docker操作，重复之前部署流程即可

---

### 5. 后续优化

- 支持添加/删除 FAQ。
  - 目前只能通过修改faq_data.json进行
- 添加管理员后台控制面板。
- 继续优化前端显示效果。
- 将数据库RAG化，同时将成熟模型的api引入，增加逻辑能力。

