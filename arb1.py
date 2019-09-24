import ApicEM

IntProfName = 'test'

#print(ApicEM.createIntProf(IntProfName))# for IntProfName in IntProfNames])


portname = 'PtSel_X'
port = '22'
AEP_name = 'AEP-testCCG'
VPCPolGrpName = 'PolGrp_VPC_CCGTest'

#print(ApicEM.createVPCPolGrp(VPCPolGrpName, AEP_name)) #takes kwargs

#print(ApicEM.AddPortSeltoIntProf(IntProfName,portname,port,VPCPolGrpName))
print(ApicEM.addVPCPolGrptoPortSel(IntProfName,portname,port,VPCPolGrpName))