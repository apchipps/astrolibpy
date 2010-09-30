# Copyright (C) 2010 Sergey Koposov
# This file is part of astrolibpy
#
#    astrolibpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#   astrolibpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with astrolibpy.  If not, see <http://www.gnu.org/licenses/>.

from matplotlib.widgets import Lasso
from matplotlib.nxutils import points_inside_poly
from matplotlib.pyplot import gca
from numpy import nonzero

class lasso_plot:
    """ The class is designed to select the datapoints by drawing the region
    around it. 
    Example:
    plot(xs, ys, ps=3 ) # first plot the data
    las = lasso_plot.lasso_plot(xs,ys)
    Now click on the plot and do not release the mouse button till 
    you draw your region 
    After that the variable las.ind will contain the indices of those 
    points inside the region and las.verts will contain the vertices of the 
    polygon you've just drawn """
    def __init__(self, xs, ys):
        self.axes = gca()
        self.canvas = self.axes.figure.canvas
        self.xys = [d for d in zip(xs,ys)]
        fig = self.axes.figure
        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        self.ind = None
        self.mask = None
        self.verts = None

    def callback(self, verts):
        mask = points_inside_poly(self.xys, verts)
        ind = nonzero(mask)[0]
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        del self.lasso
        del self.xys
        self.verts = verts
        self.ind = ind
        self.mask = mask

    def inside(self, xs,ys):
        tmpxys = zip(xs,ys)
        return points_inside_poly(tmpxys, self.verts)

    def onpress(self, event):
        if self.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)

