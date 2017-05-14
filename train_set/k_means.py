from PIL import Image
import os

class PIC_NODE:
    def __init__(self,pic_name,pic_list):
        self.pic_name=pic_name
        self.pic_list=pic_list
        self.cluster=-1

def walk(path='train'):
    file_names=[]
    for root,dirs,files in os.walk(path):
        file_names.append(files)
    return file_names

def resize_pic(pic_name,out_path='handled_train'
               ,new_size=(15,15),h_thresh=20,w_thresh=20):
    im=Image.open(pic_name)
    if im.size[0]>w_thresh or im.size[1]>w_thresh:
        return
    new_im=im.resize(new_size)
    new_im.save(out_path+'\\'+pic_name.split('\\')[-1])

def handle_pic(path):
    for files in walk(path):
        for fp in files:
            resize_pic(path+'\\'+fp,'handled_train')
            print fp

def get_pic_list(pic_name):
    im=Image.open(pic_name)
    width,height=im.size
    pix=im.load()

    pic_list=[]
    for x in range(width):
        for y in range(height):
            pic_list.append(1 if pix[x,y]==0 else -1)

    return pic_list

def read_pic(path='handled_train'):
    result=[]
    for files in walk(path):
        for fp in files:
            result.append(PIC_NODE(fp,get_pic_list(path+'\\'+fp)))
    return result

def init_k_center(path='handled_train'):
    pic_list=['0_0.png','1_3.png','2_0.png','3_3.png','4_0.png','5_1.png',
              '5_2.png','6_2.png','8_3.png','46_0.png']

    result=[]
    for fp in pic_list:
        result.append([float(item) for item in get_pic_list(path+'\\'+fp)])
        
    return result

def get_distance(sou,dest):
    result=0.0
    for i in range(len(sou)):
        result+=(sou[i]-dest[i])**2
    return result

def expectation(data,avg):
    delta=0.0
    counts=[0]*len(avg)
    for item in data:
        pt,min_value=0,get_distance(item.pic_list,avg[0])
        for offset,center in enumerate(avg):
            tmp=get_distance(item.pic_list,center)
            if tmp<min_value:
                pt,min_value=offset,tmp
        counts[pt]+=1
        delta+=tmp
        item.cluster=pt
    return counts,delta/sum(counts)

def maximization(data,counts,length=225):
    avg=[[0.0]*length for i in range(len(counts))]

    for item in data:
        pic_list=item.pic_list
        for i in range(len(counts)):
            avg[item.cluster][i]+=pic_list[i]

    for i in range(len(counts)):
        for j in range(length):
            if counts[i]==0:
                avg[i][j]=0.0
            else:
                avg[i][j]/=counts[i]

    return avg

def k_means(path='10',threshold=0.005):
    avg=init_k_center(path)
    data=read_pic(path)

    tmp=0.0
    counts,delta=expectation(data,avg)
    print delta,counts
    avg=maximization(data,counts)
    '''while abs(delta-tmp)>threshold:
        tmp=delta
        counts,delta=expectation(data,avg)
        print delta,counts
        avg=maximization(data,counts)

    print counts'''
    
    for item in data:
        print "'%s':%d," %(item.pic_name,item.cluster)

def get_dict():
    d={}
    for root,dirs,files in os.walk('.'):
        for directory in dirs:
            tmp=[0.0]*225
            if directory.find('-')>0:
                for root2,dirs2,files2 in os.walk(directory):
                    for fp in files2:
                        print directory+'\\'+fp
                        tmp2=get_pic_list(directory+'\\'+fp)
                        for i in range(225):
                            tmp[i]+=tmp2[i]
                    count=len(files2)
                    for i in range(225):
                        tmp[i]/=count
                d[tuple(tmp)]=directory.split('-')[-1]
    return d

if __name__=='__main__':
    #handle_pic('train')
    #k_means()
    #f=open('result.txt','w')
    print get_dict()

    #f.write(str(d))
    #f.close()
