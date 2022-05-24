import staticmaps
import cv2
import numpy as np
import os
import random as rng

rng.seed(12345)

context = staticmaps.Context()

center1 = staticmaps.create_latlng(55.578100, 42.052772)
context.set_center(center1)
context.set_zoom(17)

size = (1000, 1000)
context.set_tile_provider(staticmaps.tile_provider_CartoNoLabels)
img1 = context.render_pillow(size[0], size[1])

context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery)
img2 = context.render_pillow(size[0], size[1])
# displayPair(img1, img2)

cxtCarto = staticmaps.Context()
cxtCarto.set_tile_provider(staticmaps.tile_provider_CartoNoLabels)

cxtImagry = staticmaps.Context()
cxtImagry.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery)

size = (500, 515)


def getCartoTile(center, zoom, size):
    cxtCarto.set_center(center)
    cxtCarto.set_zoom(zoom)
    return cxtCarto.render_pillow(size[0], size[1])


def getImagryTile(center, zoom, size):
    cxtImagry.set_center(center)
    cxtImagry.set_zoom(zoom)
    return cxtImagry.render_pillow(size[0], size[1])



def getBuildings(img):
    sourceColor = np.array(img)[:-15,:]
    layers = cv2.split(sourceColor)
    imgnp = layers[1]

    _,imgnp = cv2.threshold(imgnp, 238, 255, cv2.THRESH_BINARY_INV)

    imgnp_med = cv2.medianBlur(imgnp, 5)
    imgnp = cv2.bitwise_and(imgnp_med, imgnp)

    contours, _ = cv2.findContours(imgnp, cv2.RETR_LIST, cv2.LINE_4)

    drawing = np.zeros_like(imgnp)
    for cnt in contours:
        M = cv2.moments(cnt)
        if M['m00'] == 0:
            continue

        if cv2.contourArea(cnt) < cv2.arcLength(cnt,True):
            continue

        cv2.drawContours(drawing, [cnt], 0, (255), cv2.FILLED)

    drawing = cv2.bitwise_and(imgnp, drawing)

    return drawing

# def getBuildingsLine(img):
#     sourceColor = np.array(img)[:-15,:]
#     layers = cv2.split(sourceColor)
#     imgnp = layers[1]

#     _,imgnp = cv2.threshold(imgnp, 238, 255, cv2.THRESH_BINARY_INV)

#     imgnp_med = cv2.medianBlur(imgnp, 5)
#     imgnp = cv2.bitwise_and(imgnp_med, imgnp)

#     contours, _ = cv2.findContours(imgnp, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#     for count in contours:
#         epsilon = 0.01 * cv2.arcLength(count, True)
#         approximations = cv2.approxPolyDP(count, epsilon, True)
#         st = '4rfd'

#     drawing = np.zeros_like(imgnp)
#     for cnt in contours:
#         M = cv2.moments(cnt)
#         if M['m00'] == 0:
#             continue

#         if cv2.contourArea(cnt) < cv2.arcLength(cnt,True):
#             continue

#         cv2.drawContours(drawing, [cnt], 0, (255), cv2.LINE_4)

#     drawing = cv2.bitwise_and(imgnp, drawing)

#     return drawing

def createImages():

    dir = os.path.dirname(__file__)
    dir = os.path.join(dir,'tiles4/')

    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    k = 0
    with open('coords.txt', 'r') as fileparams:
        for line in fileparams:
            if len(line) == 0 or line[0] == '#':
                continue

            prm = line.split('|')
            if len(prm) != 3:
                continue

            print(line)
            center = staticmaps.create_latlng(float(prm[0]), float(prm[1]))
            zoom = int(prm[2])

            img1 = getImagryTile(center, zoom, size)
            img2 = getCartoTile(center, zoom, size)
            img3 = getBuildings(img2)
            img4 = cv2.copyMakeBorder(img3, 20, 20, 20, 20, cv2.BORDER_CONSTANT)
            #img5 = cv2.copyMakeBorder(img2, 20, 20, 20, 20, cv2.BORDER_CONSTANT)

            img1 = np.array(img1)[:-15,:]
            cv2.imwrite(os.path.join(dir, str(k) + '_set.png'), img1)
          #  img2.save(os.path.join(dir, str(k) + '_sgd.png'))
            # cv2.imwrite(os.path.join(dir, '1_cat.png'), img2)
            cv2.imwrite(os.path.join(dir, str(k) + '_bld.png'), img3)
            cv2.imwrite(os.path.join(dir, str(k) + '_contr.png'), img4)
            #cv2.imwrite(os.path.join(dir, str(k) + '_setGr.png'), img5)
            k += 1

hsv_min = np.array((2, 28, 65), np.uint8)
hsv_max = np.array((26, 238, 255), np.uint8)
createImages()
