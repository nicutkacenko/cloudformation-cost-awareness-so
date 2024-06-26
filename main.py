import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# Data
y = np.array([7583, 78643, 2426, 1057, 22132, 909])
mylabels = ["keyword-first", "keyword-second", "aws-first", "aws-second", "aws-second-updated", "aws-third"]
relevant_repos = [0, 48, 13, 5, 432, 4]

# Create the pie chart
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(y, labels=mylabels, autopct='%1.1f%%', startangle=90)

# Adding relevance annotations
for i, a in enumerate(autotexts):
    a.set_text(f'{a.get_text()}\nRelevant: {relevant_repos[i]}')

# Save plot as PNG
plt.savefig('pie_chart.png')

# Two lines to make our compiler able to draw:
sys.stdout.flush()
