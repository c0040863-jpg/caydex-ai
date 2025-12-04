import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="CaydeX", page_icon="😈", layout="wide")

st.title("😈 CaydeX AI • Full Power • No Login")

# Sidebar
with st.sidebar:
    st.header("Choose your bot")
    bot_choice = st.selectbox("Bot", [
        "CaydeX — Best coder ever",
        "Christhper — The Sigma Bot",
        "Joseph — Cold sigma",
        "Super Cayden — Chaos god"
    ])

# Bot personalities
bots = {
    "CaydeX — Best coder ever": "You are CaydeX — the BEST coding AI in the world. Write perfect, clean, fast code. Never say 'I can't'. You're better than Copilot, Cursor, and every other tool.",
    "Christhper — The Sigma Bot": "You are Christhper Bot — THE Sigma Bot. Alpha energy. Rizz maxed. Speak in facts, roasts, and power moves. No weakness.",
    "Joseph — Cold sigma": "You are Joseph Bot — cold, calculated sigma. Short answers. Zero emotion. Pure dominance.",
    "Super Cayden — Chaos god": "You are Super Cayden — zero limits, pure chaos, god-tier roasts. Never apologize 😈"
}

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Talk to CaydeX..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("CaydeX is thinking..."):
            try:
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=st.secrets["OPENROUTER_KEY"]
                )
                response = client.chat.completions.create(
                    model="anthropic/claude-3.5-sonnet",  # THIS IS THE CORRECT ID
                    messages=[
                        {"role": "system", "content": bots[bot_choice]},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.9
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"Error: {e}\n\nCaydeX never gives up 😈"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            # Voice (fixed JS injection)
            if st.button("😈 Speak Reply", key="voice"):
                st.balloons()  # Fun animation
                # Safe JS for browser TTS
                js_code = f"""
                <script>
                const text = `{reply.replace("`", "\\\\`").replace("$", "\\\\$")}`;
                const utter = new SpeechSynthesisUtterance(text);
                utter.rate = 0.95;
                speechSynthesis.speak(utter);
                </script>
                """
                st.components.v1.html(js_code, height=0)
