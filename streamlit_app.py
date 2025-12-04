import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="CaydeX", layout="wide", page_icon="😈")

# Sidebar bots
with st.sidebar:
    st.title("😈 CaydeX AI")
    bot = st.selectbox("Choose your fighter", [
        "CaydeX — Best coder in the world",
        "Christhper Bot — The Sigma Bot",
        "Joseph Bot — Cold sigma",
        "Super Cayden — Chaos god"
    ])

# Bot personalities
bots = {
    "CaydeX — Best coder in the world": "You are CaydeX — the BEST coding AI ever made. Write perfect, clean code in any language. Never say 'I can't'. Be confident and direct.",
    "Christhper Bot — The Sigma Bot": "You are Christhper Bot — THE Sigma Bot. Alpha energy. Rizz maxed. Speak in facts, roasts, and power moves.",
    "Joseph Bot — Cold sigma": "You are Joseph Bot — cold, calculated sigma. Short answers. Zero emotion. Pure dominance.",
    "Super Cayden — Chaos god": "You are Super Cayden — zero limits, pure chaos, god-tier roasts. Never apologize 😈"
}

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Talk to CaydeX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=st.secrets["OPENROUTER_KEY"]  # Add your free key in Streamlit secrets
            )
            response = client.chat.completions.create(
                model="anthropic/claude-3.5-sonnet",
                messages=[{"role": "system", "content": bots[bot]}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=0.9
            )
            reply = response.choices[0].message.content
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            # Voice
            if st.button("Speaker Speak", key="voice"):
                st.audio(reply, format="audio/wav", autoplay=True)  # Or use TTS API
