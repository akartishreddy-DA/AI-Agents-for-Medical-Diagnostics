from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from datetime import datetime
import sqlite3
import os


# ---------------------------
# DATABASE SETUP
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "diagnosis.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input_text TEXT,
            cardiologist TEXT,
            psychologist TEXT,
            pulmonologist TEXT,
            final_assessment TEXT
        )
    """)

    conn.commit()
    conn.close()


# Initialize DB when module loads
init_db()


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def run_diagnosis(medical_text: str) -> dict:

    medical_report = medical_text.strip()

    if not medical_report:
        return {
            "Cardiologist": "No input provided.",
            "Psychologist": "No input provided.",
            "Pulmonologist": "No input provided.",
            "Final Assessment": "No input provided."
        }

    agents = {
        "Cardiologist": Cardiologist(None, medical_report),
        "Psychologist": Psychologist(None, medical_report),
        "Pulmonologist": Pulmonologist(None, medical_report)
    }

    results = {}

    # Run in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(agent.run): name
            for name, agent in agents.items()
        }

        for future in as_completed(futures):
            agent_name = futures[future]
            try:
                results[agent_name] = future.result()
            except Exception as e:
                results[agent_name] = f"Error: {str(e)}"

    team = MultidisciplinaryTeam(
        None,
        results.get("Cardiologist"),
        results.get("Psychologist"),
        results.get("Pulmonologist")
    )

    results["Final Assessment"] = team.run()

    # ---------------------------
    # SAVE TO DATABASE
    # ---------------------------
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO diagnoses (
                timestamp,
                input_text,
                cardiologist,
                psychologist,
                pulmonologist,
                final_assessment
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            medical_report,
            results.get("Cardiologist"),
            results.get("Psychologist"),
            results.get("Pulmonologist"),
            results.get("Final Assessment")
        ))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Database insert failed:", str(e))

    return results
