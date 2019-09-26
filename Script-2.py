import ApicEM
import csv

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)

l = open('logScript-2.txt', "w+")
old_physical_domain_list=[]
old_vpc_list=[]
new_vpc_list=[]
new_physical_domain_list=[]
a = 0
for i in your_list:
    a += 1    
    if a == 1: continue
    tenant_name,AP,EPG,pod,leaf,port,vpc,New_vpc,vlan,physical_domain,new_physical_domain = i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]
    if [tenant_name,AP,EPG,new_physical_domain] not in new_physical_domain_list:
        if new_physical_domain != '':
            new_physical_domain_list.append([tenant_name,AP,EPG,new_physical_domain])
    if [tenant_name,AP,EPG,physical_domain] not in old_physical_domain_list:
        if physical_domain != '':
            old_physical_domain_list.append([tenant_name,AP,EPG,physical_domain])
    if port == '':
        old_vpc_list.append([tenant_name, AP,EPG,vlan,pod,leaf,vpc])
        new_vpc_list.append([tenant_name, AP,EPG,vlan,pod,leaf,New_vpc])

######################################################################################################
l.write("****************Remmoving old VPCs from EPG****************"+ "\n")
for i in old_vpc_list:
    l.write("detaching pod:%s leaf:%s vpc:%s from EPG:%s at tennatnt name:%s and AP profile:%s "%(i[4],i[5],i[6],i[2],i[0],i[1]) +"response: " +  str(ApicEM.DeassociateVPC(i[0],i[1],i[2],i[4],i[5],i[6]))+"\n")
l.write("\n\n\n\n")

l.write("****************Remmoving old physical domains from EPG****************"+ "\n")
for i in old_physical_domain_list:
    l.write("detaching " + i[3] + " from " + i[2] + "response: " + str(ApicEM.DeassociatePHY(i[0],i[1],i[2],i[3])))
    l.write("\n")
l.write("\n\n\n\n")

l.write("****************Associating new VPCs to EPG****************"+ "\n")
for i in new_vpc_list:
    l.write("Adding VPC:%s to tennant:%s ap:%s epg:%s at pod:%s leaf:%s with vlan:%s "%(i[6],i[0],i[1],i[2],i[4],i[5],i[3]) + "response:" + str(ApicEM.AssociateVPCPort2EPG(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))+"\n")
l.write("\n\n\n\n")

l.write("****************Associating new physical domains to EPG****************"+ "\n")
for i in new_physical_domain_list:
     l.write("adding physical domain:%s to epg: %s at tennatnt name: %s and AP profile: %s"%(i[3],i[2],i[0],i[1]) + "response:" + str(ApicEM.AssociatePhyDom2EPG(i[0],i[1],i[2],i[3]))+"\n")
######################################################################################################


######################################################################################################
################################################Backup################################################
# l.write("****************Remmoving new VPCs from EPG****************"+ "\n")
# for i in new_vpc_list:
#    l.write("detaching pod:%s leaf:%s vpc:%s from EPG:%s at tennatnt name:%s and AP profile:%s "%(i[4],i[5],i[6],i[2],i[0],i[1]) +"response: " +  str(ApicEM.DeassociateVPC(i[0],i[1],i[2],i[4],i[5],i[6]))+"\n")
# l.write("\n\n\n\n")

# l.write("****************Remmoving new physical domains from EPG****************"+ "\n")
# for i in new_physical_domain_list:
#    l.write("detaching " + i[3] + " from " + i[2] + "response: " + str(ApicEM.DeassociatePHY(i[0],i[1],i[2],i[3])))
#    l.write("\n")
# l.write("\n\n\n\n")
# l.write("****************Associating old VPCs to EPG****************"+ "\n")
# for i in old_vpc_list:
#    l.write("Adding VPC:%s to tennant:%s ap:%s epg:%s at pod:%s leaf:%s with vlan:%s "%(i[6],i[0],i[1],i[2],i[4],i[5],i[3]) + "response:" + str(ApicEM.AssociateVPCPort2EPG(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))+"\n")
# l.write("\n\n\n\n")

# l.write("****************Associating old physical domains to EPG****************"+ "\n")
# for i in old_physical_domain_list:
#     l.write("adding physical domain:%s to epg: %s at tennatnt name: %s and AP profile: %s"%(i[3],i[2],i[0],i[1]) + "response:" + str(ApicEM.AssociatePhyDom2EPG(i[0],i[1],i[2],i[3]))+"\n")
######################################################################################################

l.close()
