import tensorflow as tf
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

def getNN(n):
    xl = []
    i = 0
    while i<=n:
        xl.append((i*2))
        i=i+1
    #print(xl)
    return xl
def getN(n):
    xl = []
    i = 0
    while i<=n:
        xl.append(i)
        i = i+1;
    #print(xl);
    return xl



l0 = Dense(units=10, input_shape=[1])
model = Sequential([l0])
model.compile(optimizer='sgd', loss='mean_squared_error')
#y = x^2
xss = getN(30);
print(xss)
yss = getNN(30)
print(yss)
xs = np.array(xss, dtype=float)
ys = np.array(yss, dtype=float)
print(xs)

model.fit(xs, ys, epochs=20000)

print("Learn : {}".format(l0.get_weights()))

#2350 = , -2345 = 36
x = model.predict([200])
print("200,-200, {}".format(x))
print("200,-200, {}".format(np.mean(x)))
print("200^2 =  "+ str(200*200))