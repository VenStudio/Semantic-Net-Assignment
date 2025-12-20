class Inference:
    def __init__(self, graph):
        self.graph = graph
    
    def count(self):
        count = 0
        
        # Create a list of all "is-a" edges
        is_a_edges = [(c, p) for c, p, d in self.graph.edges(data=True) if d.get('relation') == 'is-a']

        for child, parent in is_a_edges:
            for target, edge_data in self.graph[parent].items():

                # Check if rel exists
                if self.graph.has_edge(child, target):
                    # Check for conflicting relations
                    if self.graph[child][target].get('relation') != edge_data.get('relation'):
                        count = -1
                    break

                count += 1

        return count

    # Note: I implemented inference for "is-a" relationships only with basic conflict handling
    def run(self):
        new_edges = []
        conflicts = []

        # Create a list of all "is-a" edges
        is_a_edges = [(c, p) for c, p, d in self.graph.edges(data=True) if d.get('relation') == 'is-a']

        for child, parent in is_a_edges:
            for target, edge_data in self.graph[parent].items():
                rel = edge_data.get('relation')

                # Check if relation already exists
                if self.graph.has_edge(child, target):
                    existing = self.graph[child][target].get('relation')
                    # Check for conflicting relations
                    if existing != rel:
                        conflicts.append({
                            "child": child,
                            "target": target,
                            "existing_relation": existing,
                            "inferred_relation": rel
                        })
                    continue

                # Add inferred edge and mark it
                self.graph.add_edge(child, target, relation=rel, inferred=True)
                new_edges.append({
                    "source": child,
                    "target": target,
                    "relation": rel
                })

        return new_edges, conflicts