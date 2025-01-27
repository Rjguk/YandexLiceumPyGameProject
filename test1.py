import noise
x = 10
y = 10
seed = 1111

s = noise.pnoise3(float(x)*0.05, float(y)*0.05, seed, 1)
print(s)