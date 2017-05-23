import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_hdf(
    "/home/victor/Awale/V0/size-3-epochs-10000-memory_size-8192-batch_size-128-comment--date-2017_05_23_23:39:43.hdf5")

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
