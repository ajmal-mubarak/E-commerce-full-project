// Sync navbar counts on load
const cartBadge = document.getElementById("cart-count");
if (cartBadge && typeof window.INITIAL_CART_COUNT !== "undefined") {
    cartBadge.innerText = window.INITIAL_CART_COUNT;
}

const wishlistBadge = document.getElementById("wishlist-count");
if (wishlistBadge && typeof window.INITIAL_WISHLIST_COUNT !== "undefined") {
    wishlistBadge.innerText = window.INITIAL_WISHLIST_COUNT;
}

/* ================= PREMIUM WELCOME TOAST ================= */
function showWelcomeToast(message) {
    // Create container for toast
    const toastContainer = document.createElement("div");
    toastContainer.className = "welcome-toast-container";
    toastContainer.innerHTML = `
        <div class="welcome-toast">
            <div class="toast-header">
                <span class="toast-icon">👋</span>
                <span class="toast-text">${message}</span>
            </div>
            <div class="toast-progress"></div>
        </div>
    `;
    
    // Add styles if not already present
    if (!document.getElementById("welcome-toast-styles")) {
        const style = document.createElement("style");
        style.id = "welcome-toast-styles";
        style.textContent = `
            .welcome-toast-container {
                position: fixed;
                top: 100px;
                right: 20px;
                z-index: 10000;
                font-family: 'Poppins', sans-serif;
            }
            
            .welcome-toast {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 12px;
                padding: 16px 24px;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
                animation: toastSlideIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
                overflow: hidden;
                min-width: 320px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .welcome-toast:hover,
            .welcome-toast:focus {
                transform: translateY(-5px) scale(1.02);
                box-shadow: 0 12px 48px rgba(102, 126, 234, 0.7), 0 0 30px rgba(102, 126, 234, 0.5);
                outline: 2px solid rgba(255, 255, 255, 0.3);
                outline-offset: 2px;
            }
            
            .welcome-toast:active {
                transform: translateY(-3px) scale(0.98);
            }
            
            .toast-header {
                display: flex;
                align-items: center;
                gap: 12px;
                font-weight: 500;
                font-size: 16px;
                letter-spacing: 0.3px;
            }
            
            .toast-icon {
                font-size: 24px;
                animation: toastIconBounce 0.8s ease-out;
            }
            
            .toast-text {
                flex: 1;
            }
            
            .toast-progress {
                height: 3px;
                background: rgba(255, 255, 255, 0.6);
                margin-top: 12px;
                border-radius: 2px;
                animation: toastProgress 3s linear forwards;
            }
            
            @keyframes toastSlideIn {
                from {
                    transform: translateX(400px) translateY(-20px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0) translateY(0);
                    opacity: 1;
                }
            }
            
            @keyframes toastIconBounce {
                0% {
                    transform: scale(0.8) rotate(-20deg);
                }
                50% {
                    transform: scale(1.1) rotate(5deg);
                }
                100% {
                    transform: scale(1) rotate(0deg);
                }
            }
            
            @keyframes toastProgress {
                from {
                    width: 100%;
                    opacity: 1;
                }
                to {
                    width: 0%;
                    opacity: 0.3;
                }
            }
            
            /* Mobile responsiveness */
            @media (max-width: 576px) {
                .welcome-toast-container {
                    right: 10px;
                    left: 10px;
                    top: 80px;
                }
                
                .welcome-toast {
                    min-width: auto;
                }
                
                .toast-header {
                    font-size: 14px;
                }
                
                .toast-icon {
                    font-size: 20px;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(toastContainer);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toastContainer.style.animation = "toastSlideOut 0.5s ease-in forwards";
        setTimeout(() => toastContainer.remove(), 500);
    }, 3000);
}

/* ================= NOTIFICATION FUNCTION ================= */
function showNotification(message, type = "success") {
    // Create notification element
    const notification = document.createElement("div");
    
    // Map type to Bootstrap alert class
    let alertClass = "alert-success";
    let icon = "✓";
    
    if (type === "error" || type === "danger") {
        alertClass = "alert-danger";
        icon = "✕";
    } else if (type === "warning") {
        alertClass = "alert-warning";
        icon = "⚠";
    } else if (type === "info") {
        alertClass = "alert-info";
        icon = "ℹ";
    }
    
    notification.className = `alert ${alertClass} position-fixed`;
    notification.style.cssText = `
        top: 80px;
        right: 20px;
        z-index: 10000;
        min-width: 300px;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-radius: 6px;
    `;
    notification.innerHTML = `
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        ${message}
    `;
    
    // Add animation styles if not already present
    if (!document.getElementById("notification-styles")) {
        const style = document.createElement("style");
        style.id = "notification-styles";
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

/* ================= LOGIN REQUIRED MODAL ================= */
function showLoginModal() {
    // Create modal HTML
    const modalHTML = `
        <div class="modal fade" id="loginModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white border-0">
                        <h5 class="modal-title">
                            <i class="fa fa-lock me-2"></i> Login Required
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center py-4">
                        <i class="fa fa-sign-in fa-3x text-primary mb-3"></i>
                        <h5 class="fw-bold mb-2">Please Login to Continue</h5>
                        <p class="text-muted">You need to be logged in to access this feature.</p>
                    </div>
                    <div class="modal-footer border-0 d-flex gap-2 justify-content-center">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <a href="/accounts/login/" class="btn btn-primary">Go to Login</a>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById("loginModal");
    if (existingModal) existingModal.remove();
    
    // Add modal to body
    document.body.insertAdjacentHTML("beforeend", modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById("loginModal"));
    modal.show();
}

/* ================= CSRF (GLOBAL) ================= */
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || window.CSRF_TOKEN;
}

