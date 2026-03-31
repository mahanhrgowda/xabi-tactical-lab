import matplotlib.pyplot as plt
import numpy as np

def draw_pitch(players, triangles, control):
    fig, ax = plt.subplots(figsize=(6,10))

    # players
    for name, pos in players.items():
        ax.scatter(pos[0], pos[1])
        ax.text(pos[0]+1, pos[1]+1, name)

    # triangles
    for t in triangles:
        pts = [players[n] for n in t]
        xs = [p[0] for p in pts] + [pts[0][0]]
        ys = [p[1] for p in pts] + [pts[0][1]]
        ax.plot(xs, ys, alpha=0.4)

    # heatmap
    ax.contourf(control[0], control[1], control[2], levels=20, alpha=0.3)

    ax.set_xlim(0,68)
    ax.set_ylim(0,105)
    ax.invert_yaxis()

    return fig