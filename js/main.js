/* ===== THREE.JS BACKGROUND ===== */
const canvas = document.getElementById('bg-canvas');
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x050505, 0.002);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 50;

const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

/* Nodes */
const nodeCount = 80;
const nodes = [];
const nodeGeometry = new THREE.SphereGeometry(0.3, 16, 16);
const nodeColors = [0x00ff9d, 0x0088ff, 0xff0044, 0xffff00];

for (let i = 0; i < nodeCount; i++) {
    const color = nodeColors[Math.floor(Math.random() * nodeColors.length)];
    const material = new THREE.MeshBasicMaterial({ color: color });
    const mesh = new THREE.Mesh(nodeGeometry, material);

    mesh.position.x = (Math.random() - 0.5) * 120;
    mesh.position.y = (Math.random() - 0.5) * 80;
    mesh.position.z = (Math.random() - 0.5) * 60;

    mesh.userData = {
        velX: (Math.random() - 0.5) * 0.02,
        velY: (Math.random() - 0.5) * 0.02,
        velZ: (Math.random() - 0.5) * 0.01,
        baseColor: color
    };

    scene.add(mesh);
    nodes.push(mesh);
}

/* Connections */
const lineMaterial = new THREE.LineBasicMaterial({ 
    color: 0x00ff9d, 
    transparent: true, 
    opacity: 0.08 
});
const lines = [];

function updateConnections() {
    // Remove old lines
    lines.forEach(l => scene.remove(l));
    lines.length = 0;

    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const dist = nodes[i].position.distanceTo(nodes[j].position);
            if (dist < 18) {
                const geometry = new THREE.BufferGeometry().setFromPoints([
                    nodes[i].position,
                    nodes[j].position
                ]);
                const line = new THREE.Line(geometry, lineMaterial);
                scene.add(line);
                lines.push(line);
            }
        }
    }
}

/* Mouse interaction */
let mouseX = 0, mouseY = 0;
let targetX = 0, targetY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX - window.innerWidth / 2) * 0.001;
    mouseY = (e.clientY - window.innerHeight / 2) * 0.001;
});

/* Animation Loop */
let frame = 0;
function animate() {
    requestAnimationFrame(animate);
    frame++;

    targetX += (mouseX - targetX) * 0.02;
    targetY += (mouseY - targetY) * 0.02;

    camera.position.x += (mouseX * 30 - camera.position.x) * 0.01;
    camera.position.y += (-mouseY * 30 - camera.position.y) * 0.01;
    camera.lookAt(scene.position);

    nodes.forEach(node => {
        node.position.x += node.userData.velX;
        node.position.y += node.userData.velY;
        node.position.z += node.userData.velZ;

        // Boundary wrap
        if (Math.abs(node.position.x) > 60) node.userData.velX *= -1;
        if (Math.abs(node.position.y) > 40) node.userData.velY *= -1;
        if (Math.abs(node.position.z) > 30) node.userData.velZ *= -1;

        // Pulse effect
        const scale = 1 + Math.sin(frame * 0.05 + node.position.x) * 0.2;
        node.scale.set(scale, scale, scale);
    });

    if (frame % 10 === 0) updateConnections();

    renderer.render(scene, camera);
}
animate();

/* Resize */
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

/* ===== GSAP SCROLL ANIMATIONS ===== */
gsap.registerPlugin(ScrollTrigger);

// Hero elements
gsap.from('.hero-title', { opacity: 0, y: 50, duration: 1.2, ease: 'power3.out', delay: 0.2 });
gsap.from('.hero-subtitle', { opacity: 0, y: 30, duration: 1, ease: 'power3.out', delay: 0.5 });
gsap.from('.hero-cta', { opacity: 0, y: 20, duration: 0.8, ease: 'power3.out', delay: 0.8 });
gsap.from('.stat-card', { 
    opacity: 0, y: 40, duration: 0.8, stagger: 0.15, ease: 'back.out(1.7)', delay: 1.1 
});

// Features
gsap.from('.feature-card', {
    scrollTrigger: { trigger: '#features', start: 'top 75%' },
    opacity: 0, y: 60, rotateX: 15, stagger: 0.15, duration: 0.9, ease: 'power3.out'
});

// Simulation
gsap.from('.sim-visual', {
    scrollTrigger: { trigger: '#simulation', start: 'top 70%' },
    opacity: 0, x: -60, duration: 1, ease: 'power3.out'
});
gsap.from('.sim-info .info-card', {
    scrollTrigger: { trigger: '#simulation', start: 'top 70%' },
    opacity: 0, x: 60, stagger: 0.2, duration: 0.9, ease: 'power3.out'
});

// Tech orbit
gsap.from('.tech-orbit', {
    scrollTrigger: { trigger: '#tech', start: 'top 70%' },
    opacity: 0, scale: 0.8, duration: 1.2, ease: 'elastic.out(1, 0.5)'
});

// CTA
gsap.from('.cta-content', {
    scrollTrigger: { trigger: '.cta', start: 'top 75%' },
    opacity: 0, y: 50, duration: 1, ease: 'power3.out'
});

/* ===== STAT COUNTER ANIMATION ===== */
const statNumbers = document.querySelectorAll('.stat-number');
statNumbers.forEach(num => {
    const target = parseInt(num.getAttribute('data-target'));
    gsap.to(num, {
        scrollTrigger: { trigger: num, start: 'top 85%' },
        innerHTML: target,
        duration: 2,
        snap: { innerHTML: 1 },
        ease: 'power2.out'
    });
});

/* ===== SIMULATION TERMINAL ===== */
const terminalOutput = document.getElementById('terminal-output');
const metricNodes = document.getElementById('metric-nodes');
const metricBlocked = document.getElementById('metric-blocked');
const metricComp = document.getElementById('metric-comp');
const metricThreat = document.getElementById('metric-threat');
const phaseItems = document.querySelectorAll('.phase-item');

