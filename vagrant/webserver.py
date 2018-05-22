from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_Setup import Restaurant, Base, MenuItem
import re

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        session = DBSession()
        try:
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Rename the restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' 
                           action='''''+self.path+''' '><h2>Name of the Restaurant?</h2><input name="message" type="text" >
                           <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete this restaurant?</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' 
                                          action=''''' + self.path + ''' '><h2>
                                          <input type="submit" value="yes"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a new Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' 
                action='/restaurants/new'><h2>Name of the Restaurant?</h2><input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants around you</h1> <h2><a href='/restaurants/new'>Add a new restaurant</a></h2>"
                result=session.query(Restaurant)
                for restaurants in result:
                    output+="<p>"+restaurants.name+"<br> <a href='/%s/edit'>edit</a>" %str(restaurants.id)
                    output+="<br> <a href='%s/delete'>delete</a> </p>"%str(restaurants.id)

                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        session = DBSession()
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Location', "/restaurants")
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    restaurant=Restaurant(name=messagecontent[0])
                    session.add(restaurant)
                    session.commit()
            if self.path.endswith("/edit"):
                identifier=re.findall(r'\d+',self.path)
                self.send_response(301)
                self.send_header('Location', "/restaurants")
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    restaurant=session.query(Restaurant).filter_by(id=identifier[0]).one()
                    restaurant.name=messagecontent[0]
                    session.add(restaurant)
                    session.commit()
            if self.path.endswith("/delete"):
                identifier = re.findall(r'\d+', self.path)
                self.send_response(301)
                self.send_header('Location', "/restaurants")
                self.end_headers()
                restaurant = session.query(Restaurant).filter_by(id=identifier[0]).one()
                session.delete(restaurant)
                session.commit()
                return

        except IOError as e:
            print(e)



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()