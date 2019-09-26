#Script1
import ApicEM

VLP_name = "CCGTest_VLP"
Phy_name = "CCGTest_PhysDom"
AEP_name = "CCGTest_AEP"
IntPolGrpName = "CCGTest_single_Polgrp" #policy group for single interfaces

IntProfNames = ['CCGTest_IntProf_101','CCGTest_IntProf_102','CCGTest_IntProf_103','CCGTest_IntProf_104']
SwProfNames = ['CCGTest_SwProf_101', 'CCGTest_SwProf_102','CCGTest_SwProf_103','CCGTest_SwProf_104']

rangeFrom = "60"
rangeTo = "65"
allocationMode = "static" #or dynamic
print('creating VLP'+str(ApicEM.addVLP(VLP_name, allocationMode)))
print((ApicEM.addVlans2VLP(VLP_name, rangeFrom, rangeTo, allocationMode)))
print('creating Physical domain' +str(ApicEM.createPHY(Phy_name, VLP_name)))
print('creating AEP'+str(ApicEM.attachAEP(AEP_name, Phy_name)))
print('creating IntProfiles'+str([ApicEM.createIntProf(IntProfName) for IntProfName in IntProfNames]))
print('creating SwProfiles'+str([ApicEM.createSwitchProf(SwitchProfName) for SwitchProfName in SwProfNames]))
print('adding IntProfiles to SwProfiles'+str([ApicEM.addIntProfToSwitchProf(SwProfNames[i], IntProfNames[i]) for i in range(len(SwProfNames))]))


#Uncommentline below to execute on Apic:
print('creating PolGrp for single interfaces'+str(ApicEM.createIntPolGrp(IntPolGrpName, AEP_name, LLDP="lldp_enable", CDP = 'CDP_ENABLE')))


portname = 'CCGTest_Int_sel_17'
port = '17'
print('adding port to IntProf'+str(ApicEM.AddPortSeltoIntProf('CCGTest_IntProf_104',portname,port,IntPolGrpName)))

VPCPolGrpName = 'PolGrp_VPC_CCGTest_1718'
lacp_policy = 'default' #for CCG its LACP_active
print(ApicEM.createVPCPolGrp(VPCPolGrpName, AEP_name,LACP = lacp_policy)) #takes kwargs

print(ApicEM.AddPortSeltoIntProf('CCGTest_IntProf_101','PtSel_17','17','PolGrp_VPC_CCGTest_1718'))
print(ApicEM.AddPortSeltoIntProf('CCGTest_IntProf_102','PtSel_18','18','PolGrp_VPC_CCGTest_1718'))

print(ApicEM.addVPCPolGrptoPortSel('CCGTest_IntProf_101','PtSel_17','17','PolGrp_VPC_CCGTest_1718'))
print(ApicEM.addVPCPolGrptoPortSel('CCGTest_IntProf_102','PtSel_18','18','PolGrp_VPC_CCGTest_1718'))
