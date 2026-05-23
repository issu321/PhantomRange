/* ===== THREE.JS BACKGROUND ===== */
const canvas = document.getElementById('bg-canvas');
if (canvas) {
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x050505, 0.002);
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.z = 50;
  const renderer = new THREE.WebGLRenderer({ canvas, alpha:true, antialias:true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const nodeCount = 70;
  const nodes = [];
  const geo = new THREE.SphereGeometry(0.25, 16, 16);
  const cols = [0x00ff9d, 0x0088ff, 0xff0044, 0xffff00];
  for (let i=0;i<nodeCount;i++) {
    const mat = new THREE.MeshBasicMaterial({ color: cols[Math.floor(Math.random()*cols.length)] });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set((Math.random()-0.5)*120, (Math.random()-0.5)*80, (Math.random()-0.5)*60);
    mesh.userData = { vx:(Math.random()-0.5)*0.02, vy:(Math.random()-0.5)*0.02, vz:(Math.random()-0.5)*0.01 };
    scene.add(mesh); nodes.push(mesh);
  }
  const lineMat = new THREE.LineBasicMaterial({ color:0x00ff9d, transparent:true, opacity:0.07 });
  let lines = [];
  function updateLines() {
    lines.forEach(l=>scene.remove(l)); lines=[];
    for (let i=0;i<nodes.length;i++) for (let j=i+1;j<nodes.length;j++) {
      if (nodes[i].position.distanceTo(nodes[j].position) < 18) {
        const g = new THREE.BufferGeometry().setFromPoints([nodes[i].position, nodes[j].position]);
        const line = new THREE.Line(g, lineMat); scene.add(line); lines.push(line);
      }
    }
  }
  let mx=0, my=0, tx=0, ty=0;
  document.addEventListener('mousemove', e=>{ mx=(e.clientX-window.innerWidth/2)*0.001; my=(e.clientY-window.innerHeight/2)*0.001; });
  let frame=0;
  function animate() {
    requestAnimationFrame(animate); frame++;
    tx+=(mx-tx)*0.02; ty+=(my-ty)*0.02;
    camera.position.x+=(mx*30-camera.position.x)*0.01; camera.position.y+=(-my*30-camera.position.y)*0.01;
    camera.lookAt(scene.position);
    nodes.forEach(n=>{ n.position.x+=n.userData.vx; n.position.y+=n.userData.vy; n.position.z+=n.userData.vz; if(Math.abs(n.position.x)>60)n.userData.vx*=-1; if(Math.abs(n.position.y)>40)n.userData.vy*=-1; if(Math.abs(n.position.z)>30)n.userData.vz*=-1; const s=1+Math.sin(frame*0.05+n.position.x)*0.2; n.scale.set(s,s,s); });
    if(frame%10===0) updateLines(); renderer.render(scene, camera);
  }
  animate();
  window.addEventListener('resize',()=>{ camera.aspect=window.innerWidth/window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth,window.innerHeight); });
}

/* ===== GSAP SCROLL ===== */
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
  gsap.utils.toArray('.glass-card, .glass-panel, .feature-card, .about-card').forEach(el=>{
    gsap.from(el, { scrollTrigger:{ trigger:el, start:'top 85%' }, opacity:0, y:40, duration:0.8, ease:'power3.out' });
  });
}

/* ===== MOBILE NAV ===== */
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', ()=>{ navLinks.classList.toggle('open'); });
}

/* ===== NAV SCROLL ===== */
let lastScroll=0;
window.addEventListener('scroll',()=>{
  const nav=document.querySelector('.glass-nav');
  if(!nav)return;
  if(window.pageYOffset>100){ nav.style.background='rgba(5,5,10,0.85)'; nav.style.boxShadow='0 4px 30px rgba(0,0,0,0.5)'; }
  else { nav.style.background='rgba(5,5,10,0.4)'; nav.style.boxShadow='none'; }
});

/* ===== COPY TO CLIPBOARD ===== */
function copyCode(btn) {
  const block = btn.closest('.code-block');
  if(!block)return;
  const code = block.querySelector('code, pre');
  const text = code ? code.textContent : block.textContent;
  navigator.clipboard.writeText(text.trim()).then(()=>{ btn.style.color='var(--ng)'; setTimeout(()=>btn.style.color='',1500); });
}

