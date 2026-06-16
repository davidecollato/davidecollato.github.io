---
permalink: /
title: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Hi! My name is Davide Collato, I'm a PhD student in Mathematical Sciences at [Politecnico di Torino](https://www.polito.it/).

## Research Interests

- Numerical approximation of integral equations
- Boundary Integral Equations and Boundary Element Method (BEM)
- Coupling between Virtual Element Method (VEM) and BEM
- Partial Differential Equations and their approximation

## Numerical Simulations

<div class="sim-wrapper">

  <!-- Viewport scorrevole -->
  <div class="sim-track-outer">
    <div class="sim-track" id="simTrack">
      <div class="sim-slide">
        <img src="/images/slideshow/half_real_kappa10.png" alt="Simulation 1">
        <div class="sim-caption">Descrizione simulazione 1</div>
      </div>
      <div class="sim-slide">
        <img src="/images/slideshow/pikachu_finenothresh.gif" alt="Simulation 2">
        <div class="sim-caption">Descrizione simulazione 2</div>
      </div>
    </div>
  </div>

  <!-- Controlli centrati sotto -->
  <div class="sim-controls">
    <a class="sim-btn" onclick="changeSlide(-1)">&#10094;</a>
    <span class="sim-dot active" onclick="goToSlide(0)"></span>
    <span class="sim-dot" onclick="goToSlide(1)"></span>
    <a class="sim-btn" onclick="changeSlide(1)">&#10095;</a>
  </div>

</div>

<style>
.sim-wrapper {
  max-width: 700px;
  margin: 1.5em auto;
}
.sim-track-outer {
  overflow: hidden;
  border-radius: 6px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.sim-track {
  display: flex;
  transition: transform 0.5s ease-in-out;
}
.sim-slide {
  min-width: 100%;
  box-sizing: border-box;
}
.sim-slide img {
  width: 100%;
  display: block;
}
.sim-caption {
  text-align: center;
  font-size: 0.9em;
  color: #555;
  padding: 8px 0 4px;
  background: white;
}
.sim-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}
.sim-btn {
  cursor: pointer;
  padding: 6px 14px;
  color: white;
  background: rgba(0,0,0,0.45);
  border-radius: 4px;
  font-size: 1.1em;
  user-select: none;
  text-decoration: none;
}
.sim-btn:hover { background: rgba(0,0,0,0.75); }
.sim-dot {
  display: inline-block;
  width: 10px; height: 10px;
  background: #bbb;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.3s;
}
.sim-dot.active { background: #555; }
</style>

<script>
document.addEventListener('DOMContentLoaded', function () {
  let idx = 0;
  const track = document.getElementById('simTrack');
  const dots = document.querySelectorAll('.sim-dot');
  const total = dots.length;

  function showSlide(n) {
    idx = (n + total) % total;
    track.style.transform = `translateX(-${idx * 100}%)`;
    dots.forEach(d => d.classList.remove('active'));
    dots[idx].classList.add('active');
  }

  window.changeSlide = dir => showSlide(idx + dir);
  window.goToSlide = n => showSlide(n);

  setInterval(() => showSlide(idx + 1), 4000);
});
</script>
