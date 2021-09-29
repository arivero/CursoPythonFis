print("en modB, circular a A...")
import modA
print("...done")
c=modA.c #from modA import c
l=modA.l #from modA import l
def printvar():
        global c
        global l
        print("lista en B, pre:",l, modA.l)
        print("var en B,pre",c,modA.c)
        c+=1
        l[0]+=1
        modA.c+=1000
        modA.l[0]+=1000
        print("lista en B, post:",l, modA.l)
        print("var en B, post",c,modA.c)

        
