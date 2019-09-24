import ApicEM

tenant_name = 'testCCG'
apProfile = 'AP'
EPGname = 'testCCG'
VPCPolGrpName = 'PolGrp_VPC_CCGTest'
print('adding VPC to EPG'+str(ApicEM.AssociateVPCPort2EPG(tenant_name, apProfile, EPGname, '62', '1','101-102',VPCPolGrpName, mode='untagged')))