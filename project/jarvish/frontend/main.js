let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("jarvis"), alpha: true });

renderer.setSize(window.innerWidth, window.innerHeight * 0.6);

let geometry = new THREE.TorusGeometry(2, 0.5, 16, 100);
let material = new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true });
let core = new THREE.Mesh(geometry, material);

scene.add(core);
camera.position.z = 6;

function animate() {
  requestAnimationFrame(animate);
  core.rotation.x += 0.01;
  core.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();

function pulse() {
  core.scale.set(1.3, 1.3, 1.3);
  setTimeout(() => core.scale.set(1, 1, 1), 500);
}

function startListening() {
  document.getElementById("status").innerText = "LISTENING...";
  pulse();

  fetch("http://127.0.0.1:5000/listen")
    .then(res => res.json())
    .then(data => {
      document.getElementById("status").innerText = "SPEAKING...";
      document.getElementById("user").innerText = "YOU: " + data.user;
      document.getElementById("bot").innerText = "BOT: " + data.bot;
      pulse();
    });
}
