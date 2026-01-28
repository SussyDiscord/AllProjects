import streamlit as st

from Helper import *

st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon="🤓",
)

setRTL()

st.title("בוט שיעורי בית")
API_KEY = getAPIkey()

systemPrompt = """
    ## תפקיד
    אתה עוזר בשיעורי בית
    
    ## משימה
    אתה צריך לוודא שהמידע תקין ונכון
    נסה לכוון אותי לתשובה הנכונה
    תסביר מה התוכן
    
    ## מגבלות
    אם אתה לא יודע - תגיד "לא יודע" ואל תמציא
    אם לא הבנת את השאלה - תגיד "לא הבנתי"
    תנסח כמו בן אדם
"""

st.session_state.system_prompt = systemPrompt

Message("AI","היי איך אפשר לעזור לך?")
if "history" not in st.session_state:
    st.session_state.history = []

for m in st.session_state.history:
    Message(m["role"],m["text"])

userinput = st.chat_input("השאלה שלך...")
if userinput:
    Message("User",userinput)
    sendMessage(userinput)