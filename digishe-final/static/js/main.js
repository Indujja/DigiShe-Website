// Main JavaScript for DigiShe application

document.addEventListener('DOMContentLoaded', function() {
    // Animation on scroll
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    // Set initial state for elements that are already in viewport
    animateElements.forEach(element => {
        if (isInViewport(element)) {
            element.classList.add('in-view');
        }
    });
    
    // Add scroll event listener for animations
    window.addEventListener('scroll', function() {
        animateElements.forEach(element => {
            if (isInViewport(element)) {
                element.classList.add('in-view');
            }
        });
    });
    
    // Language selector functionality
    const languageSelector = document.getElementById('language-selector');
    if (languageSelector) {
        languageSelector.addEventListener('change', function() {
            const currentUrl = new URL(window.location.href);
            const params = new URLSearchParams(currentUrl.search);
            
            // Update or add the lang parameter
            params.set('lang', this.value);
            
            // Redirect to the same page with updated language
            currentUrl.search = params.toString();
            window.location.href = currentUrl.toString();
        });
    }
    
    // Search form on home page
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const searchInput = document.getElementById('search-input');
            const query = searchInput.value.trim();
            
            if (query) {
                // Get the current language
                const urlParams = new URLSearchParams(window.location.search);
                const currentLang = urlParams.get('lang') || 'en';
                
                // Redirect to schemes page with search query
                window.location.href = `/schemes?lang=${currentLang}&query=${encodeURIComponent(query)}`;
            }
        });
    }
    
    // Category buttons
    const categoryButtons = document.querySelectorAll('.category-btn');
    if (categoryButtons.length > 0) {
        categoryButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                const selectedCategory = this.getAttribute('data-category');
                filterSchemesByCategory(selectedCategory);
            });
        });
    }
    
    // Colorize category tags
    const categoryTags = document.querySelectorAll('.category-tag');
    if (categoryTags.length > 0) {
        categoryTags.forEach(tag => {
            const category = tag.textContent.trim();
            tag.classList.add('category-' + category.split(' ')[0]); // Add first word of category as class
        });
    }
    
    // Live search on schemes page
    const schemeSearch = document.getElementById('scheme-search');
    if (schemeSearch) {
        schemeSearch.addEventListener('input', function() {
            const query = this.value.trim().toLowerCase();
            
            if (query === '') {
                // Reset category filters
                const allCategoryButton = document.querySelector('.category-btn[data-category="all"]');
                if (allCategoryButton) {
                    allCategoryButton.click();
                } else {
                    showAllSchemes();
                }
                return;
            }
            
            const schemeItems = document.querySelectorAll('.scheme-item');
            let matchFound = false;
            
            schemeItems.forEach(item => {
                const schemeCard = item.querySelector('.scheme-card');
                const schemeName = schemeCard.querySelector('h3').textContent.toLowerCase();
                const schemeDesc = schemeCard.querySelector('p').textContent.toLowerCase();
                
                if (schemeName.includes(query) || schemeDesc.includes(query)) {
                    item.style.display = 'block';
                    matchFound = true;
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Show or hide no results message
            const noResults = document.getElementById('no-results');
            if (noResults) {
                noResults.style.display = matchFound ? 'none' : 'block';
            }
        });
        
        // Trigger search on page load if there's a query parameter
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('query');
        if (searchQuery) {
            schemeSearch.value = searchQuery;
            // Trigger the input event to filter results
            schemeSearch.dispatchEvent(new Event('input'));
        }
    }
});

// Filter schemes by category
function filterSchemesByCategory(category) {
    const schemeItems = document.querySelectorAll('.scheme-item');
    let visibleCount = 0;
    
    schemeItems.forEach(item => {
        if (category === 'all') {
            item.style.display = 'block';
            visibleCount++;
        } else {
            const itemCategory = item.getAttribute('data-category');
            if (itemCategory === category) {
                item.style.display = 'block';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        }
    });
    
    // Show or hide no results message
    const noResults = document.getElementById('no-results');
    if (noResults) {
        noResults.style.display = visibleCount > 0 ? 'none' : 'block';
    }
}

// Show all schemes
function showAllSchemes() {
    const schemeItems = document.querySelectorAll('.scheme-item');
    schemeItems.forEach(item => {
        item.style.display = 'block';
    });
    
    // Hide no results message
    const noResults = document.getElementById('no-results');
    if (noResults) {
        noResults.style.display = 'none';
    }
}

// Helper function to check if an element is in the viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0 &&
        rect.left <= (window.innerWidth || document.documentElement.clientWidth) &&
        rect.right >= 0
    );
}