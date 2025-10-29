from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from datetime import datetime

app = FastAPI()

# Allow all origins for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data/experiment_data.csv"
os.makedirs("data", exist_ok=True)


# --- Expected dates for each trial ---
# We'll assume each participant must enter these 20 dates.
EXPECTED_DATES = [
    "2025-01-15", "2025-02-20", "2025-03-10", "2025-03-25", "2025-04-12",
    "2025-05-05", "2025-06-01", "2025-07-04", "2025-08-18", "2025-09-09",
    "2025-10-22", "2025-11-11", "2025-12-25", "2026-01-01", "2026-02-14",
    "2026-03-17", "2026-04-22", "2026-05-30", "2026-06-21", "2026-07-15"
]

@app.post("/api/log")
async def log_data(request: Request):
    data = await request.json()

    # --- Extract data from frontend ---
    method = data.get("method")
    entered_value = data.get("value")
    time_taken = data.get("timeTaken")
    participant_id = data.get("participant_id", "P01")  # can add input field later
    trial_number = data.get("trial_number") or None

    # If frontend doesn’t send trial index, derive based on existing entries
    if trial_number is None:
        trial_number = get_next_trial_number(participant_id)

    expected_value = EXPECTED_DATES[trial_number - 1] if 1 <= trial_number <= len(EXPECTED_DATES) else None
    correct = int(entered_value == expected_value)

    # --- Store in dataframe ---
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

    # --- Optional live summary ---
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
