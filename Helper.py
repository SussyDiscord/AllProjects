
from dotenv import load_dotenv
import os
import streamlit as st


def getAPIkey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
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
        self.role = role
        self.text = text
        self.showMessage()

    def showMessage(self):
        message = st.chat_message(self.role)
        message.write(self.text)