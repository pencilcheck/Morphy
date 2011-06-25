'''
    input parameters:

    src image[m1 x n1] * 1
    des image[m2 x n2] * 1
    
    src lines * n
    des lines * n

    t -> time
    p -> for warp
    a -> for warp
    b -> for warp

                (LineLength ^ p)   b
    weight =  [ ---------------- ]      , where "dist" is the distance from the corresponding point to the line
                   (a + dist)             and "LineLength" is the length of new corresponding line

    output:

    out image[m1?m2 x n1?n2] * 1

'''

from glob import glob
from os.path import splitext
import Image
import math

def inputImage (jpg1, jpg2, LineSrc):
    # open a graph and print its information
    im1 = Image.open(jpg1)
    im2 = Image.open(jpg2)
    
    # --- declare the new IMAGE width and height ---
    if int(im1.size[0]) > int(im2.size[0]) :
        tempSizeX = int(im1.size[0])
    else :
        tempSizeX = int(im2.size[0])
    if int(im1.size[1]) > int(im2.size[1]) :
        tempSizeY = int(im1.size[1])
    else :
        tempSizeY = int(im2.size[1])
    
    newX = tempSizeX
    newY = tempSizeY
    
    #print newX, newY
    
    # --- new object ---
    nim1 = Image.new(im1.mode, [im1.size[0], im1.size[1]], None)
    nim2 = Image.new(im2.mode, [im2.size[0], im2.size[1]], None)
    nim  = Image.new(im1.mode, [newX       , newY       ], None)
    #print nim.mode, nim.size, nim.format
    
    # --- load model ---
    ipixel1 = im1.load()
    ipixel2 = im2.load()
    opixel1 = nim1.load()
    opixel2 = nim2.load()
    opixel  = nim.load()
    
    # --- set the width and height ---
    w2 = nim.size[0]
    h2 = nim.size[1]

    # --- parameters ---
    n = 4
    t = 0.5
    p = 0
    a = 1
    b = 2

    # read
    #LineSrc = [[[50 ,50 ], [30 ,80 ]], \
    #           [[30 ,80 ], [50 ,110]], \
    #           [[50 ,110], [80 ,80 ]], \
    #           [[80 ,80 ], [50 ,50 ]]]
    LineDes = [[[60 ,60 ], [20 ,100]], \
               [[20 ,100], [60 ,140]], \
               [[60 ,140], [100,100]], \
               [[100,100], [60 ,60 ]]]

    Line = [[[0,0],[0,0]], \
            [[0,0],[0,0]], \
            [[0,0],[0,0]], \
            [[0,0],[0,0]]]

    # ---------- interpolation ----------
    for i in range(0,n): # t -> time
        Line[i][0][0] = (1-t) * LineSrc[i][0][0] + t * LineDes[i][0][0]  # LinePX
        Line[i][0][1] = (1-t) * LineSrc[i][0][1] + t * LineDes[i][0][1]  # LinePY
        Line[i][1][0] = (1-t) * LineSrc[i][1][0] + t * LineDes[i][1][0]  # LineQX
        Line[i][1][1] = (1-t) * LineSrc[i][1][1] + t * LineDes[i][1][1]  # LineQY

    #print Line[i][0][0], Line[i][0][1], Line[i][1][0], Line[i][1][1]

    # ---------- warp ----------
    for x in range(0,newX):
        for y in range(0,newY):
    
            # ---------- Source ----------
            sum_x     = 0
            sum_y     = 0
            weightSum = 0
        
            for i in range(0,n):
                # x,y to Line
                xSrc = x - Line[i][0][0] # pd.x
                ySrc = y - Line[i][0][1] # pd.y

                # length
                xDis = Line[i][1][0] - Line[i][0][0] # pq.x
                yDis = Line[i][1][1] - Line[i][0][1] # pq.y
    
                # u and v
                LineLength = xDis * xDis + yDis * yDis
                u = (xSrc * xDis + ySrc * yDis) / LineLength # pd.x * pq.x + pd.y * pq.y

                LineLength = pow(LineLength, 0.5)
                v = (xSrc * yDis - ySrc * xDis) / LineLength # pd.x * pq.y - pd.y * pq.x

                # Src Length
                xDis = LineSrc[i][1][0] - LineSrc[i][0][0] # pq.x
                yDis = LineSrc[i][1][1] - LineSrc[i][0][1] # pq.y

                SrcLength = xDis * xDis + yDis * yDis
                SrcLength = pow(SrcLength, 0.5)

                # corresponding point based on the ith line
                X = LineSrc[i][0][0] + u * xDis + v * yDis / SrcLength
                Y = LineSrc[i][0][1] + u * yDis - v * xDis / SrcLength

                # the distance from the corresponding point to the line
                if   u < 0 :
                    dist = xSrc * xSrc + ySrc * ySrc
                    dist = pow(dist, 0.5)
                elif u > 1 :
                    xSrc = x - Line[i][1][0]
                    ySrc = y - Line[i][1][1]
                    dist = xSrc * xSrc + ySrc * ySrc
                    dist = pow(dist, 0.5)
                else :
                    dist = abs(v)

                # weight
                weight = pow(pow(LineLength, p) / (a + dist), b)
                sum_x += X * weight
                sum_y += Y * weight
                weightSum += weight

            # the final point coordination of source
            xFinalSrc = sum_x / weightSum
            yFinalSrc = sum_y / weightSum

            # ---------- adjust ----------
            if xFinalSrc < 0:
               xFinalSrc = 0
            if xFinalSrc > im1.size[0]-2:
               xFinalSrc = im1.size[0]-2
            if yFinalSrc < 0:
               yFinalSrc = 0
            if yFinalSrc > im1.size[1]-2:
               yFinalSrc = im1.size[1]-2

            #print xFinalSrc, yFinalSrc
           
            # ---------- bilinear interpolation ----------
            # left-top
            x_temp = int(xFinalSrc)
            y_temp = int(yFinalSrc)

            # distance
            w = xFinalSrc - x_temp
            h = yFinalSrc - y_temp

            # extract the neighbor tuples
            A = ipixel1[x_temp  , y_temp]
            B = ipixel1[x_temp+1, y_temp]
            C = ipixel1[x_temp  , y_temp+1]
            D = ipixel1[x_temp+1, y_temp+1]

            # update three colors
            Red   = (int)(A[0]*(1-w)*(1-h) + B[0]*(w)*(1-h) + \
                          C[0]*(1-w)*(h)   + D[0]*(w)*(h))
            Green = (int)(A[1]*(1-w)*(1-h) + B[1]*(w)*(1-h) + \
                          C[1]*(1-w)*(h)   + D[1]*(w)*(h))
            Blue  = (int)(A[2]*(1-w)*(1-h) + B[2]*(w)*(1-h) + \
                          C[2]*(1-w)*(h)   + D[2]*(w)*(h))

            # update the pixel
            opixel1[xFinalSrc, yFinalSrc] = (Red, Green, Blue)

            # ---------- Destination ----------
            sum_x     = 0
            sum_y     = 0
            weightSum = 0
        
            for i in range(0,n):
                # x,y to Line
                xDes = x - Line[i][0][0] # pd.x
                yDes = y - Line[i][0][1] # pd.y

                # length
                xDis = Line[i][1][0] - Line[i][0][0] # pq.x
                yDis = Line[i][1][1] - Line[i][0][1] # pq.y
                
                # u and v
                LineLength = xDis * xDis + yDis * yDis
                u = (xDes * xDis + yDes * yDis) / LineLength # pd.x * pq.x + pd.y * pq.y
            
                LineLength = pow(LineLength, 0.5)
                v = (xDes * yDis - yDes * xDis) / LineLength # pd.x * pq.y - pd.y * pq.x

                # Des Length
                xDis = LineDes[i][1][0] - LineDes[i][0][0] # pq.x
                yDis = LineDes[i][1][1] - LineDes[i][0][1] # pq.y
    
                DesLength = xDis * xDis + yDis * yDis
                DesLength = pow(DesLength, 0.5)
    
                # corresponding point based on the ith line
                X = LineDes[i][0][0] + u * xDis + v * yDis / DesLength
                Y = LineDes[i][0][1] + u * yDis - v * xDis / DesLength

                #print X,Y

                # the distance from the corresponding point to the line
                if   u < 0 :
                    dist = xDes * xDes + yDes * yDes
                    dist = pow(dist, 0.5)
                elif u > 1 :
                    xDes = x - Line[i][1][0]
                    yDes = y - Line[i][1][1]
                    dist = xDes * xDes + yDes * yDes
                    dist = pow(dist, 0.5)
                else :
                    dist = abs(v)

                # weight
                weight = pow(pow(LineLength, p) / (a + dist), b)
                sum_x += X * weight
                sum_y += Y * weight
                weightSum += weight
    
            # the final point coordination of destination
            xFinalDes = sum_x / weightSum
            yFinalDes = sum_y / weightSum
                   
            # ---------- adjust ----------
            if xFinalDes < 0:
               xFinalDes = 0
            if xFinalDes > im2.size[0]-2:
               xFinalDes = im2.size[0]-2
            if yFinalDes < 0:
               yFinalDes = 0
            if yFinalDes > im2.size[1]-2:
               yFinalDes = im2.size[1]-2

            # ---------- bilinear interpolation ----------
            # left-top
            x_temp = int(xFinalDes)
            y_temp = int(yFinalDes)

            # distance
            w = xFinalDes - x_temp
            h = yFinalDes - y_temp

            # extract the neighbor tuples
            A = ipixel2[x_temp  , y_temp]
            B = ipixel2[x_temp+1, y_temp]
            C = ipixel2[x_temp  , y_temp+1]
            D = ipixel2[x_temp+1, y_temp+1]

            # update three colors
            Red   = (int)(A[0]*(1-w)*(1-h) + B[0]*(w)*(1-h) + \
                          C[0]*(1-w)*(h)   + D[0]*(w)*(h))
            Green = (int)(A[1]*(1-w)*(1-h) + B[1]*(w)*(1-h) + \
                          C[1]*(1-w)*(h)   + D[1]*(w)*(h))
            Blue  = (int)(A[2]*(1-w)*(1-h) + B[2]*(w)*(1-h) + \
                          C[2]*(1-w)*(h)   + D[2]*(w)*(h))

            # update the pixel
            opixel2[xFinalDes,yFinalDes] = (Red, Green, Blue)

            # ---------- colorinterpolation ----------
            Finalopixel_R = int((1-t) * opixel1[xFinalSrc,yFinalSrc][0] + t * opixel2[xFinalDes,yFinalDes][0])
            Finalopixel_G = int((1-t) * opixel1[xFinalSrc,yFinalSrc][1] + t * opixel2[xFinalDes,yFinalDes][1])
            Finalopixel_B = int((1-t) * opixel1[xFinalSrc,yFinalSrc][2] + t * opixel2[xFinalDes,yFinalDes][2])

            # ---------- assign to new IMAGE ----------
            opixel[x,y] = (Finalopixel_R, Finalopixel_G, Finalopixel_B)

            # ---------- end for new IMAGE ----------

    return nim


    
    


