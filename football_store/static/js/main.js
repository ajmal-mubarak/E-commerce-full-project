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
                    const badges = document.querySelectorAll("#cart-count");
                    if (badges.length > 0) {
                        // Update existing badges
                        badges.forEach(badge => {
                            badge.innerText = data.cart_count;
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
                const badges = document.querySelectorAll("#cart-count");
                badges.forEach(badge => {
                    badge.innerText = data.cart_count;
                });

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

// Initialize category slider when DOM is ready
document.addEventListener("DOMContentLoaded", initCategorySlider);