/* ================= CATEGORY SLIDER ================= */
function initCategorySlider() {
    const container = document.getElementById('categorySlider');
    if (!container) return;

    const rawItems = Array.from(container.querySelectorAll('.category-slide-item'));
    if (rawItems.length === 0) return;

    const viewport = container.querySelector('.category-slider-viewport');
    const track = container.querySelector('.category-slider-track');

    // Inject basic styles once
    if (!document.getElementById('category-slider-styles')) {
        const s = document.createElement('style');
        s.id = 'category-slider-styles';
        s.textContent = `
            .category-slider { position: relative; }
            .category-slider-viewport { overflow: hidden; }
            .category-slider-track { display: flex; width: 100%; transition: transform 0.5s ease; will-change: transform; }
            .category-slide { flex: 0 0 100%; display: flex; gap: 1rem; }
            .category-slide-item { box-sizing: border-box; padding: 0 0.5rem; }
            .category-slider-controls { position: relative; }
            .category-slider-controls button { min-width: 44px; }
            @media (max-width: 768px) {
                /* perView handled in JS */
            }
            @media (max-width: 576px) {
                /* perView handled in JS */
            }
            /* Overlay arrows */
            .category-arrow { position: absolute; top: 50%; transform: translateY(-50%); z-index: 1000; background: rgba(255,255,255,0.85); border: none; width: 44px; height: 44px; border-radius: 50%; display:flex; align-items:center; justify-content:center; font-size:20px; color:#333; opacity:0.5; transition: opacity 0.2s ease, transform 0.15s ease; }
            .category-arrow:hover { opacity: 1; transform: translateY(-50%) scale(1.05); }
            .category-arrow:active { transform: translateY(-48%) scale(0.98); }
            .category-arrow-left { left: 8px; }
            .category-arrow-right { right: 8px; }
        `;
        document.head.appendChild(s);
    }

    // Determine items per slide depending on width
    function itemsPerView() {
        const w = window.innerWidth;
        if (w < 576) return 1;
        if (w < 768) return 2;
        return 3;
    }

    let perView = itemsPerView();

    // Build track as a single flex row of items (no grouping) so we can slide by one item
    function buildSlides() {
        track.innerHTML = '';
        rawItems.forEach((itm) => {
            // ensure item is detached and reset styles
            itm.style.flex = '';
            itm.style.maxWidth = '';
            track.appendChild(itm);
        });

        // set widths
        const itemWidthPercent = 100 / perView;
        track.querySelectorAll('.category-slide-item').forEach(itm => {
            itm.style.flex = `0 0 ${itemWidthPercent}%`;
            itm.style.maxWidth = `${itemWidthPercent}%`;
        });
    }

    buildSlides();

    let index = 0; // index of first visible item
    function goTo(idx) {
        const items = track.querySelectorAll('.category-slide-item');
        if (items.length === 0) return;

        const maxIndex = Math.max(0, items.length - perView);

        // Wrap around for continuous looping
        if (idx > maxIndex) {
            index = 0;
        } else if (idx < 0) {
            index = maxIndex;
        } else {
            index = idx;
        }

        const itemWidthPx = viewport.clientWidth / perView;
        const offset = index * itemWidthPx;
        track.style.transform = `translateX(-${offset}px)`;
    }

    // Controls (bottom)
    const btnPrev = container.querySelector('#catPrev');
    const btnNext = container.querySelector('#catNext');
    // Overlay controls
    const btnPrevOverlay = container.querySelector('#catPrevOverlay');
    const btnNextOverlay = container.querySelector('#catNextOverlay');

    function bindControl(btn) {
        if (!btn) return;
        btn.addEventListener('click', () => { goTo(index - 1); resetAuto(); });
    }

    function bindControlNext(btn) {
        if (!btn) return;
        btn.addEventListener('click', () => { goTo(index + 1); resetAuto(); });
    }

    bindControl(btnPrev); bindControl(btnPrevOverlay);
    bindControlNext(btnNext); bindControlNext(btnNextOverlay);

    // Touch swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    
    viewport.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    viewport.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) { // Minimum swipe distance
            if (diff > 0) {
                goTo(index + 1); // Swipe left -> next
            } else {
                goTo(index - 1); // Swipe right -> prev
            }
            resetAuto();
        }
    }

    // Auto-play (advance by one item)
    let auto = setInterval(() => { goTo(index + 1); }, 3000);
    function resetAuto() { clearInterval(auto); auto = setInterval(() => { goTo(index + 1); }, 3000); }

    // Rebuild on resize if perView changes
    let resizeTimer = null;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const newPer = itemsPerView();
            if (newPer !== perView) {
                perView = newPer;
                // Recompute rawItems from current DOM in case other scripts modified
                const currentItems = Array.from(container.querySelectorAll('.category-slide-item'));
                rawItems.length = 0; currentItems.forEach(it => rawItems.push(it));
                buildSlides();
                goTo(0);
            } else {
                // adjust position using new viewport width
                goTo(index);
            }
        }, 150);
    });
}

