"""
Danish Waheed
CAP5415 - Fall 2017

This Python program is the supporting library for Q1 and Q2
"""

import numpy as np
import cv2
import math

# This sets the program to ignore a divide error which does not affect the outcome of the program
np.seterr(divide='ignore', invalid='ignore')

'''
TODO: Add comments for this method
'''
def reduce(image, level=1):
    result = np.copy(image)

    for _ in range(level - 1):
        result = cv2.pyrDown(result)

    return result


'''
TODO: Add comments for this method
'''
def expand(image, level=1):
    return cv2.pyrUp(np.copy(image))


'''
TODO: Add comments for this method
'''
def compute_flow_map(u, v, gran=8):
    flow_map = np.zeros(u.shape)

    for y in range(flow_map.shape[0]):
        for x in range(flow_map.shape[1]):

            if y % gran == 0 and x % gran == 0:
                dx = 10 * int(u[y, x])
                dy = 10 * int(v[y, x])
                length = float(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))
                scalar = 10

                if ((abs(dx) > 0) or (abs(dy) > 0)):
                    try:
                        cv2.arrowedLine(flow_map, (x, y), (x + scalar*int(dx/length), y + scalar*int(dy/length)), 255, 1)
                        if(dx < 0):
                            print("dx is negative at (%s, %s). Phase: %s" % (y, x, float(math.atan(dy/dx))))
                        if(dy < 0):
                            print("dy is negative at (%s, %s. Phase: %s" % (y, x, float(math.atan(dy/dx))))
                    except:
                        continue

    return flow_map

def compute_heat_map(u, v, gran=8):
    heat_map = np.zeros(u.shape)

    for y in range(heat_map.shape[0]):
        for x in range(heat_map.shape[1]):

            if y % gran == 0 and x % gran == 0:
                dx = 10 * int(u[y, x])
                dy = 10 * int(v[y, x])
                length = float(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))
                scalar = 10

                if ((abs(dx) > 0) or (abs(dy) > 0)):
                    try:
                        heat_map[y, x] = math.atan(dy/dx) * int(128/(math.pi)) + 128
                    except:
                        continue

    return heat_map

def compute_phase_map(u, v, gran=8):
    phase_map = np.zeros((u.shape[0], u.shape[1], 3), np.uint8)

    for y in range(phase_map.shape[0]):
        for x in range(phase_map.shape[1]):

            if y % gran == 0 and x % gran == 0:
                dx = 10 * int(u[y, x])
                dy = 10 * int(v[y, x])
                blue_comp = 0
                if ((abs(dx) > 0) or (abs(dy) > 0)):
                    try:
                        phase = math.atan(dy/dx)
                        cos = math.cos(phase)
                        sin = math.sin(phase)
                        if((dx < 0) or (dy < 0)):
                            blue_comp = 255
                        phase_map[y, x] = (blue_comp, 127*sin + 128, 127*cos + 128)
                    except:
                        continue
    return phase_map

'''
TODO: Add comments for this method
'''
def lucas_kanade(im1, im2, win=3):
    assert im1.shape == im2.shape
    I_x = np.zeros(im1.shape)
    I_y = np.zeros(im1.shape)
    I_t = np.zeros(im1.shape)
    I_x[1:-1, 1:-1] = (im1[1:-1, 2:] - im1[1:-1, :-2]) / 2
    I_y[1:-1, 1:-1] = (im1[2:, 1:-1] - im1[:-2, 1:-1]) / 2
    I_t[1:-1, 1:-1] = im1[1:-1, 1:-1] - im2[1:-1, 1:-1]
    params = np.zeros(im1.shape + (5,)) #Ix2, Iy2, Ixy, Ixt, Iyt
    params[..., 0] = I_x * I_x # I_x2
    params[..., 1] = I_y * I_y # I_y2
    params[..., 2] = I_x * I_y # I_xy
    params[..., 3] = I_x * I_t # I_xt
    params[..., 4] = I_y * I_t # I_yt
    del I_x, I_y, I_t
    cum_params = np.cumsum(np.cumsum(params, axis=0), axis=1)
    del params
    win_params = (cum_params[2 * win + 1:, 2 * win + 1:] -
                  cum_params[2 * win + 1:, :-1 - 2 * win] -
                  cum_params[:-1 - 2 * win, 2 * win + 1:] +
                  cum_params[:-1 - 2 * win, :-1 - 2 * win])
    del cum_params
    det = win_params[...,0] * win_params[..., 1] - win_params[..., 2] **2
    op_flow_x = np.where(det != 0,
                         (win_params[..., 1] * win_params[..., 3] -
                          win_params[..., 2] * win_params[..., 4]) / det,
                         0)
    op_flow_y = np.where(det != 0,
                         (win_params[..., 0] * win_params[..., 4] -
                          win_params[..., 2] * win_params[..., 3]) / det,
                         0)
    return op_flow_x, op_flow_y

    # Ix = np.zeros(im1.shape)
    # Iy = np.zeros(im1.shape)
    # It = np.zeros(im1.shape)

    # Ix[1:-1, 1:-1] = (im1[1:-1, 2:] - im1[1:-1, :-2]) / 2
    # Iy[1:-1, 1:-1] = (im1[2:, 1:-1] - im1[:-2, 1:-1]) / 2
    # It[1:-1, 1:-1] = im1[1:-1, 1:-1] - im2[1:-1, 1:-1]

    # params = np.zeros(im1.shape + (5,))
    # params[..., 0] = cv2.GaussianBlur(Ix * Ix, (5, 5), 3)
    # params[..., 1] = cv2.GaussianBlur(Iy * Iy, (5, 5), 3)
    # params[..., 2] = cv2.GaussianBlur(Ix * Iy, (5, 5), 3)
    # params[..., 3] = cv2.GaussianBlur(Ix * It, (5, 5), 3)
    # params[..., 4] = cv2.GaussianBlur(Iy * It, (5, 5), 3)

    # cum_params = np.cumsum(np.cumsum(params, axis=0), axis=1)
    # win_params = (cum_params[2 * win + 1:, 2 * win + 1:] -
    #               cum_params[2 * win + 1:, :-1 - 2 * win] -
    #               cum_params[:-1 - 2 * win, 2 * win + 1:] +
    #               cum_params[:-1 - 2 * win, :-1 - 2 * win])

    # u = np.zeros(im1.shape)
    # v = np.zeros(im1.shape)

    # Ixx = win_params[..., 0]
    # Iyy = win_params[..., 1]
    # Ixy = win_params[..., 2]
    # Ixt = -win_params[..., 3]
    # Iyt = -win_params[..., 4]

    # M_det = Ixx * Iyy - Ixy ** 2
    # temp_u = Iyy * (-Ixt) + (-Ixy) * (-Iyt)
    # temp_v = (-Ixy) * (-Ixt) + Ixx * (-Iyt)
    # op_flow_x = np.where(M_det != 0, temp_u / M_det, 0)
    # op_flow_y = np.where(M_det != 0, temp_v / M_det, 0)

    # u[win + 1: -1 - win, win + 1: -1 - win] = op_flow_x[:-1, :-1]
    # v[win + 1: -1 - win, win + 1: -1 - win] = op_flow_y[:-1, :-1]

    # return u, v