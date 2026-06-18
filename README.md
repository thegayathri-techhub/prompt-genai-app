# 🚀 Prompt-Based Generative AI Application

A sleek, interactive webpage dashboard utilizing Python, Streamlit, and Hugging Face's serverless inference API to manage text tasks with Meta's Llama-3-8B-Instruct model.

### 🔗 Live Application Link
👉 **[Click Here to Access the Live Dashboard](https://prompt-genai-app-8x363bjxxaadjyyxc4vtj6.streamlit.app/)**

---

## 🛠️ Features

- **📝 Text Summarization:** Condense complex articles into high-quality summaries with configurable sentence constraints and custom tone styling (informative, professional, casual, or academic).
- **❓ Factual Grounded QA:** An absolute strict-grounded question-answering terminal equipped with system guardrails to explicitly prevent LLM hallucinations.
- **🎯 LLM-as-a-Judge Evaluation:** An automated quality control auditor pipeline that scores outputs from 1-5 on metrics like *Relevance*, *Coherence*, and performs an strict *Hallucination Check*.

---

## 🏗️ Local Installation Guide

If you want to run this project locally on your machine via **VS Code**, follow these steps:

### 1. Clone the Repository
```bash
# Clone this repository via manual zip download or Git:
git clone [https://github.com/thegayathri-techhub/prompt-genai-app.git](https://github.com/thegayathri-techhub/prompt-genai-app.git)
cd prompt-genai-app

2. Install Project Dependencies
Ensure you have Python installed, then run the following in your terminal:
pip install streamlit python-dotenv huggingface_hub

3. Configure Local Credentials
Create a file named .env in the root directory and add your unique Hugging Face Read Token:
Code snippet
HF_TOKEN="your_huggingface_access_token_here"

4. Run the Web Dashboard
Execute the application module directly via your command line interface:
python -m streamlit run app.py

🧰 Technology Stack
Frontend Interface: Streamlit (Custom Minimal UI)
Language Engine Model: Meta-Llama-3-8B-Instruct (Serverless Hub Router)
Environment Management: Python-Dotenv
