import streamlit as st
import numpy as np
import networkx as nx
import pandas as pd

from utils.geometry import find_triangles
from utils.ai import best_pass, xai_tactical_advice
from utils.visualization import draw_pitch

st.set_page_config(layout="wide")
st.title("⚽ Xabi Alonso Tactical Lab")

# -------------------
# PLAYER CONTROL
# -------------------
st.sidebar.header("🎮 Player Positions")

default_players = {
    "LCB": (30, 10), "CB": (42, 10), "RCB": (54, 10),
    "CDM1": (36, 20), "CDM2": (48, 20),
    "LAM": (30, 35), "RAM": (54, 35),
    "LW": (24, 50), "ST": (42, 50), "RW": (60, 50)
}

players = {}

for name, (x, y) in default_players.items():
    px = st.sidebar.slider(f"{name} X", 0, 68, int(x))
    py = st.sidebar.slider(f"{name} Y", 0, 105, int(y))
    players[name] = np.array([px, py])

# -------------------
# TRIANGLES
# -------------------
triangles = find_triangles(players)

# -------------------
# AI PASS
# -------------------
holder = st.selectbox("Ball Holder", list(players.keys()))
suggestion = best_pass(players, holder)

st.success(f"🧠 Best Pass: {holder} → {suggestion}")

# -------------------
# HEATMAP
# -------------------
grid_x, grid_y = np.meshgrid(np.linspace(0,68,50), np.linspace(0,105,50))
control = np.zeros_like(grid_x)

for i in range(len(grid_x)):
    for j in range(len(grid_x[0])):
        point = np.array([grid_x[i,j], grid_y[i,j]])
        control[i,j] = min(np.linalg.norm(point - p) for p in players.values())

# -------------------
# VISUAL
# -------------------
fig = draw_pitch(players, triangles, (grid_x, grid_y, control))
st.pyplot(fig)

# -------------------
# NETWORK
# -------------------
G = nx.Graph()

for t in triangles:
    for i in range(3):
        for j in range(i+1,3):
            G.add_edge(t[i], t[j])

st.write("📊 Connectivity:", round(nx.average_clustering(G),2))

# -------------------
# XAI ADVICE
# -------------------
if st.button("🤖 Get XAI Tactical Advice"):
    advice = xai_tactical_advice(players)
    st.write(advice)

# -------------------
# CSV UPLOAD
# -------------------
uploaded = st.file_uploader("📡 Upload CSV")

if uploaded:
    df = pd.read_csv(uploaded)
    st.write(df.head())