import sharedarray.SharedArray as SharedArray
from Other import ModColor
import numpy as np
from Other import MyLogger
log=MyLogger.getLogger("NpShared")

def zeros(*args,**kwargs):
    return SharedArray.create(*args,**kwargs)
    
def ToShared(Name,A):

    try:
        a=SharedArray.create(Name,A.shape,dtype=A.dtype)
    except:
        print>>log, ModColor.Str("File %s exists, delete it..."%Name)
        DelArray(Name)
        a=SharedArray.create(Name,A.shape,dtype=A.dtype)

    a[:]=A[:]
    return a

def DelArray(Name):
    SharedArray.delete(Name)

def ListNames():
    ll=list(SharedArray.list())
    return [AR.name for AR in ll]
    
def DelAll(key=None):
    ll=ListNames()
    for name in ll:
        if key!=None:
            if key in name: SharedArray.delete(name)
        else:
            SharedArray.delete(name)

def GiveArray(Name):
    try:
        return SharedArray.attach(Name)
    except:
        return None


def DicoToShared(Prefix,Dico):
    DicoOut={}
    print>>log, ModColor.Str("DicoToShared: start [prefix = %s]"%Prefix)
    for key in Dico.keys():
        if type(Dico[key])!=np.ndarray: continue
        #print "%s.%s"%(Prefix,key)
        ThisKeyPrefix="%s.%s"%(Prefix,key)
        print>>log, ModColor.Str("  %s -> %s"%(key,ThisKeyPrefix))
        ar=Dico[key].copy()
        Shared=ToShared(ThisKeyPrefix,ar)
        DicoOut[key]=Shared
    print>>log, ModColor.Str("DicoToShared: done")

    return DicoOut


def SharedToDico(Prefix):

    print>>log, ModColor.Str("SharedToDico: start [prefix = %s]"%Prefix)
    Lnames=ListNames()
    keys=[Name for Name in Lnames if Prefix in Name]
    if len(keys)==0: return False
    DicoOut={}
    for Sharedkey in keys:
        key=Sharedkey.split(".")[-1]
        print>>log, ModColor.Str("  %s -> %s"%(Sharedkey,key))
        Shared=GiveArray(Sharedkey)
        DicoOut[key]=Shared
    print>>log, ModColor.Str("SharedToDico: done")


    return DicoOut

