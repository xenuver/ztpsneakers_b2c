// ================= HERO SLIDER =================
const track = document.querySelector(".slider-track");
const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");
const prevBtn = document.querySelector(".slider-btn.prev");
const nextBtn = document.querySelector(".slider-btn.next");
const wrapper = document.querySelector(".slider-wrapper");

let currentIndex = 0;
let autoSlideTimer = null;

// kalau belum ada banner, hentikan
if (slides.length > 0) {

    function updateSlider(index) {
        if (index < 0) currentIndex = slides.length - 1;
        else if (index >= slides.length) currentIndex = 0;
        else currentIndex = index;

        // geser track
        track.style.transform = `translateX(-${currentIndex * 100}%)`;

        // update dots
        dots.forEach(dot => dot.classList.remove("active"));
        if (dots[currentIndex]) {
            dots[currentIndex].classList.add("active");
        }
    }

    function startAutoSlide() {
        stopAutoSlide();
        autoSlideTimer = setInterval(() => {
            updateSlider(currentIndex + 1);
        }, 4000); // 4 detik
    }

    function stopAutoSlide() {
        if (autoSlideTimer) clearInterval(autoSlideTimer);
    }

    // tombol panah
    if (prevBtn && nextBtn) {
        prevBtn.addEventListener("click", () => {
            updateSlider(currentIndex - 1);
            startAutoSlide();
        });

        nextBtn.addEventListener("click", () => {
            updateSlider(currentIndex + 1);
            startAutoSlide();
        });
    }

    // dots
    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            updateSlider(i);
            startAutoSlide();
        });
    });

    // swipe di HP
    let startX = 0;

    wrapper.addEventListener("touchstart", (e) => {
        startX = e.touches[0].clientX;
        stopAutoSlide();
    });

    wrapper.addEventListener("touchend", (e) => {
        const endX = e.changedTouches[0].clientX;
        const diff = endX - startX;

        if (Math.abs(diff) > 50) {
            if (diff < 0) {
                // geser kiri -> slide berikut
                updateSlider(currentIndex + 1);
            } else {
                // geser kanan -> slide sebelumnya
                updateSlider(currentIndex - 1);
            }
        }
        startAutoSlide();
    });

    // initial
    updateSlider(0);
    startAutoSlide();
}

// ================= NAVBAR ACTIVE LINK =================
const navLinks = document.querySelectorAll(".nav-menu a");

navLinks.forEach(link => {
    link.addEventListener("click", () => {
        navLinks.forEach(l => l.classList.remove("active"));
        link.classList.add("active");
    });
});

// ================= FOOTER TOP SCROLL ANIMATION =================
const footerTop = document.querySelector(".footer-top");
if (footerTop) {
    const items = footerTop.querySelectorAll(".footer-top-item");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    // tampilkan satu per satu dari kiri
                    items.forEach((item, index) => {
                        setTimeout(() => {
                            item.classList.add("ft-show");
                        }, index * 200); // jeda 200ms antar item
                    });

                    // tidak perlu observe lagi setelah animasi pertama
                    observer.unobserve(footerTop);
                }
            });
        },
        {
            threshold: 0.2,
        }
    );

    observer.observe(footerTop);
}

document.addEventListener("DOMContentLoaded", function() {
    const hamburger = document.getElementById("hamburger");
    const navMenu = document.querySelector(".nav-menu");
    const navOverlay = document.getElementById("nav-overlay");
    const body = document.body; // Targetkan seluruh body halaman

    if (hamburger && navMenu && navOverlay) {
        
        // Buat fungsi pendek agar kode lebih rapi
        function toggleMobileMenu() {
            navMenu.classList.toggle("active");
            navOverlay.classList.toggle("active");
            
            // Tambah/hapus class no-scroll pada body web kamu
            body.classList.toggle("no-scroll"); 
        }

        // Buka menu saat klik ikon garis tiga
        hamburger.addEventListener("click", toggleMobileMenu);

        // Tutup menu saat area gelap diklik
        navOverlay.addEventListener("click", toggleMobileMenu);
    }
});