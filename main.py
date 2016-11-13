import sys
import os
import argparse
from getpass import getpass
from views import BaseView, MainView, ListView, AddView
from models import Storage

if sys.version.find("3.5") < 0:
    raise NotImplementedError()

parser = argparse.ArgumentParser()
parser.add_argument("db", help="Path to database file. If file doesn't exists it will be created.'")
args = parser.parse_args()

cnt = 0
pw = getpass()
while not Storage.load(args.db, pw):
    cnt = cnt + 1
    if cnt >= 3:
        print("Access Denied")
        exit()
    pw = getpass()

# repeat password for new db file
if Storage.is_new:
    rep_pass = getpass(prompt="Repeat Password: ")
    if rep_pass != pw:
        print("Password do to match. ")
        exit()

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