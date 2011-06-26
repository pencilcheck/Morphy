from glob import glob
from os.path import splitext
import Image
import math

import os

import tornado.ioloop
import tornado.web

import pprint
pp = pprint.PrettyPrinter(indent=4)

import final

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("static/index.html")

    def post(self):
        print self.request.arguments
        lines = []
	if 'lines' in self.request.arguments:
		for x in self.request.arguments['lines'][0].split():
		    tmp = x.split(',')
		    line = [[float(tmp[0]), float(tmp[1])], [float(tmp[2]), float(tmp[3])]]
		    lines.append(line)
		#print lines

        rlines = []
	if 'rlines' in self.request.arguments:
		for x in self.request.arguments['rlines'][0].split():
		    tmp = x.split(',')
		    rline = [[float(tmp[0]), float(tmp[1])], [float(tmp[2]), float(tmp[3])]]
		    rlines.append(rline)

        #print rlines

        out = final.inputImage(self.request.arguments['left'][0], self.request.arguments['right'][0], lines, rlines, 0.5, 1, 1, 2)
        #out.save('test.jpg', quality = 100)
        #jpg_temp = splitext(jpg1)[0]+"_Resized1.jpg"
        #nim.save(jpg_temp, quality = 100)


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

