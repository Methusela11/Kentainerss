document.addEventListener("click", function (e) {
    if (!e.target.classList.contains("cart-remove")) return;

    e.preventDefault();

    const itemId = e.target.dataset.id;
    const csrfToken = document.getElementById("csrf-token").value;

    fetch(`/cart/remove/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Remove failed");
        }
        return response.text();
    })
    .then(() => {
        // Reload page cart to refresh totals + rows
        location.reload();
    })
    .catch(err => console.error(err));
});

document.addEventListener("pointerdown", function (e) {

    if (
        !e.target.classList.contains("qty-increase") &&
        !e.target.classList.contains("qty-decrease")
    ) return;

    e.preventDefault();

    const btn = e.target;
    const row = btn.closest(".cart-row");

    const qtySpan = row.querySelector(".qty-value");
    const unitPrice = parseFloat(row.dataset.unitPrice);
    const totalCell = row.querySelector(".cart-col.total");

    let qty = parseInt(qtySpan.textContent);

    // Calculate instantly
    if (btn.classList.contains("qty-increase")) {
        qty++;
    } else {
        if (qty <= 1) return;
        qty--;
    }

    // 🚀 INSTANT UI UPDATE
    qtySpan.textContent = qty;
    totalCell.textContent =
        (qty * unitPrice).toLocaleString() + " KES";

    // Backend sync (no reload)
    fetch(`/cart/update-quantity/${btn.dataset.id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.getElementById("csrf-token").value,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `quantity=${qty}`,
    }).catch(() => {
        // rollback if error
        qtySpan.textContent = qty - 1;
    });
});
