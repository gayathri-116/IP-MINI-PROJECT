document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu
  const burger = document.querySelector('.burger'), nav = document.getElementById('nav');
  burger?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });

  // Live total on the booking form
  const form = document.getElementById('bookForm');
  if (form) {
    const price = parseFloat(form.dataset.price), n = form.elements.travellers, out = document.getElementById('total');
    n.addEventListener('input', () => {
      const count = Math.max(1, Math.min(20, parseInt(n.value) || 1));
      out.textContent = '₹' + (price * count).toLocaleString('en-IN');
    });
  }

  // Confirm dialogs for destructive forms
  document.querySelectorAll('form[data-confirm]').forEach(f =>
    f.addEventListener('submit', e => { if (!confirm(f.dataset.confirm)) e.preventDefault(); }));
});

// Photo gallery on package page
document.addEventListener('click', e => {
  const t = e.target.closest('.thumb'); if (!t) return;
  const main = document.getElementById('mainImg');
  main.style.visibility = 'visible'; main.src = t.dataset.src;
  document.querySelectorAll('.thumb').forEach(x => x.classList.remove('active')); t.classList.add('active');
});
