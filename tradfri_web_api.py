

from flask import Flask, render_template
from tradfri_server_03 import Tradfri_conn
import json


app = Flask(__name__)

@app.route("/")
def index():
    return "trad api"


@app.route("/render_light_data")
def render_light_data():
    return render_template('/hate_my_life.html')


@app.route("/update_lights")
def update_lights():

   # initialize Gateway connection
    trad_conn = Tradfri_conn("192.168.222.104")



    light_dict = {}
    lights = trad_conn.lights

    i = 0
    while i < len(lights):
        name = trad_conn.get_light_name(i)
        status = trad_conn.get_status(i)
        dimmer_status = trad_conn.get_dimmer_status(i)

        light_dict[name] = {
            'status'        : status,
            'dimmer_status' : dimmer_status,
            'light_index'   : i
        }
        i+=1

    json_data = json.dumps(light_dict)
    return json_data


@app.route("/set_brightness/<light_index>/<level>")
def set_brightness(light_index, level):

    # initialize Gateway connection
    trad_conn = Tradfri_conn("192.168.222.104")

    trad_conn.set_brightness(int(light_index), int(level))

    return '200'





@app.route("/set_hex_color/<light_index>/<hex_color>")
def set_hex_color(light_index, hex_color):


    # initialize Gateway connection
    trad_conn = Tradfri_conn("192.168.222.104")

    trad_conn.set_hex_color(int(light_index), hex_color)

    return '200'



@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response

if __name__ == "__main__":
    app.run(debug=True)
