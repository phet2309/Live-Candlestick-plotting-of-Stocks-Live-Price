import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.widgets import Cursor

fig=plt.figure()
ax1=fig.add_subplot(1,1,1)

def animate(i):
    graph_data=open('basic.txt','r').read()
    lines=graph_data.split('\n')
    xs=[]
    ys=[]
    for line in lines:
        if len(line)>1:
            x,y=line.split(',')
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs,ys)

    
    
    
ani=animation.FuncAnimation(fig,animate,interval=1000)
cursor=Cursor(ax1,horizOn=True,vertiOn=True,color='green',linewidth=2.0)
   
plt.show()

