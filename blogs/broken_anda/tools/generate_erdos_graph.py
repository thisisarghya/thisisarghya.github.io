'''
On cloudtop:
arghyabh@arghya:~$ python3 --version
Python 3.13.12
arghyabh@arghya:~$ sudo apt install python3-pip python3-venv
arghyabh@arghya:~$ python3 -m venv env
arghyabh@arghya:~$ source env/bin/activate
arghyabh@arghya:~$ pip install networkx matplotlib
arghyabh@arghya:~$ python generate_erdos_graph.py

On local:
scp root@arghya.c.googlers.com:/usr/local/google/home/arghyabh/erdos_path/png .
'''


import networkx as nx
import matplotlib.pyplot as plt

def generate_erdos_graph():
    # 1. Create a new undirected graph
    G = nx.Graph()

    # 2. Define the edges based on all the collaborations
    edges = [
        # Your path via Bender (Length 3)
        ("Paul Erdős", "Michael E. Saks"),
        ("Michael E. Saks", "Michael A. Bender"),
        ("Michael A. Bender", "Arghya Bhattacharya"),
        
        # Rezaul's Path 1 via Thorup (Length 3)
        ("Paul Erdős", "Peter Winkler"),
        ("Peter Winkler", "Mikkel Thorup"),
        ("Mikkel Thorup", "Rezaul A. Chowdhury"),
        
        # Rezaul's Path 2 via Szegedy (Length 3)
        ("Paul Erdős", "Márió Szegedy"),
        ("Márió Szegedy", "Phillip Gibbons"),
        ("Phillip Gibbons", "Rezaul A. Chowdhury"),
        
        # Rezaul's Path 3 via Mitchell (Length 3)
        ("Paul Erdős", "Craig Tovey"),
        ("Craig Tovey", "Joseph Mitchell"),
        ("Joseph Mitchell", "Rezaul A. Chowdhury"),
        
        # Cross connections
        ("Rezaul A. Chowdhury", "Michael A. Bender"),
        ("Arghya Bhattacharya", "Rezaul A. Chowdhury"),

        ("Michael A. Bender", "Helen Xu"),
        ("Rezaul A. Chowdhury", "Helen Xu"),
        ("Arghya Bhattacharya", "Helen Xu")
    ]
    
    G.add_edges_from(edges)

    # 3. Assign nodes to "layers" based on their shortest distance to Paul Erdős
    # This keeps the graph organized left-to-right
    for node in G.nodes():
        try:
            # Calculate shortest path length to Erdős
            distance = nx.shortest_path_length(G, source="Paul Erdős", target=node)
            G.nodes[node]["layer"] = distance
        except nx.NetworkXNoPath:
            G.nodes[node]["layer"] = 5 # Fallback

    # 4. Setup the visual layout
    plt.figure(figsize=(16, 10))
    
    # Use multipartite layout to arrange nodes by their 'layer' attribute
    pos = nx.multipartite_layout(G, subset_key="layer", align="horizontal")
    
    # 5. Configure visual styling
    # Highlight the primary shortest path (Erdős -> Saks -> Bender -> Arghya)
    primary_path = [("Paul Erdős", "Michael E. Saks"), ("Michael E. Saks", "Michael A. Bender"), ("Michael A. Bender", "Arghya Bhattacharya")]
    
    # Draw all edges in a light gray/blue first
    nx.draw_networkx_edges(G, pos, edge_color='#cccccc', width=2)
    
    # Draw the primary shortest path bolder and in a different color
    nx.draw_networkx_edges(G, pos, edgelist=primary_path, edge_color='#ff9f1c', width=4)
    
    # Draw the nodes
    nx.draw_networkx_nodes(
        G, pos, 
        node_size=7000, 
        node_color='#e0fbfc', 
        edgecolors='#3d5a80', 
        linewidths=3
    )
    
    # Customize label appearance. We'll split long names into two lines for readability.
    labels = {node: node.replace(" ", "\n") for node in G.nodes()}
    nx.draw_networkx_labels(
        G, pos, 
        labels=labels,
        font_size=14, 
        font_family='sans-serif', 
        font_weight='bold',
        font_color='#293241'
    )

    # 6. Clean up the plot and save
    plt.axis('off')
    plt.title("My Erdős number is 3!", fontsize=22, fontweight='bold', pad=30)
    plt.tight_layout()

    filename = "erdos_path.png"
    plt.savefig(filename, format="PNG", dpi=300, bbox_inches="tight")
    print(f"Graph image successfully generated and saved as '{filename}'")

if __name__ == "__main__":
    generate_erdos_graph()
