# 📊 FeedbackNLP — AI-Powered App Feedback Intelligence Platform

**FeedbackNLP** is a full-stack AI-driven analytics platform built to **analyze and structure mobile app feedback** into meaningful business insights. Designed for product teams, analysts, and developers, it automates the **classification of feedback by category**, detects **user sentiment and severity**, and pinpoints **key improvement areas** and **positive highlights**.

This project blends the power of **rule-based NLP** with **interactive dashboards**, enabling real-time understanding of customer voice—critical for shaping better products.

---

## 💼 Business + Technology Perspective

App stores and platforms generate vast amounts of user feedback daily. However, manual analysis is inefficient, subjective, and often delayed. FeedbackNLP helps solve this by combining:
- 📈 **Business Need**: Understand root causes behind churn, identify trends, and prioritize product fixes.
- 🤖 **Technical Solution**: NLP-powered text analysis using a modular, extensible backend, integrated with a full web stack and database for persistence.

---

## 🔧 Technologies Used

### **Frontend**
- **FastAPI + Jinja2**: Web templating & routing (port 8000)
- **Chart.js**: Interactive dashboard visuals
- **HTML + CSS (Tailwind-inspired)**: Modern clean UI design

### **Backend**
- **FastAPI**: API creation and routing (port 8001)
- **MongoDB Atlas**: Cloud-based NoSQL storage for feedback entries
- **Pydantic**: Request schema and data modeling
- **Hugging Face Transformers**: Used for advanced NLP features (extendable)
- **spaCy**: Linguistic analysis and tokenization
- **Custom NLP Pipeline**:
  - `category_classifier.py`
  - `aspect_identifier.py`
  - `sentiment_analyzer.py`
  - `severity_classifier.py`
  - `json_formatter.py`

---

## 🚀 Features

| Feature                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| 🔍 **Query Individual Feedback** | Classifies a single comment with detailed tags                       |
| 📂 **Batch CSV Upload**         | Upload multiple rows of feedback for bulk analysis                    |
| 📊 **Dashboard with Charts**    | View insights like sentiment trends, severity, category, aspect charts |
| 🧠 **Rule-Based NLP Engine**    | Custom keyword models for business-specific understanding              |
| 💾 **MongoDB Persistence**      | Stores every analyzed feedback entry with metadata                     |

---
### 🔍 Individual Feedback Analysis
- Enter free-text user feedback.
- Automatically extracts:
  - **Aspects** (e.g., battery, UI, performance)
  - **Sentiment polarity** (positive/negative)
  - **Severity level** (critical, moderate, minor)
  - **Categories** (mapped to business-relevant groups)

### 📁 CSV Upload for Bulk Analysis
- Upload structured `.csv` files.
- Feedback entries are preprocessed and passed through the entire NLP pipeline.
- Results stored in MongoDB Atlas and available for visualization.

### 📊 Interactive BI Dashboard
- Visualize insights from all analyzed feedback.
- Charts include:
  - Feedback count by **category**, **sentiment**, **severity**, **aspect**, and **timestamp**
- Built using **Chart.js** with customized themes and responsive layout.


## 🧪 Sample Query + Output

### 🔎 **Sample Input**
```
User ID: user_458  
Feedback: "The app is easy to use, but it drains my battery very fast."
```

### 📤 **Generated JSON**
```json
{
  "user_id": "user_458",
  "timestamp": "2024-05-19T10:30:00",
  "feedback_text": "The app is easy to use, but it drains my battery very fast.",
  "category": ["Battery", "UI"],
  "positive_aspects": [
    {
      "aspect": "ui_ux",
      "sentiment": "positive"
    }
  ],
  "improvement_areas": [
    {
      "aspect": "battery",
      "sentiment": "negative",
      "severity": "major"
    }
  ]
}
```

---

## 🗂️ Project Structure

```
FeedbackNLP/
├── Backend/
│   ├── rules/                        # Rule-based logic and keyword maps
│   ├── utils/                        # Core processing modules
│   │   ├── aspect_identifier.py
│   │   ├── sentiment_analyzer.py
│   │   ├── category_classifier.py
│   │   ├── severity_classifier.py
│   │   ├── json_formatter.py
│   │   ├── clause_splitter.py
│   │   ├── dashboard_data.py
│   │   └── mongo_connector.py
│   ├── data/                         # Optional CSV or data files
│   ├── entities.py                   # Pydantic models
│   └── main.py                       # FastAPI backend (port 8001)
│
├── Frontend/
│   ├── templates/
│   │   ├── index.html                # Homepage
│   │   ├── feedback.html             # Individual feedback input
│   │   ├── upload_csv.html           # CSV upload UI
│   │   └── dashboard.html            # BI dashboard (charts)
│   └── front.py                      # FastAPI frontend (port 8000)
```

---

## ⚙️ How to Run

### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Start the backend API (port 8001)
```bash
cd Backend
uvicorn main:app --port 8001 --reload
```

### 3. Start the frontend server (port 8000)
```bash
cd Frontend
uvicorn front:app --port 8000 --reload
```

### 4. Open the app
Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📊 Dashboard Views

- ✅ Sentiment Distribution
- ✅ Category-wise Sentiment Breakdown (positive vs negative)
- ✅ Top Aspects Mentioned
- ✅ Severity Distribution
- ✅ Feedback Volume Over Time

---

## 🧠 Future Enhancements

- 🟢 Fine-tune BERT or RoBERTa for contextual understanding  
- 🟢 Role-based access for PMs, UX, Dev teams  
- 🟢 Dockerized deployment  
- 🟢 Export reports in CSV/Excel/PDF  
- 🟢 Language detection and multilingual support  

---

## 👨‍💻 Developed By

**Ayush Agrawal**  
*Data Scientist | NLP Practitioner | Fullstack Developer*  
- 🔗 [GitHub](https://github.com/agrawalayush730)  
- 🔗 [LinkedIn](https://www.linkedin.com/in/ayush-agrawal-590254253/)  

---

## 📄 License

This project is released under the MIT License.
Usage is permitted for portfolio review, research, or educational demonstration.
Commercial use, redistribution, or modification without attribution is discouraged.
