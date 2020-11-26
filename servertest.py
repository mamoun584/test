# Khaldoon esmail/0990715 - Raspberry pi /

import matplotlib.pyplot as plt
import sqlite3
import time
import numpy as np
import zmq
dfdfdgdgggffg
dggrrhgrhrgg
tijd = time.ctime()
situatie =""
db = sqlite3.connect("database.db")
db.execute("CREATE TABLE IF NOT EXISTS data (distance Real , tijd text,situatie text )") #, temp Real, Humindity Real

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
plot_window = 20
y_var = np.array(np.zeros([plot_window]))
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(y_var)

while True:
    #  wacht op een singal van de client
    distance = socket.recv_json()
    socket.send_json("Is goed")
    print("de distans is: %s" %distance)
    distance_filter = 20
    if distance < distance_filter:
        situatie= 'De afvalpak is vol'
        db.execute("insert into data( distance  ,tijd , situatie ) values (? , ? ,?)", (distance, tijd, situatie))
        db.commit()
    else:
        situatie = 'De prullenpak is bijna vol'
        db.execute("insert into data( distance  ,tijd , situatie ) values (? , ? ,?)", (distance, tijd, situatie))
    time.sleep(1)
    y_var = np.append(y_var, float(distance))
    y_var = y_var[1:plot_window + 1]
    line.set_ydata(y_var)
    ax.relim()
    ax.autoscale_view()
    plt.xlabel('time (s)')
    plt.ylabel('situatie')
    fig.canvas.draw()
    fig.canvas.flush_events()
