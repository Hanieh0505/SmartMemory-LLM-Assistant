# 🤖 SmartMemory LLM Assistant

A Python-based intelligent conversational chatbot built using **Groq API** and **Hugging Face Transformers**. This project focuses on efficient token management, conversation history trimming, and automated context summarization for Large Language Models (LLMs).

## ✨ Key Features
- **Streaming Responses:** Real-time token streaming like ChatGPT.
- **Token Tracking & Limits:** Precise token counting using local tokenizers (`Qwen` tokenizer) with daily/session limits.
- **Smart History Management:** Automatic message trimming (`max_history`) to keep context windows optimal.
- **Automated Summarization:** Summarizes older conversation blocks periodically to retain crucial historical facts without blowing up the context length.

## 🛠️ Tech Stack
- **Python**
- **OpenAI SDK** (integrated with Groq API)
- **Hugging Face Transformers** (Tokenization)
- **python-dotenv**

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Hanieh0505/SmartMemory-LLM-Assistant.git
   cd SmartMemory-LLM-Assistant
