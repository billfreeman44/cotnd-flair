from PIL import Image
import os

#read in image list and cut out
#images we already edited so we
#dont make infinite images
pngfolder='C:\\Users\\munka\\Desktop\\cotnd\\full_images'
imgs=os.listdir(pngfolder)
imgs.pop()
cimgs=[]
for img in imgs:
    s=img.split(".")
    if s[-1] == 'png': cimgs.append(s[0])

#get info about how many cols and rows 
f=open("cutimages.csv",'r')
names=[]
ncols=[]
nrows=[]
nset=[]
ischaracter=[]
for line in f:
    x=line.split(" ")
    names.append(x[0])
    ncols.append(int(x[1]))
    nrows.append(int(x[2]))
    nset.append(int(x[3]))
    ischaracter.append(int(x[4]))
f.close()


#get info about images to skip
f=open("blacklist.txt",'r')
blist=[]
for line in f:
    blist.append(line.rstrip('\n'))
f.close()


for img in cimgs:
    if (img+'.png' in names) == False: print "WARNING, "+img+" not found!!"
    if img+'.png' in names:
        #get index for ncols and n rows
        index=names.index(img+'.png')
        
        if ischaracter[index] == 0 and ncols[index] != 0:
            
            #load image
            z=Image.open('full_images\\'+img+'.png')
            z.load()

            #get size
            size = z.size
            nx=size[0]
            ny=size[1]

            #loop over number of sets
            for set_number in range(nset[index]):
                skip_factor=abs(ncols[index]/nset[index])
                print set_number,ncols[index],nset[index],skip_factor
                single_width=nx/ncols[index]
                im1=z
                left=single_width*(set_number*skip_factor)
                upper=0
                right=single_width*(set_number*skip_factor+1)
                lower=ny/nrows[index]
                if set_number == 0:
                    post_str=''
                else:
                    post_str='v'+str(set_number+1)
                if (img+post_str+'.png').replace("_","") not in blist:
                    im1.crop((left, upper, right, lower)).save('cutouts\\'+img.replace("_","")+post_str+'.png')
                #im1.load()














