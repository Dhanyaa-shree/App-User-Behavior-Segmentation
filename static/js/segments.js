// static/js/segments.js

function setView(view) {
    var container = document.getElementById('segmentsContainer');
    var buttons = document.querySelectorAll('.view-options .btn');
    
    if (buttons.length > 0) {
        buttons[0].classList.remove('active');
        buttons[1].classList.remove('active');
    }
    
    if (view === 'grid') {
        container.className = 'segments-grid-full';
        if (buttons.length > 0) {
            buttons[0].classList.add('active');
        }
    } else {
        container.className = 'segments-grid-full list-view';
        if (buttons.length > 0) {
            buttons[1].classList.add('active');
        }
    }
}

// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('segmentSearch');
    if (searchInput) {
        searchInput.oninput = function() {
            var query = this.value.toLowerCase();
            var cards = document.querySelectorAll('.segment-card-full');
            
            for (var i = 0; i < cards.length; i++) {
                var text = cards[i].textContent.toLowerCase();
                if (text.indexOf(query) > -1) {
                    cards[i].style.display = 'block';
                } else {
                    cards[i].style.display = 'none';
                }
            }
        };
    }
});