/* ===== SIMULATION TERMINAL ===== */
const termOut = document.getElementById('terminal-output');
const mNodes = document.getElementById('metric-nodes');
const mBlocked = document.getElementById('metric-blocked');
const mComp = document.getElementById('metric-comp');
const mThreat = document.getElementById('metric-threat');
const pItems = document.querySelectorAll('.phase-item');

let curPhase=-1, nCount=0, bCount=0, cCount=0, tLevel=0;
const PHASES=[
  {name:"Reconnaissance",lines:[{t:"[*] Initializing virtual network scan...",c:"info"},{t:"[+] Discovered 8 active nodes in subnet 192.168.1.0/24",c:"info"},{t:"[*] Fingerprinting services on open ports...",c:"info"}]},
  {name:"Scanning",lines:[{t:"[*] Executing port enumeration...",c:"info"},{t:"[!] Open ports detected: 80, 443, 22, 3306, 8080",c:"alert"},{t:"[+] Service versions identified successfully",c:"info"}]},
  {name:"Credential Discovery",lines:[{t:"[*] Testing authentication mechanisms...",c:"info"},{t:"[!] Weak password policy detected on NODE-003",c:"alert"},{t:"[DEFENSE] AI Defender: Raised auth threshold for NODE-003",c:"defense"}]},
  {name:"Privilege Escalation",lines:[{t:"[*] Simulating access elevation vectors...",c:"info"},{t:"[!] ALERT: NODE-005 (Database) virtual compromise simulated",c:"alert"},{t:"[DEFENSE] Isolated NODE-005 in virtual quarantine zone",c:"defense"}]},
  {name:"Lateral Movement",lines:[{t:"[*] Mapping lateral traversal paths...",c:"info"},{t:"[DEFENSE] Deployed virtual honeypot on subnet 47",c:"defense"},{t:"[+] Lateral path blocked by AI Defender",c:"defense"}]},
  {name:"Data Exfiltration",lines:[{t:"[*] Scanning for sensitive virtual data stores...",c:"info"},{t:"[DEFENSE] Activated simulated IPS ruleset #8842",c:"defense"},{t:"[PATCH] Unpatched Service remediated on NODE-002",c:"patch"},{t:"[*] Simulation complete. Export report available.",c:"info"}]}
];
function typeLine(text,type,delay){
  return new Promise(r=>{
    setTimeout(()=>{
      const div=document.createElement('div'); div.className='out-line '+type; termOut.appendChild(div);
      let i=0; const iv=setInterval(()=>{ div.textContent+=text[i]; i++; if(i>=text.length){ clearInterval(iv); termOut.scrollTop=termOut.scrollHeight; r(); } },14);
    },delay);
  });
}
async function runPhase(){
  if(curPhase>=PHASES.length-1)return; curPhase++;
  pItems.forEach((item,idx)=>{ item.classList.remove('active','completed'); if(idx<curPhase)item.classList.add('completed'); if(idx===curPhase)item.classList.add('active'); });
  const phase=PHASES[curPhase]; await typeLine('>> PHASE '+(curPhase+1)+': '+phase.name,'phase',200);
  for(let line of phase.lines) await typeLine(line.t,line.c,350);
  nCount=8; bCount+=Math.floor(Math.random()*3)+1; if(curPhase>=3)cCount=Math.min(cCount+1,2); tLevel=Math.min(tLevel+Math.floor(Math.random()*3)+1,10);
  if(mNodes)mNodes.textContent=nCount; if(mBlocked)mBlocked.textContent=bCount; if(mComp)mComp.textContent=cCount; if(mThreat)mThreat.textContent=tLevel+'/10';
}
function autoRun(){ if(curPhase>=PHASES.length-1)resetSim(); const iv=setInterval(()=>{ if(curPhase>=PHASES.length-1)clearInterval(iv); else runPhase(); },2200); }
function resetSim(){ curPhase=-1; nCount=0; bCount=0; cCount=0; tLevel=0; if(termOut)termOut.innerHTML=''; pItems.forEach(i=>i.classList.remove('active','completed')); if(mNodes)mNodes.textContent='0'; if(mBlocked)mBlocked.textContent='0'; if(mComp)mComp.textContent='0'; if(mThreat)mThreat.textContent='0/10'; }
