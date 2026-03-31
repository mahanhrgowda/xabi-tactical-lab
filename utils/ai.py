import numpy as np
import requests
import os

def best_pass(players, holder):
    p1 = players[holder]
    best = None
    best_score = -999

    for name, p2 in players.items():
        if name == holder:
            continue
        
        dist = np.linalg.norm(p1 - p2)
        progression = p2[1] - p1[1]
        
        score = -abs(dist - 12) + progression
        
        if score > best_score:
            best_score = score
            best = name
    
    return best


# 🔥 XAI API integration
def xai_tactical_advice(players):
    api_key = os.getenv("XAI_API_KEY")
    
    if not api_key:
        return "⚠️ No XAI API key found"

    prompt = f"""
    Analyze this football formation and give tactical advice:
    {players}
    Focus on Xabi Alonso style.
    """

    try:
        res = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-4-1-fast-reasoning",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        return res.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"