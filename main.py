from os import walk, makedirs
import os
import shutil

def main(): 
    
    #Make a copy to preserve original directory
    olist=SearchForExtensionType("inputdata",".TXT") 
    CopyTo(olist,"appdata/intermediate") 
    ilist=SearchForExtensionType("appdata/intermediate",".TXT")

    
    #List of Files in the directory of splits
    InitializeSplitFiles(['01234','56789','abcd','efgh','ijklmn','opqrst','uvwxyz'],"appdata/splits")
    slist=SearchForExtensionType("appdata/splits",".TXT")

    #catchall for records that aren't picked up by the splits
    miscfilepath='appdata/splits/othercharacters.txt'
    miscfile=open(miscfilepath,'w',encoding='utf-8') 
    miscfile.close() 

    for spath in slist:
        sname=os.path.splitext(os.path.basename(spath))[0]
        with open(spath,'a') as writefile:
            for ifile in ilist:
                #OPEN THE FILE
                with open(ifile,'r',errors='ignore',encoding='utf-8') as infile:
                    copyfilepath=str('{}_copy'.format(ifile))
                    thecopy=open(copyfilepath,'w',encoding='utf-8')
                    i = 0
                    for l in infile:
                        i = i + 1 
                        if (i==1 or i%1000000==0):
                            print('{} - {} - {}'.format(sname,ifile,i))
                        m=l.strip()
                        k=m[0:1].lower()
                        if k in sname:
                            writefile.write('{}\n'.format(m))
                        else: 
                            thecopy.write('{}\n'.format(m))
                thecopy.close()
                os.rename(copyfilepath,ifile)
    

    #write to misc directory
    with open(miscfilepath,'a') as writefile2:
        for ifile in ilist:
            print('{} - {}'.format(miscfilepath,ifile))
            with open(ifile,'r',errors='ignore',encoding='utf-8') as infile:
                for l in infile:
                    m=l.strip()
                    writefile2.write('{}\n'.format(m))

    #SORT OUT DUPLICATES AND WRITE TO THE BIG LIST
    biglist=open('biglist.txt','w',encoding='utf-8')
    slist2=SearchForExtensionType("appdata/splits",".TXT")
    for sf in slist2:
        print('removing duplicates from {}.'.format(sf))
        uniquewords=set()
        recordcount=0
        with open(sf,'r') as infile:
            for l in infile:
                uniquewords.add(l)
                recordcount=recordcount+1
        print(recordcount)
        print(len(uniquewords))
        
        print('writing words to file')
        for w in uniquewords:
            biglist.write('{}/n'.format(w))


    biglist.close()
    return None
                             

def CopyTo(flist,destdir):
    #dumb copy utility-enter a List of filepaths and where you wish them to be copied
    for f in flist:
        print('copying {} to {}'.format(f,destdir))
        shutil.copyfile(f,str('{}/{}'.format(destdir,os.path.basename(f))))

def SearchForExtensionType(path,FeType):
    #RECURSIVE SEARCH THROUGH ALL FILES IN DIRECTORY MATCHING EXTENSIONTYPE
    print("Searching for .TXTs")
    filelist=[]
    for dir, subdirs, fnames in walk(path):
        for fname in fnames:
            fe = os.path.splitext(fname)[1]
            if(fe.upper()==FeType):
                fullpath=str('{}/{}'.format(dir,fname))
                filelist.append(fullpath)
    filelist.sort()
    return filelist

def InitializeSplitFiles(files,path):
    print("generating files")
    for x in files:
        print(x)
        x=open(str('{}/{}.txt'.format(path,x)),'w',encoding='utf-8') 
        x.close()


if __name__=="__main__":
    main()
