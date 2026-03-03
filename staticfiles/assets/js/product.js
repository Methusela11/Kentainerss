// product.js — lightweight gallery + quantity + dynamic add-to-cart price
document.addEventListener('DOMContentLoaded', function () {
  // Gallery thumbnail click
  const thumbs = document.querySelectorAll('.gallery-thumbs .thumb');
  const mainImage = document.getElementById('main-image');

  if (thumbs && mainImage) {
    thumbs.forEach(btn => {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const src = this.getAttribute('data-src');
        if (!src) return;
        // smooth swap
        mainImage.style.opacity = '0';
        setTimeout(() => {
          mainImage.src = src;
          mainImage.style.opacity = '1';
        }, 160);
      });
    });
  }

  // Quantity buttons
  const qtyInput = document.getElementById('quantity');
  const qtyButtons = document.querySelectorAll('.qty-btn');

  qtyButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const action = this.dataset.action;
      let val = parseInt(qtyInput.value, 10) || 1;
      if (action === 'increase') val++;
      else if (action === 'decrease') val = Math.max(1, val - 1);
      qtyInput.value = val;
      updateAddToCartPrice();
    });
  });

  qtyInput && qtyInput.addEventListener('change', () => {
    let v = parseInt(qtyInput.value, 10) || 1;
    if (v < 1) v = 1;
    qtyInput.value = v;
    updateAddToCartPrice();
  });

  // update price on quantity or selection change
  const priceBase = parseFloat(document.getElementById('add-to-cart-price').textContent) || 0;
  const sizeSelect = document.getElementById('size-select');

  function getSizeMultiplier() {
    // If your backend provides per-size price, you should embed price data attributes.
    // This is a simple placeholder: if sizes change price, adjust accordingly.
    if (!sizeSelect) return 1;
    const val = sizeSelect.value;
    // Example: if option text contains "500L - 5,000" you could parse; better: include data-price in option
    const selected = sizeSelect.selectedOptions[0];
    if (selected && selected.dataset && selected.dataset.price) {
      return parseFloat(selected.dataset.price) || 1;
    }
    return 1;
  }

  function updateAddToCartPrice() {
    const qty = parseInt(qtyInput.value, 10) || 1;
    const sizeMult = getSizeMultiplier();
    const computed = Math.round(priceBase * sizeMult * qty);
    document.getElementById('add-to-cart-price').textContent = computed.toLocaleString();
  }

  if (sizeSelect) {
    sizeSelect.addEventListener('change', updateAddToCartPrice);
  }

  // initialize
  updateAddToCartPrice();

  // graceful fallback for add-to-cart form: submits normally to server route
  const addToCartForm = document.getElementById('add-to-cart-form');
  if (addToCartForm) {
    addToCartForm.addEventListener('submit', function (e) {
      // let default submission occur; if you want AJAX, implement here.
      // e.preventDefault();
    });
  }
});
