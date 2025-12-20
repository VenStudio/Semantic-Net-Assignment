/*
 * graph.js
 * Wrapper for the Vis.js Network library.
 * Manages the visual rendering, physics, and data state (nodes/edges).
 */

const Graph = {
    network: null,
    // The source of truth for the visual state
    nodes: new vis.DataSet([]),
    edges: new vis.DataSet([]),

    // Initialize the canvas
    init(containerId) {
        const container = document.getElementById(containerId);

        const data = {
            nodes: this.nodes,
            edges: this.edges
        };

        // Configuration ported from your original ui.js
        const options = {
            physics: {
                enabled: true,
                stabilization: {
                    enabled: true,
                    iterations: 200 // Kept your original iteration count
                },
                barnesHut: {
                    gravitationalConstant: -5000, // Stronger repulsion as per your original
                    centralGravity: 0.015,        // Very weak center pull (spreads graph out)
                    springLength: 150,
                    springConstant: 0.04,
                    damping: 0.3,                 // Higher damping = less jittery
                    avoidOverlap: 0.1
                }
            },
            nodes: {
                shape: 'dot',
                size: 25, // Your original size
                font: {
                    size: 16,
                    color: '#fff8d6', // Updated to match Dark Theme (was #000)
                    face: 'Segoe UI',
                    strokeWidth: 0,
                    vadjust: -40      // Pushes label slightly above node
                },
                borderWidth: 2,
                color: {
                    background: '#666666',
                    border: '#fff8d6',
                    highlight: {
                        background: '#eb7044', // Matches --primary
                        border: '#fff8d6'
                    }
                },
                shadow: true
            },
            edges: {
                width: 2,
                color: {
                    color: '#888888',
                    highlight: '#eb7044',
                    inherit: true
                },
                arrows: { to: { enabled: true, scaleFactor: 1 } },
                smooth: { type: 'continuous' }
            },
            interaction: {
                hover: true,             // Required for cursor changes
                selectConnectedEdges: false,
                multiselect: false       // Single node selection for orbit menu
            }
        };

        this.network = new vis.Network(container, data, options);

        // Cursor interactions
        this.network.on("hoverNode", () => container.style.cursor = 'pointer');
        this.network.on("blurNode", () => container.style.cursor = 'default');
        this.network.on("hoverEdge", () => container.style.cursor = 'pointer');
        this.network.on("blurEdge", () => container.style.cursor = 'default');

        // Empty State Logic
        const emptyState = document.getElementById('empty-state');
        const updateEmptyState = () => {
            if (!emptyState) return;
            if (this.nodes.length === 0) emptyState.classList.remove('hidden');
            else emptyState.classList.add('hidden');
        };

        this.nodes.on('add', updateEmptyState);
        this.nodes.on('remove', updateEmptyState);
        
        // Initial check
        updateEmptyState();

        return this.network;
    },

    // Helper: Reset the graph (used when loading presets)
    clear() {
        this.nodes.clear();
        this.edges.clear();
    }
};

// Expose to window so main.js can access it
window.Graph = Graph;