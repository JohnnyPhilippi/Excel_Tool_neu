import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

def translate_text(text):
    if isinstance(text, str):  # Sicherstellen, dass es sich um einen String handelt
        return GoogleTranslator(source='en', target='de').translate(text)
    return text

# Titel der Anwendung
st.title("Excel-Spaltenübersetzer")

# Hochladen der Excel-Datei
uploaded_file = st.file_uploader("Lade eine Excel-Datei hoch", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("Dateivorschau:", df.head())

    # Auswahl der Spalten zur Übersetzung
    columns_to_translate = st.multiselect(
        "Wähle die Spalten zur Übersetzung aus", df.columns
    )

    if st.button("Übersetzen"):
        for column in columns_to_translate:
            df[column] = df[column].apply(translate_text)

        st.success("Übersetzung abgeschlossen!")

        # Download der übersetzten Datei
        output_file = "translated_file.xlsx"
        df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="Lade die übersetzte Datei herunter",
                data=f,
                file_name="übersetzte_datei.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
