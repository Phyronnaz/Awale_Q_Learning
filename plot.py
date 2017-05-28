import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_hdf(
    "/home/victor/Awale/V0/gamma-0.9-epochs-100000-memory_size-25000-batch_size-512-comment--date-2017_05_26_18:34:33.hdf5")

n = len(df.loss)
y = n // 25
x = [i * y for i in range(25)]


def f(l):
    return [l[k * y:(k + 1) * y].mean() for k in range(25)]


plt.subplot(221)
plt.plot(x, f(df.loss))
plt.subplot(222)
plt.plot(x, f(df.move_count))
plt.subplot(223)
plt.plot(x, f(df.score))

plt.show()
