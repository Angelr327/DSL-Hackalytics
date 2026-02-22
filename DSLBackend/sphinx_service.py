"""
sphinx_service.py

Smart AI analysis layer.
Only sends minimal necessary data to OpenAI.
"""

import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise Exception("OPENAI_API_KEY not set.")

client = OpenAI(api_key=api_key)


def analyze_dataset_with_prompt(df, user_question):
    """
    Smart analysis:
    - If a country ISO3 is detected → send only that country.
    - Otherwise → send top 15 most underfunded countries.
    """

    user_question = user_question.strip()
    upper_question = user_question.upper()

    # Try detecting ISO3 country codes inside question
    possible_iso3 = None
    for code in df["country_iso3"].unique():
        if code in upper_question:
            possible_iso3 = code
            break

    # === CASE 1: Specific Country ===
    if possible_iso3:
        filtered_df = df[df["country_iso3"] == possible_iso3]

    # === CASE 2: General Question ===
    else:
        filtered_df = (
            df.sort_values(by="coverage_ratio")
            .head(15)
        )

    # Select only essential columns (reduces tokens)
    filtered_df = filtered_df[
        [
            "country_iso3",
            "year",
            "people_in_need",
            "people_targeted",
            "funding",
            "requirements",
            "coverage_ratio",
            "funding_per_pin",
            "targeting_gap",
        ]
    ]

    context_data = filtered_df.to_dict(orient="records")

    prompt = f"""
You are Sentinel, a UN humanitarian funding analyst.

Respond in no more than TWO sentences.
Be clear, analytical, and concise.
Provide insight, not a data recap.
Do NOT list raw numbers unless essential.
Do NOT repeat the dataset.
Avoid filler phrases.

Answer like you're briefing a policymaker who has 20 seconds.

User Question:
{user_question}

Dataset:
{context_data}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze humanitarian crisis funding data."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,      # Controlled cost
        temperature=0.2      # Analytical, not creative
    )

    return response.choices[0].message.content