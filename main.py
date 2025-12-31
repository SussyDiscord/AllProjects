import streamlit as st

st.set_page_config(
    page_title="הפרויקטים שלי",
    page_icon="💥",
    layout="wide"
)

# ----- עיצוב רקע -----
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #2E3192, #1BFFFF);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

.project-card {
    padding: 25px;
    border-radius: 15px;
    background-color: rgba(255, 255, 255, 0.88);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
    transition: 0.25s;
}
.project-card:hover {
    transform: scale(1.03);
}
.project-title {
    font-size: 26px;
    font-weight: bold;
    color: #333;
    text-align:center;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------ כותרת ------
st.markdown(
    "<h1 style='text-align:center; color:white;'>💥 הפרויקטים שלי 💥</h1>",
    unsafe_allow_html=True
)
st.write("")


# ------ כרטיס מרכזי לאליאס ------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div class='project-card'>", unsafe_allow_html=True)
    st.markdown("<div class='project-title'>🎮 משחק אליאס</div>", unsafe_allow_html=True)
    st.write("משחק מילים מהנה — נסו להסביר את המילה בלי לומר אותה!")

    # כפתור שעובד בכל מצב
    if st.button("➡️ מעבר למשחק", use_container_width=True):
        st.switch_page("Pages/Elias.py")

    st.markdown("</div>", unsafe_allow_html=True)
