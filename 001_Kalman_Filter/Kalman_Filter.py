import numpy as np
import matplotlib.pyplot as plt
import math

sigma_0=0.1
sigma_1=sigma_0
sigma_2=0.2
mu_1=10
mu_2=np.random.normal(0, sigma_2, 1 )
v=1
H=1
K=(H*sigma_1**2)/(H**2*sigma_1**2+sigma_2**2)

mu_fused=mu_1
sigma_fused=sigma_1

length=21.0
mu_t=np.arange(length)#optimal estimate value
sigma_t=np.arange(length)
z_t=np.arange(length)#measure value
x_t=np.arange(length)#pridiction value
t=np.arange(length)

t[0] = 0
mu_t[0] = mu_fused
sigma_t[0] = sigma_fused
x_t[0]=mu_1
z_t[0]=mu_2

for i in range(1,int(length)):
    mu_1=np.random.normal(mu_fused+v, sigma_fused, 1 )
    mu_2=np.random.normal(i, sigma_2, 1 )
    mu_fused=mu_1+K*(mu_2-H*mu_1)
    sigma_fused=math.sqrt( sigma_1**2-K*H*sigma_1**2)
    sigma_1=sigma_fused
    print(i,mu_1, mu_2, mu_fused,sigma_fused)
    #
    t[i]=i
    mu_t[i]=mu_fused
    sigma_t[i]=sigma_fused
    x_t[i] = mu_1
    z_t[i] = mu_2
#plot
fig,ax=plt.subplots(1,2,figsize=(10,5))
ax[0].plot(t,t,label="real value",marker='s')
ax[0].plot(t,z_t,label="measure value")
ax[0].plot(t,x_t,label="pridiction value")
ax[0].plot(t,mu_t,label="optimal estimate value",marker='o')
ax[0].legend(loc=2)
ax[0].grid(True)
ax[0].set_title('kalman filter ($\sigma_1=$'+str(sigma_0)+',$\sigma_2=$'+str(sigma_2)+')')

ax[1].plot(t,sigma_t,label="$\sigma$")
ax[1].legend(loc=1)
ax[1].grid(True)
ax[1].set_title('kalman filter ($\sigma$)')

plt.show()