__author__ = 'dias'

import matplotlib.pyplot as plt

years = [1989, 1990, 1991, 1992]

gdp = [300.2, 543.3, 1075.9, 2862.5]

labels = ['Rooselvelt','Bush', 'Clinton', 'Obama']
plt.plot(years, gdp, color='green', marker='o', linestyle='solid')

for l,x,y in zip(labels, years, gdp):
    plt.annotate(l,
                 xy=(x,y),
                 xytext=(5,-5),
                 textcoords='offset points')

plt.title('Nominal GDP')
plt.ylabel('Billions in $')
plt.xlabel('Years')

plt.savefig('gdp')