/* ================= LATEST PRODUCTS SLIDER ================= */
function initLatestSlider() {
    const container = document.getElementById('latestSlider');
    if (!container) return;

    const rawItems = Array.from(container.querySelectorAll('.latest-slide-item'));
    if (rawItems.length < 4) {
        // If less than 4 items, just display them in a grid without slider
        if (!document.getElementById('latest-grid-styles')) {
            const s = document.createElement('style');
            s.id = 'latest-grid-styles';
            s.textContent = `
                .latest-slider-viewport { overflow: visible; }
                .latest-slider-track { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; width: 100%; }
                .latest-slide-item { box-sizing: border-box; }
                .latest-arrow { display: none !important; }
            `;
            document.head.appendChild(s);
        }
        return;
    }

    const viewport = container.querySelector('.latest-slider-viewport');
    const track = container.querySelector('.latest-slider-track');

    // Inject styles once
    if (!document.getElementById('latest-slider-styles')) {
        const s = document.createElement('style');
        s.id = 'latest-slider-styles';
        s.textContent = `
            .latest-slider { position: relative; }
            .latest-slider-viewport { overflow: hidden; }
            .latest-slider-track { display: flex; width: 100%; transition: transform 0.5s ease; will-change: transform; }
            .latest-slide-item { box-sizing: border-box; padding: 0 0.5rem; }
            /* Overlay arrows */
            .latest-arrow { position: absolute; top: 50%; transform: translateY(-50%); z-index: 1000; background: #007bff; border: none; width: 44px; height: 44px; border-radius: 50%; display:flex; align-items:center; justify-content:center; font-size:20px; color:#fff; opacity:0.8; transition: opacity 0.2s ease, transform 0.15s ease; }
            .latest-arrow:hover { opacity: 1; transform: translateY(-50%) scale(1.05); }
            .latest-arrow:active { transform: translateY(-48%) scale(0.98); }
            .latest-arrow-left { left: 8px; }
            .latest-arrow-right { right: 8px; }
            @media (max-width: 768px) {
                /* perView handled in JS for 2 items on mobile */
            }
            @media (max-width: 576px) {
                /* perView handled in JS for 2 items on mobile */
            }
        `;
        document.head.appendChild(s);
    }

    // Determine items per slide depending on width
    function itemsPerView() {
        const w = window.innerWidth;
        if (w < 768) return 2;  // Mobile: 2 items
        return 4;  // Desktop: 4 items
    }

    let perView = itemsPerView();

    // Build track as a single flex row of items
    function buildSlides() {
        track.innerHTML = '';
        rawItems.forEach((itm) => {
            itm.style.flex = '';
            itm.style.maxWidth = '';
            track.appendChild(itm);
        });

        // set widths — use the smaller of perView and total items so cards fully fit
        const totalItems = rawItems.length;
        const cols = Math.min(perView, totalItems) || 1;
        const itemWidthPercent = 100 / cols;
        track.querySelectorAll('.latest-slide-item').forEach(itm => {
            itm.style.flex = `0 0 ${itemWidthPercent}%`;
            itm.style.maxWidth = `${itemWidthPercent}%`;
        });
    }

    buildSlides();

    let index = 0; // index of first visible item
    function goTo(idx) {
        const items = track.querySelectorAll('.latest-slide-item');
        if (items.length === 0) return;

        const maxIndex = Math.max(0, items.length - perView);

        // Wrap around for continuous looping
        if (idx > maxIndex) {
            index = 0;
        } else if (idx < 0) {
            index = maxIndex;
        } else {
            index = idx;
        }

        const itemWidthPx = viewport.clientWidth / perView;
        const offset = index * itemWidthPx;
        track.style.transform = `translateX(-${offset}px)`;
    }

    // Controls (overlay)
    const btnPrevOverlay = container.querySelector('#latestPrevOverlay');
    const btnNextOverlay = container.querySelector('#latestNextOverlay');

    function bindControl(btn) {
        if (!btn) return;
        btn.addEventListener('click', () => { goTo(index - 1); resetAuto(); });
    }

    function bindControlNext(btn) {
        if (!btn) return;
        btn.addEventListener('click', () => { goTo(index + 1); resetAuto(); });
    }

    bindControl(btnPrevOverlay);
    bindControlNext(btnNextOverlay);

    // Touch swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    
    viewport.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    viewport.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) { // Minimum swipe distance
            if (diff > 0) {
                goTo(index + 1); // Swipe left -> next
            } else {
                goTo(index - 1); // Swipe right -> prev
            }
            resetAuto();
        }
    }

    // Auto-play (advance by one item)
    let auto = setInterval(() => { goTo(index + 1); }, 3000);
    function resetAuto() { clearInterval(auto); auto = setInterval(() => { goTo(index + 1); }, 3000); }

    // Rebuild on resize if perView changes
    let resizeTimer = null;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const newPer = itemsPerView();
            if (newPer !== perView) {
                perView = newPer;
                const currentItems = Array.from(container.querySelectorAll('.latest-slide-item'));
                rawItems.length = 0; 
                currentItems.forEach(it => rawItems.push(it));
                buildSlides();
                goTo(0);
            } else {
                goTo(index);
            }
        }, 150);
    });
}

