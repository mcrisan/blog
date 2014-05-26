from flask.ext.script import Manager
from flask.ext.script import Command
from main import app

manager = Manager(app)

@manager.command
def hello(name="Ion"):
    print "hello", name
    
class Hello(Command):
    "prints hello world"

    def run(self):
        print "hello2 world"

@manager.option('-n', '--name', help='Your name')
def hello3(name):
    print "hello", name        
        
manager.add_command('hello2', Hello())            

if __name__ == "__main__":
    manager.run()