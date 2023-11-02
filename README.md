# PDF-GPT Switch Bot

PDF-GPT is a Switch bot powered by OpenAI's GPT-3.5 and PDFQuery. This bot can process PDF files and answer questions related to the content of the PDFs. It provides a seamless way to extract information from PDFs and get instant responses to your inquiries.

## Features

- **PDF Processing**: Upload PDF files to the bot, and it will extract text and metadata for further analysis.
- **Natural Language Processing**: Ask questions related to the content of the PDFs in natural language, and the bot will provide relevant answers.
- **Conversation Management**: Start a conversation with the bot, and clear the conversation when needed.

## Setup Guide

Follow these steps to set up the PDF-GPT Switch bot:

### Prerequisites

- Python 3.10 or higher installed on your system.
- Switch account.
- OpenAI API key.

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/hummingbird28/pdf-gpt
   cd pdf-gpt
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**

   - Open `.env` and provide your OpenAI API key and Switch bot token.
   ```
   BOT_TOKEN = 'YOUR_SWITCH_BOT_TOKEN'
   OPEN_AI_KEY = 'YOUR_OPENAI_API_KEY'
   ```

4. **Run the Bot:**

   ```bash
   python bot.py
   ```

5. **Start Using the Bot:**

   - Go to Switch and start a chat with your bot.
   - Use the `/start` command to initiate the conversation.
   - Send a PDF file to the bot to begin processing.
   - Ask questions related to the PDF content using natural language.

## Bot Commands

- **/start**: Get the start message and instructions.
- **/clear**: Clear the conversation and start fresh.

## Contributing

If you have suggestions, improvements, or issues, feel free to open an issue or create a pull request.