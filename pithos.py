import hashlib
import random
from datetime import datetime
from pyscript import document

# --- GLOBAL STATE ---
state = {
    "ostraka_votes": {},
    "current_sphinx_status": "unknown"
}

# ==========================================
# 📊 CORE LOGIC
# ==========================================
def run_core(event):
    # Input
    try:
        pop = int(document.getElementById("core-pop").value)
        budget = int(document.getElementById("core-budget").value)
        users = int(document.getElementById("core-users").value)
    except:
        document.getElementById("core-result").innerHTML = "<span class='status-err'>Error: Invalid Input</span>"
        return

    # Logic
    P_total = 124000000
    N_muni = 1718
    B_std = P_total / N_muni  # 72,176

    S_factor = pop / B_std
    std_budget = 10000000 * S_factor # 1000万単位
    
    I_budget = budget / std_budget
    I_coverage = users / B_std
    
    if I_coverage == 0:
        d_index = 9999.0
    else:
        d_index = I_budget / I_coverage

    # Output
    res_html = f"Scale Factor: {S_factor:.2f}<br>"
    res_html += f"D_index: <b>{d_index:.1f}</b><br><br>"
    
    if d_index > 100:
        res_html += "<span class='status-err'>🚨 REJECT: 異常値 (Abnormal Distortion)</span>"
    elif d_index > 10:
        res_html += "<span class='status-warn'>⚠️ WARNING: 高コスト体質</span>"
    else:
        res_html += "<span class='status-ok'>✅ APPROVED: 健全</span>"

    document.getElementById("core-result").innerHTML = res_html

# ==========================================
# 💰 TREASURER
# ==========================================
def run_treasurer(event):
    team = document.getElementById("tr-team").value
    amount = document.getElementById("tr-amount").value
    
    # Generate Hash
    raw_data = f"{team}{amount}SBCM_BANK{datetime.now()}"
    data_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    # Zengin CSV Format (Mock)
    csv_line = f"2,8888,SBCM_BANK,{team},{amount},0,{data_hash}"
    
    output = f"Generating Zengin-Format CSV...<br>"
    output += f"--------------------------------<br>"
    output += f"{csv_line}<br>"
    output += f"--------------------------------<br>"
    output += f"🔒 Integrity Hash:<br>{data_hash[:20]}..."
    
    document.getElementById("tr-result").innerHTML = output

# ==========================================
# 👁️ SPHINX
# ==========================================
def load_quest(event):
    # Randomly decide if the image is valid or fake
    is_clean = random.random() > 0.4
    state["current_sphinx_status"] = "ok" if is_clean else "ng"
    
    emoji = "✅" if is_clean else "🚧"
    # In reality, this would be hidden from the user until verified
    # For demo, we keep it hidden in logic, visual is just a placeholder
    
    # Randomly show a visual state (Demo only)
    visual = "🛣️" if is_clean else "🕳️"
    document.getElementById("sphinx-img").innerText = visual
    document.getElementById("sphinx-result").innerHTML = "New Quest Loaded. <br>Is the hole fixed?"

def sphinx_verify(event):
    if state["current_sphinx_status"] == "ok":
        msg = "<span class='status-ok'>Correct! Transaction Approved. (+5pt)</span>"
    else:
        msg = "<span class='status-err'>Alert! You verified a FAKE image. Reputation Decreased.</span>"
    document.getElementById("sphinx-result").innerHTML = msg

def sphinx_reject(event):
    if state["current_sphinx_status"] == "ng":
        msg = "<span class='status-ok'>Correct! Fraud Detected. (+10pt)</span>"
    else:
        msg = "<span class='status-warn'>Warning: You rejected a valid work.</span>"
    document.getElementById("sphinx-result").innerHTML = msg

# ==========================================
# 🏺 OSTRAKA
# ==========================================
def cast_ostraka(event):
    target = document.getElementById("os-target").value
    reason = document.getElementById("os-reason").value
    
    if target not in state["ostraka_votes"]:
        state["ostraka_votes"][target] = 0
    
    state["ostraka_votes"][target] += 1
    count = state["ostraka_votes"][target]
    
    output = f"🗳️ Shard Cast against: <b>{target}</b><br>"
    output += f"Crime: {reason}<br>"
    output += f"Total Shards: {count}<br><br>"
    
    if count >= 5:
        output += "<span class='status-err'>💀 EXECUTE BANISHMENT: Threshold Reached.</span>"
    else:
        output += f"<span class='status-warn'>... {5 - count} more shards to banish.</span>"
        
    document.getElementById("os-result").innerHTML = output

# Initialize
load_quest(None)
