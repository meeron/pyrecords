import sys
import os
from views import BaseView, MainView, ListView, AddView
from models import Storage

if sys.version.find("3.5") < 0:
    raise NotImplementedError()
    
Storage.load()

views = {
    "MainView": MainView(),
    "ListView": ListView(),
    "AddView": AddView()
}
current_view = views["MainView"]

while(True):
    os.system("clear")    
    
    current_view.render(); 
    new_view = current_view.action(input("\nChoose: "))
    if not new_view:
        continue

    if type(new_view) is BaseView:
        break

    current_view = new_view