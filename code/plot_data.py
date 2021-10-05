import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./stocks_1h.csv')

plt.yscale('log')
for c in data:
    plt.plot(data[c])
    plt.legend([c])
    plt.title('Historical price of {}'.format(c))
    plt.savefig('./plot_{}.png'.format(c))
    plt.close()

