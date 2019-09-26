import ApicEM
import csv

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)

l = open('logScript-2.txt', "w+")

a = 0
for i in your_list:
    a += 1    
    if a == 1: continue
    tenant_name,AP,EPG,pod,leaf,port,vpc,New_vpc,vlan,physical_domain,new_physical_domain = i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]
    if physical_domain:
        l.write(physical_domain+' ' + ApicEM.)

l.close()
