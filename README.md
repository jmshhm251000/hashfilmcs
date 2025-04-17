# HashFilmCS Customer Service and Chatbot Application

## Project Structure

- `__init__.py`
- `config.py`
- `data_processing.py`
- `log.py`
- `mongodb.py`
- `utils.py`
- `routes/database.py`
- `routes/webhooks.py`
- `chatbot/chatbot.py`
- `chatbot/ingestion.py`
- `chatbot/prompt.py`

## Frameworks & Libraries Used

- **Flask**: Web framework for routing and templating.
- **Flask-PyMongo**: Simplifies MongoDB integration.
- **python-dotenv**: Loads environment variables from a `.env` file.
- **Flask Session**: Manages user sessions and authentication.
- **llama_index**: Provides retrieval-augmented-generation (RAG) capabilities (Document, VectorStoreIndex, BaseQueryEngine).
- **Ollama**: Interfaces with local LLMs for response synthesis.
- **HuggingFace Embedding**: Generates semantic embeddings for document retrieval.
- **Google API Client**: Fetches and parses Q&A data from Google Docs.
- **python-json-logger**: Formats logs as structured JSON for downstream processing.

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\\Scripts\\activate     # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   Create a `.env` file in the project root with:
   ```env
   ACCESS_KEY=your_access_key_here
   DOCUMENT_ID=your_google_doc_id_here
   VERIFY_TOKEN=your_webhook_verify_token_here
   ```
5. **Run the application**
   ```bash
   flask run
   ```

## Usage

- **Login**: Navigate to `/` and enter the `ACCESS_KEY` to authenticate.
- **Chatbot**: Submit messages via the form to interact with the chatbot powered by Q&A from your Google Doc.
- **Complaints Database**: Visit `/database` to view and delete customer complaint entries in MongoDB.
- **Webhook Endpoint**: Configure your Meta webhook to point to `/webhook` for subscription verification and event handling.

## Contributing

Contributions are welcome! Please open issues or submit pull requests with improvements or bug fixes.
