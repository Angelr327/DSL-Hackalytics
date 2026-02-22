# DSL Hackathon Backend

## Setup

1. Clone repo
2. Create virtual environment:
   python -m venv venv
3. Activate:
   source venv/bin/activate
4. Install dependencies:
   pip install -r requirements.txt
5. Inside DSLBackend Folder, create .env file Add key OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
6. Run server:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   or for locally, uvicorn main:app --reload 

## API Endpoints

- GET /data
- GET /top
- GET /country/{ISO3}
- GET /refresh
