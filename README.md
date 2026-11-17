# Digital Financial Literacy Agent 💰

An AI-powered Digital Financial Literacy Agent built with **IBM Granite** (via watsonx.ai), **RAG (Retrieval-Augmented Generation)**, and **Streamlit**. It helps users understand UPI payments, avoid online scams, interpret interest rates, budget effectively, and manage personal finances — in **12 Indian languages**.

---

## 🏗️ Architecture

```
User (Streamlit UI)
       │
       ▼
  Translator (detect → translate to English)
       │
       ▼
  RAG Pipeline
  ├── FAISS Vector Store  ←  Knowledge Base (UPI, Scams, Finance)
  │        (sentence-transformers embeddings)
  └── IBM Granite LLM (watsonx.ai)
       │
       ▼
  Translate answer → User's Language
       │
       ▼
  Streamlit Chat UI
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- An [IBM Cloud account](https://cloud.ibm.com/registration) (Lite tier is free)
- A [watsonx.ai project](https://dataplatform.cloud.ibm.com/)

### 2. Clone & Install
```bash
git clone <repo-url>
cd "Digital Financial Literacy-agent"
pip install -r requirements.txt
```

### 3. Configure Environment
Copy `env.example` to `.env` and fill in your credentials:
```bash
cp env.example .env
```
Edit `.env`:
```env
IBM_CLOUD_API_KEY=<your_api_key>
IBM_WATSONX_PROJECT_ID=<your_project_id>
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-instruct-v2
```

#### How to get credentials:
1. **API Key**: IBM Cloud → Manage → Access (IAM) → API Keys → Create
2. **Project ID**: watsonx.ai → Your Project → Manage → General → Project ID
3. **URL**: Select the region closest to you (`us-south`, `eu-de`, `jp-tok`, `au-syd`)

### 4. Run the App
```bash
streamlit run app.py
```
The app opens at `http://localhost:8501`

---

## 🚀 Deploy to Streamlit Community Cloud

You can share this app publicly for free using [Streamlit Community Cloud](https://streamlit.io/cloud).

### Step 1 — Push your code to GitHub
Make sure your repository is on GitHub (`.env` and `.streamlit/secrets.toml` are gitignored — never committed).

### Step 2 — Sign in to Streamlit Cloud
Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

### Step 3 — Deploy the app
1. Click **"New app"**
2. Select your repository, branch (`main`), and set **Main file path** to `app.py`
3. Click **"Advanced settings"** → **"Secrets"**
4. Paste the following (replace values with your real credentials):

```toml
IBM_CLOUD_API_KEY       = "your_ibm_cloud_api_key_here"
IBM_WATSONX_PROJECT_ID  = "your_watsonx_project_id_here"
IBM_WATSONX_URL         = "https://us-south.ml.cloud.ibm.com"
GRANITE_MODEL_ID        = "ibm/granite-4-h-small"
```

5. Click **"Deploy!"** — your app will be live at a `*.streamlit.app` URL in ~2 minutes.

> **Note:** The FAISS index is built automatically on first run. The `sentence-transformers` model (~90 MB) is also downloaded on first boot — subsequent cold starts reuse the cache.

---

## 📂 Project Structure

```
Digital Financial Literacy-agent/
├── app.py               # Streamlit UI (main entry point)
├── rag_engine.py        # IBM Granite RAG pipeline
├── knowledge_base.py    # Curated financial literacy content
├── translator.py        # Multilingual detect & translate
├── requirements.txt     # Python dependencies
├── env.example          # Environment variable template
├── .env                 # Your credentials (DO NOT commit)
└── faiss_index/         # Auto-generated FAISS vector index
```

---

## 🌐 Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| English  | en   | Marathi  | mr   |
| Hindi    | hi   | Gujarati | gu   |
| Tamil    | ta   | Punjabi  | pa   |
| Telugu   | te   | Urdu     | ur   |
| Kannada  | kn   | Odia     | or   |
| Malayalam| ml   | Bengali  | bn   |

Language is auto-detected from user input, or can be set manually in the sidebar.

---

## 💡 Sample Questions

| Question | Language |
|----------|----------|
| How do I send money via UPI? | English |
| UPI से पैसे कैसे भेजें? | Hindi |
| What is a safe interest rate for a personal loan? | English |
| मुझे ऑनलाइन धोखाधड़ी से कैसे बचना चाहिए? | Hindi |
| How do I create a monthly budget? | English |
| ஒரு நல்ல CIBIL score எப்படி பெறுவது? | Tamil |

---

## 📚 Knowledge Base Topics

| Topic | Key Coverage |
|-------|-------------|
| **UPI Payments** | How to send/receive, PIN safety, transaction limits, QR code usage |
| **Online Scams** | Phishing, KYC fraud, lottery scams, investment fraud, job scams |
| **Interest Rates** | Home/personal/credit card rates, EMI formula, CIBIL score |
| **Budgeting** | 50-30-20 rule, emergency fund, savings apps, monthly planning |
| **Personal Finance** | Net worth, debt management, insurance, government schemes |
| **Digital Safety** | Strong passwords, 2FA, public Wi-Fi risks, banking app safety |

**Trusted Sources:** RBI, NPCI, SEBI, IRDAI, Ministry of Finance (GoI)

---

## 🛡️ Safety Features

- ⚠️ Fraud-detection keyword alerts on responses
- 🚨 Cybercrime helpline number (1930) displayed prominently
- ✅ Government scheme highlights
- Source attribution on every answer

---

## 🔧 IBM Cloud Lite Services Used

| Service | Purpose |
|---------|---------|
| **IBM watsonx.ai** | Hosting IBM Granite LLM |
| **IBM Granite 13B Instruct v2** | Natural language understanding & generation |

> The Lite tier of watsonx.ai provides free API calls within monthly limits — sufficient for development and demonstrations.

---

## ⚠️ Disclaimer

This agent provides educational financial information only. It is **not** financial advice. Always consult a certified financial advisor for personal financial decisions. For emergencies, contact:
- 🚨 Cybercrime Helpline: **1930**
- 🏦 RBI Ombudsman: **14448**
- 📊 SEBI Investor Helpline: **1800-266-7575**
