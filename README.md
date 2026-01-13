# 📘 **Study Buddy — AI-Powered Study Assistant**

![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red?logo=streamlit)
![Gemini API](https://img.shields.io/badge/Backend-Gemini%202.5%20Flash-blue?logo=google)
![Python](https://img.shields.io/badge/Language-Python-yellow?logo=python)
![IBM SkillsBuild](https://img.shields.io/badge/AICTE%20x%20IBM-SkillsBuild%20Internship-orange?logo=ibm)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen)
![Version](https://img.shields.io/badge/version-1.1.0-purple)

---

## 🧠 **Project Overview**

Students often struggle to grasp difficult topics or summarize lengthy notes.  
**Study Buddy** is an AI-powered web app that acts as a **personal academic assistant**, capable of:

- 🧩 Explaining complex concepts in simple terms  
- 📄 Summarizing notes or uploaded PDFs  
- ❓ Generating quizzes, solving exam questions, and evaluating answers

Combines **Streamlit** for UI and **Gemini 2.5 Flash API** for fast, intelligent AI responses — all in a clean chat-based interface.

🔗 [Live app](https://sgpai-study-buddy.streamlit.app/) | [User Help Guide (PDF)](https://drive.google.com/file/d/your_file_id_here/view?usp=sharing)

---

## ⚙️ **System Design**

### 🏗️ **Architecture**
A lightweight **Streamlit frontend** interacts with **Google Gemini 2.5 Flash** backend via secure API calls.  
All secrets managed safely via `.env` and `st.secrets`.

### 🧩 **Core Features**

| Mode        | Function                                                           | Example                       |
|-------------|--------------------------------------------------------------------|-------------------------------|
| 🧠 **Explainer**      | Simplifies academic concepts                                   | “Explain Deadlock in OS”      |
| 📄 **Summarizer**     | Condenses notes or PDFs                                       | Upload 20-page PDF → summary  |
| 🧩 **Quizzer**        | Quiz generator, solver, evaluator (multi-mode workflow)       | MCQs, solve/evaluate Q&As     |

Other Features:
- 📂 PDF upload (PyPDF2 extraction)
- 💬 Real-time chat interface
- 🔄 New chat/reset option
- ☁️ Deployed on Streamlit Cloud

---

## 🧙‍♂️ **Quizzer Mode — Three Powerful Sub-modes**

1. **📝 Generate Questions**  
   Enter a topic/chapter/passage. Get a variety of questions (MCQ, T/F, fill-in, descriptive) — answers listed together as an answer key for self-testing.
2. **📖 Solve Questions**  
   Paste your exam questions (optionally add word limits or marks). Get concise, exam-ready answers formatted per input.
3. **✅ Evaluate Answers**  
   Submit questions and your answers (with '---' separator, or sequential prompts). Get detailed feedback, correction, and scoring.

---

## 🧱 **Project Structure**

```
StudyBuddy/
├── main.py
├── requirements.txt
├── assets/
│ └── PROBLEM STATEMENTS.pdf
├── components/
│ ├── chat_ui.py
│ ├── pdf_handler.py
│ └── sidebar.py
├── core/
│ ├── ai_utils.py
│ ├── explainer.py
│ ├── pdf_handler.py
│ ├── quizzer.py
│ └── summarizer.py
└── utils/
└── gemini_helper.py
```

---

## 🪜 **Workflow**
![StudyBuddy Workflow](https://github.com/user-attachments/assets/ae8f9a61-c84b-4ebf-9081-f139b98cf441)
©️🖼️ Diagram Credits: [https://gitdiagram.com/](https://gitdiagram.com/)

---

## 💡 **Tech Stack**

| Category            | Technologies                             |
|---------------------|------------------------------------------|
| **Frontend**        | Streamlit                                |
| **Backend / AI**    | Google Gemini 2.5 Flash API              |
| **Language**        | Python                                   |
| **Libraries**       | PyPDF2, google-generativeai, streamlit, dotenv |
| **Deployment**      | Streamlit Community Cloud                |
| **Security**        | `.env` + `st.secrets` key handling       |

---

## 🧾 **Results**

- 🎯 Simple, modern, and interactive chat-based UI  
- 📑 Smart summarization, quiz generation, and answer evaluation  
- ⚡ Fast, context-aware AI with Gemini 2.5 Flash  
- 🧩 Smooth multi-mode workflow for study and revision

---

## 🚀 **Future Scope**

- 🗣️ Speech-to-text / text-to-speech interaction  
- 🌐 Multi-language explanations  
- 🧠 Flashcard & spaced-repetition support  
- 👤 Memory-based user personalization  
- ☁️ Drive/Notion integration for notes & sessions  

---

> 🧩 *“Integrating AI with Education — Making Learning Simpler, Smarter, and Accessible for All.”*

---

## 👨‍💻 Author's

**Ankur ,Sanjay, Jayesh , Priyanshu**  


