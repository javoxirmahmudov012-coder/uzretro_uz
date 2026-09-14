// UzRetro.uz — Main JavaScript

// Navbar scroll effekti
window.addEventListener('scroll', () => {
    const nav = document.getElementById('mainNav');
    if (nav) {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }
});

// Flash xabarlarini avtomatik yopish (5 sekund)
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
    }, 5000);
});

// Telefon raqam formatlash
const phoneInput = document.querySelector('input[type="tel"]');
if (phoneInput) {
    phoneInput.addEventListener('input', function() {
        let val = this.value.replace(/\D/g, '');
        if (val.startsWith('998')) {
            val = '+' + val;
        } else if (val.startsWith('9') && val.length > 2) {
            val = '+998' + val;
        }
        this.value = val;
    });
}

// Form yuborilayotganda loading
const orderForm = document.getElementById('orderForm');
if (orderForm) {
    orderForm.addEventListener('submit', function(e) {
        const btn = this.querySelector('button[type="submit"]');
        if (btn) {
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Yuborilmoqda...';
            btn.disabled = true;
        }
    });
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ====== COUNTER ANIMATSIYA ======
// Hero statistikalar uchun raqam sanash animatsiyasi
function animateCounter(element, target, duration = 2000) {
    const suffix = element.textContent.replace(/[\d,.]/g, '').trim();
    const isK = suffix.includes('K');
    let displayTarget = target;
    
    if (isK) displayTarget = target / 1000;
    
    let start = 0;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out-cubic)
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(eased * displayTarget);
        
        if (isK) {
            element.textContent = current + 'K+';
        } else if (suffix.includes('%')) {
            element.textContent = current + '%';
        } else {
            element.textContent = current.toLocaleString() + '+';
        }
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Counter observer — raqamlar ko'ringanda sana boshlaydi
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            const count = parseInt(el.getAttribute('data-count'));
            if (count && !el.dataset.animated) {
                el.dataset.animated = 'true';
                animateCounter(el, count);
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-num[data-count]').forEach(el => {
    counterObserver.observe(el);
});

// ====== PARALLAX EFFEKT ======
// Hero section uchun yengil parallax
const heroSection = document.querySelector('.hero-section');
if (heroSection) {
    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        if (scrolled < window.innerHeight) {
            const heroContent = heroSection.querySelector('.hero-content');
            if (heroContent) {
                heroContent.style.transform = `translateY(${scrolled * 0.15}px)`;
                heroContent.style.opacity = 1 - (scrolled / (window.innerHeight * 0.8));
            }
        }
    }, { passive: true });
}

// ====== NAVBAR ACTIVE LINK ======
// Joriy sahifaga mos nav-link ni active qilish
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath) {
        link.classList.add('active');
        link.style.color = '#38bdf8';
        link.style.opacity = '1';
    }
});

// ====== SERVICE OPTION TANLASH ANIMATSIYASI ======
// Xizmat tanlash radio buttonlar uchun kuchaytirilgan animatsiya
document.querySelectorAll('.service-option input').forEach(input => {
    input.addEventListener('change', function() {
        document.querySelectorAll('.service-option-content').forEach(c => {
            c.classList.remove('selected');
            c.style.transform = '';
        });
        if (this.checked) {
            const content = this.nextElementSibling;
            content.classList.add('selected');
        }
    });
});

// ====== SCROLL PROGRESS BAR ======
// Sahifa scroll progressini ko'rsatish
const progressBar = document.createElement('div');
progressBar.style.cssText = `
    position: fixed; top: 0; left: 0; height: 3px; z-index: 99999;
    background: linear-gradient(90deg, #007bff, #00d4ff);
    transition: width 0.1s linear; width: 0%;
`;
document.body.appendChild(progressBar);

window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    progressBar.style.width = scrollPercent + '%';
}, { passive: true });

// ====== KUNDUZGI / KECHKI REJIM (THEME SWITCHER) ======
function updateThemeUI(theme) {
    const themeToggleText = document.getElementById('themeToggleText');
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    if (themeToggleText) {
        themeToggleText.textContent = theme === 'light' ? 'Kunduzgi' : 'Kechki';
    }
    if (themeToggleBtn) {
        themeToggleBtn.setAttribute('title', theme === 'light' ? "Kechki rejimga o'tish" : "Kunduzgi rejimga o'tish");
    }
}

function initTheme() {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    updateThemeUI(currentTheme);
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('uzretro-theme', newTheme);
            updateThemeUI(newTheme);
        });
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
} else {
    initTheme();
}

console.log('🚀 UzRetro.uz loaded with animations!');

