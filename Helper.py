import time

from dotenv import load_dotenv
import os
import streamlit as st
from     google import genai
from google.genai import types

st.session_state.page = "" # באיזה דף אני
def newPage(pagename): # פונקציה שבודקת האם החלפתי דף
    if st.session_state.page != pagename: # האם התחלף הדף
        print("דף חדש")
        st.session_state.page = pagename # שומרים את השם של הדף החדש
        st.session_state.history = [] # מאפסים את ההיסטוריה

all_models = ["gemini-2.5-flash","gemini-2.0-flash","gemini-3.0-flash","gemini-2.5-flash-lite","gemini-2.0-flash-lite"]

def create_chat(model,instruction,history=[]):
    if "client" not in st.session_state:
        st.session_state.client = genai.Client(api_key=getAPIkey())
    if instruction == "":  # אם אין הוראות
        if "system_prompt" in st.session_state:  # תבדוק האם הגדרנו פרומפט
            instruction = st.session_state.system_prompt
    print(instruction)
    st.session_state.chat = st.session_state.client.chats.create(
            model=model,
            history=history,
            config= types.GenerateContentConfig(
                system_instruction=instruction
            )
        )

st.session_state.modelIndex = 0 # מתחילים מהמודל הראשון

maxTrys = 5
currentTry = 0

if "history" not in st.session_state:
    st.session_state.history = []

def sendMessage(prompt): # פונקציה ששולחת הודעה
    st.session_state.history.append(
        {
            "role" : "user",
            "text" : prompt
        }
    )
    if "chat" not in st.session_state:
        create_chat(all_models[0],"")
    global currentTry
    try: # ננסה
        answer = st.session_state.chat.send_message(prompt) # שולחים
        st.session_state.history.append(
            {
                "role" : "model",
                "text" : answer.text
            }
        )
        Message("ai",answer.text)
        currentTry = 0
        # אם הוא הצליח - נמשיך מפה
    except Exception as e: # אם לא הצליח
        error = str(e) # נהפוך לטקסט
        print(e)
        currentTry += 1
        if currentTry == maxTrys:
            st.error("תקלה - נסה שנית מאוחר יותר.")
            return
        if "overloaded" in error.lower(): # נבדוק אם מופיעה שהסיבה היא שהמודל עמוס
            newChat(prompt)
            st.session_state.modelIndex += 1 # נוסיף 1 למספר המודלים
            if st.session_state.modelIndex == len(all_models):
                st.session_state.modelIndex = 0
            newmodel = all_models[st.session_state.modelIndex]
            st.info(f"trying {newmodel}")
            create_chat(newmodel, "") # צור צ'אט חדש
            sendMessage(prompt) # תשלח את ההודעה
        if "429" in error:
            with st.spinner("יותר מידי קריאות - מחכים דקה...", show_time=True):
                time.sleep(60)
                newChat(prompt)

def newChat(prompt):
    st.session_state.modelIndex += 1  # מוסיף 1 למספר המודלים
    if st.session_state.modelIndex == len(all_models):  # אם הגענו לסוף הרשימה
        st.session_state.modelIndex = 0  # חוזר להיות 0
    newmodel = all_models[st.session_state.modelIndex]
    st.info(f"trying {newmodel}")
    create_chat(newmodel, "")  # צור צ'אט חדש
    sendMessage(prompt)  # תשלח את ההודעה

def getAPIkey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API KEY"]
    return API_KEY

def setRTL():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)


#אובייקט "שולח" - מי שלח, מה ההודעה, אייקון להודעה
class Message:
    def __init__(self,role,text): #פונקציית הבניה  - self  - מי שיצרתי
        if role.lower() == "model":
            role = "ai"
        self.role = role
        self.text = text
        self.showMessage()

    def showMessage(self):
        message = st.chat_message(self.role)
        message.write(self.text)