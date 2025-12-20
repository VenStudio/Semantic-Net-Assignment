import networkx as nx
from inference import Inference

class SemanticNet:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.inference_engine = Inference(self.graph)

    # Node Utilities
    def add_node(self, name, **kwargs):
        """
        Adds a node with attributes (color, x, y, type).
        Example: net.add_node("Hero", color="red", x=100, y=200)
        """
        if not self.graph.has_node(name):
            self.graph.add_node(name, **kwargs)
        else:
            # Update existing attributes if provided
            self.graph.nodes[name].update(kwargs)

    def remove_node(self, name):
        if not self.graph.has_node(name):
            return
        
        self.graph.remove_node(name)

    # Relationship Utilities
    def add_relation(self, source, relation, target, **kwargs):
        """
        Adds a relationship. 
        kwargs can handle: type='inferred', weight=1, etc.
        """
        # Ensure nodes exist before adding edge (safety check)
        if not self.graph.has_node(source) or not self.graph.has_node(target):
            raise ValueError(f"Both nodes must exist: {source}, {target}")

        self.graph.add_edge(source, target, relation=relation, **kwargs)

    def remove_relation(self, source, target):
        if self.graph.has_edge(source, target):
            # NetworkX edges are (u, v). We need to check if the relation matches 
            # in case multiple edges exist (MultiDiGraph) or just delete the connection.
            # For DiGraph (Single edge per pair), this removes the link:
            self.graph.remove_edge(source, target)
    
    # Inference Utilities
    def run_inference(self):
        return self.inference_engine.run()
    
    def check_inference_potential(self):
        return self.inference_engine.count()

    # Export Utilities
    def get_graph_data(self):
        """Returns the graph in the format our Frontend expects."""
        nodes = []
        for n, attrs in self.graph.nodes(data=True):
            nodes.append({
                "id": n,
                "label": n,
                "color": attrs.get("color", "#808080"),
                "x": attrs.get("x", 0),
                "y": attrs.get("y", 0)
            })
        
        edges = []
        for u, v, attrs in self.graph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "relation": attrs.get("relation"),
                "type": attrs.get("type", "manual"), # manual vs inferred
                "dashes": attrs.get("inferred", False) # Visual style hint
            })
            
        return {"nodes": nodes, "edges": edges}