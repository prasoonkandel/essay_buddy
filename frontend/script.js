function cursorAnimation() {
  const cords = { x: 0, y: 0 };
  const circles = document.querySelectorAll(".circle");

  circles.forEach((circle) => {
    circle.x = 0;
    circle.y = 0;
  });

  window.addEventListener("mousemove", (event) => {
    cords.x = event.clientX;
    cords.y = event.clientY;
  });

  function animateCircles() {
    let x = cords.x;
    let y = cords.y;

    circles.forEach((circle, index) => {
      circle.style.left = x - 15 + "px";
      circle.style.top = y - 15 + "px";
      circle.x = x;
      circle.y = y;

      circle.style.scale = (15 - index) / 15;

      const nextCircle = circles[index + 1] || circles[0];
      x += (nextCircle.x - x) * 0.3;
      y += (nextCircle.y - y) * 0.2;
    });

    requestAnimationFrame(animateCircles);
  }

  animateCircles();
}

cursorAnimation();
