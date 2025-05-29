# orchestrator/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from agents.analysis_agent import calculate_risk_exposure, compare_earnings
from agents.language_agent import generate_brief
from agents.voice_agent import VoiceAgent
from data_ingestion.api_agents import get_stock_summary

import uvicorn
import os

app = FastAPI()
voice_agent = VoiceAgent()

# Dummy portfolio - would normally come from database
portfolio = [
    {"ticker": "TSM", "sector": "Asia Tech", "value": 2_200_000},
    {"ticker": "005930.KQ", "sector": "Asia Tech", "value": 1_800_000},
    {"ticker": "AAPL", "sector": "US Tech", "value": 6_000_000},
]

# Dummy earnings data
earnings_data = {
    "TSM": {"actual": 1.04, "estimate": 1.0},
    "005930.KQ": {"actual": 1.1, "estimate": 1.12}
}


class TextQuery(BaseModel):
    query: str


@app.post("/brief/text")
def generate_market_brief(query: TextQuery):
    try:
        print("Calculating exposure...")
        exposure = calculate_risk_exposure(portfolio)
        print("Exposure:", exposure)
        surprises = compare_earnings(earnings_data)
        print("Surprises:", surprises)
        summary = generate_brief(exposure, surprises)
        print("Summary:", summary)
        voice_agent.speak(summary)
        return {"response": summary}
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=f"Error: {e}")


@app.post("/brief/voice")
async def generate_market_brief_from_voice(file: UploadFile = File(...)):
    temp_path = "temp_input.wav"
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        transcription = voice_agent.transcribe(temp_path)
        exposure = calculate_risk_exposure(portfolio)
        surprises = compare_earnings(earnings_data)
        summary = generate_brief(exposure, surprises)
        voice_agent.speak(summary)
        return {
            "transcription": transcription,
            "response": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
