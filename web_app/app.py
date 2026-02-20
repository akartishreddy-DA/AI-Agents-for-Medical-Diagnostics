import streamlit as st
from Main import run_diagnosis

st.set_page_config(page_title="AI Medical Diagnostic Assistant", layout="wide")

st.title("🩺 AI Medical Diagnostic Assistant")
st.markdown("Enter patient case details below to generate a multidisciplinary AI assessment.")

medical_text = st.text_area(
    "Enter Patient Case Details:",
    height=200,
    placeholder="Example: Patient reports chest tightness, anxiety episodes, shortness of breath..."
)

if st.button("🔎 Analyze Case"):

    if medical_text.strip() == "":
        st.warning("Please enter patient case details.")
    else:
        with st.spinner("Running AI specialist analysis..."):
            result = run_diagnosis(medical_text)

        st.success("Analysis Complete!")

        # Display Results Safely
        st.subheader("❤️ Cardiologist Opinion")
        st.write(result.get("Cardiologist", "No response"))

        st.subheader("🧠 Psychologist Opinion")
        st.write(result.get("Psychologist", "No response"))

        st.subheader("🫁 Pulmonologist Opinion")
        st.write(result.get("Pulmonologist", "No response"))

        st.subheader("📋 Final Multidisciplinary Assessment")
        st.write(result.get("Final Assessment", "No response"))