/* ================= FEATURED PRODUCTS SLIDER ================= */
function initFeaturedSlider() {
    const container = document.getElementById('featuredSlider');
    if (!container) return;

    const rawItems = Array.from(container.querySelectorAll('.featured-slide-item'));
    if (rawItems.length < 4) {
        // If less than 4 items, just display them in a grid without slider
        if (!document.getElementById('featured-grid-styles')) {
            const s = document.createElement('style');
            s.id = 'featured-grid-styles';
            s.textContent = `
                .featured-slider-viewport { overflow: visible; }
                .featured-slider-track { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; width: 100%; }
                .featured-slide-item { box-sizing: border-box; }
                .featured-arrow { display: none !important; }
            `;
            document.head.appendChild(s);
        }
        return;
    }

    const viewport = container.querySelector('.featured-slider-viewport');
    const track = container.querySelector('.featured-slider-track');

    // Inject styles once
    if (!document.getElementById('featured-slider-styles')) {
        const s = document.createElement('style');
        s.id = 'featured-slider-styles';
        s.textContent = `
            .featured-slider { position: relative; }
            .featured-slider-viewport { overflow: hidden; }
            .featured-slider-track { display: flex; width: 100%; transition: transform 0.5s ease; will-change: transform; }
            .featured-slide-item { box-sizing: border-box; padding: 0 0.5rem; }
            /* Overlay arrows */
            .featured-arrow { position: absolute; top: 50%; transform: translateY(-50%); z-index: 1000; background: #007bff; border: none; width: 44px; height: 44px; border-radius: 50%; display:flex; align-items:center; justify-content:center; font-size:20px; color:#fff; opacity:0.8; transition: opacity 0.2s ease, transform 0.15s ease; }
            .featured-arrow:hover { opacity: 1; transform: translateY(-50%) scale(1.05); }
            .featured-arrow:active { transform: translateY(-48%) scale(0.98); }
            .featured-arrow-left { left: 8px; }
            .featured-arrow-right { right: 8px; }
            @media (max-width: 768px) {
                /* perView handled in JS for 2 items on mobile */
            }
            @media (max-width: 576px) {
                /* perView handled in JS for 2 items on mobile */
            }
        `;
        document.head.appendChild(s);
    }

    // Determine items per slide depending on width
    function itemsPerView() {
        const w = window.innerWidth;
        if (w < 768) return 2;  // Mobile: 2 items
        return 4;  // Desktop: 4 items
    }

    let perView = itemsPerView();

    // Build track as a single flex row of items
    function buildSlides() {
        track.innerHTML = '';
        rawItems.forEach((itm) => {
            itm.style.flex = '';
            itm.style.maxWidth = '';
            track.appendChild(itm);
        });

        // set widths
        const itemWidthPercent = 100 / perView;
        track.querySelectorAll('.featured-slide-item').forEach(itm => {
            itm.style.flex = `0 0 ${itemWidthPercent}%`;
            itm.style.maxWidth = `${itemWidthPercent}%`;
        });
    }

    buildSlides();

    let index = 0; // index of first visible item
    function goTo(idx) {
        const items = track.querySelectorAll('.featured-slide-item');
        if (items.length === 0) return;

        const maxIndex = Math.max(0, items.length - perView);

        // Wrap around for continuous looping
        if (idx > maxIndex) {
            index = 0;
        } else if (idx < 0) {
            index = maxIndex;
        } else {
            index = idx;
        }

        const itemWidthPx = viewport.clientWidth / perView;
        const offset = index * itemWidthPx;
        track.style.transform = `translateX(-${offset}px)`;
    }

    // Controls (overlay)
    const btnPrevOverlay = container.querySelector('#featPrevOverlay');
    const btnNextOverlay = container.querySelector('#featNextOverlay');

    function bindControl(btn) {
        if (!btn) return;
        btn.addEventListener('click', () => { goTo(index - 1); resetAuto(); });
    }

    function bindControlNext(btn) {
        if (!btn) return;
        btn.addEventListener('click', () => { goTo(index + 1); resetAuto(); });
    }

    bindControl(btnPrevOverlay);
    bindControlNext(btnNextOverlay);

    // Touch swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    
    viewport.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    viewport.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) { // Minimum swipe distance
            if (diff > 0) {
                goTo(index + 1); // Swipe left -> next
            } else {
                goTo(index - 1); // Swipe right -> prev
            }
            resetAuto();
        }
    }

    // Auto-play (advance by one item)
    let auto = setInterval(() => { goTo(index + 1); }, 3000);
    function resetAuto() { clearInterval(auto); auto = setInterval(() => { goTo(index + 1); }, 3000); }

    // Rebuild on resize if perView changes
    let resizeTimer = null;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const newPer = itemsPerView();
            if (newPer !== perView) {
                perView = newPer;
                const currentItems = Array.from(container.querySelectorAll('.featured-slide-item'));
                rawItems.length = 0; 
                currentItems.forEach(it => rawItems.push(it));
                buildSlides();
                goTo(0);
            } else {
                goTo(index);
            }
        }, 150);
    });
}


