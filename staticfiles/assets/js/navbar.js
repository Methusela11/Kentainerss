
//images hover on shop links
document.addEventListener("DOMContentLoaded", function () {

    const menuItems = document.querySelectorAll(".kc-menu-list li");
    const displayImg = document.getElementById("kc-menu-img");

    menuItems.forEach(item => {
        item.addEventListener("mouseenter", () => {
            const img = item.getAttribute("data-img");
            if (img) displayImg.src = img;
        });
    });

});

const hamburger = document.getElementById("openMobile");
const closeBtn = document.getElementById("closeMobile");
const overlay = document.getElementById("mobileOverlay");
const menu = document.getElementById("mobileMenu");
const shopTrigger = document.querySelector(".submenu-trigger");
const shopSubMenu = document.getElementById("shopSubMenu");

// Open/Close Mobile Menu
const toggleMenu = () => {
    menu.classList.toggle("open");
    overlay.style.display = menu.classList.contains("open") ? "block" : "none";
    document.body.classList.toggle("menu-open", menu.classList.contains("open"));

    // toggle hamburger ↔ X
    hamburger.textContent = menu.classList.contains("open") ? "х" : "☰";
};

hamburger.addEventListener("click", toggleMenu);
closeBtn.addEventListener("click", toggleMenu);
overlay.addEventListener("click", toggleMenu);

// Shop Submenu
shopTrigger.addEventListener("click", () => {
    shopSubMenu.classList.toggle("open");
});








