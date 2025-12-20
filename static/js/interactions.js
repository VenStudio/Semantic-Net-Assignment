/*
 * interactions.js
 * Helper utilities for UI overlays (Floating Inputs, Link Mode).
 */
const Interactions = {
    
    // --- TIP BAR ---
    showTip(text) {
        const tip = document.getElementById('tip-bar');
        if (tip) {
            tip.innerText = text;
            tip.classList.remove('hidden');
        }
    },

    hideTip() {
        const tip = document.getElementById('tip-bar');
        if (tip) tip.classList.add('hidden');
    },

    isModeActive: false,

    // Spawns a temporary input box at x,y
    showFloatingInput(x, y, defaultValue, callback) {
        const input = document.createElement('input');
        input.className = 'floating-input';
        input.value = defaultValue || "";
        input.placeholder = "Node name";
        input.style.left = x + 'px';
        input.style.top = y + 'px';
        
        document.body.appendChild(input);
        input.focus();
        input.select();

        let finished = false;
        const finish = (val) => {
            if (finished) return;
            finished = true;
            input.remove();
            callback(val);
        };

        // Commit on Enter, Cancel on Escape/Blur
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') finish(input.value.trim());
            if (e.key === 'Escape') finish(null);
        });
        
        input.addEventListener('blur', () => finish(null));
    },

    // --- CUSTOM MODES ---

    // 1. Add Node Mode: Click anywhere -> Input -> Create
    startAddNodeMode(network, onNodeCreated) {
        this.isModeActive = true;
        this.showTip("Click anywhere to create a node");
        
        network.once('click', (params) => {
            this.hideTip();
            
            // If user clicked on an existing node/edge, ignore or cancel
            if (params.nodes.length > 0 || params.edges.length > 0) {
                this.isModeActive = false;
                return;
            }

            const pos = params.pointer.canvas;
            const dom = params.pointer.DOM;
            
            this.showFloatingInput(dom.x, dom.y, "", (name) => {
                this.isModeActive = false;
                if (name) onNodeCreated(name, pos.x, pos.y);
            });
        });
    },

    // 2. Link Mode: Source is pre-selected -> Click Target -> Input -> Create
    startLinkMode(network, sourceNodeId, callbacks) {
        this.isModeActive = true;
        this.showTip("Select a target node to connect");

        network.once('click', (params) => {
            this.hideTip();

            // Must click a node
            if (params.nodes.length === 0) {
                this.isModeActive = false;
                return;
            }

            const targetNodeId = params.nodes[0];

            // No self-loops
            if (sourceNodeId === targetNodeId) {
                this.isModeActive = false;
                return;
            }

            // PREVIEW: Show edge immediately
            if (callbacks.onPreview) callbacks.onPreview(sourceNodeId, targetNodeId);

            // Calculate midpoint for input
            const nodeA = network.getPositions([sourceNodeId])[sourceNodeId];
            const nodeB = network.getPositions([targetNodeId])[targetNodeId];
            const domA = network.canvasToDOM(nodeA);
            const domB = network.canvasToDOM(nodeB);
            
            const midX = (domA.x + domB.x) / 2;
            const midY = (domA.y + domB.y) / 2;

            this.showFloatingInput(midX, midY, "is-a", (label) => {
                this.isModeActive = false;
                if (label) {
                    if (callbacks.onSuccess) callbacks.onSuccess(sourceNodeId, targetNodeId, label);
                } else {
                    if (callbacks.onCancel) callbacks.onCancel();
                }
            });
        });
    }
};

window.Interactions = Interactions;