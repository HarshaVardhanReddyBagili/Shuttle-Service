#from tkinter import font
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx.algorithms.community as nx_comm
#from community import community_louvain

st.title('Shuttle Services - Optimal traffic routes prediction')

uploaded_file = st.file_uploader(" ", type=['xlsx']) #Only accepts excel file format

if uploaded_file is not None:     
    data = pd.read_excel(uploaded_file)
    data
    g = nx.karate_club_graph()
    g = nx.from_pandas_edgelist(data, source = "Origin", target = "Destination", edge_attr=['Distance_meters','Route','Duration_min_minutes']) #Use the Graph API to create an empty network graph object

    partition = nx_comm.louvain_communities(g)
    shortest_path = nx.shortest_path(g)
    color_map = []
    # color the nodes according to their partition
    for node in g:
        if node in partition[0]:
            color_map.append('red')
        elif node in partition[1]:
            color_map.append('yellow')
        elif node in partition[2]:
            color_map.append('maroon')
        elif node in partition[3]:
            color_map.append('purple')
        elif node in partition[4]:
            color_map.append('pink')
        elif node in partition[5]:
            color_map.append('grey')
        elif node in partition[6]:
            color_map.append('orange')
        elif node in partition[7]:
            color_map.append('indigo')
        elif node in partition[8]:
            color_map.append('teal')
        else:
            color_map.append('green')

    fig, ax = plt.subplots(figsize = (30,15))
    pos = nx.spring_layout(g)

    nx.draw_networkx(g, pos, partition, 
                    with_labels=True, 
                    node_size = 250, 
                    node_shape = "s", 
                    edge_color = "k", 
                    style = "--", 
                    node_color = color_map,
                    font_size = 15)
    plt.title('Louvain_communities algorithm', fontdict={'fontsize': 40})
    st.pyplot(fig)
    
    #########################################
    st.info("louvain_community Partition Graph")
    if st.button("Click here for Partition: "):
         st.write(partition, len(partition))
    if st.button("click here for Shortest Path"):
          st.write(shortest_path,nx.shortest_path(g, data.Origin, data.Destination, weight=None, method='dijkstra'))
    com = nx_comm.louvain_communities(g)
    st.subheader("For louvain_communities")
    st.write("Modularity: ", nx_comm.modularity(g, com))
    st.write("Coverage: ", nx_comm.coverage(g, com)) 
    st.write("Performance: ", nx_comm.performance(g, com))

    if st.button("Click to show edge betweeness centrality of graph"):
        edge_BC = nx.edge_betweenness_centrality(g)
        st.info(sorted(edge_BC.items(), key=lambda edge_BC : (edge_BC[1], edge_BC[0]), reverse = True))
   
