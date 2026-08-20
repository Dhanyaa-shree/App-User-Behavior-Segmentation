// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('📊 App User Behavior Segmentation Dashboard Loaded');
    
    // Highlight current page in navigation
    highlightCurrentPage();
    
    // Initialize any tooltips or popovers
    initTooltips();
});

// ============================================================
// NAVIGATION
// ============================================================

function highlightCurrentPage() {
    var currentPath = window.location.pathname;
    var navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(function(link) {
        var href = link.getAttribute('href');
        // Check if current path matches the link href
        if (href === currentPath || 
            (currentPath === '/' && href === '/') ||
            (currentPath !== '/' && href !== '/' && currentPath.indexOf(href) === 0)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

function toggleMobileMenu() {
    var navLinks = document.getElementById('navLinks');
    if (navLinks) {
        navLinks.classList.toggle('show');
    }
}

// ============================================================
// EXPORT FUNCTIONS
// ============================================================

function generatePDF() {
    alert('📄 PDF report generation will be available in the next update!');
}

function generateCSV() {
    window.location.href = '/api/export/all';
}

function exportCluster(clusterId) {
    window.location.href = '/api/export/' + clusterId;
}

// ============================================================
// SEARCH FUNCTIONS
// ============================================================

function searchUsers() {
    var query = document.getElementById('globalSearch');
    if (query) {
        var searchTerm = query.value.trim();
        if (searchTerm) {
            window.location.href = '/api/search?q=' + encodeURIComponent(searchTerm);
        }
    }
}

// ============================================================
// TOOLTIPS & HELPERS
// ============================================================

function initTooltips() {
    var tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(function(el) {
        el.addEventListener('mouseenter', function(e) {
            showTooltip(e.target, e.target.getAttribute('data-tooltip'));
        });
    });
}

function showTooltip(element, message) {
    var tooltip = document.createElement('div');
    tooltip.className = 'tooltip-custom';
    tooltip.textContent = message;
    tooltip.style.cssText = 'position: absolute; background: #0f172a; color: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; pointer-events: none; z-index: 1000;';
    
    var rect = element.getBoundingClientRect();
    tooltip.style.top = (rect.top - 30 + window.scrollY) + 'px';
    tooltip.style.left = (rect.left + rect.width/2 - 50 + window.scrollX) + 'px';
    tooltip.style.transform = 'translateX(-50%)';
    
    document.body.appendChild(tooltip);
    
    setTimeout(function() {
        if (tooltip.parentNode) {
            tooltip.remove();
        }
    }, 2000);
}

// ============================================================
// TABLE SORTING
// ============================================================

function sortTable(columnIndex) {
    var table = document.querySelector('.user-table');
    if (!table) return;
    
    var tbody = table.querySelector('tbody');
    if (!tbody) return;
    
    var rows = Array.from(tbody.querySelectorAll('tr'));
    var isAscending = table.dataset.sortAsc === 'true';
    
    rows.sort(function(a, b) {
        var aVal = a.children[columnIndex].textContent.trim();
        var bVal = b.children[columnIndex].textContent.trim();
        
        // Check if values are numbers
        if (!isNaN(aVal) && !isNaN(bVal)) {
            return isAscending ? parseFloat(aVal) - parseFloat(bVal) : parseFloat(bVal) - parseFloat(aVal);
        }
        return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    });
    
    // Re-append sorted rows
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
    table.dataset.sortAsc = !isAscending;
}

// ============================================================
// PREDICTION PAGE FUNCTIONS
// ============================================================

function loadPreset(type) {
    var presets = {
        high: {
            sessions_per_week: 12,
            avg_session_duration_min: 20,
            daily_active_minutes: 60,
            engagement_score: 85,
            feature_clicks_per_session: 20,
            notifications_opened_per_week: 10,
            in_app_search_count: 8,
            content_downloads: 5,
            social_shares: 4
        },
        moderate: {
            sessions_per_week: 6,
            avg_session_duration_min: 10,
            daily_active_minutes: 35,
            engagement_score: 65,
            feature_clicks_per_session: 12,
            notifications_opened_per_week: 5,
            in_app_search_count: 4,
            content_downloads: 2,
            social_shares: 2
        },
        low: {
            sessions_per_week: 2,
            avg_session_duration_min: 4,
            daily_active_minutes: 15,
            engagement_score: 35,
            feature_clicks_per_session: 4,
            notifications_opened_per_week: 1,
            in_app_search_count: 1,
            content_downloads: 0,
            social_shares: 0
        },
        occasional: {
            sessions_per_week: 3,
            avg_session_duration_min: 5,
            daily_active_minutes: 20,
            engagement_score: 45,
            feature_clicks_per_session: 5,
            notifications_opened_per_week: 2,
            in_app_search_count: 2,
            content_downloads: 1,
            social_shares: 1
        }
    };
    
    var preset = presets[type];
    if (!preset) return;
    
    var fields = ['sessions_per_week', 'avg_session_duration_min', 'daily_active_minutes',
                  'engagement_score', 'feature_clicks_per_session', 'notifications_opened_per_week',
                  'in_app_search_count', 'content_downloads', 'social_shares'];
    
    fields.forEach(function(field) {
        var el = document.getElementById(field);
        if (el && preset[field] !== undefined) {
            el.value = preset[field];
        }
    });
    
    // Auto-submit if form exists
    var btn = document.getElementById('predictBtn');
    if (btn) {
        btn.click();
    }
}

// ============================================================
// FILTER SEGMENTS (for segments page)
// ============================================================

function filterSegments() {
    var input = document.getElementById('segmentSearch');
    if (!input) return;
    
    var filter = input.value.toLowerCase();
    var cards = document.querySelectorAll('.segment-card, .segment-card-full');
    
    cards.forEach(function(card) {
        var text = card.textContent.toLowerCase();
        if (text.indexOf(filter) > -1) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================================
// VIEW TOGGLE (for segments page)
// ============================================================

function setView(view) {
    var container = document.getElementById('segmentsContainer');
    if (!container) return;
    
    var buttons = document.querySelectorAll('.view-options .btn');
    buttons.forEach(function(btn) {
        btn.classList.remove('active');
    });
    
    if (view === 'grid') {
        container.className = 'segments-grid-full grid-view';
        if (buttons[0]) buttons[0].classList.add('active');
    } else {
        container.className = 'segments-grid-full list-view';
        if (buttons[1]) buttons[1].classList.add('active');
    }
}

// ============================================================
// USER SEARCH (for segment detail page)
// ============================================================

function searchUsersTable() {
    var input = document.getElementById('userSearch');
    if (!input) return;
    
    var filter = input.value.toLowerCase();
    var rows = document.querySelectorAll('#userTableBody tr');
    
    rows.forEach(function(row) {
        var text = row.textContent.toLowerCase();
        if (text.indexOf(filter) > -1) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// ============================================================
// AUTO-REFRESH METRICS
// ============================================================

function refreshMetrics() {
    fetch('/api/stats')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var metricValues = document.querySelectorAll('.metric-value');
            metricValues.forEach(function(el) {
                var card = el.closest('.metric-card');
                if (card) {
                    var label = card.querySelector('.metric-label');
                    if (label) {
                        var labelText = label.textContent.trim();
                        if (labelText === 'Total Users') {
                            el.textContent = data.total_users;
                        } else if (labelText === 'User Segments') {
                            el.textContent = data.segments;
                        } else if (labelText === 'Avg Engagement Score') {
                            el.textContent = data.avg_engagement;
                        } else if (labelText === 'Avg Session Duration') {
                            el.textContent = data.avg_duration + ' min';
                        }
                    }
                }
            });
        })
        .catch(function(error) {
            console.error('Error refreshing metrics:', error);
        });
}

// ============================================================
// KEYBOARD SHORTCUTS
// ============================================================

document.addEventListener('keydown', function(e) {
    // Ctrl + / for search focus
    if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        var searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        var modals = document.querySelectorAll('.modal');
        modals.forEach(function(modal) {
            modal.style.display = 'none';
        });
    }
});

// ============================================================
// REFRESH CHARTS
// ============================================================

function refreshCharts() {
    fetch('/api/refresh', { method: 'POST' })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.message) {
                alert('Charts refreshed successfully!');
                location.reload();
            }
        })
        .catch(function(error) {
            console.error('Error refreshing charts:', error);
            alert('Failed to refresh charts. Please try again.');
        });
}

// ============================================================
// INITIALIZE SEARCH LISTENERS
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    var segmentSearch = document.getElementById('segmentSearch');
    if (segmentSearch) {
        segmentSearch.addEventListener('input', filterSegments);
    }
    
    var userSearch = document.getElementById('userSearch');
    if (userSearch) {
        userSearch.addEventListener('input', searchUsersTable);
    }
    
    var globalSearch = document.getElementById('globalSearch');
    if (globalSearch) {
        globalSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchUsers();
            }
        });
    }
});

console.log('🔍 Keyboard Shortcuts: Ctrl+/ to focus search');