function cursorAnimation() {
  const coords = { x: 0, y: 0 };
  const circles = document.querySelectorAll(".circle");
  const explosionColor = "#ff4000";
  const hideDelayMs = 200;
  const cursorUrl = "/assets/cursor.png";

  document.documentElement.style.cursor = `url("${cursorUrl}") 16 16, auto`;
  if (document.body) {
    document.body.style.cursor = `url("${cursorUrl}") 16 16, auto`;
  }

  circles.forEach((circle) => {
    circle.x = 0;
    circle.y = 0;
    circle.style.transition = "opacity 0.3s ease-in-out";
  });

  function trackMouse(event) {
    coords.x = event.clientX;
    coords.y = event.clientY;
  }

  function positionCircle(circle, x, y, scale) {
    circle.style.left = `${x - 12.5}px`;
    circle.style.top = `${y - 12.5}px`;
    circle.style.scale = scale;
    circle.x = x;
    circle.y = y;
  }

  function animateCircles() {
    let x = coords.x;
    let y = coords.y;

    circles.forEach((circle, index) => {
      positionCircle(circle, x, y, (20 - index) / 20);
      const nextCircle = circles[index + 1] || circles[0];
      x += (nextCircle.x - x) * 0.2;
      y += (nextCircle.y - y) * 0.2;
    });

    requestAnimationFrame(animateCircles);
  }

  let mouseTimeout;
  function hideCircles() {
    circles.forEach((circle) => {
      circle.style.opacity = "0";
    });
  }

  function showCircles() {
    circles.forEach((circle) => {
      circle.style.display = "block";
      circle.style.opacity = "1";
    });
  }

  function handleMouseMove(event) {
    trackMouse(event);
    showCircles();
    clearTimeout(mouseTimeout);
    mouseTimeout = setTimeout(hideCircles, hideDelayMs);
  }

  function spawnParticle(x, y) {
    const particle = document.createElement("div");
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * 167;
    const moveX = `${Math.cos(angle) * distance}px`;
    const moveY = `${Math.sin(angle) * distance}px`;

    particle.classList.add("particle");
    particle.style.left = `${x}px`;
    particle.style.top = `${y}px`;
    particle.style.background = explosionColor;
    particle.style.setProperty("--x", moveX);
    particle.style.setProperty("--y", moveY);

    document.body.appendChild(particle);

    setTimeout(() => {
      particle.remove();
    }, 500);
  }

  function explodeAt(x, y) {
    for (let i = 0; i < 30; i += 1) {
      spawnParticle(x, y);
    }
  }

  window.addEventListener("mousemove", handleMouseMove);
  window.addEventListener("click", (event) => {
    explodeAt(event.clientX, event.clientY);
  });

  animateCircles();
}

cursorAnimation();
