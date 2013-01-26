import PIL.Image
import re
import os.path
import profiles.settings as settings
from profiles.models import Image
from profiles.utils.random_keys import *

class AspectRatioException(Exception):

    pass

def upload_image(imageData,user = None,save = True,path = None):
    try:
        extension = re.search(r"\.(\w+)$",imageData.name).group(1)
    except:
        raise Exception("Cannot determine extension from filename: %s" % imageData.name)

    try:
        temporaryPath = generate_random_filename(settings.FILE_TEMPORARY_UPLOAD_PATH,extension)
        if path:
            (directory,filename) = os.path.split(path)
            match = re.search(r"^(.*)\.(\w+)$",filename)
            imageFilenameKey = match.group(1)
        else:            
            imageFilenameKey = generate_random_filename_key(settings.FILE_UPLOAD_PATH,extension = "jpg")
        
        imagePath = settings.FILE_UPLOAD_PATH+"/"+imageFilenameKey+"."+settings.IMAGE_EXTENSION
        imageUrl = settings.FILE_UPLOAD_URL+"/"+imageFilenameKey+"."+settings.IMAGE_EXTENSION
        
        temporaryFile = open(temporaryPath,'wb')
    
        for chunk in imageData.chunks():
            temporaryFile.write(chunk)
        
        temporaryFile.close()
        
        try:
            pilImage = PIL.Image.open(temporaryPath)
            
            aspectRatio = float(pilImage.size[0])/float(pilImage.size[1])
            
            if aspectRatio > 1.:
                aspectRatio = 1./aspectRatio
                
            if aspectRatio < settings.IMAGE_MINIMUM_ASPECT_RATIO:
                raise AspectRatioException("Aspect ratio of the image is too small!")
                
            pilRescaledImage = shrink_image(pilImage,settings.IMAGE_MAXIMUM_DIMENSIONS)
            
            pilRescaledImage.save(imagePath,settings.IMAGE_FORMAT)
    
            image = Image()
            image.user = user
            image.path = imagePath
            image.url = imageUrl
            image.width = pilRescaledImage.size[0]
            image.height = pilRescaledImage.size[1]
            if save:
                image.save()
            return image
        except:
            raise
    finally:
        if os.path.exists(temporaryPath):
            os.remove(temporaryPath)
        
def create_derived_image(image,pilDerivedImage,type,eraseOldVersions = True):
    
    if eraseOldVersions:
        image.derived_images.filter(type = type).delete()
        
    (directory,basename,extension) = image.splitPath()

    derivedImageFilename = basename+"_"+type+"."+extension
    derivedImagePath = directory+"/"+derivedImageFilename
    
    cnt = 1
    
    while os.path.exists(derivedImagePath): 
        derivedImageFilename = basename+"_"+type+("_%d" % cnt)+"."+extension
        derivedImagePath = directory+"/"+derivedImageFilename
        cnt+=1

    derivedImageUrl = settings.FILE_UPLOAD_URL+"/"+derivedImageFilename

    pilDerivedImage.save(derivedImagePath)

    derivedImage = Image()
    derivedImage.path = derivedImagePath
    derivedImage.user = image.user
    derivedImage.base_image = image
    derivedImage.type = type
    derivedImage.url = derivedImageUrl
    derivedImage.width = pilDerivedImage.size[0]
    derivedImage.height = pilDerivedImage.size[1]
    derivedImage.save()
    
    return derivedImage

def shrink_image(pilImage,dimensions):
    if pilImage.size[0] <= dimensions[0] and pilImage.size[1] <= dimensions[1]:
        return pilImage
    pilThumbnail =  pilImage.copy()
    pilThumbnail.thumbnail(dimensions,PIL.Image.ANTIALIAS)
    return pilThumbnail

def rescale_and_crop_image(image,position = (0,0)):

    pilImage = PIL.Image.open(image.path)
    
    dimensions = pilImage.size
    
    if dimensions[0] >= dimensions[1]:
        scaleFactor = float(settings.PROFILE_IMAGE_DIMENSIONS[1])/float(dimensions[1])
    else:
        scaleFactor = float(settings.PROFILE_IMAGE_DIMENSIONS[0])/float(dimensions[0])
    
    scaleFactorCover = float(settings.COVER_IMAGE_WIDTH)/float(dimensions[0])
    
    pilProfileImageBase = pilImage.resize((int(dimensions[0]*scaleFactor),int(dimensions[1]*scaleFactor)),PIL.Image.ANTIALIAS)
    pilProfileImageCover = pilImage.resize((int(dimensions[0]*scaleFactorCover),int(dimensions[1]*scaleFactorCover)),PIL.Image.ANTIALIAS)
    pilProfileImage = pilProfileImageBase.crop((position[0],position[1],200+position[0],200+position[1]))
    pilThumbnail = pilProfileImage.copy()
    pilProfileImageSmall = pilProfileImage.copy()
    pilProfileImageSmall.thumbnail((settings.PROFILE_IMAGE_SMALL_DIMENSIONS[0],settings.PROFILE_IMAGE_SMALL_DIMENSIONS[1]),PIL.Image.ANTIALIAS)
    pilThumbnail.thumbnail((settings.PROFILE_IMAGE_THUMBNAIL_DIMENSIONS[0],settings.PROFILE_IMAGE_THUMBNAIL_DIMENSIONS[1]),PIL.Image.ANTIALIAS)

    profileImageBase = create_derived_image(image,pilProfileImageBase,"base")
    profileImageCover = create_derived_image(profileImageBase,pilProfileImageCover,"cover")
    profileImage = create_derived_image(profileImageBase,pilProfileImage,"profile_image")
    profileImageThumbnail = create_derived_image(profileImageBase,pilThumbnail,"thumbnail")
    profileImageSmall = create_derived_image(profileImageBase,pilProfileImageSmall,"small_version")
    
    return (profileImage,profileImageCover,profileImageSmall,profileImageThumbnail)
