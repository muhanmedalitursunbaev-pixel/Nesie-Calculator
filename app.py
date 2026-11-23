
import streamlit as st

st.set_page_config(
    page_title="Несие калькуляторы",
    page_icon="💳",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8 !important;
}

p, label, div, span {
    color: white !important;
}

.stMarkdown, .stText, .stSubheader {
    color: white !important;
}

input {
    color: black !important;
}

.stButton > button {
    background-color: #2563eb;
    color: white !important;
    border-radius: 12px;
    padding: 10px 25px;
    border: none;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white !important;
}
|
[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #334155;
}

[data-testid="stMetricLabel"] p {
    color: #cbd5e1 !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


st.title("Несие калькуляторы")
st.write("Несие төлемдерін есептеу бағдарламасы")

nesie = st.number_input("Несие сомасы (теңге)", min_value=0, value=1000000)
merzimi = st.number_input("Несие мерзімі (ай)", min_value=1, value=12)
paiz = st.number_input("Жылдық пайыз (%)", min_value=0.0, value=15.0)

if st.button("Есептеу"):
    r = paiz / 100 / 12

    if r == 0:
        tolem = nesie / merzimi
    else:
        tolem = nesie * r * (1 + r) ** merzimi / ((1 + r) ** merzimi - 1)

    jalpy = tolem * merzimi
    artyk = jalpy - nesie

    st.subheader("Несие нәтижелері")

    

    
    with st.container(border=True):
        st.metric("Ай сайынғы төлем", f"{tolem:,.2f} ₸")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.metric("Жалпы төлем", f"{jalpy:,.2f} ₸")

    with col2:
        with st.container(border=True):
            st.metric("Артық төлем", f"{artyk:,.2f} ₸")


    st.subheader("Ай сайынғы төлем кестесі")

    kaldyk = float(nesie)
    keste = []

    for ai in range(1, merzimi + 1):
        paiz_tolemi = kaldyk * r
        negizgi_karyz = tolem - paiz_tolemi
        ai_tolemi = tolem

        if ai == merzimi:
            negizgi_karyz = kaldyk
            ai_tolemi = negizgi_karyz + paiz_tolemi

        kaldyk = max(0, kaldyk - negizgi_karyz)

        keste.append({
            "Ай": ai,
            "Төлем": round(ai_tolemi, 2),
            "Пайыз": round(paiz_tolemi, 2),
            "Негізгі қарыз": round(negizgi_karyz, 2),
            "Қалдық": round(kaldyk, 2)
        })

    st.dataframe(keste, hide_index=True)

    st.subheader("Несие нұсқаларын салыстыру")

    salystyru = []

    for p in [12, 15, 18]:
        r2 = p / 100 / 12

        if r2 == 0:
            monthly = nesie / merzimi
        else:
            monthly = nesie * r2 / (1 - (1 + r2) ** (-merzimi))

        total = monthly * merzimi
        extra = total - nesie

        salystyru.append({
            "Пайыз (%)": p,
            "Ай сайынғы төлем": round(monthly, 2),
            "Жалпы төлем": round(total, 2),
            "Артық төлем": round(extra, 2)
        })

    st.dataframe(salystyru, hide_index=True)
