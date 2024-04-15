import json
import networkx as nx

# Parse the JSON file
with open('build_dag.json') as f:
    modules = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for module, data in modules.items():
    G.add_node(module)
    for dependency in data['dependencies']:
        G.add_edge(dependency['artifactId'], module)

# Perform topological sort
sorted_modules = list(nx.topological_sort(G))

# Print the sorted modules to a text file
with open('sorted_modules.txt', 'w') as f:
    for module in sorted_modules:
        f.write(module + '\n')