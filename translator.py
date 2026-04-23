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

# Session State initialisieren
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translation" not in st.session_state:
    st.session_state.translation = ""

source_lang = st.selectbox("Ausgangssprache", LANGUAGES)

input_text = st.text_area(
    "Text zum Übersetzen",
    value=st.session_state.input_text,
    height=200,
    placeholder="Text hier eingeben...",
    key="input_area",
)

# Buttons: Übersetzen + Löschen nebeneinander
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🗑️ Löschen"):
        st.session_state.input_text = ""
        st.session_state.translation = ""
        st.rerun()
with col2:
    translate = st.button("Übersetzen", type="primary", disabled=not input_text.strip())

if translate:
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
            st.session_state.translation = message.content[0].text
            st.session_state.input_text = input_text
            st.caption(f"Modell: {message.model} · Tokens: {message.usage.input_tokens} → {message.usage.output_tokens}")
        except Exception as e:
            st.error(f"Fehler: {e}")

if st.session_state.translation:
    st.subheader("Übersetzung")
    st.text_area("", value=st.session_state.translation, height=200, key="output")

    # Kopieren-Button via JavaScript
    copy_js = f"""
        <script>
        function copyText() {{
            navigator.clipboard.writeText({repr(st.session_state.translation)}).then(function() {{
                const btn = document.getElementById('copyBtn');
                btn.innerText = '✅ Kopiert!';
                setTimeout(() => btn.innerText = '📋 Kopieren', 2000);
            }});
        }}
        </script>
        <button id="copyBtn" onclick="copyText()"
            style="background-color:#4CAF50; color:white; border:none; padding:8px 16px;
                   border-radius:6px; cursor:pointer; font-size:14px;">
            📋 Kopieren
        </button>
    """
    st.components.v1.html(copy_js, height=50)
