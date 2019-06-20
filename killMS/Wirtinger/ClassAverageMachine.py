import numpy as np

class ClassAverageMachine():
    def __init__(self,GD,PM_Compress,SM_Compress,PolMode="Scalar"):
        self.GD=GD
        self.PM_Compress=PM_Compress
        self.SM_Compress=SM_Compress
        self.PolMode=PolMode
        if self.GD["Solvers"]["NChanSols"]!=1:
            raise ValueError("Only deal with NChanSol=1")
        if self.GD["Solvers"]["PolMode"]!="Scalar":
            raise ValueError("Only deal with PolMode=Scalar")

    def AverageKernelMatrix(self,DicoData,K):
        #A0,A1=DicoData[""]
        A0=DicoData["A0"]
        A1=DicoData["A1"]
            
        NDir,Np,Npol=K.shape
        NpBlBlocks=DicoData["NpBlBlocks"][0]
        A0A1=sorted(list(set([(A0[i],A1[i]) for i in range(A0.size)])))
        NpOut=len(A0A1)
        NDirAvg=self.SM_Compress.NDir
        KOut=np.zeros((NDir,NDirAvg,NpOut,Npol),K.dtype)

        IndList=[(np.where((A0==ThisA0)&(A1==ThisA1))[0]) for (ThisA0,ThisA1) in A0A1]

        for iDirAvg in range(NDirAvg):
            K_Compress=self.PM_Compress.predictKernelPolCluster(DicoData,self.SM_Compress,iDirection=iDirAvg)
            for iDir in range(NDir):
                p=K[iDir,:,:]
                pp=p*K_Compress[:,:,0].conj()
                for iBl,ind in enumerate(IndList):
                    KOut[iDir,iDirAvg,iBl,0]=np.mean(pp[ind])

        KOut=KOut.reshape((NDir,NDirAvg*NpOut,Npol))
        KOut[:,:,3]=KOut[:,:,0]

        return KOut

    def AverageDataVector(self,DicoData):
        A0=DicoData["A0_freq_flat"]
        A1=DicoData["A1_freq_flat"]
            

        NpBlBlocks=DicoData["NpBlBlocks"][0]
        A0A1=sorted(list(set([(A0[i],A1[i]) for i in range(A0.size)])))
        NpOut=len(A0A1)
        NDirAvg=self.SM_Compress.NDir
        Data_Avg = np.zeros((NDirAvg,NpOut,Npol),K.dtype)

        IndList=[(np.where((A0==ThisA0)&(A1==ThisA1))[0]) for (ThisA0,ThisA1) in A0A1]

        d=DicoData["data"]
        f=DicoData["flag"]
        FOut=np.zeros(d.shape,f.dtype)

        for iDirAvg in range(NDirAvg):
            K_Compress=self.PM_Compress.predictKernelPolCluster(DicoData,self.SM_Compress,iDirection=iDirAvg)
            dp=d*K_Compress[:,:,0].conj()
            for iBl,ind in enumerate(IndList):
                if np.min(f[ind])==0:
                    FOut[iDirAvg,iBl,0]=1
                    continue
                KOut[iDirAvg,iBl,0]=np.sum(dp[ind]*(1-f[ind])))/np.sum(1-f[ind])

        DicoData["flags_flat"]=np.rollaxis(KOut,2).reshape(self.NJacobBlocks_X,nr*nch*self.NJacobBlocks_Y)
        DicoData["data_flat"]=np.rollaxis(DicoData["data"],2).reshape(self.NJacobBlocks_X,nr*nch*self.NJacobBlocks_Y)

        KOut=KOut.reshape((NDir,NDirAvg*NpOut,Npol))
        KOut[:,:,3]=KOut[:,:,0]

        return KOut
      