document.addEventListener("DOMContentLoaded", function () {

    /* ================= WISHLIST ================= */
    document.querySelectorAll(".wishlist-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            console.log("Wishlist button clicked");
            
            // Check if user is authenticated
            if (!window.IS_AUTHENTICATED) {
                console.log("User not authenticated");
                showLoginModal();
                return;
            }
            
            const productId = this.dataset.productId;
            const icon = this.querySelector("i");
            
            console.log("Product ID:", productId);
            console.log("Icon before:", icon.className);
            
            // Add animation class
            this.classList.add("active");

            fetch(window.WISHLIST_TOGGLE_URL, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `product_id=${productId}`
            })
            .then(res => res.json())
            .then(data => {
                console.log("Response received:", data);
                if (data.status === "added") {
                    console.log("Status: ADDED - changing icon to filled");
                    icon.classList.remove("fa-heart-o");
                    icon.classList.add("fa-heart");
                    console.log("Icon after:", icon.className);
                    showNotification("Added to wishlist!", "success");
                } else if (data.status === "removed") {
                    console.log("Status: REMOVED - changing icon to empty");
                    icon.classList.remove("fa-heart");
                    icon.classList.add("fa-heart-o");
                    console.log("Icon after:", icon.className);
                    showNotification("Removed from wishlist", "success");
                }

                // Update ALL wishlist badges (mobile + desktop)
                const badges = document.querySelectorAll("#wishlist-count");
                if (data.count > 0) {
                    if (badges.length > 0) {
                        // Update existing badges
                        badges.forEach(badge => {
                            badge.innerText = data.count;
                        });
                    } else {
                        // Create badges if they don't exist
                        document.querySelectorAll("a[href*='/wishlist']").forEach(wishlistLink => {
                            const newBadge = document.createElement("span");
                            newBadge.id = "wishlist-count";
                            newBadge.className = "cart-badge";
                            newBadge.innerText = data.count;
                            wishlistLink.appendChild(newBadge);
                        });
                    }
                } else {
                    // Remove all badges if count is 0
                    badges.forEach(badge => badge.remove());
                }
            })
            .catch(err => {
                console.error("Error:", err);
                showNotification("Error updating wishlist", "error");
            })
            .finally(() => {
                this.classList.remove("active");
            });
        });
    });

    /* ================= ADD TO CART ================= */
    document.querySelectorAll(".add-to-cart-form").forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            fetch(this.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: new FormData(this)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Update ALL cart badges (mobile + desktop)
                    const badges = document.querySelectorAll("#cart-count, .cart-badge");
                    if (badges.length > 0) {
                        // Update existing badges
                        badges.forEach(badge => {
                            badge.innerText = data.cart_count;
                            badge.style.display = data.cart_count === 0 ? 'none' : '';
                        });
                    } else {
                        // Create badges if they don't exist
                        document.querySelectorAll("a[href*='/cart']").forEach(cartLink => {
                            const newBadge = document.createElement("span");
                            newBadge.id = "cart-count";
                            newBadge.className = "cart-badge";
                            newBadge.innerText = data.cart_count;
                            cartLink.appendChild(newBadge);
                        });
                    }

                    // Also update cart page header badge (if present) with pluralization
                    const headerBadges = document.querySelectorAll('.cart-header .badge');
                    if (headerBadges.length > 0) {
                        headerBadges.forEach(hb => {
                            hb.textContent = `${data.cart_count} item${data.cart_count !== 1 ? 's' : ''}`;
                        });
                    }
                    // Show success message
                    showNotification("Item added to cart!", "success");
                }
            })
            .catch(err => {
                console.error("Error:", err);
                showNotification("Error adding to cart", "error");
            });
        });
    });

    /* ================= CART QUANTITY (+ / -) ================= */
    document.querySelectorAll(".qty-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const itemId = this.dataset.itemId;
            const action = this.dataset.action;
            const input = document.querySelector(`.cart-qty[data-item-id="${itemId}"]`);

            let qty = parseInt(input.value);
            if (action === "plus") qty++;
            if (action === "minus" && qty > 1) qty--;

            input.value = qty;

            fetch(`/cart/update/${itemId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: `quantity=${qty}`
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById(`item-total-${itemId}`).innerText = data.item_total;
                document.getElementById("cart-subtotal").innerText = data.subtotal;
            });
        });
    });

    /* ================= REMOVE CART ITEM ================= */
    document.querySelectorAll(".remove-cart-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const itemId = this.dataset.itemId;

            fetch(`/cart/remove/${itemId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json())
            .then(data => {
                // Remove item from DOM
                const itemElement = document.getElementById(`cart-item-${itemId}`);
                if (itemElement) {
                    itemElement.style.animation = "fadeOut 0.3s ease-out";
                    setTimeout(() => itemElement.remove(), 300);
                }

                // Update ALL cart badges (mobile + desktop)
                const badges = document.querySelectorAll("#cart-count, .cart-badge");
                badges.forEach(badge => {
                    badge.innerText = data.cart_count;
                    badge.style.display = data.cart_count === 0 ? 'none' : '';
                });

                // Update cart page header badge (if present)
                const headerBadges2 = document.querySelectorAll('.cart-header .badge');
                if (headerBadges2.length > 0) {
                    headerBadges2.forEach(hb => {
                        hb.textContent = `${data.cart_count} item${data.cart_count !== 1 ? 's' : ''}`;
                    });
                }

                // Update subtotal
                const subtotalElement = document.getElementById("cart-subtotal");
                if (subtotalElement) {
                    subtotalElement.innerText = data.subtotal;
                }

                // Update total (if on cart page with summary)
                // We need to recalculate or request total from backend
                // For now, total = subtotal (unless there's a coupon)
                const totalElement = document.querySelector(".summary-row.total span:last-child");
                if (totalElement) {
                    totalElement.innerText = "₹" + data.subtotal;
                }

                showNotification("Item removed from cart", "success");

                // If cart is empty, reload page to show empty state
                if (data.cart_count === 0) {
                    setTimeout(() => location.reload(), 500);
                }
            })
            .catch(err => {
                console.error("Error:", err);
                showNotification("Error removing item", "error");
            });
        });
    });

    /* ================= REMOVE WISHLIST ITEM ================= */
    document.querySelectorAll(".remove-wishlist-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const itemId = this.dataset.itemId;

            fetch(this.href, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Remove the product card from DOM
                    const productCard = this.closest(".col-6");
                    if (productCard) {
                        productCard.style.animation = "fadeOut 0.3s ease-out";
                        setTimeout(() => productCard.remove(), 300);
                    }
                    
                    // Update wishlist badges
                    const badges = document.querySelectorAll("#wishlist-count");
                    if (data.count > 0) {
                        badges.forEach(badge => {
                            badge.innerText = data.count;
                        });
                    } else {
                        // Remove all badges if count is 0
                        badges.forEach(badge => badge.remove());
                    }
                    
                    showNotification("Removed from wishlist", "success");

                    // Reload page if no items left
                    if (data.count === 0) {
                        setTimeout(() => location.reload(), 500);
                    }
                }
            })
            .catch(err => {
                console.error("Error:", err);
                showNotification("Error removing item", "error");
            });
        });
    });

});

