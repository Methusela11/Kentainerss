const cartWrapper = document.getElementById('cartWrapper');
const cartOverlay = document.getElementById('cartOverlay');
const cartCloseBtn = document.querySelector('.cart-close');

function openCart() {
    cartWrapper.classList.add('cart-open');
    document.body.classList.add('cart-open');
}

function closeCart() {
    cartWrapper.classList.remove('cart-open');
    document.body.classList.remove('cart-open');
}

/* Close on overlay click */
cartOverlay.addEventListener('click', closeCart);

/* Close on X click */
cartCloseBtn.addEventListener('click', closeCart);

/* Optional: ESC key */
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && cartWrapper.classList.contains('cart-open')) {
        closeCart();
    }
});


document.addEventListener("DOMContentLoaded", function () {
    // Delegate click events to dynamically updated buttons
    document.querySelector(".cart-sidebar").addEventListener("click", function(e) {
        if (e.target.classList.contains("cart-remove")) {
            const itemId = e.target.dataset.id;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/cart/remove/${itemId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
            .then(res => res.text())
            .then(html => {
                document.getElementById("cartSidebar").innerHTML = html;
            })
            .catch(err => {
                console.error("Error removing item:", err);
            });
        }
    });
});
