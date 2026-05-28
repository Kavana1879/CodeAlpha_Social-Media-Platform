// StudySphere Main UI Javascript
document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile Navbar Toggle
    const navToggle = document.querySelector(".nav-toggle");
    const navMenu = document.querySelector(".nav-menu");
    
    if (navToggle && navMenu) {
        navToggle.addEventListener("click", () => {
            navMenu.classList.toggle("show");
            const icon = navToggle.querySelector("i");
            if (icon) {
                if (navMenu.classList.contains("show")) {
                    icon.className = "fa-solid fa-xmark";
                } else {
                    icon.className = "fa-solid fa-bars";
                }
            }
        });
    }

    // 2. Animated Splash Screen Particles & Redirection
    const splashContainer = document.querySelector(".splash-container");
    if (splashContainer) {
        // Generate beautiful neon floating particles in background
        const spawnParticles = () => {
            const particleCount = 15;
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement("div");
                particle.className = "particle";
                
                // Random properties
                const size = Math.random() * 8 + 4;
                const left = Math.random() * 100;
                const delay = Math.random() * 5;
                const duration = Math.random() * 6 + 6;
                const glowChoice = Math.random();
                
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${left}%`;
                particle.style.animationDelay = `${delay}s`;
                particle.style.animationDuration = `${duration}s`;
                
                if (glowChoice > 0.6) {
                    // Blue Glow
                    particle.style.background = "rgba(0, 191, 255, 0.4)";
                    particle.style.boxShadow = "0 0 10px rgba(0, 191, 255, 0.6)";
                } else if (glowChoice > 0.3) {
                    // Pink Glow
                    particle.style.background = "rgba(255, 105, 180, 0.4)";
                    particle.style.boxShadow = "0 0 10px rgba(255, 105, 180, 0.6)";
                } // default is purple
                
                splashContainer.appendChild(particle);
            }
        };
        
        spawnParticles();
        
        // Auto Redirect after 3.5 seconds
        setTimeout(() => {
            splashContainer.style.transition = "opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1)";
            splashContainer.style.opacity = 0;
            setTimeout(() => {
                const redirectUrl = splashContainer.dataset.redirect;
                window.location.href = redirectUrl || "/feed/";
            }, 600);
        }, 3200);
    }
    
    // 3. Image Upload Field Preview (Create Post Page)
    const fileInput = document.querySelector('.post-image-input');
    const previewBox = document.querySelector('.image-preview-box');
    
    if (fileInput && previewBox) {
        previewBox.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    let previewImg = previewBox.querySelector('img');
                    let previewIcon = previewBox.querySelector('.preview-placeholder');
                    
                    if (!previewImg) {
                        previewImg = document.createElement('img');
                        previewBox.appendChild(previewImg);
                    }
                    
                    previewImg.src = event.target.result;
                    previewImg.style.display = 'block';
                    if (previewIcon) {
                        previewIcon.style.display = 'none';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