let currentPhase = -1;
let nodesCount = 0;
let blockedCount = 0;
let compCount = 0;
let threatLevel = 0;

const PHASES = [
    { name: "Reconnaissance", lines: [
        { text: "[*] Initializing virtual network scan...", type: "info" },
        { text: "[+] Discovered 8 active nodes in subnet 192.168.1.0/24", type: "info" },
        { text: "[*] Fingerprinting services on open ports...", type: "info" }
    ]},
    { name: "Scanning", lines: [
        { text: "[*] Executing port enumeration...", type: "info" },
        { text: "[!] Open ports detected: 80, 443, 22, 3306, 8080", type: "alert" },
        { text: "[+] Service versions identified successfully", type: "info" }
    ]},
    { name: "Credential Discovery", lines: [
        { text: "[*] Testing authentication mechanisms...", type: "info" },
        { text: "[!] Weak password policy detected on NODE-003", type: "alert" },
        { text: "[DEFENSE] AI Defender: Raised auth threshold for NODE-003", type: "defense" }
    ]},
    { name: "Privilege Escalation", lines: [
        { text: "[*] Simulating access elevation vectors...", type: "info" },
        { text: "[!] ALERT: NODE-005 (Database) virtual compromise simulated", type: "alert" },
        { text: "[DEFENSE] Isolated NODE-005 in virtual quarantine zone", type: "defense" }
    ]},
    { name: "Lateral Movement", lines: [
        { text: "[*] Mapping lateral traversal paths...", type: "info" },
        { text: "[DEFENSE] Deployed virtual honeypot on subnet 47", type: "defense" },
        { text: "[+] Lateral path blocked by AI Defender", type: "defense" }
    ]},
    { name: "Data Exfiltration", lines: [
        { text: "[*] Scanning for sensitive virtual data stores...", type: "info" },
        { text: "[DEFENSE] Activated simulated IPS ruleset #8842", type: "defense" },
        { text: "[PATCH] Unpatched Service remediated on NODE-002", type: "patch" },
        { text: "[*] Simulation complete. Export report available.", type: "info" }
    ]}
];

function typeLine(text, type, delay) {
    return new Promise(resolve => {
        setTimeout(() => {
            const div = document.createElement('div');
            div.className = `out-line ${type}`;
            terminalOutput.appendChild(div);

            let i = 0;
            const interval = setInterval(() => {
                div.textContent += text[i];
                i++;
                if (i >= text.length) {
                    clearInterval(interval);
                    terminalOutput.scrollTop = terminalOutput.scrollHeight;
                    resolve();
                }
            }, 15);
        }, delay);
    });
}

async function runPhase() {
    if (currentPhase >= PHASES.length - 1) return;
    currentPhase++;

    // Update phase list UI
    phaseItems.forEach((item, idx) => {
        item.classList.remove('active', 'completed');
        if (idx < currentPhase) item.classList.add('completed');
        if (idx === currentPhase) item.classList.add('active');
    });

    const phase = PHASES[currentPhase];
    await typeLine(`>> PHASE ${currentPhase + 1}: ${phase.name}`, 'phase', 200);

    for (let line of phase.lines) {
        await typeLine(line.text, line.type, 400);
    }

    // Update metrics
    nodesCount = 8;
    blockedCount += Math.floor(Math.random() * 3) + 1;
    if (currentPhase >= 3) compCount = Math.min(compCount + 1, 2);
    threatLevel = Math.min(threatLevel + Math.floor(Math.random() * 3) + 1, 10);

    metricNodes.textContent = nodesCount;
    metricBlocked.textContent = blockedCount;
    metricComp.textContent = compCount;
    metricThreat.textContent = threatLevel + "/10";
}

function autoRun() {
    if (currentPhase >= PHASES.length - 1) resetSim();
    const interval = setInterval(() => {
        if (currentPhase >= PHASES.length - 1) {
            clearInterval(interval);
        } else {
            runPhase();
        }
    }, 2500);
}

function resetSim() {
    currentPhase = -1;
    nodesCount = 0;
    blockedCount = 0;
    compCount = 0;
    threatLevel = 0;
    terminalOutput.innerHTML = '';
    phaseItems.forEach(item => item.classList.remove('active', 'completed'));
    metricNodes.textContent = '0';
    metricBlocked.textContent = '0';
    metricComp.textContent = '0';
    metricThreat.textContent = '0/10';
}

/* ===== COPY INSTALL COMMAND ===== */
function copyInstall() {
    const cmd = document.getElementById('install-cmd').textContent;
    navigator.clipboard.writeText(cmd).then(() => {
        const btn = document.querySelector('.copy-btn');
        btn.style.color = 'var(--neon-green)';
        setTimeout(() => btn.style.color = '', 1500);
    });
}

/* ===== MOBILE NAV ===== */
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
    navLinks.style.position = 'absolute';
    navLinks.style.top = '100%';
    navLinks.style.left = '0';
    navLinks.style.right = '0';
    navLinks.style.flexDirection = 'column';
    navLinks.style.background = 'rgba(5,5,10,0.95)';
    navLinks.style.backdropFilter = 'blur(20px)';
    navLinks.style.padding = '1rem 2rem';
    navLinks.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
});

/* ===== NAV SCROLL EFFECT ===== */
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.glass-nav');
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        nav.style.background = 'rgba(5, 5, 10, 0.85)';
        nav.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
    } else {
        nav.style.background = 'rgba(5, 5, 10, 0.4)';
        nav.style.boxShadow = 'none';
    }
    lastScroll = currentScroll;
});
