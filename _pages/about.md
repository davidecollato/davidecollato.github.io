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

<div class="slideshow">
  <img id="slide" src="/images/hal_real_kappa10.png" style="width:100%; border-radius:8px;">
  <p id="caption" style="text-align:center; font-style:italic;"></p>
  <div style="text-align:center; margin-top:8px;">
    <button onclick="prevSlide()">&#8592;</button>
    <button onclick="nextSlide()">&#8594;</button>
  </div>
</div>

<script>
const slides = [
  { src: "/images/hal_real_kappa10.png", caption: "Descrizione simulazione 1" },
];
let i = 0;
function update() {
  document.getElementById('slide').src = slides[i].src;
  document.getElementById('caption').innerText = slides[i].caption;
}
function nextSlide() { i = (i + 1) % slides.length; update(); }
function prevSlide() { i = (i - 1 + slides.length) % slides.length; update(); }
update();
</script>
