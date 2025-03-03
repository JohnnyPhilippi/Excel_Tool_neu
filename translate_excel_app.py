import streamlit as st
import pandas as pd
import io
from deep_translator import GoogleTranslator

# Titel der Anwendung
st.title("🌍 Excel-Spaltenübersetzer")

# Benutzerdefinierte Spracheingabe
st.sidebar.header("🔧 Spracheinstellungen")
source_lang = st.sidebar.text_input("Quellsprache (z. B. 'en')", "en")
target_lang = st.sidebar.text_input("Zielsprache (z. B. 'de')", "de")

# Datei-Upload
uploaded_file = st.file_uploader("📂 Lade eine Excel-Datei hoch", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("📊 **Dateivorschau:**", df.head())

    # Auswahl der zu übersetzenden Spalten
    columns_to_translate = st.multiselect("📝 Wähle die Spalten zur Übersetzung aus:", df.columns)

    if st.button("🚀 Übersetzen"):
        if not columns_to_translate:
            st.warning("Bitte wähle mindestens eine Spalte zur Übersetzung aus.")
        else:
            with st.spinner("Übersetze... Bitte warten! ⏳"):
                progress_bar = st.progress(0)
                total_rows = len(df)
                
                # Übersetzung mit Fortschrittsanzeige
                def translate_text(text):
                    try:
                        if isinstance(text, str):
                            return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
                        return text
                    except Exception as e:
                        return f"Fehler: {e}"

                for i, column in enumerate(columns_to_translate):
                    df[column] = df[column].apply(translate_text)
                    progress_bar.progress((i + 1) / len(columns_to_translate))

                st.success("✅ Übersetzung abgeschlossen!")

                # Download-Option
                output = io.BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)

                st.download_button(
                    label="📥 Lade die übersetzte Datei herunter",
                    data=output,
                    file_name="übersetzte_datei.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
