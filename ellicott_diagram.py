import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Mine Air Explosivity Analysis",
    page_icon="",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: black;
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    color: #D6D9DE;
}

.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    margin-bottom: 15px;
}

.metric-title {
    font-size: 18px;
    color: #cbd5e1;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}

.zone-box {
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Mine Air Inputs")

st.sidebar.markdown("### Enter Gas Concentrations (% Volume)")

O2 = st.sidebar.number_input(
    "Oxygen (O₂) %",
    min_value=0.0,
    max_value=100.0,
    step=0.1
)

N2 = st.sidebar.number_input(
    "Nitrogen (N₂) %",
    min_value=0.0,
    max_value=100.0,
    step=0.1
)

CO2 = st.sidebar.number_input(
    "Carbon Dioxide (CO₂) %",
    min_value=0.0,
    max_value=100.0,
    step=0.1
)

st.sidebar.markdown("---")

ch4 = st.sidebar.number_input(
    "Methane (CH₄) %",
    min_value=0.0,
    max_value=100.0,
    step=0.001
)

co = st.sidebar.number_input(
    "Carbon Monoxide (CO) %",
    min_value=0.0,
    max_value=100.0,
    step=0.001
)

h2 = st.sidebar.number_input(
    "Hydrogen (H₂) %",
    min_value=0.0,
    max_value=100.0,
    step=0.001
)

analyze = st.sidebar.button("🚀 Analyze Sample", use_container_width=True)

# ---------------- MAIN HEADER ----------------
st.title("Mine Air Explosivity Analysis Dashboard")

st.markdown("""
Analyze mine atmosphere samples to determine:

- Lower Explosivity Limit (LEL)
- Upper Explosivity Limit (UEL)
- Excess Nitrogen Requirement
- Oxygen Requirement
- Ellicot Explosion Zone
""")

# ---------------- ANALYSIS ----------------
if analyze:

    P = [ch4, co, h2]

    total_sum = O2 + N2 + CO2 + ch4 + co + h2

    if not np.isclose(total_sum, 100, atol=0.01):

        st.error(
            f"❌ Total gas concentration must equal 100%.\n\nCurrent Total = {total_sum:.2f}%"
        )

    else:

        # Explosion Data
        lel = [5.0, 12.5, 4.0]
        uel = [14.0, 74.2, 74.2]
        mcl = [5.9, 13.8, 4.3]
        list4 = [12.2, 6.1, 5.1]
        list5 = [6.07, 4.13, 16.59]

        pt = sum(P)

        if pt == 0:

            st.warning("⚠️ Explosive gas concentration is zero.")

        else:

            sum1 = sum(P[i] / lel[i] for i in range(3))
            sum2 = sum(P[i] / uel[i] for i in range(3))
            sum3 = sum(P[i] / mcl[i] for i in range(3))

            lel_mix = pt / sum1
            uel_mix = pt / sum2
            Lmin = pt / sum3

            Nex = (Lmin / pt) * np.dot(list5, P)
            O2_req = 0.2093 * (100 - Nex - Lmin)

            # ---------------- METRICS ----------------
            st.markdown("## 📊 Analysis Results")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">LEL</div>
                    <div class="metric-value">{lel_mix:.3f}%</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">UEL</div>
                    <div class="metric-value">{uel_mix:.3f}%</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Excess N₂</div>
                    <div class="metric-value">{Nex:.3f}%</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Required O₂</div>
                    <div class="metric-value">{O2_req:.3f}%</div>
                </div>
                """, unsafe_allow_html=True)

            # ---------------- ELLICOT CHART ----------------
            st.markdown("## 📈 Ellicot Explosion Chart")

            x = pt - Lmin
            y = O2 - O2_req

            col5, col6 = st.columns([2, 1])

            with col5:

                fig, ax = plt.subplots(figsize=(8, 6))

                ax.set_xlim(-15, 15)
                ax.set_ylim(-15, 15)

                # Quadrant colors
                ax.fill_between([0, 15], 0, 15, color="red", alpha=0.3)
                ax.fill_between([-15, 0], 0, 15, color="green", alpha=0.3)
                ax.fill_between([-15, 0], -15, 0, color="yellow", alpha=0.3)
                ax.fill_between([0, 15], -15, 0, color="blue", alpha=0.3)

                ax.axhline(0, color='black', linewidth=1.2)
                ax.axvline(0, color='black', linewidth=1.2)

                ax.scatter(
                    x,
                    y,
                    s=180,
                    color='black',
                    edgecolors='white',
                    linewidth=2,
                    zorder=5
                )

                ax.grid(True, linestyle='--', alpha=0.5)

                ax.set_xlabel("Fuel Content", fontsize=12)
                ax.set_ylabel("Oxygen Content", fontsize=12)

                ax.set_title(
                    "Ellicot Explosion Classification",
                    fontsize=16,
                    fontweight='bold'
                )

                st.pyplot(fig)

            with col6:

                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Fuel Content</div>
                    <div class="metric-value">{pt:.3f}%</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Oxygen Content</div>
                    <div class="metric-value">{O2:.3f}%</div>
                </div>
                """, unsafe_allow_html=True)

            # ---------------- ZONE CLASSIFICATION ----------------
            if x >= 0 and y >= 0:
                zone = "🔥 Explosive Zone"
                color = "#dc2626"

            elif x < 0 and y >= 0:
                zone = "⚠️ Potentially Explosive (Fuel-Lean)"
                color = "#16a34a"

            elif x < 0 and y < 0:
                zone = "⚠️ Potentially Explosive (Fuel-Rich)"
                color = "#ca8a04"

            else:
                zone = "✅ Non-Explosive Zone"
                color = "#2563eb"

            st.markdown(f"""
            <div class="zone-box" style="background-color:{color};">
                {zone}
            </div>
            """, unsafe_allow_html=True)

# ---------------- DEFAULT MESSAGE ----------------
else:

    st.info("👈 Enter gas concentrations from the sidebar and click 'Analyze Sample'.")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Developed for Mine Air Explosivity Assessment
</div>
""", unsafe_allow_html=True)