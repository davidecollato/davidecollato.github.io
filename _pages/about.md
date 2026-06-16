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

<!-- Slideshow simulazioni -->
<div class="slideshow-container">
  <div class="slide fade">
    <img src="/images/slideshow/half_real_kappa10.png" alt="Simulation 1">
    <div class="caption">Descrizione simulazione 1</div>
  </div>
  <div class="slide fade">
    <img src="/images/slideshow/pikachu_finenothresh.gif" alt="Simulation 1">
    <div class="caption">Descrizione simulazione 1</div>
  </div>

  <!-- Controlli -->
  <a class="prev" onclick="changeSlide(-1)">&#10094;</a>
  <a class="next" onclick="changeSlide(1)">&#10095;</a>
</div>

<!-- Pallini indicatori -->
<div style="text-align:center; margin-top: 8px;">
  <span class="dot" onclick="goToSlide(0)"></span>
  <span class="dot" onclick="goToSlide(1)"></span>
  <span class="dot" onclick="goToSlide(2)"></span>
</div>

<style>
.slideshow-container {
  position: relative;
  max-width: 700px;
  margin: 1.5em auto;
}
.slide { display: none; }
.slide img {
  width: 100%;
  border-radius: 6px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.caption {
  text-align: center;
  font-size: 0.9em;
  color: #555;
  padding: 6px 0;
}
.prev, .next {
  cursor: pointer;
  position: absolute;
  top: 45%;
  padding: 10px 16px;
  color: white;
  background: rgba(0,0,0,0.45);
  border-radius: 4px;
  font-size: 1.2em;
  user-select: none;
}
.prev { left: 0; }
.next { right: 0; }
.prev:hover, .next:hover { background: rgba(0,0,0,0.75); }
.dot {
  display: inline-block;
  width: 10px; height: 10px;
  margin: 4px;
  background: #bbb;
  border-radius: 50%;
  cursor: pointer;
}
.dot.active { background: #555; }
.fade { animation: fadeIn 0.6s ease-in; }
@keyframes fadeIn { from { opacity: 0.4 } to { opacity: 1 } }
</style>

<script>
let idx = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

function showSlide(n) {
  slides.forEach(s => s.style.display = 'none');
  dots.forEach(d => d.classList.remove('active'));
  idx = (n + slides.length) % slides.length;
  slides[idx].style.display = 'block';
  dots[idx].classList.add('active');
}
function changeSlide(dir) { showSlide(idx + dir); }
function goToSlide(n) { showSlide(n); }

// Autoplay ogni 4 secondi
showSlide(0);
setInterval(() => changeSlide(1), 4000);
</script>
