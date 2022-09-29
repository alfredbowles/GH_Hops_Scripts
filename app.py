from xmlrpc.client import boolean
from flask import Flask
import ghhops_server as hs

import numpy as np

import rhino3dm

app = Flask(__name__)
hops = hs.Hops(app)



@hops.component(
        "/pointAt",
        name="PointAt",
        description="Get point along curve",
        inputs=[
            hs.HopsCurve("Curve", "C", "Curve to evaluate"),
            hs.HopsNumber("t","t", "Parameter on Curve to evaluate", default=2.0),
        ],
        outputs=[
            hs.HopsPoint("P","P","Point on curve at t"),
        ],
)

def pointat(curve: rhino3dm.Curve , t):
    return curve.PointAt(t)

@hops.component(
        "/multiply",
        name="Multiply",
        description="Multiply 2 numbers",
        inputs=[
            hs.HopsNumber("A", "A", "First Number",default=0),
            hs.HopsNumber("B","B", "Second Number", default=0),
        ],
        outputs=[
            hs.HopsNumber("Out","Output","Output"),
        ],
)

def multiply(a: float, b: float):
    return a*b

@hops.component(
        "/contour",
        name="Contour",
        description="Contour a surface",
        inputs=[
            hs.HopsSurface("Surface","S","Surface to evaluate"),
            hs.HopsPoint("N", "N", "Number of contours",default=0),
        ],
        outputs=[
            hs.HopsCurve("Curves","C","Contour Curves new")
        ],
)


def contour(surface: rhino3dm.Surface , n: rhino3dm.Point):
    u = n.X
    v = n.Y
    curves = []
    for i in np.arange(u-0.2, u+0.21, 0.2):
        curves.append(surface.IsoCurve(0, i))

    for i in np.arange(v-0.2, v+0.21, 0.2):
        curves.append(surface.IsoCurve(1, i))

    curves.append(surface.IsoCurve(1, v))
    return curves


if __name__ == "__main__":
    app.run()