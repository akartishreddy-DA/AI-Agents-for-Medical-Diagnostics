class BaseAgent:
    def __init__(self, client, medical_report):
        self.medical_report = medical_report

    def run(self):
        raise NotImplementedError


class Cardiologist(BaseAgent):
    def run(self):
        return f"""
Cardiology Assessment:
Based on the reported symptoms ({self.medical_report}),
there is a possibility of cardiovascular stress or arrhythmia.
Recommend ECG, troponin levels, and cardiac imaging if needed.
"""


class Psychologist(BaseAgent):
    def run(self):
        return f"""
Psychological Assessment:
Symptoms may indicate anxiety-related responses.
Stress management techniques and cognitive behavioral evaluation recommended.
"""


class Pulmonologist(BaseAgent):
    def run(self):
        return f"""
Pulmonology Assessment:
Shortness of breath may indicate respiratory dysfunction.
Recommend spirometry and chest imaging to rule out pulmonary causes.
"""


class MultidisciplinaryTeam:
    def __init__(self, client, cardio, psycho, pulmo):
        self.cardio = cardio
        self.psycho = psycho
        self.pulmo = pulmo

    def run(self):
        return f"""
Final Multidisciplinary Summary:

• Cardiology Perspective:
{self.cardio}

• Psychological Perspective:
{self.psycho}

• Pulmonary Perspective:
{self.pulmo}

Conclusion:
Further clinical evaluation and diagnostic testing recommended.
"""
