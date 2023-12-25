# Human Trafficking Network in Mexico (HumanTMexicoNetwork)

This repository contains the code and data for the research paper titled "Modeling Human Trafficking Networks in Mexico and the Limits of Dismantling Strategies".

## Overview
Human trafficking is an egregious crime, ranking as the second most profitable illicit activity globally. Mexico, due to its strategic geographic location, experiences high levels of human trafficking. This research employs the snowball sampling method to abstract the interactions within human trafficking networks along Mexico's southern border. Utilizing social network analysis, we discovered that the network is moderately centralized (44.32%) and has a medium density (0.401), indicating limited cohesiveness and challenges in information, money, or product sharing within the network.

## Key Findings
Our analysis evaluates different strategies to dismantle these criminal organizations. The findings suggest that the initial focus should not be on the most connected or isolated individuals but rather on those with moderate connections within the network. This nuanced approach to network disruption is crucial for developing effective strategies against human trafficking.

## Repository Contents
- `Data.txt`: Contains the graph representation of the network with 34 operator nodes, detailing the nodes and edges.
- `Human_Capital.py`: Implements the algorithms necessary to identify the optimal strategy for isolating critical nodes in the network as described in the paper.
- `Human Trafficking Network in Mexico (GND).py`: Implements the Generalize Network Dismantling Algorithm cited in the paper.
- `labels.csv`: Contains a comprehensive mapping of role labels to the nodes listed in `Data.txt`, serving as a key to identify and categorize each node's function within the network.

Our comprehensive dataset and algorithms provide a significant advancement in quantitatively understanding the roles and interactions of individuals within real-world human trafficking networks, as well as assessing the potential impact of various network dismantling strategies.

Please refer to each document for a detailed description of its contents and role in the research.
