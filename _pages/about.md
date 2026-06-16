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
</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
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

  window.changeSlide = dir => showSlide(idx + dir);
  window.goToSlide = n => showSlide(n);

  showSlide(0);
  setInterval(() => showSlide(idx + 1), 4000);
});
</script>
