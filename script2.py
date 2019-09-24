#Script 2
import ApicEM
IntProfNames = ['CCGTest_IntProf_101','CCGTest_IntProf_102','CCGTest_IntProf_103','CCGTest_IntProf_104']
SwProfNames = ['CCGTest_SwProf_101', 'CCGTest_SwProf_102','CCGTest_SwProf_103','CCGTest_SwProf_104']
Switches = ['101','102','103','104']
tenant_name = 'testCCG'
apProfile = 'AP'
EPGname = 'testCCG'

print('Adding actual leafs to switch profiles'+str([ApicEM.AddLeafSeltoSwitchProf(SwProfNames[i],SwProfNames[i]+'_Sel',Switches[i]) for i in range(len(Switches))]))
VPCPolGrpName = 'PolGrp_VPC_CCGTest_1718'
print('adding VPC to EPG'+str(ApicEM.AssociateVPCPort2EPG(tenant_name, apProfile, EPGname, '62', '1','101-102',VPCPolGrpName)))
#AssociateVPCPort2EPG(tenant_name, apProfile, EPGname, Vlan, pod,leafpath,port)
