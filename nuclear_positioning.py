import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("C:/Users/Casperr/PycharmProjects/tahaProje/pic2.png", cv2.IMREAD_COLOR)

# This function takes img as an input and determines the coordinates of every pixel and gives coordinates.
def img_coordinator():

    row_counter = -1
    column_counter = -1
    location = []
    nuclei_list = []
    border_list = []
    for row in img:
        column_counter = -1
        row_counter += 1

        for column in row:

            column_counter += 1
            location.append(row_counter)
            location.append(column_counter)



            B = column[0]
            G = column[1]
            R  = column[2]


            if B >= 250 and G <= 50 and R <= 50:

                border_list.append(location)


            elif R >= 250 and G <= 10 and B <= 10 :
                nuclei_list.append(location)

            location = []

    return border_list, nuclei_list


def area_calculator():
    sum_list = {}
    for coordinate in border_list:
        sum = 0
        sum = coordinate[0] + coordinate[1]
        sum_list[sum] = coordinate

    A = sum_list[min(sum_list)]
    C = sum_list[max(sum_list)]

    for elem in sum_list:
        if elem != min(sum_list) and elem != max(sum_list):
            B = sum_list[elem]
            Belem = elem

    for elem in sum_list:
        if elem != min(sum_list) and elem != max(sum_list) and elem != Belem:
            D = sum_list[elem]

    Area = 0.5 * abs( (A[0] * B[1] + B[0] * C[1] + C[0] * D[1] + D[0] * A[1]) - (A[1] * B[0] + B[1] * C[0] + C[1] * D[0] + D[1] * A[0]))

    borders = [A,B,C,D]
    return Area, borders


def avg_distance_calculator():
    nuclei_list.sort()
    counter = 0
    distance = 0
    distlist = []


    for nucleus in nuclei_list :
        if counter < len(nuclei_list) - 1:
            distance = math.sqrt(pow(nuclei_list[counter][0]-nuclei_list[counter+1][0],2)+pow(nuclei_list[counter][1]-nuclei_list[counter+1][1],2))
            distlist.append(distance)
            distance = 0
            counter = counter + 1

    sum = 0
    for distance in distlist:
        sum = sum + distance

    avg = sum/len(distlist)

    return distlist, avg


def min_max_dist_calculator():
    nuclei_list.sort()
    for nucleus in nuclei_list:
        min_dist = min(distlist)
        max_dist = max(distlist)

    return min_dist, max_dist


def image_drawer():
    # Drawing borders of the specified muscle

    cv2.line(img, [borders[0][1],borders[0][0]], [borders[1][1],borders[1][0]], (255,0,255), 2)
    cv2.line(img, [borders[1][1], borders[1][0]], [borders[2][1], borders[2][0]], (0,255,255), 2)
    cv2.line(img, [borders[2][1], borders[2][0]], [borders[3][1], borders[3][0]], (255,255,255), 2)
    cv2.line(img, [borders[3][1], borders[3][0]], [borders[0][1], borders[0][0]], (255,255,255), 2)
    # Drawing lines between nuclei
    counter = 0
    for nucleus in nuclei_list:
        if counter < len(nuclei_list) - 1:
            cv2.line(img, [nuclei_list[counter][1], nuclei_list[counter][0]], [nuclei_list[counter+1][1], nuclei_list[counter+1][0]], (255, 255, 0), 2)
            counter = counter + 1

    # Drawing centers of nuclei
    for nucleus in nuclei_list:
        cv2.circle(img, [nucleus[1], nucleus[0]], 2, (255,255,255), 2)

    # Drawing min distance.
    dict = {}
    counter2 = 0
    for nucleus in nuclei_list:
        if counter2 < len(nuclei_list) - 1:


            dict[distlist[counter2]] = [nuclei_list[counter2], nuclei_list[counter2+1]]

            counter2 = counter2 + 1


    for distance in distlist:
        if distance == min_dist:
            cv2.line(img, [dict[distance][0][1],dict[distance][0][0]],[dict[distance][1][1],dict[distance][1][0]], (255, 50, 50), 2)
        if distance == max_dist:
            cv2.line(img, [dict[distance][0][1],dict[distance][0][0]],[dict[distance][1][1],dict[distance][1][0]], (0, 0, 255), 2)





def nucleiToBorderDists():
    distList = []

    nucleus = nuclei_list[5]

    for i in range(4):
            pt1 = borders[i]
            if i+1 == 4:
                pt2 = borders[0]
            else:
                pt2 = borders[i+1]

            pt1x = pt1[0]
            pt1y = 1023-pt1[1]
            pt2x = pt2[0]
            pt2y = 1023-pt2[1]
            nucleusx = nucleus[0]
            nucleusy = 1023-nucleus[1]

            slope = (pt1y-pt2y) / (pt1x-pt2x)
            alpha = pt2y - slope * pt2x
            beta = nucleusy + (nucleusx / slope)

            intersectionX = int((beta-alpha) / (slope + (1/slope)))
            intersectionY = int(slope * intersectionX + alpha)

            distance = math.sqrt(((intersectionY - nucleusy)**2) + ((intersectionX - nucleusx)**2))
            distList.append(distance)

            cv2.line(img,[nucleusx,nucleusy],[intersectionY,intersectionX],(0,200,200),2)



def image_texter():
    print("A")
    muscle_area = round(Area * 0.63* 0.63,2)
    cv2.putText(img, f"Muscle Area = {muscle_area} um^2", (10, 760), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2,
                cv2.LINE_AA)
    print("b")
    cv2.putText(img, f"Average distance between neighbor nuclei = {round(avg_dist_neighbor*0.63,2)} um (normaliazed: {round((avg_dist_neighbor*0.63)/math.sqrt(muscle_area),4)})", (10, 780), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 2,
                cv2.LINE_AA)
    cv2.putText(img,
                f"Number of nuclei = {len(nuclei_list)}",(10, 800), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(img,
                f"Minimum Distance between neighbor nuclei = {round(min_dist*0.63,2)} um (normalized: {round((min_dist*0.63)/math.sqrt(muscle_area),4)})", (10, 740), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 50, 50), 2,
                cv2.LINE_AA)
    cv2.putText(img,
                f"Maximum Distance between neighbor nuclei = {round(max_dist * 0.63, 2)} um (normalized: {round((max_dist * 0.63) / math.sqrt(muscle_area), 4)})",
                (10, 820), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0, 255), 2,
                cv2.LINE_AA)

border_list, nuclei_list = img_coordinator()
Area, borders = area_calculator()
distlist, avg_dist_neighbor = avg_distance_calculator()
min_dist, max_dist = min_max_dist_calculator()
image_drawer()
image_texter()
nucleiToBorderDists()


cv2.imshow('NMJ',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
