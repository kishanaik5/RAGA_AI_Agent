# 🧠 Multi-Agent Voice Finance Assistant

This is a fully offline, voice-enabled multi-agent finance assistant built for the RAGA AI internship assignment. It delivers concise spoken market briefs on Asia tech stock exposure and earnings surprises using free open-source LLMs, embeddings, and speech tools.

---

## 🚀 Use Case

> “What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?”

🗣️ The assistant responds (text + audio):

> “Today, your Asia tech allocation is 22% of AUM. TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral with a cautionary tilt.”

---

## 🧱 Architecture

| Agent         | Description |
|---------------|-------------|
| **API Agent**      | Fetches live stock data using `yfinance` |
| **Scraper Agent**  | Pulls headlines/earnings news from Yahoo Finance |
| **Retriever Agent**| Embeds and retrieves documents using **BGE Large + FAISS** |
| **Analysis Agent** | Computes AUM exposure and surprise scores |
| **Language Agent** | Uses **DeepSeek R1 (GGUF)** via `llama-cpp` for summary |
| **Voice Agent**    | Uses **Whisper** for STT and **pyttsx3** for TTS |

---

## 📦 Project Structure

