print "lol"


#a[href="#TEMPhephaestus"]:
#after {background-position:0 0;width:25px;height:25px;content:" ";background-
#image: url(%%spritesheet%%);display:inline-block;pointer-events:none;}

prefix='a[href="#'
post='content:" ";background-\
image: url(%%spritesheet%%);display:inline-block;pointer-events:none;}'

f=open("inline_stylesheet.css",'r')
out=open("inline_stylesheet_output.css",'w')
out2=open("slim_flair_output.css",'w')
out2=open("slim_flair_output.css",'w')
flairname=''
width=''
height=''
bp=''
print "|code | image "
print "|:---|:---"
for line in f:
    if ".flair-" in line:
        flairname=line[7:-3]
    if "width" in line:
        width=line[:-1]
    if "height" in line:
        height=line[:-1]
    if "background-position" in line:
        bp=line[:-1]
    if flairname !='' and width !='' and height !='' and bp !='':
        #print prefix+flairname+'"]: after {'+bp+width+height+post
        out.write(prefix+flairname+'"]: after {'+bp+width+height+post+'\n')
        out2.write(".flair-"+flairname+width+height+bp+"}\n")
        print "| "+flairname+"|[](#"+flairname+") "
        flairname=''
        width=''
        height=''
        bp=''
print
print
print

f.close
out.close
out2.close
