import glob
import pandas as pd
from matplotlib import pyplot as plt

#looks for .ras file, reads and trims the fat
ras_file = glob.glob("*.ras")
raw = pd.read_fwf(ras_file[0])
data_header=(raw.columns)[0]
reduced_input=list(raw[data_header])

#this variable stores the number of scans in the .ras
n = 0

#we count the scans!
for a in reduced_input:
    if a == "*RAS_INT_START":
        n+=1
print(str(n)+" scans counted.")

#these lists store the start and end markers for scans
starts=[]
ends=[]

for a, b in enumerate(reduced_input):
    if b == "*RAS_INT_START":
        starts.append(a)
    if b == "*RAS_INT_END":
        ends.append(a)

#for each scan, we then remove the chaff and output a cut-down .txt
for i in range(0, n):
    data_split=[]
    deg=[]
    counts=[]
    
    data=reduced_input[starts[i]+1:ends[i]]
    for j in data:
        data_split.append(j.split())
    with open ("scan "+str(i+1)+".txt", "w") as f:
        print("Printing scan "+str(i+1)+" to text file...")
        for k in data_split:
            f.write(str(k[0])+", "+str(k[1])+"\n")
            deg.append(float(k[0]))
            counts.append(float(k[1]))

    #for good measure, why not output an image of the spectrum?
    print("Saving image of scan "+str(i+1)+"...")
    plt.close()
    plt.plot(deg, counts)
    plt.xlabel("Theta/2Theta")
    plt.ylabel("Intensity")
    plt.savefig("Diffractogram "+str(i+1)+".png")
