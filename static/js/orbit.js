/*
 * orbit.js
 * Manages the visual logic for the Orbit Context Menu.
 */
const Orbit = {
    menu: null,
    satellitesContainer: null,
    selectedNodeId: null,

    init() {
        this.menu = document.getElementById('orbit');
        this.satellitesContainer = document.getElementById('orbit-satellites');
    },

    show(nodeId, domPos, palette, onColorSelect, scale = 1) {
        if (!this.menu) this.init();
        this.selectedNodeId = nodeId;

        this.menu.classList.remove('hidden');

        // Position the container exactly on the node center
        this.menu.style.left = domPos.x + 'px';
        this.menu.style.top = domPos.y + 'px';
        
        // Scale the menu based on zoom level
        this.menu.style.transform = `scale(${scale})`;

        // Render Satellites
        this.satellitesContainer.innerHTML = ''; // Clear old

        // Arc Geometry: Span from -20deg (left) to 200deg (right)
        const totalSpan = 240; 
        const startAngle = -10; 

        palette.forEach((color, index) => {
            const btn = document.createElement('div');
            btn.className = 'satellite';
            btn.style.backgroundColor = color;
            
            // Calculate Angle
            const step = totalSpan / (palette.length - 1);
            const angle = startAngle - (index * step);
            
            btn.style.setProperty('--angle', `${angle}deg`);
            
            btn.onclick = (e) => {
                e.stopPropagation(); // Prevent Vis.js background click
                onColorSelect(nodeId, color);
            };
            
            this.satellitesContainer.appendChild(btn);

            // Staggered Animation
            setTimeout(() => {
                btn.classList.add('visible');
            }, index * 30);
        });
    },

    hide() {
        if (this.menu) this.menu.classList.add('hidden');
        this.selectedNodeId = null;
    }
};

window.Orbit = Orbit;