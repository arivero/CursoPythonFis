print("en A, name=",__name__)
c=8
l=[8]
print("en A, import modA...")
import modA
print("...done import A")
if __name__=='__main__':
    print("en if main ")
    #import modA
    from modA import c
    l=modA.l
    c=c+200
    l[0]+=200
    import modB
    modB.printvar()
    c=c+2
    l[0]+=2
    print("c en A:",c,modA.c,modB.c)
    print("l en A:",l,modA.l,modB.l)
#c=8
#l=[8]
