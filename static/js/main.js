class BookFoldingApp {
    constructor() {
        this.currentPattern = null;
        this.selectedTemplate = null;
        this.templates = null;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadTemplates();
        this.setupFormSync();
        this.initAnimations();
    }
    
    bindEvents() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Text input
        const textInput = document.getElementById('text-input');
        if (textInput) {
            textInput.addEventListener('input', () => this.updateTextPreview());
            textInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.generatePattern();
                }
            });
        }
        
        // Generate button
        const generateBtn = document.getElementById('generate-btn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generatePattern());
        }
        
        // Export button
        const exportBtn = document.getElementById('export-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportPattern());
        }
        
        // New pattern button
        const newPatternBtn = document.getElementById('new-pattern-btn');
        if (newPatternBtn) {
            newPatternBtn.addEventListener('click', () => this.resetForm());
        }
        
        // Gallery items
        document.querySelectorAll('.gallery-item').forEach(item => {
            item.addEventListener('click', () => this.selectGalleryTemplate(item.dataset.template));
        });
        
        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }
    
    setupFormSync() {
        // Sync sliders with inputs
        const syncInputs = [
            ['book-pages-slider', 'book-pages'],
            ['book-height-slider', 'book-height'],
            ['book-page-width-slider', 'book-page-width'],
            ['book-width-slider', 'book-width']
        ];
        
        syncInputs.forEach(([sliderId, inputId]) => {
            const slider = document.getElementById(sliderId);
            const input = document.getElementById(inputId);
            
            if (slider && input) {
                slider.addEventListener('input', () => input.value = slider.value);
                input.addEventListener('input', () => slider.value = input.value);
            }
        });
    }
    
    async loadTemplates() {
        try {
            const response = await fetch('/get_templates');
            this.templates = await response.json();
            this.renderTemplates();
        } catch (error) {
            console.error('Failed to load templates:', error);
        }
    }
    
    renderTemplates() {
        if (!this.templates) return;
        
        Object.keys(this.templates).forEach(category => {
            const grid = document.getElementById(`${category}-grid`);
            if (grid) {
                grid.innerHTML = '';
                this.templates[category].forEach(template => {
                    const item = this.createTemplateItem(template);
                    grid.appendChild(item);
                });
            }
        });
    }
    
    createTemplateItem(template) {
        const item = document.createElement('div');
        item.className = 'template-item';
        item.dataset.templateId = template.id;
        item.title = template.description;
        
        // Get icon for template
        const icon = this.getTemplateIcon(template.id);
        
        item.innerHTML = `
            <div class="template-content">
                ${icon}
            </div>
            <div class="template-label">${template.name}</div>
        `;
        
        item.addEventListener('click', () => this.selectTemplate(template.id));
        
        return item;
    }
    
    getTemplateIcon(templateId) {
        const iconMap = {
            'apple': '<i class="fab fa-apple"></i>',
            'nike': '<i class="fas fa-check"></i>',
            'batman': '<i class="fas fa-mask"></i>',
            'superman': '<span style="font-family: serif; font-weight: bold;">S</span>',
            'heart': '<i class="fas fa-heart"></i>',
            'star': '<i class="fas fa-star"></i>',
            'peace': '<span>☮</span>',
            'infinity': '<span>∞</span>',
            'smile': '<span>😊</span>',
            'love': '<span>😍</span>',
            'thumbs_up': '<span>👍</span>',
            'fire': '<span>🔥</span>'
        };
        
        return iconMap[templateId] || '<i class="fas fa-question"></i>';
    }
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-tab`);
        });
        
        // Clear selections when switching tabs
        this.clearSelections();
    }
    
    clearSelections() {
        this.selectedTemplate = null;
        document.querySelectorAll('.template-item').forEach(item => {
            item.classList.remove('selected');
        });
    }
    
    selectTemplate(templateId) {
        this.selectedTemplate = templateId;
        
        // Update visual selection
        document.querySelectorAll('.template-item').forEach(item => {
            item.classList.toggle('selected', item.dataset.templateId === templateId);
        });
    }
    
    selectGalleryTemplate(templateId) {
        // Switch to template tab and select template
        this.switchTab('template');
        setTimeout(() => {
            this.selectTemplate(templateId);
        }, 100);
    }
    
    updateTextPreview() {
        const textInput = document.getElementById('text-input');
        const preview = document.getElementById('text-preview-display');
        const charCount = document.getElementById('char-count');
        
        if (!textInput || !preview || !charCount) return;
        
        const text = textInput.value.toUpperCase();
        charCount.textContent = text.length;
        
        if (text) {
            preview.textContent = text;
            preview.style.color = 'var(--primary-color)';
        } else {
            preview.textContent = 'Введите текст';
            preview.style.color = 'var(--text-muted)';
        }
    }
    
    async generatePattern() {
        const activeTab = document.querySelector('.tab-btn.active').dataset.tab;
        
        let requestData = {
            book_pages: parseInt(document.getElementById('book-pages').value),
            book_height: parseFloat(document.getElementById('book-height').value),
            book_page_width: parseFloat(document.getElementById('book-page-width').value),
            book_width: parseFloat(document.getElementById('book-width').value)
        };
        
        let endpoint = '';
        
        if (activeTab === 'text') {
            const text = document.getElementById('text-input').value.trim();
            if (!text) {
                this.showError('Пожалуйста, введите текст');
                return;
            }
            
            requestData.text = text;
            endpoint = '/generate_pattern';
        } else if (activeTab === 'template') {
            if (!this.selectedTemplate) {
                this.showError('Пожалуйста, выберите шаблон');
                return;
            }
            
            requestData.template_id = this.selectedTemplate;
            endpoint = '/generate_template_pattern';
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Ошибка генерации паттерна');
            }
            
            this.currentPattern = data;
            this.displayResults(data);
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    displayResults(data) {
        const resultsSection = document.getElementById('results-section');
        if (!resultsSection) return;
        
        // Update statistics
        document.getElementById('total-folds').textContent = data.statistics.total_folds;
        document.getElementById('pages-used').textContent = data.statistics.pages_used;
        document.getElementById('estimated-time').textContent = data.statistics.estimated_time_minutes;
        
        // Display pattern visualization
        this.renderPatternVisualization(data.pattern);
        
        // Display instructions
        this.renderInstructions(data.pattern);
        
        // Show results section with animation
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Animate stats
        this.animateStats();
    }
    
    renderPatternVisualization(pattern) {
        const visual = document.getElementById('pattern-visual');
        if (!visual) return;
        
        visual.innerHTML = '';
        
        if (pattern.length === 0) {
            visual.innerHTML = '<div class="no-pattern">Нет данных для отображения</div>';
            return;
        }
        
        // Create book visualization
        const bookContainer = document.createElement('div');
        bookContainer.className = 'book-visualization';
        
        const pagesContainer = document.createElement('div');
        pagesContainer.className = 'book-pages-container';
        
        // Show only first 10 pages for visualization
        const visibleFolds = pattern.slice(0, 10);
        
        visibleFolds.forEach((fold, index) => {
            const page = document.createElement('div');
            page.className = 'folded-page';
            page.style.zIndex = 100 - index;
            page.style.left = `${index * 2}px`;
            page.style.animationDelay = `${index * 0.3}s`;
            
            // Add fold lines
            const foldStart = (fold.start_mm / 200) * 100;
            const foldEnd = (fold.end_mm / 200) * 100;
            const foldHeight = foldEnd - foldStart;
            
            const foldLine = document.createElement('div');
            foldLine.className = 'fold-line';
            foldLine.style.cssText = `
                top: ${foldStart}%;
                height: ${foldHeight}%;
                animation-delay: ${index * 0.3}s;
            `;
            
            // Add actual page number from fold data
            const pageNumber = document.createElement('div');
            pageNumber.style.cssText = `
                position: absolute;
                top: 5px;
                right: 5px;
                font-size: 10px;
                color: var(--text-muted);
                background: rgba(255,255,255,0.8);
                padding: 2px 4px;
                border-radius: 2px;
                font-weight: bold;
            `;
            pageNumber.textContent = fold.page;
            
            page.appendChild(foldLine);
            page.appendChild(pageNumber);
            page.classList.add('active');
            
            // Add hover effect
            page.addEventListener('mouseenter', () => {
                page.style.transform = 'rotateY(-35deg) scale(1.05)';
                page.style.zIndex = 200;
            });
            
            page.addEventListener('mouseleave', () => {
                page.style.transform = 'rotateY(0deg) scale(1)';
                page.style.zIndex = 100 - index;
            });
            
            pagesContainer.appendChild(page);
        });
        
        // Add summary text
        const summary = document.createElement('div');
        summary.style.cssText = `
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-align: center;
        `;
        summary.innerHTML = `
            <strong>${pattern.length}</strong> страниц будут согнуты<br>
            <small>Показаны первые ${Math.min(10, pattern.length)} страниц</small>
        `;
        
        bookContainer.appendChild(pagesContainer);
        visual.appendChild(bookContainer);
        visual.appendChild(summary);
    }
    
    renderInstructions(pattern) {
        const container = document.getElementById('instructions-container');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (pattern.length === 0) {
            container.innerHTML = '<div class="no-instructions">Нет инструкций для отображения</div>';
            return;
        }
        
        pattern.forEach((fold, index) => {
            const instruction = document.createElement('div');
            instruction.className = 'instruction-visual';
            instruction.style.animationDelay = `${index * 0.05}s`;
            
            // Create visual book representation
            const bookVisual = document.createElement('div');
            bookVisual.className = 'instruction-book';
            
            const spine = document.createElement('div');
            spine.className = 'instruction-book-spine';
            
            const cover = document.createElement('div');
            cover.className = 'instruction-book-cover';
            
            const foldPage = document.createElement('div');
            foldPage.className = 'instruction-fold-page folded';
            
            // Calculate fold position (assuming 200mm book height)
            const foldStart = (fold.start_mm / 200) * 100;
            const foldHeight = ((fold.end_mm - fold.start_mm) / 200) * 100;
            
            const foldLine = document.createElement('div');
            foldLine.className = 'instruction-fold-line';
            foldLine.style.cssText = `
                top: ${foldStart}%;
                height: ${foldHeight}%;
            `;
            
            foldPage.appendChild(foldLine);
            bookVisual.appendChild(spine);
            bookVisual.appendChild(cover);
            bookVisual.appendChild(foldPage);
            
            // Create instruction details
            const details = document.createElement('div');
            details.className = 'instruction-details';
            
            const pageNumber = document.createElement('div');
            pageNumber.className = 'instruction-page-number';
            pageNumber.textContent = `Шаг ${index + 1}: Страница ${fold.page}`;
            
            const measurements = document.createElement('div');
            measurements.className = 'instruction-measurements';
            measurements.innerHTML = `
                <span class="measurement-item">От: ${fold.start_mm}мм</span>
                <span class="measurement-item">До: ${fold.end_mm}мм</span>
                <span class="measurement-item">Глубина: ${fold.depth_mm}мм</span>
            `;
            
            details.appendChild(pageNumber);
            details.appendChild(measurements);
            
            instruction.appendChild(bookVisual);
            instruction.appendChild(details);
            
            container.appendChild(instruction);
        });
    }
    
    animateStats() {
        document.querySelectorAll('.stat-value').forEach((stat, index) => {
            const finalValue = parseInt(stat.textContent);
            let currentValue = 0;
            const increment = finalValue / 30;
            
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    stat.textContent = finalValue;
                    clearInterval(timer);
                } else {
                    stat.textContent = Math.floor(currentValue);
                }
            }, 50);
        });
    }
    
    async exportPattern() {
        if (!this.currentPattern) return;
        
        try {
            const response = await fetch('/export_pattern', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.currentPattern)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Ошибка экспорта');
            }
            
            // Download file
            const blob = new Blob([data.instructions], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            a.click();
            URL.revokeObjectURL(url);
            
            this.showSuccess('Инструкции успешно экспортированы!');
            
        } catch (error) {
            this.showError(error.message);
        }
    }
    
    resetForm() {
        // Hide results
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            resultsSection.style.display = 'none';
        }
        
        // Clear form data
        document.getElementById('text-input').value = '';
        this.updateTextPreview();
        this.clearSelections();
        this.currentPattern = null;
        
        // Reset to text tab
        this.switchTab('text');
        
        // Scroll to generator
        document.getElementById('generator').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.toggle('active', show);
        }
    }
    
    showError(message) {
        // Create toast notification
        this.showToast(message, 'error');
    }
    
    showSuccess(message) {
        this.showToast(message, 'success');
    }
    
    showToast(message, type = 'info') {
        // Remove existing toasts
        document.querySelectorAll('.toast').forEach(toast => toast.remove());
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : 'var(--primary-color)'};
            color: white;
            padding: var(--spacing-md);
            border-radius: var(--radius-md);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            z-index: 10001;
            max-width: 400px;
            animation: slideInRight 0.3s ease;
        `;
        
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: var(--spacing-xs);">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
        
        // Add click to dismiss
        toast.addEventListener('click', () => {
            toast.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        });
    }
    
    initAnimations() {
        // Add scroll-triggered animations if GSAP is available
        if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
            
            // Animate sections on scroll
            gsap.utils.toArray('.glass-card').forEach(card => {
                gsap.fromTo(card, {
                    opacity: 0,
                    y: 50
                }, {
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    scrollTrigger: {
                        trigger: card,
                        start: "top 80%",
                        toggleActions: "play none none reverse"
                    }
                });
            });
        }
    }
}

// Add CSS for toast animations
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(toastStyles);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BookFoldingApp();
});
