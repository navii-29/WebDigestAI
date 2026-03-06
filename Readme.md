# 🧠 AI Web Digest Summarizer

An **LLM-powered web application** that generates concise **digest-style
summaries of websites**.\
Users can register, submit a webpage URL, and receive an **AI-generated
summary** of the page content.

The system scrapes the webpage, extracts relevant content, and uses a
**Large Language Model (LLM)** to generate a readable digest.

------------------------------------------------------------------------

# 🚀 Features

-   🔐 **User Authentication**
    -   Register new users
    -   Secure password hashing using **bcrypt**
-   🪙 **Token-Based Usage**
    -   Each user receives tokens
    -   Each summary request consumes one token
    -   Admin endpoint allows token refill
-   🌐 **Web Scraping**
    -   Extracts website content using **BeautifulSoup**
-   🤖 **LLM Summarization**
    -   Uses **Groq API with OpenAI-compatible interface**
    -   Generates structured summaries of webpage content
-   🎨 **Frontend Interface**
    -   Simple and clean UI
    -   Separate **register and summary pages**
    -   Markdown-style summary rendering

------------------------------------------------------------------------

# 🏗️ Tech Stack

### Backend

-   Flask
-   Flask-RESTful
-   MongoDB
-   bcrypt
-   BeautifulSoup
-   Playwright
-   Groq LLM API

### Frontend

-   HTML
-   CSS
-   JavaScript

------------------------------------------------------------------------

# 📂 Project Structure

project/ │ ├── app.py ├── scraper.py ├── prompts.py │ ├── templates/ │
├── register.html │ └── summary.html │ ├── static/ │ └── style.css │ ├──
.env └── README.md

------------------------------------------------------------------------

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

git clone https://github.com/yourusername/WebDigestAI.git cd
ai-web-digest

------------------------------------------------------------------------

## 2️⃣ Install Dependencies

pip install flask flask-restful pymongo bcrypt python-dotenv requests
beautifulsoup4 openai

------------------------------------------------------------------------

## 3️⃣ Environment Variables

Create a `.env` file:

MONGO_URI=your_mongodb_connection_string GROQ_API_KEY=your_groq_api_key

------------------------------------------------------------------------

## 4️⃣ Run Application

python app.py

Server will start at:

http://localhost:5010

------------------------------------------------------------------------

# 🧑‍💻 API Endpoints

## Register User

POST /register

Body:

{ "Username": "user1", "Password": "Password@123" }

------------------------------------------------------------------------

## Generate Summary

POST /summary

Body:

{ "Username": "user1", "Password": "Password@123", "Url":
"https://example.com" }

------------------------------------------------------------------------

## Refill Tokens (Admin)

POST /refill

Body:

{ "Username": "user1", "Admin_Password": "123abc", "amount": 10 }

------------------------------------------------------------------------

# 🧠 How It Works

1.  User registers an account.
2.  User submits a **website URL**.
3.  The application:
    -   Scrapes the webpage
    -   Extracts content
4.  The content is passed to an **LLM prompt**.
5.  The LLM generates a **digest-style summary**.
6.  The summary is displayed in the frontend.

------------------------------------------------------------------------

# 📌 Example Output

Hot Topics

• Politics -- Deep dives into election debates\
• Science & Tech -- Insights into emerging technologies\
• Culture -- Stories that explore society and art

------------------------------------------------------------------------

# 🔮 Future Improvements

-   Session-based authentication
-   Async web scraping
-   Better content extraction
-   Rate limiting
-   Multi-page summarization
-   Deploy on Render / Docker

------------------------------------------------------------------------

# 📜 License

MIT License

------------------------------------------------------------------------

# 👨‍💻 Author

Built by **Navi-29**\
An experimental project exploring **LLM-powered web summarization and
scraping pipelines**.
