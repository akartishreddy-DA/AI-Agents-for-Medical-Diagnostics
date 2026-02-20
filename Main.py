from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam


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

    with ThreadPoolExecutor() as executor:
        future_to_agent = {
            executor.submit(agent.run): name
            for name, agent in agents.items()
        }

        for future in as_completed(future_to_agent):
            agent_name = future_to_agent[future]
            results[agent_name] = future.result()

    team = MultidisciplinaryTeam(
        None,
        results.get("Cardiologist"),
        results.get("Psychologist"),
        results.get("Pulmonologist")
    )

    results["Final Assessment"] = team.run()

    return results
