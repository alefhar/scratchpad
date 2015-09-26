#! /usr/bin/python3.4
#
# Simulates the Nagel-Schreckenberg model for
# a closed loop. The model has four steps:
#   1) accelerate: increase current velocity v by one
#   2) brake: reduce velocity, if v cells ahead arent empty
#   3) delay: with a certain probability brake by one
#   4) drive: move v cells forward
#
# Requires a config file called 'nasch.json' of the
# following form:
# {
#     "lane_length"  : 1000,
#     "cell_length"  : 7.5,
#     "density"      : 0.5,
#     "delay_factor" : 0.3,
#     "history"      : 10,
#     "v_max"        : 5,
#     "delta_t"      : 1,
#     "empty"        : -2,
#     "num_cars"     : 1      <- optional
# }
# The key "num_cars" is optional, if not supplied it's value
# is computed from "lane_length", "cell_length" and "density"

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.cm as cm
import numpy as np
import random as rnd
import time
import json

def accelerate(config, lane):
    # increase current velocity by one or stop at v_max:
    # v = min(v + 1, v_max)

    for c in range(config["num_cells"]):
        vel = lane[0, c]
        if vel != config["empty"]:
            lane[0, c] = min(vel + 1, config["v_max"])


def brake(config, lane):
    # decrease velocity if the v cells ahead are not empty
    # v = min(v, distance_to_next_car)

    for c in range(config["num_cells"]):
        if lane[0, c] != config["empty"]:
            empty_cells = 0
            vel = lane[0, c]
            for n in range(1, vel + 1):
                i = (c + n) % config["num_cells"]
                if lane[0, i] == config["empty"]:
                    empty_cells = empty_cells + 1
                else:
                    break

            lane[0, c] = min(vel, empty_cells)


def delay(config, lane):
    # with the probablity delay_factor reduce v by one
    # to delay acceleration or model non-constant driving speeds
    # v = v - 1, if p < delay_factor

    for c in range(config["num_cells"]):
        if lane[0, c] > 0 and rnd.random() < config["delay_factor"]:
            lane[0, c] = lane[0, c] - 1


def drive(config, lane):
    # move v cells forward

    for c in range(config["num_cells"]):
        vel = lane[0, c]
        i = (c + vel) % config["num_cells"]
        if vel > 0 and lane[1, c] != config["empty"]:
            lane[0, i] = vel
            lane[0, c] = config["empty"]


def main():
    with open('nasch.json', 'r') as f:
        config = json.load(f)

    config["num_cells"] = int(config["lane_length"] // config["cell_length"])
    config["num_cars"]  = config.get("num_cars", int(config["num_cells"] * config["density"]))
    
    lane = np.full((config["history"], config["num_cells"]), config["empty"], dtype=np.int32)

    cmap = cm.get_cmap('RdYlGn', config["v_max"] + 2)
    cmap.set_under(color='white')
    cmap.set_over(color='pink')
    norm = colors.BoundaryNorm(list(range(-1, config["v_max"] + 2)), cmap.N)

    c = config["num_cars"]
    while c > 0:
        pos = rnd.randint(0, config["num_cells"] - 1)
        vel = rnd.randint(0, config["v_max"])
        if lane[0, pos] == config["empty"]:
            lane[0, pos] = vel
            c = c - 1

    while True:
        # copy all data one line up
        for t in range(config["history"] - 1, 0, -1):
            lane[t, :] = lane[t - 1, :]
    
        # execute model steps
        accelerate(config, lane)
        brake(config, lane)
        delay(config, lane)
        drive(config, lane)

        plt.ion()
        plt.imshow(lane, interpolation='nearest', origin='lower',
            cmap=cmap, norm=norm, aspect='equal')
        plt.grid(True)
        wm = plt.get_current_fig_manager()
        wm.window.wm_geometry("1200x400+0+0")
        plt.draw()

        time.sleep(1)

if __name__ == "__main__":
  main()
