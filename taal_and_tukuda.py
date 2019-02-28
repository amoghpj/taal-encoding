# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt

def createCircle(ax):
    all_thetas = np.arange(0,2*np.pi+2*np.pi/400,2*np.pi/400)
    X = [np.cos(theta) for theta in all_thetas]
    Y = [np.sin(theta) for theta in all_thetas]
    ax.axvline(0,color='gray',alpha=0.3)
    ax.axhline(0,color='gray',alpha=0.3)    
    ax.plot(X,Y,'gray',lw=1)


def createTaal(name, ax,taaldict,num_avartans=1):
    createCircle(ax)
    distance = 2*np.pi/(taaldict[name]['matra'] )
    matras = np.arange(num_avartans*2*np.pi,0-distance,-distance)
    m_count = 1
    for m in matras:
        if m_count == taaldict[name]['sam']:
            ax.plot(np.cos(m),np.sin(m),marker='o',markerfacecolor='none',color='k',ms=10)
        if m_count in taaldict[name]['taali']:
            ax.plot(np.cos(m),np.sin(m),'ko')
        if m_count in taaldict[name]['khaali']:
            ax.plot(np.cos(m),np.sin(m),'kx',ms=10)#color='#67db45'
        else:
            ax.plot(np.cos(m),np.sin(m),'k.')                    
        m_count +=1 

def newplot():
    f, ax = plt.subplots(1,1,figsize=(3,3))
    ax.set_xticks([])
    ax.set_yticks([])
    return ax
def prettystring(total, i):
    if i +1 <10:
        return("0"+str(i+1))
    else:
        return(str(i+1))
def executeAvartan(bol, taaldict, num_avartans):
    name = bol.guessTaal()
    print(name)
    distance = 2*np.pi/(taaldict[name]['matra'] )
    matras = np.arange(num_avartans*2*np.pi,0-distance,-distance)
    aksharlist = bol.Akshar
    for i,(m,a) in enumerate(zip(matras, aksharlist)):
        plt.close()
        ax = newplot()
        createTaal(name, ax, taaldict,num_avartans=num_avartans)
        ax.plot([0.5*np.cos(m),np.cos(m)],[0.5*np.sin(m),np.sin(m)],'gray')
        if a != 'S':
            ax.plot(np.cos(m),np.sin(m),'bo',ms=10)
            ax.annotate(a,xy=(0,0),xytext=(0,0))
        else:
            ax.annotate(a,xy=(0,0),xytext=(0,0))
        ax.axis('off')
        ax.set_title(name + ' (' +prettystring(len(aksharlist),i)+'/'+ str(len(aksharlist)) +')')
        plt.savefig('../experiments/animation/taal/' + name.replace(' ','-') + '-' + prettystring(len(aksharlist),i) +'.png')


class bolParser:
    def __init__(self, bol):
        self.bol = bol
        self.Avartan = list()
        self.Vibhaag = list()
        self.Akshar = list()
        self.num_avartans = 0
        self.taaldict = {'teen taal':{'matra':16,
                                      'taali':[5,13],
                                      'khaali':[9],
                                      'sam':1},
                         'jhap taal':{'matra':10,
                                      'taali':[6],
                                      'khaali':[3,8],
                                      'sam':1},
                         'roopak taal':{'matra':7,
                                        'taali':[6],
                                        'khaali':[1],
                                        'sam':4},
                         'keherwa taal':{'matra':8,
                                         'taali':[],
                                         'khaali':[5],
                                         'sam':1},
                         'ek taal':{'matra':12,
                                    'taali':[5,8],
                                    'khaali':[3,7],
                                    'sam':1}}

        self.__getAvartan()
        self.__getVibhaag()
        self.__getAkshar()
        self.num_avartans = len(self.Avartan)
        
    def __getAvartan(self):
        self.Avartan = self.bol.split('||')[:-1]

    def __getVibhaag(self):
        self.Vibhaag = [av.split('|') for av in self.Avartan]

    def __getAkshar(self):
        GroupedAkshars = [[v.split(' ') for v in V] for V in self.Vibhaag]
        for av in GroupedAkshars:
            for v in av:
                for a in v:
                    self.Akshar.append(a)
        

    def guessTaal(self):
        matra_per_avartan = int(float(len(self.Akshar))/float(len(self.Avartan)))
        print(matra_per_avartan)
        for taal in self.taaldict.keys():
            if matra_per_avartan == self.taaldict[taal]['matra']:
                return(taal)
    
bol = \
    "dha S na dha|" \
    "ti ta dhi ki|" \
    "ta na ghe na|" \
    "na ghe na dha||" \
    "ti ta dhi ki|" \
    "ta na ghe na|" \
    "taa S na taa|" \
    "ti ta ti ki||" \
    "ta na ghe na|" \
    "na ghe na dha|" \
    "ti ta dhi ki|" \
    "ta na ghe na||" \
    "dha S na dha|" \
    "ti ta dhi ki|" \
    "ta na ghe na|" \
    "na ghe na dha||" \
    "ti ta dhi ki|" \
    "ta na ghe na|" \
    "dha S na dha|" \
    "ti ta dha S||" \
    "S ta ki ta|" \
    "dha S S ta|" \
    "ki ta dha S|" \
    "S ta ki ta||"

# bol = \
#     "dhi kita dhin|"\
#     "ta dha dha din||"\
#     "ta dhin na|"\
#     "S kata dha S||"\
#     "ti kita tin|"\
#     "ta taa taa tin||"\
#     "ta tin na|"\
#     "S kata dha S||"

#bol = u"धा धीं धीं धा|धा धीं धीं धा|धा तिं तिं ता|ता धीं धीं धा||"

matras = bolParser(bol)

plt.close()    

executeAvartan(matras,
               matras.taaldict,
               matras.num_avartans)
