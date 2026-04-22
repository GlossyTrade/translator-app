import anthropic
import streamlit as st

st.set_page_config(page_title="Übersetzer", page_icon="🌐", layout="centered")

st.title("🌐 Übersetzer → Englisch")
st.caption("Übersetzt beliebige Texte ins Englische mit Claude AI")

LANGUAGES = [
    "Automatisch erkennen",
    "Deutsch",
    "Französisch",
    "Spanisch",
    "Italienisch",
    "Portugiesisch",
    "Niederländisch",
    "Polnisch",
    "Russisch",
    "Japanisch",
    "Chinesisch",
    "Arabisch",
]

source_lang = st.selectbox("Ausgangssprache", LANGUAGES)

input_text = st.text_area(
    "Text zum Übersetzen",
    height=200,
    placeholder="Text hier eingeben...",
)

if st.button("Übersetzen", type="primary", disabled=not input_text.strip()):
    lang_instruction = (
        "Detect the source language automatically."
        if source_lang == "Automatisch erkennen"
        else f"The source language is {source_lang}."
    )

    prompt = (
        f"Translate the following text into English. {lang_instruction} "
        f"Return only the translated text, nothing else.\n\n{input_text}"
    )

    with st.spinner("Übersetze..."):
        try:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            translation = message.content[0].text
            st.subheader("Übersetzung")
            st.text_area("", value=translation, height=200, key="output")
            st.caption(f"Modell: {message.model} · Tokens: {message.usage.input_tokens} → {message.usage.output_tokens}")
        except Exception as e:
            st.error(f"Fehler: {e}")
