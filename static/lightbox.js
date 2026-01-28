document.addEventListener("click", (e) => {
  const img = e.target.closest(".post-body img");
  if (!img) return;

  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.innerHTML = `<img src="${img.src}" alt="">`;

  const close = () => overlay.remove();

  overlay.addEventListener("click", close);
  document.addEventListener(
    "keydown",
    (ev) => ev.key === "Escape" && close(),
    { once: true }
  );

  document.body.appendChild(overlay);
});
