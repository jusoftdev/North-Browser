import os
import sys
from datetime import datetime
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import improver
import man_db
import subprocess
import worker
import requests
import keyboard
from PIL import ImageGrab
import json
from types import SimpleNamespace
import browser
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtWidgets import QApplication, QSplitter, QVBoxLayout


Man_db = man_db.Man_Db(path="..\\ressources\\data\\db.db")
worker = worker.Worker()


# main window
class MainWindow(QMainWindow):
    htmlFinished = pyqtSignal()

    def __init__(self, incognito=False, darkmode=False,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.view = QWebView(self)
        self.view.settings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled, True)
        self.inspector = QWebInspector()
        self.inspector.setPage(self.view.page())
        self.inspector.show()
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.inspector)
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        # backround color
        # self.textbox.setStyleSheet("background-color:lightgreen")

        # creating a tab widget
        # making document mode true

        self.mHtml = ""


        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # making tabs closeable
        self.tabs.setTabsClosable(True)

        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # making tabs as central widget
        self.setCentralWidget(self.tabs)

        # creating a status bar
        self.status = QStatusBar()

        # setting status bar to the main window
        self.setStatusBar(self.status)

        self.Darkmode = darkmode
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.incognito = incognito
        if not self.Darkmode:
            if self.incognito:
                self.setStyleSheet("background-color:gray")
                #self.setStyleSheet(open('..\\ressources\\css\\white-mode-incognito.css').read())
                self.tabs.setStyleSheet("background-color:gray;")
                self.setWindowIcon(QtGui.QIcon('..\\ressources\\icons\\incognito.png'))
            else:
                self.setStyleSheet("background-color:green")
                #self.setStyleSheet(open('..\\ressources\\css\\white-mode.css').read())
                self.tabs.setStyleSheet("background-color:green;")
                self.setWindowIcon(QtGui.QIcon('..\\ressources\\icons\\256x256.png'))

        elif self.Darkmode:
            if self.incognito:
                self.setStyleSheet("background-color:black")
                #self.setStyleSheet(open('..\\ressources\\css\\dark-mode-incognito.css').read())
                self.setWindowIcon(QtGui.QIcon('..\\ressources\\icons\\incognito.png'))
                self.tabs.setStyleSheet("background-color:black;")
            else:
                self.setStyleSheet("background-color:gray")
                #self.setStyleSheet(open('..\\ressources\\css\\dark-mode.css').read())
                self.tabs.setStyleSheet("background-color:gray;")
                self.setWindowIcon(QtGui.QIcon('..\\ressources\\icons\\256x256.png'))
        self.Maximized = False

        # creating a tool bar for navigation
        self.navtb = QToolBar("Navigation")

        # adding tool bar tot he main window
        self.addToolBar(self.navtb)
        # creating back action
        self.back_btn = QAction(QIcon("..\\ressources\\icons\\backward.png"), "Backward", self)
        # setting status tip
        self.back_btn.setStatusTip("Back to previous page")
        self.back_btn.setShortcut('Ctrl+Shift+B')
        # adding action to back button
        # making current tab to go back
        self.back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.navtb.addAction(self.back_btn)


        reload_btn = QAction(QIcon("..\\ressources\\icons\\reload.png"), "Reload", self)
        reload_btn.setShortcut('F5')
        # reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        self.navtb.addAction(reload_btn)

        # similarly adding next button
        self.next_btn = QAction(QIcon("..\\ressources\\icons\\forward.png"), "Forward", self)
        self.next_btn.setStatusTip("Forward to next page")
        self.next_btn.setShortcut('Ctrl+P')
        self.next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.navtb.addAction(self.next_btn)



        # creating home action
        home_btn = QAction(QIcon("..\\ressources\\icons\\home.png"), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.setShortcut('Ctrl+Shift+O')
        # adding action to home button
        home_btn.triggered.connect(self.navigate_home)
        self.navtb.addAction(home_btn)

        # add new tab button
        add_new_tab_btn = QAction(QIcon("..\\ressources\\icons\\add.png"), "Add Tab", self)
        add_new_tab_btn.setStatusTip("Open New Tab")
        # set Shortcut
        add_new_tab_btn.setShortcut('Ctrl+T')
        add_new_tab_btn.triggered.connect(self.open_new_Tab)
        self.navtb.addAction(add_new_tab_btn)

        # incognito mode btn
        incognito_tab_btn = QAction(QIcon("..\\ressources\\icons\\incognito.png"), "Incognito_Mode", self)
        incognito_tab_btn.setStatusTip("Open Incognito Tab")
        incognito_tab_btn.setShortcut('Ctrl+Shift+N')
        incognito_tab_btn.triggered.connect(self.open_new_tab_incognito)
        self.navtb.addAction(incognito_tab_btn)

        # adding a separator
        self.navtb.addSeparator()

        # creating a line edit widget for URL
        self.urlbar = QLineEdit()
        Imp = improver.Improver(path="..\\ressources\\data\\db.db")
        completer = Imp.improve()
        self.urlbar.setCompleter(completer)

        # adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # adding line edit to tool bar
        self.navtb.addWidget(self.urlbar)

        # similarly adding stop action
        stop_btn = QAction(QIcon("..\\ressources\\icons\\stop.png"), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(stop_btn)
        close_btn = QAction(QIcon("..\\ressources\\icons\\close.png"), "Close", self)
        close_btn.setStatusTip("Close Window")
        close_btn.triggered.connect(lambda: self.close())
        self.navtb.addAction(close_btn)


        self.navtb_side = QToolBar("Navigation")

        # adding tool bar tot he main window
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.navtb_side)
        history_btn = QAction(QIcon("..\\ressources\\icons\\history.png"), "History", self)
        history_btn.setStatusTip("Show history")
        history_btn.setShortcut('Ctrl+Shift+B')
        history_btn.triggered.connect(lambda: self.show_history())

        download_btn = QAction(QIcon("..\\ressources\\icons\\down.png"), "Download Page", self)
        download_btn.setStatusTip("Save File")
        download_btn.setShortcut('Ctrl+S')
        download_btn.triggered.connect(lambda: self.save_file())

        self.screenshot_btn = QAction(QIcon("..\\ressources\\icons\\cam.png"), "Save Screenshot", self)
        self.screenshot_btn.setStatusTip("Save Scrennshot")
        self.screenshot_btn.setShortcut('Ctrl+Shift+S')
        self.screenshot_btn.triggered.connect(lambda: self.save_screenshot())

        if self.Darkmode:
            self.darkmode_btn = QAction(QIcon("..\\ressources\\icons\\sun.png"), "Activate Whitemode", self)
        else:
            self.darkmode_btn = QAction(QIcon("..\\ressources\\icons\\moon.png"), "Activate Darkmode", self)

        self.darkmode_btn.setStatusTip("Change Mode")
        self.darkmode_btn.setShortcut('Ctrl+Shift+C')
        self.darkmode_btn.triggered.connect(lambda: self.choose_mode())

        self.navtb_side.addAction(history_btn)
        self.navtb_side.addAction(download_btn)
        self.navtb_side.addAction(self.screenshot_btn)
        self.navtb_side.addAction(self.darkmode_btn)
        self.navtb_side.addSeparator()


        # creating first tab
        # If an new version appears the site will switch to an info page
        try:
            if str(sys.argv[1]) != "newv":
                if str(sys.argv[1]) != "newvgit":
                    self.add_new_tab(QUrl('https://searchify.vercel.app/'), 'Homepage')
                else:
                    self.add_new_tab(QUrl('https://searchify.vercel.app/'), 'Homepage')
                    self.add_new_tab(QUrl("about:blank"), 'New Version!')
                    self.navigate_to_url("localhost/newv")
                    self.add_new_tab(QUrl("https://git-scm.com/download/win"), 'New Version!')
            else:
                self.add_new_tab(QUrl('https://searchify.vercel.app/'), 'Homepage')
                self.add_new_tab(QUrl("about:blank"), 'New Version!')
                self.navigate_to_url("localhost/newv")
        except:
            self.add_new_tab(QUrl('https://searchify.vercel.app/'), 'Homepage')

        # showing all the components
        self.showMaximized()

        # setting window title
        self.setWindowTitle("Jusoft-Browser")

    # method for adding new tab


    def open_new_tab_incognito(self):
        self.open_new_Tab(incognito=True)

    def add_new_tab(self, qurl=None, label="Blank"):

        # if url is blank
        r = requests.get("https://searchify.vercel.app/")
        if r.status_code == 200:
            if qurl is None:
                # creating a google url
                qurl = QUrl('https://searchify.vercel.app/')
        else:
            if qurl is None:
                # creating a google url
                qurl = QUrl('https://www.google.com/')


        # creating a QWebEngineView object
        #browser = browser.Browser()
        self.browser = browser.Browser()
        # setting url to browser
        self.browser.setUrl(qurl)

        # setting tab index
        i = self.tabs.addTab(self.browser, label)
        self.tabs.setCurrentIndex(i)

        # adding action to the browser when url is changed
        # update the url
        self.browser.urlChanged.connect(lambda qurl, browser=self.browser:
                                   self.update_urlbar(qurl, browser=self.browser))

        # adding action to the browser when loading is finished
        # set the tab title
        self.browser.loadFinished.connect(lambda _, i=i, browser=self.browser:
                                     self.tabs.setTabText(i, self.browser.page().title()), )
        self.browser.loadFinished.connect(lambda: self.on_load_finished())

        self.browser.page().fullScreenRequested.connect(
            lambda request, browser=self.browser: self.handle_fullscreen_requested(request))

        self.browser.reloadpressed.connect(lambda: self.tabs.currentWidget().reload())
        self.browser.forwardpressed.connect(lambda: self.tabs.currentWidget().forward())
        self.browser.backpressed.connect(lambda: self.tabs.currentWidget().back())
        self.browser.viewpressed.connect(lambda: self.viewSource())
        self.browser.inspectpressed.connect(lambda: self.inspectElement())

        thread = QThread(parent=self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.pressed.connect(lambda: self.on_Escape())
        thread.start()

    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):

        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_new_tab()

    def callback(self, html):
        self.viewSource(html)

    def callback2(self, html):
        self.save_file(html)

    # wen tab is changed
    def current_tab_changed(self, i):
        # get the curl
        qurl = self.tabs.currentWidget().url()

        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())

        # update the title
        self.update_title(self.tabs.currentWidget())
        self.track(url=qurl.toString())  # url = qurl
        #print(qurl)
        # print(type(qurl))

    # when tab is closed
    def close_current_tab(self, i):
        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return

        # else remove the tab
        self.tabs.removeTab(i)
        qurl = self.tabs.currentWidget().url()
        self.track(url=qurl.toString(), delete=True)




    # method for updating the title
    def update_title(self, browser):

        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return

        # get the page title
        title = self.tabs.currentWidget().page().title()

        # set the window title
        self.setWindowTitle("% s - Jusoft-Browser" % title)

    # action to go to home
    def navigate_home(self):
        # go to google
        r = requests.get("https://searchify.vercel.app/")
        if r.status_code == 200:
            self.tabs.currentWidget().setUrl(QUrl("https://searchify.vercel.app/"))
        else:
            self.tabs.currentWidget().setUrl(QUrl("https://www.google.com/"))

    # method for navigate to url
    def navigate_to_url(self, url=None):

        # get the line edit text
        # convert it to QUrl object
        if url == None:
            if "www" in self.urlbar.text():
                q = QUrl(self.urlbar.text())
                x = self.urlbar.text()
                if q.scheme() == "":
                    x = "https://" + str(x)
                q = QUrl(x)

            elif "localhost" in self.urlbar.text():
                q = QUrl(self.urlbar.text())
                x = self.urlbar.text()
                if q.scheme() == "":
                    x = "http://" + str(x)
                q = QUrl(x)

            else:
                q = QUrl(f"https://searchify.vercel.app/search?term={self.urlbar.text()}")

        else:
            if "localhost" in url:
                url = "http://" + str(url)
                q = QUrl(url)


        self.track(url=q.toString())
        self.track(url=self.urlbar.text())

        # set the url
        try:
            r = requests.get(q.toString())
            if r.status_code == 200 or "localhost" in url:
                pass
            else:
                q = QUrl("http://localhost/error_404")
        except:
            q = QUrl("http://localhost/error_404")




        self.tabs.currentWidget().setUrl(q)

    # method to update the url
    def update_urlbar(self, q, browser=None):

        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return

        # set text to the url bar
        self.urlbar.setText(q.toString())
        self.track(url=q.toString())

        # set cursor position
        self.urlbar.setCursorPosition(0)

    def handle_fullscreen_requested(self, request):
        request.accept()

        if request.toggleOn():
            self.browser.showFullScreen()
            #browser.setParent(None)
            self.statusBar().hide()
            self.navtb.hide()
            self.navtb_side.hide()
            self.tabs.tabBar().hide()
            self.Maximized = True
        else:
            self.browser.showNormal()
            self.statusBar().show()
            self.navtb.show()
            self.navtb_side.show()
            self.tabs.tabBar().show()
            self.tabs.currentWidget().showNormal()
            self.Maximized = False
            #self.setCentralWidget(browser)

    def on_Escape(self):
        if self.Maximized:
            self.browser.showNormal()
            self.statusBar().show()
            self.navtb.show()
            self.navtb_side.show()
            self.tabs.tabBar().show()
            self.tabs.currentWidget().showNormal()
            keyboard.press_and_release('f')
            self.Maximized = False
        else:
            pass
        return(0)

    def open_new_Tab(self, url="", incognito=False):
        if incognito == True:
            incognitowindow = MainWindow(incognito=True)
        elif incognito == False:
            r = requests.get("https://searchify.vercel.app/")
            if r.status_code == 200:
                self.add_new_tab(QUrl('https://searchify.vercel.app/'), 'New Tab')
            else:
                self.add_new_tab(QUrl('https://www.google.com/'), 'New Tab')

    def show_history(self):
        self.add_new_tab(QUrl("about:blank"))
        self.navigate_to_url(url="localhost/history")

    def save_file(self, html="None"):
        try:
            if html == "None":
                self.browser.page().toHtml(self.callback2)
                return(1)
            else:
                raw = html
            print("Get", self.browser.page().url())
            filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                      "Hypertext Markup Language (*.htm *.html);;" "All files(*.*)")
            with open(filename, encoding='utf-8', errors='ignore', mode="w") as f:
                f.write(str(raw))
        except:
            pass

    def save_screenshot(self):
        try:
            screenshot = ImageGrab.grab(all_screens=True)
            filename, _ = QFileDialog.getSaveFileName(self, "Save Screenshot As", "",
                                                              "Portable Network Graphics (*.png);;" "All files(*.*)")
            screenshot.save(filename, 'PNG')
        except:
            pass



    def on_load_finished(self):
        if self.browser.history().canGoBack():
            self.back_btn.setEnabled(True)
        else:
            self.back_btn.setEnabled(False)
        if self.browser.history().canGoForward():
            self.next_btn.setEnabled(True)
        else:
            self.next_btn.setEnabled(False)

    def activate_darkmode(self):
        f = open("..\\ressources\\data\\settings.json", "r", encoding="utf-8")
        settings = f.read()
        f.close()
        set = json.loads(settings, object_hook=lambda d: SimpleNamespace(**d))
        wf = open("..\\ressources\\data\\settings.json", "w", encoding="utf-8")
        if set.settings.mode.darkmode == "False":
            settings = settings.replace('"darkmode":"False"', '"darkmode":"True"')
            wf.write(settings)
        wf.close()
        self.add_new_tab(QUrl("about:blank"))
        self.navigate_to_url("localhost/darkmode")

    def deactivate_darkmode(self):
        f = open("..\\ressources\\data\\settings.json", "r", encoding="utf-8")
        settings = f.read()
        f.close()
        set = json.loads(settings, object_hook=lambda d: SimpleNamespace(**d))
        wf = open("..\\ressources\\data\\settings.json", "w", encoding="utf-8")
        if set.settings.mode.darkmode == "True":
            settings = settings.replace('"darkmode":"True"', '"darkmode":"False"')
            wf.write(settings)
        wf.close()

        self.add_new_tab(QUrl("about:blank"))
        self.navigate_to_url("localhost/whitemode")

    def choose_mode(self):
        f = open("..\\ressources\\data\\settings.json", "r", encoding="utf-8")
        settings = f.read()
        f.close()
        set = json.loads(settings, object_hook=lambda d: SimpleNamespace(**d))
        if set.settings.mode.darkmode == "True":
            self.deactivate_darkmode()

        elif set.settings.mode.darkmode == "False":
            self.activate_darkmode()


    def viewSource(self):
        self.view.load(QUrl('http://www.google.com'))



    def inspectElement(self):
        self.inspector.setPage(self.browser.page())
        self.inspector.show()
        self.splitter.addWidget(self.browser)
        self.splitter.addWidget(self.inspector)





    def track(self, url, delete=False):
        if self.incognito == False:
            if not os.path.exists("..\\ressources\\data\\db.db"):
                Man_db.create_db_history()
            if delete == True:
                #print("deleted {}".format(str(url)))
                Man_db.write_db_history(Id=str(0), Date=str(datetime.now()), Url=str(url), Event="deleted")
            else:
                #print("added {}".format(str(url)))
                Man_db.write_db_history(Id=str(1), Date=str(datetime.now()), Url=str(url), Event="added")
        return 0


