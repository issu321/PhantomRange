<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-00ff9d?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.28%2B-ff0044?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-1.3%2B-0088ff?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
</p>

<h1 align="center" style="color:#00ff9d; font-family:monospace;">
  🔮 PHANTOM RANGE
</h1>
<p align="center">
  <em>NeuralCTF CyberArena X — Adaptive AI-Powered Cybersecurity Training Simulator</em>
</p>

---

## 🌐 Overview

**PhantomRange** is a futuristic, defensive-focused cybersecurity simulation platform built entirely in Python. It generates dynamic virtual infrastructures, simulates safe educational attack chains, and deploys an **AI Defender** that adapts in real time. Designed for training, CTF practice, and portfolio demonstration, it delivers a cyberpunk-hacker aesthetic with production-grade architecture.

> **Developer:** [issu321](https://github.com/issu321)  
> **Repository:** [github.com/issu321/PhantomRange](https://github.com/issu321/PhantomRange)

---

## ✨ Features

- 🎯 **Adaptive Simulation Engine** — Randomized or scenario-based network generation
- 🤖 **AI Defender System** — scikit-learn powered threat detection with real-time countermeasures
- 🕸️ **Interactive Network Graphs** — Plotly-powered topology visualization
- ⚔️ **Safe Attack Chain Simulation** — Educational reconnaissance → exfiltration pipeline
- 📊 **Cyberpunk Dashboard** — Neon-themed metrics, risk heatmaps, and terminal streams
- 📁 **Exportable Reports** — JSON session dumps and CSV node inventories
- 🧠 **Explainable AI** — Feature importance and remediation recommendations

---

## 🚀 Installation

### Linux / macOS
```bash
git clone https://github.com/issu321/PhantomRange.git
cd PhantomRange
bash install.sh
```

### Windows
```cmd
git clone https://github.com/issu321/PhantomRange.git
cd PhantomRange
install.bat
```

The installer automatically creates a virtual environment, installs dependencies, and launches the Streamlit interface.

---

## 🎮 Usage

1. Open the **Dashboard** from the sidebar
2. Select a **Scenario** (or Random Generation) and **Difficulty**
3. Click **Initialize Simulation**
4. Navigate to **Simulation Lab** to execute attack phases
5. Monitor the **AI Defender** responses and patch vulnerabilities in **Network Graph**
6. Export reports from the **Reports** tab

---

## 🧪 Simulation Overview

| Phase | Description |
|-------|-------------|
| Reconnaissance | Simulated information gathering |
| Scanning | Port and service enumeration |
| Credential Discovery | Weak credential detection (educational) |
| Privilege Escalation | Simulated access elevation |
| Lateral Movement | Virtual network traversal |
| Data Exfiltration | Sensitive data store discovery |

All phases are **sandboxed and simulated**. No real exploitation occurs.

---

## 📸 Screenshots

> Placeholder: Dashboard with live metrics  
> Placeholder: Network topology graph  
> Placeholder: AI Defender feature importance  
> Placeholder: Hacker terminal event stream

---

## 🛠️ Technologies Used

- **Python 3.11+**
- **Streamlit** — Frontend UI
- **Plotly** — Interactive visualizations
- **NetworkX** — Graph topology generation
- **scikit-learn** — AI defender RandomForest classifier
- **NumPy & Pandas** — Data processing
- **Matplotlib** — Static chart exports

---

## 📁 Folder Structure

```
PhantomRange/
├── app.py                 # Main application (backend + frontend)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── install.sh             # Linux/macOS installer
├── install.bat            # Windows installer
├── inputguide.md          # Usage guide
├── scenarios.json         # Predefined simulation scenarios
├── .gitignore             # Git exclusions
└── assets/
    └── styles.css         # Cyberpunk Streamlit theme
```

---

## 🧠 AI Defender Explanation

The AI Defender uses a **RandomForestClassifier** trained on synthetic feature vectors representing:
- Node security level
- Vulnerability count
- Historical alert frequency
- Current attack phase index

When the simulation advances, the model predicts compromise probability per node. If risk exceeds the difficulty-adjusted threshold, the defender triggers actions such as virtual honeypot deployment, quarantine isolation, or authentication hardening.

---

## ⚠️ Educational Disclaimer

**PhantomRange is a SAFE educational simulation only.**  
- No real malware is generated  
- No actual network exploitation occurs  
- All attack chains are abstracted and sandboxed  
- Intended for cybersecurity education, CTF training, and defensive skill development

---

## 🗺️ Future Roadmap

- [ ] Plugin system for custom scenarios
- [ ] Multiplayer CTF mode via WebSocket
- [ ] LLM-powered narrative generation
- [ ] MITRE ATT&CK framework mapping
- [ ] Docker containerization

---

## 🤝 Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center" style="font-family:monospace; color:#888;">
  <strong>Developed by <a href="https://github.com/issu321">issu321</a></strong>
</p>
