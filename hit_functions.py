def in_polygon(x, y, tpx, tpy):
    c = 0
    for i in range(len(tpx)):
        if ((tpy[i] <= y < tpy[i - 1]) or (tpy[i - 1] <= y < tpy[i])) \
                and (x > (tpx[i - 1] - tpx[i]) * (y - tpy[i]) / (tpy[i - 1] - tpy[i]) + tpx[i]):
            c = 1 - c
    if c == 1:
        return True   


def objects_hit(f1, f2):
    xc = (f1.pos.x * f1.m + f2.pos.x * f2.m) / (f1.m + f2.m)
    yc = (f1.pos.y * f1.m + f2.pos.y * f2.m) / (f1.m + f2.m)
    k = (f1.r + f2.r) / ((f1.pos.x - f2.pos.x) ** 2 + (f1.pos.y - f2.pos.y) ** 2) ** 0.5
    f1.pos.x = xc + (f1.pos.x - xc) * k
    f1.pos.y = yc + (f1.pos.y - yc) * k
    f2.pos.x = xc + (f2.pos.x - xc) * k
    f2.pos.y = yc + (f2.pos.y - yc) * k
    x = f2.pos.x - f1.pos.x
    y = f2.pos.y - f1.pos.y
    p = (2 / (f1.m + f2.m)) * ((f2.vx - f1.vx) * x + (f2.vy - f1.vy) * y) / (x**2 + y**2)
    f1.vx += p * f2.m * x
    f1.vy += p * f2.m * y
    f2.vx -= p * f1.m * x
    f2.vy -= p * f1.m * y

def food_hit(arr_food_to_render):
    for i in range(len(arr_food_to_render) - 1):
        for j in range(i + 1, len(arr_food_to_render)):
            f1 = arr_food_to_render[i]
            f2 = arr_food_to_render[j]
            if ((f1.pos.x - f2.pos.x) ** 2 + (f1.pos.y - f2.pos.y) ** 2) <= (f1.r + f2.r) ** 2:
                objects_hit(f1, f2)


if __name__ == "__main__":
    print("This module is not for direct call!")