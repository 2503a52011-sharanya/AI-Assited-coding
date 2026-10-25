// Main UI Interactions
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Destination search autocomplete
    const searchInputs = document.querySelectorAll('.dest-search-input');
    searchInputs.forEach(input => {
        const resultsContainer = input.parentElement.querySelector('.dest-autocomplete-results');
        if (!resultsContainer) return;

        let debounceTimer;
        input.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            const val = e.target.value.trim();
            if (val.length < 2) {
                resultsContainer.innerHTML = '';
                resultsContainer.classList.add('hidden');
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/destinations/api/autocomplete/?term=${encodeURIComponent(val)}`)
                    .then(res => res.json())
                    .then(data => {
                        resultsContainer.innerHTML = '';
                        if (data.length > 0) {
                            resultsContainer.classList.remove('hidden');
                            data.forEach(item => {
                                const div = document.createElement('div');
                                div.className = 'px-4 py-3 hover:bg-teal-50 cursor-pointer flex items-center justify-between border-b border-gray-100 last:border-b-0 text-sm text-gray-800';
                                div.innerHTML = `
                                    <span><i class="fa-solid fa-location-dot text-teal-600 mr-2"></i>${item.label}</span>
                                    <span class="text-xs bg-teal-100 text-teal-800 px-2 py-0.5 rounded-full">Explore</span>
                                `;
                                div.addEventListener('click', () => {
                                    window.location.href = `/destinations/${item.slug}/`;
                                });
                                resultsContainer.appendChild(div);
                            });
                        } else {
                            resultsContainer.classList.add('hidden');
                        }
                    })
                    .catch(err => console.error(err));
            }, 250);
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !resultsContainer.contains(e.target)) {
                resultsContainer.classList.add('hidden');
            }
        });
    });
});
