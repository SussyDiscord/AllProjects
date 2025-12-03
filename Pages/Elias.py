import os #Operation system
from dotenv import load_dotenv
from google import genai
import streamlit as st

st.title(" AI משחק אליאס מול")

st.set_page_config(
    page_title="משחק אליאס מול AI",
    page_icon='🤖'

)


load_dotenv()
API_KEY = os.getenv("API_KEY")
def start():
    st.session_state.end = False
    st.session_state.gemini = genai.Client(api_key=API_KEY)
    st.session_state.history = []
    message = send(prompt)
    # st.text(message)
#    ai_text = st.chat_message("ai")
#    ai_text.write(message)


prompt = """
### הקשר 
אנחנו במשחק  "אליאס" - שזה משחק ניחושים 
עליך להגריל מילה ואני צריך לנחש  מה המילה שהגרלת

### חוקים 
אתנ צריך לתת לי רמזים 
אסור שהמילה או השורש שלה יופיעו 
כל פעם תן רמז אחד הראשון כללי מאוד והשאר יותר ויותר ספציפי 
אל תגלה את המילה אף פעם  

### סיום משחמק 
לאחר שלוש ניסיונות כתוב את הקוד שהגרלת 

### סיום 
כתוב בסיום END 
"""



all_models = ["gemini-2.5-flash","gemini-2.0-flash","gemini-2.5-flash-lite","gemini-2.0-flash-lite"]




def send(prompt):
    st.session_state.loading = True
    st.session_state.history.append({
        "sender": "user",
        "text": prompt
        })
    context = ("זו השיחה המלאה: \n")
    for line in st.session_state.history:
        context += f"{line['sender']}: {line['text']}\n"
    with st.spinner("חושב..."):
        for model in all_models:
            print(model)
            chat = st.session_state.gemini.chats.create(model=model)
            try:
                message = chat.send_message(context)
                st.session_state.history.append({
                    "sender": "ai",
                    "text": message.text
                })
                st.session_state.loading = False
                return message.text
            except:
                print("לא הצליח - מנסה את המודל הבא")

if "gemini" not in st.session_state:
    start()
#else:
if 'history' in st.session_state and len(st.session_state.history)> 0:
    for line in st.session_state.history[1:]:
        chat = st.chat_message(line["sender"])
        chat.write(line["text"])

if 'end' in st.session_state and st.session_state.end:
    st.balloons()
    st.success("המשחק הסתיים")

#message = chat.send_message(prompt)
# message = send(prompt)
# st.text(message)

else:
    user = st.chat_input("ניחוש")
    if user:
        user_text = st.chat_message("user")
        user_text.write(user)

        ai = send("הניחוש שלי: " + user)
        ai_text = st.chat_message("ai")
        ai_text.write(ai)

        if 'END' in ai:
            st.session_state.end = True
            st.rerun()


# while True:
#     user = input("הניחוש שלך >> ")
#     message = send(prompt)
#     print(message)
#     if "END" in message.text:
#         break

# to = input("למי לכתוב את הברכה? >>")
# content = input("למתי הברכה? >>")
# addons = input("מידע נוסף >>")
#
# prot = f"""אתה מומחה לכתיבת ברכות
# כתוב ברכה ל {to}
# לכבוד "{content}
# שים לב ש{addons}
# עד 3 שורות עם אימוגים ושיהיה אנושי"""
#
#
# gemini = genai.Client(api_key=API_KEY)
# ai = gemini.chats.create(model="gemini-2.0-flash")
# message = ai.send_message(prompt)
# print(message.text)