/* ================= RELATED PRODUCTS SLIDER ================= */
function initRelatedSlider() {
    const container = document.getElementById('relatedSlider');
    if (!container) return;

    const rawItems = Array.from(container.querySelectorAll('.related-slide-item'));
    if (rawItems.length === 0) return;

    const viewport = container.querySelector('.related-slider-viewport');
    const track = container.querySelector('.related-slider-track');

    // Inject styles once
    if (!document.getElementById('related-slider-styles')) {
        const s = document.createElement('style');
        s.id = 'related-slider-styles';
        s.textContent = `
            .related-slider { position: relative; }
            .related-slider-viewport { overflow: hidden; }
            .related-slider-track { display: flex; width: 100%; transition: transform 0.5s ease; will-change: transform; }
            .related-slide-item { box-sizing: border-box; padding: 0 0.5rem; }
            /* Overlay arrows */
            .related-arrow { position: absolute; top: 50%; transform: translateY(-50%); z-index: 1000; background: #007bff; border: none; width: 44px; height: 44px; border-radius: 50%; display:flex; align-items:center; justify-content:center; font-size:20px; color:#fff; opacity:0.8; transition: opacity 0.2s ease, transform 0.15s ease; }
            .related-arrow:hover { opacity: 1; transform: translateY(-50%) scale(1.05); }
            .related-arrow:active { transform: translateY(-48%) scale(0.98); }
            .related-arrow-left { left: 8px; }
            .related-arrow-right { right: 8px; }
        `;
        document.head.appendChild(s);
    }

    // Determine items per slide depending on width
    function itemsPerView() {
        const w = window.innerWidth;
        if (w < 768) return 2;  // Mobile: 2 items
        if (w < 1200) return 3; // Tablet: 3 items
        return 4;               // Desktop: 4 items
    }

    let perView = itemsPerView();

    // Controls (overlay)
    const btnPrevOverlay = container.querySelector('#relatedPrevOverlay');
    const btnNextOverlay = container.querySelector('#relatedNextOverlay');

    // Build track as a single flex row of items
    function buildSlides() {
        track.innerHTML = '';
        rawItems.forEach((itm) => {
            itm.style.flex = '';
            itm.style.maxWidth = '';
            track.appendChild(itm);
        });

        // set widths — use the smaller of perView and total items so cards fully fit
        const totalItems = rawItems.length;
        const cols = Math.min(perView, totalItems) || 1;
        const itemWidthPercent = 100 / cols;
        track.querySelectorAll('.related-slide-item').forEach(itm => {
            itm.style.flex = `0 0 ${itemWidthPercent}%`;
            itm.style.maxWidth = `${itemWidthPercent}%`;
        });

        updateControlsVisibility();
    }

    function updateControlsVisibility() {
        const total = track.querySelectorAll('.related-slide-item').length;
        // On mobile we want slider when 2+ items exist
        if (window.innerWidth < 768) {
            if (total >= 2) {
                if (btnPrevOverlay) btnPrevOverlay.style.display = 'flex';
                if (btnNextOverlay) btnNextOverlay.style.display = 'flex';
            } else {
                if (btnPrevOverlay) btnPrevOverlay.style.display = 'none';
                if (btnNextOverlay) btnNextOverlay.style.display = 'none';
            }
        } else {
            // Desktop/tablet: show arrows only if more items than perView
            if (total > perView) {
                if (btnPrevOverlay) btnPrevOverlay.style.display = 'flex';
                if (btnNextOverlay) btnNextOverlay.style.display = 'flex';
            } else {
                if (btnPrevOverlay) btnPrevOverlay.style.display = 'none';
                if (btnNextOverlay) btnNextOverlay.style.display = 'none';
            }
        }
    }

    buildSlides();

    let index = 0; // index of first visible item
    function goTo(idx) {
        const items = track.querySelectorAll('.related-slide-item');
        if (items.length === 0) return;

        const maxIndex = Math.max(0, items.length - perView);

        // Wrap around for continuous looping
        if (idx > maxIndex) {
            index = 0;
        } else if (idx < 0) {
            index = maxIndex;
        } else {
            index = idx;
        }

        const itemWidthPx = viewport.clientWidth / perView;
        const offset = index * itemWidthPx;
        track.style.transform = `translateX(-${offset}px)`;
    }

    function bindControl(btn, step) {
        if (!btn) return;
        btn.addEventListener('click', () => { goTo(index + step); });
    }

    bindControl(btnPrevOverlay, -1);
    bindControl(btnNextOverlay, +1);

    // Touch swipe support for mobile: allow users to swipe to next/prev
    let touchStartX = 0;
    let touchEndX = 0;
    const SWIPE_THRESHOLD = 30; // px

    if (viewport) {
        viewport.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
            touchEndX = touchStartX;
        }, { passive: true });

        viewport.addEventListener('touchmove', (e) => {
            touchEndX = e.touches[0].clientX;
        }, { passive: true });

        viewport.addEventListener('touchend', () => {
            const dx = touchStartX - touchEndX;
            if (Math.abs(dx) > SWIPE_THRESHOLD) {
                if (dx > 0) {
                    goTo(index + 1);
                } else {
                    goTo(index - 1);
                }
            }
        }, { passive: true });
    }

    // Rebuild on resize if perView changes
    let resizeTimer = null;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const newPer = itemsPerView();
            if (newPer !== perView) {
                perView = newPer;
                const currentItems = Array.from(container.querySelectorAll('.related-slide-item'));
                rawItems.length = 0; 
                currentItems.forEach(it => rawItems.push(it));
                buildSlides();
                goTo(0);
            } else {
                updateControlsVisibility();
                goTo(index);
            }
        }, 150);
    });
}

// Initialize category slider and featured slider and latest slider when DOM is ready
document.addEventListener("DOMContentLoaded", initCategorySlider);
document.addEventListener("DOMContentLoaded", initFeaturedSlider);
document.addEventListener("DOMContentLoaded", initLatestSlider);
document.addEventListener("DOMContentLoaded", initRelatedSlider);
