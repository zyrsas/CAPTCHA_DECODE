from PIL import Image
import os

def get_matrix(pic_name):
    im=Image.open(pic_name)
    pix=im.load()

    width,height=im.size
    result=[]
    for y in range(height):
        result.append([])
        target=result[-1]
        for x in range(width):
            target.append(pix[x,y])

    return result

if __name__=='__main__':
    result=[]
    for name in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if os.path.exists('%s.png' %name):
            result.append('\'%s\': %s,' %(name,get_matrix('%s.png' %name)))
    result='{'+''.join(result)+'}'

    f=open('result.txt','w')
    f.write(result)
    f.close()
