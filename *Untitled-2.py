def barycentric_out(pointXY, triangle):
    pointX = pointXY[0]
    pointY = pointXY[1]
    point1X = triangle[0][0]
    point1Y = triangle[0][1]
    point2X = triangle[1][0]
    point2Y = triangle[1][1]
    point3X = triangle[2][0]
    point3Y = triangle[2][1]
    s = ((point2X - point1X)*(point3Y - point1Y) - (point3X - point1X)*(point2Y - point1Y))/2
    s1 = ((point2X - point1X)*(pointY - point1Y) - (pointX - point1X)*(point2Y - point1Y))/2
    s2 = ((pointX - point1X)*(point3Y - point1Y) - (point3X - point1X)*(pointY - point1Y))/2
    s3 = ((point2X - pointX)*(point3Y - pointY) - (point3X - pointX)*(point2Y - pointY))/2
    u = s1/s
    v = s2/s
    w = s3/s
    coor = [u, v, w]
    return coor
[[43.41195783, 53.13140333],[41.36483497, 54.44852309],[40.24252552, 53.05242233]]
print(barycentric_out([41.61204711, 53.39903661], [[43.41195783, 53.13140333],[41.36483497, 54.44852309],[40.24252552, 53.05242233]]))