# creating a PyQt5 application
f = open("..\\ressources\\data\\settings.json", "r", encoding="utf-8")
settings = f.read()
f.close()
set = json.loads(settings, object_hook=lambda d: SimpleNamespace(**d))
#print(set.settings.mode.darkmode)
#print(type(set.settings.mode.darkmode))
if set.settings.mode.darkmode == "True":
    Darkmode = True
    #print("Dark-Mode")
    args = sys.argv + ["--blink-settings=darkModeEnabled=true,darkModeInversionAlgorithm=4"]
elif set.settings.mode.darkmode == "False":
    Darkmode = False
    #print("White-Mode")
    args = sys.argv
else:
    Darkmode = False
    args = sys.argv

app = QApplication(args)
app.setStyle("fusion")
# setting name to the application
app.setApplicationName("Jusoft-Browser")
app.setOrganizationName("Jusoft")
app.setOrganizationDomain("https://jusoft.dev")
app_icon = QtGui.QIcon()
app_icon.addFile('..\\..\\ressources\\icons\\16x16.png', QtCore.QSize(16, 16))
app_icon.addFile('..\\..\\ressources\\icons\\24x24.png', QtCore.QSize(24, 24))
app_icon.addFile('..\\..\\ressources\\icons\\32x32.png', QtCore.QSize(32, 32))
app_icon.addFile('..\\..\\ressources\\icons\\48x48.png', QtCore.QSize(48, 48))
app_icon.addFile('..\\..\\ressources\\icons\\256x256.png', QtCore.QSize(256, 256))
app.setWindowIcon(app_icon)

# creating MainWindow object
if __name__ == "__main__":
    process = subprocess.Popen(['python', 'srv.py'], stdout=subprocess.DEVNULL)
    window = MainWindow(darkmode=Darkmode)

    c = app.exec_()
    process.kill()
    sys.exit(c)