class AnimationController {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupScrollAnimations();
        this.setupHeaderAnimation();
        this.setupParticleAnimations();
        this.setupHoverEffects();
        this.setupPageTransitions();
    }
    
    setupScrollAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        document.querySelectorAll('.glass-card, .instruction-step, .gallery-item').forEach(el => {
            observer.observe(el);
        });
        
        // Add CSS for scroll animations
        this.addScrollAnimationStyles();
    }
    
    setupHeaderAnimation() {
        let lastScrollY = window.scrollY;
        const header = document.querySelector('.header');
        
        if (!header) return;
        
        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            // Hide header when scrolling down, show when scrolling up
            if (currentScrollY > lastScrollY && currentScrollY > 100) {
                header.style.transform = 'translateY(-100%)';
            } else {
                header.style.transform = 'translateY(0)';
            }
            
            // Add background blur when scrolled
            if (currentScrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
            
            lastScrollY = currentScrollY;
        });
    }
    
    setupParticleAnimations() {
        // Enhanced particle system
        const particles = document.querySelectorAll('.particle');
        
        particles.forEach((particle, index) => {
            // Random properties for more natural movement
            const randomSize = 20 + Math.random() * 100;
            const randomDelay = Math.random() * 15;
            const randomDuration = 10 + Math.random() * 10;
            
            particle.style.width = randomSize + 'px';
            particle.style.height = randomSize + 'px';
            particle.style.animationDelay = randomDelay + 's';
            particle.style.animationDuration = randomDuration + 's';
            
            // Add mouse interaction
            this.addParticleInteraction(particle);
        });
    }
    
    addParticleInteraction(particle) {
        document.addEventListener('mousemove', (e) => {
            const rect = particle.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            const deltaX = e.clientX - centerX;
            const deltaY = e.clientY - centerY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            if (distance < 200) {
                const force = (200 - distance) / 200;
                const moveX = (deltaX / distance) * force * 20;
                const moveY = (deltaY / distance) * force * 20;
                
                particle.style.transform = `translate(${moveX}px, ${moveY}px)`;
                particle.style.opacity = 0.3 * force;
            } else {
                particle.style.transform = 'translate(0, 0)';
                particle.style.opacity = 0.1;
            }
        });
    }
    
    setupHoverEffects() {
        // Enhanced button hover effects
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                this.animateButtonHover(btn, true);
            });
            
            btn.addEventListener('mouseleave', () => {
                this.animateButtonHover(btn, false);
            });
        });
        
        // Glass card hover effects
        document.querySelectorAll('.glass-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px) scale(1.02)';
                card.style.boxShadow = '0 20px 60px rgba(139, 92, 246, 0.3)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = '0 8px 32px rgba(139, 92, 246, 0.1)';
            });
        });
    }
    
    animateButtonHover(btn, isHover) {
        if (isHover) {
            btn.style.transform = 'translateY(-3px) scale(1.05)';
            if (btn.classList.contains('btn-primary')) {
                btn.style.boxShadow = '0 12px 35px rgba(139, 92, 246, 0.5)';
            }
            
            // Add ripple effect
            this.createRippleEffect(btn);
        } else {
            btn.style.transform = 'translateY(0) scale(1)';
            if (btn.classList.contains('btn-primary')) {
                btn.style.boxShadow = '0 4px 20px rgba(139, 92, 246, 0.3)';
            }
        }
    }
    
    createRippleEffect(element) {
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        ripple.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%) scale(0);
            animation: rippleEffect 0.6s ease-out;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }
    
    setupPageTransitions() {
        // Smooth page transitions
        const transitionOverlay = document.createElement('div');
        transitionOverlay.className = 'page-transition';
        transitionOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
            z-index: 10000;
            transform: translateX(-100%);
            transition: transform 0.5s ease;
            pointer-events: none;
        `;
        document.body.appendChild(transitionOverlay);
        
        // Animate sections when they come into view
        this.setupSectionTransitions();
    }
    
    setupSectionTransitions() {
        const sections = document.querySelectorAll('section');
        const options = {
            threshold: 0.2,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('section-visible');
                    this.animateSection(entry.target);
                }
            });
        }, options);
        
        sections.forEach(section => {
            sectionObserver.observe(section);
        });
    }
    
    animateSection(section) {
        const elements = section.querySelectorAll('.section-title, .section-subtitle, .glass-card, .instruction-step');
        
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.style.transform = 'translateY(0)';
                el.style.opacity = '1';
            }, index * 100);
        });
    }
    
    // Loading animations
    showLoadingAnimation() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.add('active');
            this.animateSpinner();
        }
    }
    
    hideLoadingAnimation() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
    }
    
    animateSpinner() {
        const spinner = document.querySelector('.spinner');
        if (spinner) {
            spinner.style.animation = 'spin 1s linear infinite, pulse 2s ease-in-out infinite';
        }
    }
    
    // Form animations
    animateFormValidation(input, isValid) {
        if (isValid) {
            input.style.borderColor = '#10b981';
            input.style.boxShadow = '0 0 0 3px rgba(16, 185, 129, 0.1)';
        } else {
            input.style.borderColor = '#ef4444';
            input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
            
            // Shake animation
            input.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                input.style.animation = '';
            }, 500);
        }
    }
    
    // Text animation effects
    animateText(element, text, speed = 50) {
        element.textContent = '';
        let i = 0;
        
        const typeWriter = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }
        };
        
        typeWriter();
    }
    
    addScrollAnimationStyles() {
        const styles = document.createElement('style');
        styles.textContent = `
            .header.scrolled {
                background: rgba(11, 11, 26, 0.95);
                box-shadow: 0 4px 20px rgba(139, 92, 246, 0.1);
            }
            
            .glass-card, .instruction-step, .gallery-item {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.8s ease;
            }
            
            .glass-card.animate-in, .instruction-step.animate-in, .gallery-item.animate-in {
                opacity: 1;
                transform: translateY(0);
            }
            
            .section-title, .section-subtitle {
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.6s ease;
            }
            
            .section-visible .section-title,
            .section-visible .section-subtitle {
                opacity: 1;
                transform: translateY(0);
            }
            
            @keyframes rippleEffect {
                from {
                    transform: translate(-50%, -50%) scale(0);
                    opacity: 1;
                }
                to {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 0;
                }
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .animate-fade-in-up {
                animation: fadeInUp 0.8s ease forwards;
            }
        `;
        
        document.head.appendChild(styles);
    }
}

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AnimationController();
});

// Export for use in other modules
window.AnimationController = AnimationController;
