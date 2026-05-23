# PhantomRange Input Guide

## Simulation Usage

1. **Launch the App**
   - Linux: `bash install.sh`
   - Windows: `install.bat`

2. **Dashboard**
   - Select a predefined scenario or use "Random Generation"
   - Choose difficulty: Easy, Medium, Hard, Insane
   - Click **Initialize Simulation** to spawn the virtual network

3. **Simulation Lab**
   - Execute attack phases one by one or auto-run
   - Watch the AI Defender respond to each simulated threat
   - Monitor defense metrics in real time

4. **Network Graph**
   - Visualize node relationships with color-coded status
   - Green = Secure, Yellow = Alerted, Red = Compromised
   - Click individual nodes to inspect vulnerabilities
   - Patch discovered vulnerabilities directly from the UI

5. **AI Defender**
   - Review feature importance from the ML model
   - Read defense action logs
   - Follow AI-generated remediation recommendations

6. **Reports**
   - Export session data as JSON
   - Export node inventory as CSV
   - View matplotlib status distribution charts

7. **Terminal**
   - Real-time event stream with color-coded log levels
   - Download full session logs as plain text

## Difficulty Examples

| Difficulty | Nodes | Vulns | AI Aggression |
|------------|-------|-------|---------------|
| Easy       | 5     | Low   | Defensive     |
| Medium     | 8     | Med   | Balanced      |
| Hard       | 12    | High  | Aggressive    |
| Insane     | 16    | Max   | Relentless    |

## Scenario Examples

- **CyberHeist 2077**: Finance sector simulation
- **Neural Hospital**: Healthcare IoT environment
- **Shadow Grid**: Industrial control systems

## Troubleshooting

- **Port already in use**: Streamlit will prompt to run on another port
- **Module not found**: Ensure you activated the virtual environment
- **CSS not loading**: Verify `assets/styles.css` exists in the project root
