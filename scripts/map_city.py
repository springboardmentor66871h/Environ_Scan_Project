import osmnx as ox
import matplotlib.pyplot as plt

place = "Chennai, India"

print("Downloading map...")
graph = ox.graph_from_place(place, network_type="drive")

fig, ax = ox.plot_graph(graph)
plt.show()

print("Map displayed ✅")