
import random
from altair import Detail
import streamlit as st
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Ethical Clothing Score", page_icon="🧵", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #E6DAC6;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <h1 style='text-align: center; color: #2C3E50;'>Ethical Clothing Score</h1>
    <p style='text-align: center; color: grey;'>Enter a product URL to analyze its ethical impact.</p>
""", unsafe_allow_html=True)

product_url = st.text_input("Product URL")

def get_star_rating(score):
    if score < 20:
        return "★☆☆☆☆"
    elif score < 40:
        return "★★☆☆☆"
    elif score < 60:
        return "★★★☆☆"
    elif score < 80:
        return "★★★★☆"
    else:
        return "★★★★★"

def get_color(score):
    if score >= 75:
        return "#27ae60"  # green
    elif score >= 45:
        return "#e67e22"  # orange
    else:
        return "#c0392b"  # red

def get_colored_stars(score):
    full = score // 20
    empty = 5 - full
    color = get_color(score)
    return f"<span style='color:{color}; font-size:20px;'>{'★' * full}{'☆' * empty}</span>"

pros_cons_options = {
    'Environmental Impact': {
        'pros': [
            "Low carbon footprint", "Sustainable water usage",
            "Eco-friendly packaging", "Renewable energy production"
        ],
        'cons': [
            "Chemical processing", "Water pollution risks",
            "Land use for production", "Transportation emissions"
        ]
    },
    'Human Costs': {
        'pros': [
            "Fair wages", "Safe working conditions",
            "No child labour", "Employee benefits"
        ],
        'cons': [
            "Limited transparency", "Supply chain oversight",
            "Overtime issues", "Worker representation"
        ]
    },
    'Material Sustainability': {
        'pros': [
            "Recycled materials", "Biodegradable components",
            "Renewable resources", "Durability and longevity"
        ],
        'cons': [
            "Mixed materials", "Non-recyclable components",
            "Synthetic fibres", "Limited repairability"
        ]
    }
}

if st.button("Analyze"):
    sub_scores = {
    'Environmental Impact': random.randint(0, 100),
    'Human Costs': random.randint(0, 100),
    'Material Sustainability': random.randint(0, 100)
}
    overall_score = int(sum(sub_scores.values()) / len(sub_scores))
    
    import random
    sub_details = {}
    for name in sub_scores:
        pros = random.sample(pros_cons_options[name]['pros'], k=random.randint(2, 3))
        cons = random.sample(pros_cons_options[name]['cons'], k=random.randint(2, 3))
        sub_details[name] = {'pros': pros, 'cons': cons}

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall_score,
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': get_color(overall_score)},
            'steps': [
                {'range': [0, 44], 'color': '#f8d7da'},
                {'range': [45, 74], 'color': '#ffeeba'},
                {'range': [75, 100], 'color': '#d4edda'}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"<h2 style='color: #2C3E50;'>Overall Ethical Score</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: #2C3E50;'>{overall_score}/100</h1>", unsafe_allow_html=True)
    st.markdown(get_colored_stars(overall_score), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    for idx, (label, score) in enumerate(sub_scores.items()):
        col = [col1, col2, col3][idx]
        with col:
            bg_color = "#CFF1D4" if "Environmental" in label else "#FDD6D6" if "Human" in label else "#FFEDC2"
            icon = "🌿" if "Environmental" in label else "✋" if "Human" in label else "♻️"
            color = get_color(score)
            st.markdown(f"""
                <div style='background-color: {bg_color}; padding: 20px; border-radius: 10px;'>
                    <h3 style='color: #2C3E50;'>{icon} {label}</h3>
                    <b>Score:</b> {score}/100<br>
                    {get_colored_stars(score)}
            """, unsafe_allow_html=True)

            pros = random.sample(pros_cons_options[label]['pros'], k=3)
            cons = random.sample(pros_cons_options[label]['cons'], k=2)

            with st.expander("Details"):
                st.markdown("**Pros:**")
                for item in sub_details[label]["pros"]:
                    st.markdown(f"✅ {item}")
                st.markdown("**Cons:**")
                for item in sub_details[label]["cons"]:
                    st.markdown(f"❌ {item}")
        st.markdown("</div>", unsafe_allow_html=True)

IMAGE_FOLDER = "images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

DB_FILE = "articles.csv"
LOG_FILE = "modifications.log"
