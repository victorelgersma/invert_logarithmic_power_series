import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math

# Force a wide layout to place controls and the plot side-by-side
st.set_page_config(layout="wide")

st.title("Newton's Series Inversion: $\ln(1+x)$ and $e^x - 1$")

# --- 1. SETUP STATE AND CALLBACKS ---
if "num_terms" not in st.session_state:
    st.session_state.num_terms = 5

min_t, max_t = 1, 12

def decrease_terms():
    if st.session_state.num_terms > min_t:
        st.session_state.num_terms -= 1

def increase_terms():
    if st.session_state.num_terms < max_t:
        st.session_state.num_terms += 1

num_terms = st.session_state.num_terms

# --- 2. CREATE THE SIDE-BY-SIDE DASHBOARD LAYOUT ---
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.write("### Controls")
    
    # Sub-columns for clean, side-by-side push buttons
    btn_col1, btn_col2, _ = st.columns([0.25, 0.25, 0.5])
    with btn_col1:
        st.button("➖ Remove Term", on_click=decrease_terms, use_container_width=True)
    with btn_col2:
        st.button("➕ Add Term", on_click=increase_terms, use_container_width=True)
        
    st.markdown(f"**Currently plotting:** $n = {num_terms}$ terms")
    st.write("---")
    
    # Dynamic Math Strings
    log_terms = []
    exp_terms = []
    for i in range(1, num_terms + 1):
        if i == 1:
            log_terms.append("x")
            exp_terms.append("x")
        else:
            sign = "-" if i % 2 == 0 else "+"
            log_terms.append(f"{sign} \\frac{{x^{{{i}}}}}{{{i}}}")
            exp_terms.append(f"+ \\frac{{x^{{{i}}}}}{{{math.factorial(i)}}}")

    log_equation = " ".join(log_terms)
    exp_equation = " ".join(exp_terms)

    st.markdown("**Logarithmic Series:**")
    st.latex(f"y = {log_equation}")

    st.markdown("**Exponential Inversion:**")
    st.latex(f"y = {exp_equation}")

with right_col:
    # --- 3. MATH CALCULATIONS & PLOT ---
    view_limit = 0.95
    x = np.linspace(-view_limit, view_limit, 400)

    y1 = np.zeros_like(x)
    for i in range(1, num_terms + 1):
        sign = 1 if i % 2 != 0 else -1
        y1 += sign * (x**i) / i

    y2 = np.zeros_like(x)
    for i in range(1, num_terms + 1):
        y2 += (x**i) / math.factorial(i)

    mask1 = (y1 >= -view_limit) & (y1 <= view_limit)
    mask2 = (y2 >= -view_limit) & (y2 <= view_limit)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x[mask1], y=y1[mask1], mode='lines', 
        name="ln(1+x) Approx",
        line=dict(color='royalblue', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=x[mask2], y=y2[mask2], mode='lines', 
        name="e^x - 1 Approx",
        line=dict(color='firebrick', width=3, dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=[-view_limit, view_limit], y=[-view_limit, view_limit], mode='lines',
        name="y = x (Mirror)",
        line=dict(color='rgba(128,128,128,0.6)', width=1.5, dash='dot')
    ))

    # Slightly reduced size (500x500) to keep the layout entirely above the fold
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        xaxis=dict(range=[-view_limit, view_limit], constrain="domain"),
        yaxis=dict(
            range=[-view_limit, view_limit],
            scaleanchor="x",
            scaleratio=1,
            constrain="domain"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        width=500,  
        height=500,
        margin=dict(l=10, r=10, t=10, b=10)
    )

    st.plotly_chart(fig, use_container_width=False)