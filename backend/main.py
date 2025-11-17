from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from datetime import datetime

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data/experiment_data.csv"
os.makedirs("data", exist_ok=True)



# Change to what we want to have them enter
EXPECTED_DATES = [
    "1983-07-08", "1957-08-11", "2019-05-28", "1901-01-15", "1907-01-25",
    "1965-03-05", "1910-04-18", "1940-04-22", "1997-07-07", "2011-08-09",
    "1923-07-15", "1943-01-16", "1969-06-02", "1994-08-13", "1910-03-17",
    "1955-02-26", "1986-05-10", "1971-06-27", "1925-09-07", "1980-01-28"
]

@app.post("/api/log")
async def log_data(request: Request):
    data = await request.json()

    
    method = data.get("method")
    entered_value = data.get("value")
    time_taken = data.get("timeTaken")
    participant_id = data.get("participant_id", "P01")  # can add input field later
    trial_number = data.get("trial_number") or None

    
    if trial_number is None:
        trial_number = get_next_trial_number(participant_id)

    expected_value = EXPECTED_DATES[trial_number - 1] if 1 <= trial_number <= len(EXPECTED_DATES) else None
    correct = int(entered_value == expected_value)


    row = {
        "timestamp": datetime.now().isoformat(),
        "participant_id": participant_id,
        "trial_number": trial_number,
        "method": method,
        "expected_value": expected_value,
        "entered_value": entered_value,
        "correct": correct,
        "timeTaken_ms": time_taken
    }

    df = pd.DataFrame([row])
    if os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(DATA_FILE, index=False)

    
    all_data = pd.read_csv(DATA_FILE)
    summary = all_data.groupby("method")["timeTaken_ms"].mean().to_dict()
    accuracy = all_data.groupby("method")["correct"].mean().to_dict()

    return {
        "message": "Data logged successfully",
        "total_entries": len(all_data),
        "average_time_per_method": summary,
        "accuracy_per_method": accuracy
    }


def get_next_trial_number(participant_id: str) -> int:
    """Return the next trial number for this participant based on existing data."""
    if not os.path.exists(DATA_FILE):
        return 1
    df = pd.read_csv(DATA_FILE)
    if "participant_id" not in df.columns:
        return 1
    subset = df[df["participant_id"] == participant_id]
    if subset.empty:
        return 1
    return int(subset["trial_number"].max()) + 1
