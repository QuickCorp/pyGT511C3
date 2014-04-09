import FPS
from PIL import Image, ImageEnhance
import numpy as np
FPS.BAUD = 115200

def desplazarImagen(image,image2,delta):
    "Roll an image sideways"
    xsize, ysize = image.size
    delta = delta % xsize
    if delta == 0: return image
    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize-delta, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))
    image.save(image2)
    return image

def cortarImagen(img, image2):
    img2 = img.crop((8,7,141,112)) # cuadro que solo contiene la huella sin borde
    img2.save(image2)
    return img2


def normalize(arr):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = arr.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
    return arr

def normalizeImage(img,image2):
    arr=np.array(np.asarray(img).astype('float'))
    new_img = Image.fromarray(normalize(arr).astype('uint8'))
    new_img.save(image2)
    return new_img
    
def binarizeImage(img,image2):
    img = img.convert('1') # convertir en 1-bitpixels,blackandwhite,storedas8-bitpixels
    img.save(image2)
    return img
    
def rotateImage(img,image2):
    img = img.transpose(Image.ROTATE_270)
    img.save(image2)
    return img

def pixelesVecinos(image,pixel):
    x = pixel[0]
    y = pixel[1]
    vecinos = [(x-1,y-1),
               (x-1,y),
               (x-1,y+1),
               (x,y+1),
               (x+1,y+1),
               (x+1,y),
               (x+1,y-1),
               (x,y-1)]
    return [image.getpixel(v) for v in vecinos]

def segmentacion(im,image2):
    im = im.point(lambda i: i*0.9 if i >=sum(list(im.getdata()))/(list(im.getdata()).__len__())  else 255)
    enh = ImageEnhance.Contrast(im)
    im = enh.enhance(1.2)
    im.save(image2)
    return im

def bifurcaciones(image,size):
    bifurcacion = [0,0,255,0,0,255,0,255]
    inicioFin =   [0,0,255,0,0,0,0,0]
    sizeX = size[0]-2
    sizeY = size[1]-2
    pixs = []
    for x in range(1,sizeX):
        for y in range (1,sizeY):
            pixs.append((x,y))
    return [1 if pixelesVecinos(image, (x1,y1) ) == bifurcacion else -1  for (x1,y1) in pixs]

def contarBifurcaciones(bifurcaciones):
    return sum(filter(lambda x: x==1, bifurcaciones))

def contarNoBifurcaciones(bifurcaciones):
    return sum(map(lambda m: -1*m,filter(lambda x: not x==1, bifurcaciones)))

def matchBif(im1,im2):
    bif1 = (contarBifurcaciones(bifurcaciones(im1,im1.size)),
           contarNoBifurcaciones(bifurcaciones(im1,im1.size)))
    bif2 = (contarBifurcaciones(bifurcaciones(im2,im2.size)),
           contarNoBifurcaciones(bifurcaciones(im2,im2.size)))
    tolerance = 0.1
    print bif1
    print bif2
    return True if bif2[0]-bif1[0] <= bif2[0]*tolerance or bif2[1]-bif1[1] <= bif2[0]*tolerance else False

def GetRawImg(fps):
    ret = bytes()
    if fps.SetLED(True) and fps.IsPressFinger():
        if fps.GetRawImage():
            response = fps._lastResponse.RawBytes[16:]
            print fps.serializeToSend(response)
            print u'Size %s' % str(response.__len__())
            ret = bytes(response)
    FPS.delay(0.1)
    fps.SetLED(False)
    return ret

def SavedImg(imgName):    
    img = Image.open(imgName + '.binar.bmp')
    return img

def processImage(imgName,imgRaw):
    img = Image.fromstring(mode='L',size=(160,120),data= imgRaw)
    enh = ImageEnhance.Brightness(img)
    img = enh.enhance(1.2)
    enh = ImageEnhance.Contrast(img)
    img = enh.enhance(4)
    enh = ImageEnhance.Sharpness(img)
    img = enh.enhance(1.2)
    img.save(imgName + '.bmp','BMP')
#    img = rotateImage(img, imgName  + '.rotate.bmp')
    img = normalizeImage(img,imgName + '.norm.bmp')
    img = segmentacion(img,imgName + '.seg.bmp')
    img = cortarImagen(img,imgName   + '.crop.bmp')
    img = binarizeImage(img,imgName  + '.binar.bmp')
    return img

def SaveImage(imgName,imgRaw):
    """
    f = open(imgName, "w")
    f.write(imgRaw)
    f.close()
    """
    processImage(imgName,imgRaw)

def Enroll(fps,id):
    imgRaw = GetRawImg(fps)
    if imgRaw.__len__()>0:
        FPS.delay(3)
        SaveImage('fingerprint'+id+'.raw', imgRaw)
    """
        imgRaw2 = GetRawImg(fps)
        if imgRaw2.__len__()>0:
            FPS.delay(3)
            SaveImage('fingerprint2.raw', imgRaw2)
            imgRaw3 = GetRawImg(fps)
            if imgRaw3.__len__()>0:
                FPS.delay(3)
                SaveImage('fingerprint3.raw', imgRaw3)
    """

def Verify(fps,id):
    imgRaw = GetRawImg(fps)
    if imgRaw.__len__()>0:
        FPS.delay(3)
        img = processImage('fingerprint_verify_'+id+'.raw',imgRaw)
        savedImg1 = SavedImg('fingerprint'+id+'.raw')
        return 'Verified is: %s' % (str(matchBif(img, savedImg1)))
    else:
        return 'Not Verified'

