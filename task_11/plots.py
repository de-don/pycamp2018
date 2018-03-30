import re

import matplotlib.pyplot as plt

data_file = './results_futures.md'

data = {}

title = ""
with open(data_file) as f:
    for line in f:
        if line.startswith("##"):
            title = line.replace("#", "").strip()
            data[title] = []
            continue
        match = re.search(r'count = (\d+)(?:.*?)Time: ([\d\.]+)', line)
        if match:
            x, y = match.groups()
            data[title].append((int(x), float(y)))

fig = plt.figure()
ax = plt.subplot(111)

for title, values in data.items():
    x, y = list(zip(*values))
    t = "--" if "Cats" in title else "-"
    ax.plot(x, y, t, label=title)

ax.legend()

plt.show()
