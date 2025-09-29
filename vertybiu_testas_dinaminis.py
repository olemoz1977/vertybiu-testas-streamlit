
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Streamlit app title
st.title("Vertybių testas")

# File uploader for Excel file
uploaded_file = st.file_uploader("Įkelk savo Excel failą (.xlsm)", type=["xlsm"])

if uploaded_file:
    # Read Excel file
    xls = pd.ExcelFile(uploaded_file, engine="openpyxl")

    # Try to read the 'Įvedimas' sheet
    try:
        df_input = pd.read_excel(xls, sheet_name="Įvedimas", engine="openpyxl")
    except Exception as e:
        st.error(f"Nepavyko nuskaityti lapo 'Įvedimas': {e}")
        st.stop()

    # Extract vertybės from column that contains 'Vertybė'
    vertybe_col = [col for col in df_input.columns if "Vertybė" in col]
    if not vertybe_col:
        st.error("Lape 'Įvedimas' nerasta stulpelio su pavadinimu 'Vertybė'")
        st.stop()

    vertybes_raw = df_input[vertybe_col[0]].dropna().unique()
    vertybes = [v for v in vertybes_raw if str(v).lower() != "nėra"]

    # Generate all unique pairs of vertybės
    poros = []
    for i in range(len(vertybes)):
        for j in range(i + 1, len(vertybes)):
            poros.append((vertybes[i], vertybes[j]))

    st.subheader("Pasirink laimėtoją kiekvienoje poroje")

    # Dictionary to store results
    laimetojai = {}

    for idx, (v1, v2) in enumerate(poros):
        choice = st.radio(f"{v1} vs {v2}", options=[v1, v2], key=f"pair_{idx}")
        laimetojai[choice] = laimetojai.get(choice, 0) + 1

    if laimetojai:
        st.subheader("Rezultatai")

        # Convert results to DataFrame
        results_df = pd.DataFrame(list(laimetojai.items()), columns=["Vertybė", "Taškai"])
        results_df = results_df.sort_values(by="Taškai", ascending=False)

        st.dataframe(results_df)

        # Plot results
        fig, ax = plt.subplots()
        ax.barh(results_df["Vertybė"], results_df["Taškai"], color="skyblue")
        ax.invert_yaxis()
        ax.set_xlabel("Taškai")
        ax.set_title("Vertybių palyginimo rezultatai")
        st.pyplot(fig)
