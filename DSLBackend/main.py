from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data_processing import build_master_table, get_top_countries, get_country
from sphinx_service import analyze_dataset_with_prompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

master_df = build_master_table()

@app.get("/")
def root():
    return {"message": "DSL Backend Running"}

@app.get("/data")
def get_all_data():
    return master_df.to_dict(orient="records")

@app.get("/top")
def get_top():
    return get_top_countries(master_df, 10).to_dict(orient="records")

@app.get("/country/{iso3}")
def get_single_country(iso3: str):
    return get_country(master_df, iso3).to_dict(orient="records")


# -------- SPHINX --------

class InsightRequest(BaseModel):
    question: str

@app.post("/sphinx/analyze")
def analyze_data(request: InsightRequest):

    # ---- Guardrail: basic domain filter ----
    allowed_keywords = [
        "funding",
        "coverage",
        "gap",
        "targeted",
        "people",
        "requirements",
        "need",
        "crisis",
        "underfunded",
        "country",
        "compare",
        "trend",
    ]

    question_lower = request.question.lower()

    if not any(keyword in question_lower for keyword in allowed_keywords):
        return {
            "response": "This assistant only answers humanitarian funding and crisis-related questions."
        }
    
    if len(request.question) > 300:
        return {"response": "Question too long. Please summarize your request."}

    # ---- If question passes filter, call AI ----
    # Reduce dataset before sending to AI
    relevant_df = master_df.sort_values(by="coverage_ratio").head(15)

    answer = analyze_dataset_with_prompt(relevant_df, request.question)

    return {"response": answer}