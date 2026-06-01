import streamlit as st
import random
import json
import time
import os
import html
import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

# ============== CONFIGURATION ==============
st.set_page_config(
    page_title="PhantomRange | NeuralCTF",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CUSTOM CSS ==============
def inject_cyberpunk_css():
    css_path = os.path.join("assets", "styles.css")
    css_content = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
    else:
        css_content = """
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        body { background-color: #050505; color: #00ff9d; font-family: 'Share Tech Mono', monospace; }
        .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #111111 100%); }
        """
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# ============== SESSION STATE ==============
def init_state():
    defaults = {
        'page': 'Dashboard',
        'simulation_active': False,
        'difficulty': 'Medium',
        'logs': [],
        'sim_engine': None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# ============== DATA LOADING ==============
@st.cache_data
def load_scenarios():
    path = "scenarios.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# ============== SIMULATION ENGINE ==============
NODE_TYPES = ["Web Server", "Database", "API Gateway", "Cloud Node", "Workstation", "Firewall"]
VULN_TEMPLATES = [
    {"name": "Default Credentials", "severity": 8, "type": "Authentication", "fix": "Change default passwords immediately"},
    {"name": "Unpatched Service", "severity": 7, "type": "Patching", "fix": "Apply latest security patches"},
    {"name": "Weak Password Policy", "severity": 6, "type": "Policy", "fix": "Enforce strong password requirements"},
    {"name": "Exposed API Endpoint", "severity": 7, "type": "Configuration", "fix": "Implement API authentication and rate limiting"},
    {"name": "Missing MFA", "severity": 5, "type": "Authentication", "fix": "Enable multi-factor authentication"},
    {"name": "Verbose Error Messages", "severity": 4, "type": "Configuration", "fix": "Configure generic error responses"},
    {"name": "Open Management Port", "severity": 9, "type": "Network", "fix": "Restrict administrative ports via firewall"},
    {"name": "Outdated TLS Version", "severity": 6, "type": "Encryption", "fix": "Upgrade to TLS 1.3"},
]

ATTACK_STEPS = [
    {"phase": "Reconnaissance", "desc": "AI simulates information gathering about target infrastructure"},
    {"phase": "Scanning", "desc": "Simulated port and service enumeration on virtual nodes"},
    {"phase": "Credential Discovery", "desc": "Educational simulation of weak credential detection"},
    {"phase": "Privilege Escalation", "desc": "Simulated elevation of access in controlled environment"},
    {"phase": "Lateral Movement", "desc": "Virtual traversal between simulated network segments"},
    {"phase": "Data Exfiltration", "desc": "Simulated discovery of sensitive virtual data stores"},
]

DEFENSE_ACTIONS = [
    "Increased log monitoring on {node}",
    "Deployed virtual honeypot on subnet {subnet}",
    "Raised authentication threshold for {node}",
    "Activated simulated IPS ruleset #{rule_id}",
    "Recommended patch deployment for {vuln}",
    "Isolated {node} in virtual quarantine zone",
]

class PhantomNode:
    def __init__(self, node_id, node_type, difficulty):
        self.id = node_id
        self.type = node_type
        self.status = "Online"
        self.compromised = False
        self.security_level = random.randint(3, 9)
        self.open_ports = random.sample([80, 443, 22, 3306, 5432, 8080, 8443], k=random.randint(1, 4))
        self.services = [f"{node_type.lower()}-service-{i}" for i in range(random.randint(1, 3))]
        self.vulnerabilities = []
        self.alerts = 0
        self._apply_difficulty(difficulty)

    def _apply_difficulty(self, diff):
        mod = {"Easy": -2, "Medium": 0, "Hard": 2, "Insane": 4}.get(diff, 0)
        self.security_level = max(1, min(10, self.security_level + mod))
        vuln_count = max(0, random.randint(0, 3) + mod // 2)
        used_names = set()
        attempts = 0
        while len(used_names) < vuln_count and attempts < 20:
            template = random.choice(VULN_TEMPLATES)
            if template["name"] not in used_names:
                used_names.add(template["name"])
                vuln = {
                    "name": template["name"],
                    "severity": max(1, min(10, template["severity"] + mod)),
                    "type": template["type"],
                    "fix": template["fix"],
                    "discovered": False,
                    "patched": False
                }
                self.vulnerabilities.append(vuln)
            attempts += 1

class AIDefender:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.scaler = StandardScaler()
        self.trained = False
        self.threat_level = 0
        self.actions_log = []
        self._train_dummy()

    def _train_dummy(self):
        X = np.random.rand(100, 4) * 10
        y = (X[:, 0] + X[:, 1] > 10).astype(int)
        self.scaler.fit(X)
        Xs = self.scaler.transform(X)
        self.model.fit(Xs, y)
        self.trained = True

    def analyze(self, node, step_index):
        features = np.array([[node.security_level, len(node.vulnerabilities), node.alerts, step_index]])
        fs = self.scaler.transform(features)
        risk = self.model.predict_proba(fs)[0][1]
        self.threat_level = int(risk * 10)

        actions = []
        if risk > 0.6:
            action = random.choice(DEFENSE_ACTIONS).format(
                node=node.id,
                subnet=random.randint(1, 255),
                rule_id=random.randint(1000, 9999),
                vuln=random.choice(node.vulnerabilities)["name"] if node.vulnerabilities else "unknown"
            )
            actions.append(action)
            node.security_level = min(10, node.security_level + 1)
            node.alerts += 1
        return risk, actions

class PhantomSimulation:
    def __init__(self, difficulty="Medium", scenario_data=None):
        self.difficulty = difficulty
        self.nodes = []
        self.graph = nx.Graph()
        self.defender = AIDefender()
        self.step_index = 0
        self.logs = []
        self.metrics = {"attacks_blocked": 0, "nodes_compromised": 0, "vulns_found": 0, "vulns_patched": 0}
        self._generate_network(scenario_data)

    def _generate_network(self, scenario_data=None):
        if scenario_data and "nodes" in scenario_data:
            for n in scenario_data["nodes"]:
                node = PhantomNode(n["id"], n["type"], self.difficulty)
                self.nodes.append(node)
                self.graph.add_node(node.id, type=n["type"], status="Online")
        else:
            count = {"Easy": 5, "Medium": 8, "Hard": 12, "Insane": 16}.get(self.difficulty, 8)
            for i in range(count):
                ntype = random.choice(NODE_TYPES)
                node = PhantomNode(f"NODE-{i:03d}", ntype, self.difficulty)
                self.nodes.append(node)
                self.graph.add_node(node.id, type=ntype, status="Online")

        for i, node in enumerate(self.nodes):
            targets = random.sample(self.nodes, k=min(random.randint(1, 3), max(1, len(self.nodes)-1)))
            for t in targets:
                if t.id != node.id:
                    weight = random.randint(1, 10)
                    self.graph.add_edge(node.id, t.id, weight=weight)

        self.log("Initialized NeuralCTF simulation environment")
        self.log(f"Generated {len(self.nodes)} virtual nodes at {self.difficulty} difficulty")

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {msg}"
        self.logs.append(entry)
        return entry

    def step_attack(self):
        if self.step_index >= len(ATTACK_STEPS):
            return False

        step = ATTACK_STEPS[self.step_index]
        self.log(f"ATTACK PHASE: {step['phase']} - {step['desc']}")

        targets = random.sample(self.nodes, k=min(random.randint(1, 3), len(self.nodes)))
        for node in targets:
            risk, actions = self.defender.analyze(node, self.step_index)
            threshold = 0.5 - ({"Easy": 0.2, "Medium": 0.0, "Hard": -0.1, "Insane": -0.2}.get(self.difficulty, 0))

            if risk > threshold and node.vulnerabilities and not node.compromised:
                node.compromised = True
                node.status = "Compromised"
                self.metrics["nodes_compromised"] += 1
                self.log(f"ALERT: {node.id} ({node.type}) virtual compromise simulated")
                for v in node.vulnerabilities:
                    if not v["discovered"]:
                        v["discovered"] = True
                        self.metrics["vulns_found"] += 1
            else:
                self.metrics["attacks_blocked"] += 1
                self.log(f"DEFENSE: {node.id} attack vector neutralized by AI Defender")

            for a in actions:
                self.log(f"DEFENSE ACTION: {a}")
                self.defender.actions_log.append(a)

        self.step_index += 1
        return True

    def patch_vulnerability(self, node_id, vuln_name):
        for node in self.nodes:
            if node.id == node_id:
                for v in node.vulnerabilities:
                    if v["name"] == vuln_name and not v["patched"]:
                        v["patched"] = True
                        self.metrics["vulns_patched"] += 1
                        node.security_level = min(10, node.security_level + 1)
                        self.log(f"PATCH: {vuln_name} remediated on {node_id}")
                        return True
        return False

# ============== UI RENDERERS ==============
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="color:#00ff9d; font-family:monospace; text-shadow: 0 0 10px #00ff9d;">🔮 PHANTOMRANGE</h1>
            <p style="color:#0088ff; font-size:12px;">NeuralCTF CyberArena X</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        page = st.radio("Navigation", ["Dashboard", "Simulation Lab", "Network Graph", "AI Defender", "Reports", "Terminal"], label_visibility="collapsed")
        st.session_state.page = page

        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; margin-top:30px; opacity:0.7;">
            <p style="font-size:11px; color:#888;">Developed by <a href="https://github.com/issu321" target="_blank" style="color:#00ff9d; text-decoration:none;">issu321</a></p>
        </div>
        """, unsafe_allow_html=True)

def render_dashboard():
    st.markdown("""
    <div class="cyber-header">
        <h1>PHANTOM RANGE <span style="color:#00ff9d">DASHBOARD</span></h1>
        <p>Adaptive AI-Powered Cybersecurity Training Simulator</p>
    </div>
    """, unsafe_allow_html=True)

    sim = st.session_state.get('sim_engine')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Nodes", len(sim.nodes) if sim else 0, delta="Virtual")
    with col2:
        comp = sim.metrics["nodes_compromised"] if sim else 0
        st.metric("Compromised", comp, delta="Simulated")
    with col3:
        blocked = sim.metrics["attacks_blocked"] if sim else 0
        st.metric("Blocked", blocked, delta="By AI")
    with col4:
        risk = sim.defender.threat_level if sim else 0
        st.metric("Threat Level", f"{risk}/10", delta="Live")

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🎯 Mission Control")
        scenarios = load_scenarios()
        scenario_names = ["Random Generation"] + list(scenarios.keys()) if scenarios else ["Random Generation"]
        selected_scenario = st.selectbox("Scenario", scenario_names)
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Insane"], index=1)
        st.session_state.difficulty = diff

        if st.button("🚀 Initialize Simulation", use_container_width=True):
            scenario_data = scenarios.get(selected_scenario) if selected_scenario != "Random Generation" else None
            st.session_state.sim_engine = PhantomSimulation(diff, scenario_data)
            st.session_state.simulation_active = True
            st.session_state.logs = st.session_state.sim_engine.logs
            st.rerun()

        if st.button("🔄 Reset Environment", use_container_width=True):
            st.session_state.sim_engine = None
            st.session_state.simulation_active = False
            st.session_state.logs = []
            st.rerun()

    with c2:
        st.subheader("📊 Risk Heatmap")
        if sim:
            nodes = [n.id for n in sim.nodes]
            risks = [10 - n.security_level + len(n.vulnerabilities) for n in sim.nodes]
            df = pd.DataFrame({"Node": nodes, "Risk Score": risks})
            fig = px.bar(df, x="Node", y="Risk Score", color="Risk Score", 
                        color_continuous_scale=["#00ff9d", "#ffff00", "#ff0044"],
                        template="plotly_dark")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Initialize simulation to view risk analytics")

def render_simulation_lab():
    st.markdown("""
    <div class="cyber-header">
        <h1>SIMULATION <span style="color:#ff0044">LAB</span></h1>
        <p>Controlled Attack Chain & Defense Response Environment</p>
    </div>
    """, unsafe_allow_html=True)

    sim = st.session_state.get('sim_engine')
    if not sim:
        st.warning("No active simulation. Start one from the Dashboard.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("⚔️ Attack Chain Progression")
        progress = sim.step_index / len(ATTACK_STEPS)
        st.progress(progress)
        st.caption(f"Phase {sim.step_index}/{len(ATTACK_STEPS)}")

        if sim.step_index < len(ATTACK_STEPS):
            current = ATTACK_STEPS[sim.step_index]
            st.markdown(f"""
            <div style="background:#1a1a1a; border-left:4px solid #ff0044; padding:15px; margin:10px 0;">
                <h4 style="color:#ff0044; margin:0;">{current['phase']}</h4>
                <p style="color:#ccc; margin:5px 0 0 0;">{current['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("▶️ Execute Next Phase", use_container_width=True):
            sim.step_attack()
            st.session_state.logs = sim.logs
            st.rerun()

        if st.button("⏩ Auto-Run Remaining", use_container_width=True):
            while sim.step_index < len(ATTACK_STEPS):
                sim.step_attack()
            st.session_state.logs = sim.logs
            st.rerun()

    with col2:
        st.subheader("🛡️ Defense Metrics")
        m = sim.metrics
        st.metric("Attacks Blocked", m["attacks_blocked"])
        st.metric("Vulns Discovered", m["vulns_found"])
        st.metric("Vulns Patched", m["vulns_patched"])

        st.markdown("---")
        st.subheader("🧠 AI Defender Status")
        st.write(f"Threat Level: {sim.defender.threat_level}/10")
        st.write(f"Model Trained: {'Yes' if sim.defender.trained else 'No'}")
        st.write(f"Actions Taken: {len(sim.defender.actions_log)}")

def render_network_graph():
    st.markdown("""
    <div class="cyber-header">
        <h1>NETWORK <span style="color:#0088ff">TOPOLOGY</span></h1>
        <p>Live Virtual Infrastructure Visualization</p>
    </div>
    """, unsafe_allow_html=True)

    sim = st.session_state.get('sim_engine')
    if not sim:
        st.warning("Initialize simulation first.")
        return

    pos = nx.spring_layout(sim.graph, seed=42)

    edge_x, edge_y = [], []
    for edge in sim.graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x, node_y, node_color, node_text = [], [], [], []
    for node in sim.nodes:
        x, y = pos[node.id]
        node_x.append(x)
        node_y.append(y)
        if node.compromised:
            node_color.append("#ff0044")
        elif node.alerts > 0:
            node_color.append("#ffff00")
        else:
            node_color.append("#00ff9d")
        vulns = ", ".join([v["name"] for v in node.vulnerabilities]) or "None"
        node_text.append(f"{node.id}<br>Type: {node.type}<br>Status: {node.status}<br>Security: {node.security_level}<br>Vulns: {vulns}")

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color="#444"), hoverinfo='none', mode='lines')
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', hoverinfo='text',
        text=[n.id for n in sim.nodes], textposition="top center",
        marker=dict(size=20, color=node_color, line=dict(width=2, color="#fff")),
        hovertext=node_text
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, margin=dict(l=0, r=0, b=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Node Inspector")
    selected = st.selectbox("Select Node", [n.id for n in sim.nodes])
    for node in sim.nodes:
        if node.id == selected:
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Type:** {node.type}")
                st.write(f"**Status:** {node.status}")
                st.write(f"**Security Level:** {node.security_level}")
                st.write(f"**Open Ports:** {', '.join(map(str, node.open_ports))}")
            with c2:
                st.write("**Vulnerabilities:**")
                for v in node.vulnerabilities:
                    status = "🟢 Patched" if v["patched"] else "🔴 Active" if v["discovered"] else "⚪ Hidden"
                    st.write(f"- {v['name']} (Sev: {v['severity']}) {status}")
                    if v["discovered"] and not v["patched"]:
                        if st.button(f"Patch {v['name']}", key=f"patch_{node.id}_{v['name']}"):
                            sim.patch_vulnerability(node.id, v["name"])
                            st.rerun()

def render_ai_defender():
    st.markdown("""
    <div class="cyber-header">
        <h1>AI <span style="color:#00ff9d">DEFENDER</span></h1>
        <p>Adaptive Defense Intelligence & Recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    sim = st.session_state.get('sim_engine')
    if not sim:
        st.warning("No simulation data available.")
        return

    st.subheader("🧠 Neural Defense Analysis")

    features = ["Security Level", "Vuln Count", "Alert History", "Attack Phase"]
    importance = sim.defender.model.feature_importances_ if hasattr(sim.defender.model, 'feature_importances_') else [0.3, 0.4, 0.2, 0.1]
    df_imp = pd.DataFrame({"Feature": features, "Importance": importance})
    fig = px.bar(df_imp, x="Importance", y="Feature", orientation='h', color="Importance",
                color_continuous_scale=["#0088ff", "#00ff9d"], template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Defense Action Log")
    for action in reversed(sim.defender.actions_log[-10:]):
        st.markdown(f"""
        <div style="background:#0f1f0f; border-left:3px solid #00ff9d; padding:10px; margin:5px 0; font-family:monospace;">
            🛡️ {action}
        </div>
        """, unsafe_allow_html=True)

    st.subheader("💡 AI Recommendations")
    recs = set()
    for node in sim.nodes:
        for v in node.vulnerabilities:
            if v["discovered"] and not v["patched"]:
                recs.add(f"**{node.id}**: {v['fix']} to resolve *{v['name']}*")
    if recs:
        for r in recs:
            st.markdown(f"- {r}")
    else:
        st.success("No critical recommendations. Environment is secure.")

def render_reports():
    st.markdown("""
    <div class="cyber-header">
        <h1>SIMULATION <span style="color:#ffff00">REPORTS</span></h1>
        <p>Exportable Session Analytics & Audit Logs</p>
    </div>
    """, unsafe_allow_html=True)

    sim = st.session_state.get('sim_engine')
    if not sim:
        st.warning("Run a simulation to generate reports.")
        return

    st.subheader("📄 Session Summary")
    report = {
        "timestamp": datetime.now().isoformat(),
        "difficulty": sim.difficulty,
        "total_nodes": len(sim.nodes),
        "compromised_nodes": sum(1 for n in sim.nodes if n.compromised),
        "metrics": sim.metrics,
        "defender_actions": sim.defender.actions_log,
        "logs": sim.logs
    }

    st.json(report)

    report_json = json.dumps(report, indent=2)
    st.download_button("⬇️ Download JSON Report", report_json, "phantomrange_report.json", "application/json")

    node_data = []
    for n in sim.nodes:
        node_data.append({
            "ID": n.id, "Type": n.type, "Status": n.status, 
            "Security": n.security_level, "Vuln Count": len(n.vulnerabilities),
            "Compromised": n.compromised, "Alerts": n.alerts
        })
    df_nodes = pd.DataFrame(node_data)
    csv = df_nodes.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Node CSV", csv, "phantomrange_nodes.csv", "text/csv")

    st.subheader("📊 Status Distribution")
    fig, ax = plt.subplots(facecolor='#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    statuses = ["Online", "Compromised", "Alerted"]
    counts = [
        sum(1 for n in sim.nodes if n.status == "Online" and not n.compromised),
        sum(1 for n in sim.nodes if n.compromised),
        sum(1 for n in sim.nodes if n.alerts > 0 and not n.compromised)
    ]
    colors = ['#00ff9d', '#ff0044', '#ffff00']
    ax.bar(statuses, counts, color=colors, edgecolor='white')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.set_title("Node Status Distribution", color='white')
    st.pyplot(fig)

def render_terminal():
    st.markdown("""
    <div class="cyber-header">
        <h1>HACKER <span style="color:#00ff9d">TERMINAL</span></h1>
        <p>Real-time Simulation Event Stream</p>
    </div>
    """, unsafe_allow_html=True)

    logs = st.session_state.get('logs', [])

    terminal_html = '<div style="background:#050505; border:1px solid #333; border-radius:8px; padding:15px; font-family:monospace; color:#00ff9d; height:500px; overflow-y:auto;">'
    for log in logs[-50:]:
        color = "#ff0044" if "ALERT" in log else "#ffff00" if "DEFENSE" in log else "#00ff9d"
        if "PATCH" in log:
            color = "#0088ff"
        terminal_html += f'<div style="color:{color}; font-size:13px; margin:2px 0;">{html.escape(log)}</div>'
    terminal_html += '</div>'

    st.markdown(terminal_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Clear Terminal"):
            st.session_state.logs = []
            if st.session_state.get('sim_engine'):
                st.session_state.sim_engine.logs = []
            st.rerun()
    with col2:
        log_text = "\n".join(logs)
        st.download_button("💾 Save Logs", log_text, "phantomrange_logs.txt", "text/plain")

def main():
    inject_cyberpunk_css()
    init_state()
    render_sidebar()

    page = st.session_state.page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Simulation Lab":
        render_simulation_lab()
    elif page == "Network Graph":
        render_network_graph()
    elif page == "AI Defender":
        render_ai_defender()
    elif page == "Reports":
        render_reports()
    elif page == "Terminal":
        render_terminal()

    st.markdown("""
    <hr style="border-color:#333; margin-top:40px;">
    <div style="text-align:center; padding:20px; opacity:0.6;">
        <p style="font-family:monospace; font-size:12px; color:#888;">
        PhantomRange v1.0 | NeuralCTF Engine | <a href="https://github.com/issu321/PhantomRange" style="color:#00ff9d; text-decoration:none;">github.com/issu321/PhantomRange</a><br>
        Developed by <a href="https://github.com/issu321" style="color:#00ff9d; text-decoration:none;">issu321</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
