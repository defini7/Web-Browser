from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction, QLineEdit, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import validators


class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)
    
    self.main()

  def add_to_navbar(self, btn_name: str, btn_event):
    btn = QAction(btn_name, self)
    btn.triggered.connect(btn_event)
    self.navbar.addAction(btn)

  def navigate_home(self):
    self.tabs.currentWidget().setUrl(QUrl('https://google.com'))

  def navigate_url(self):
    search = self.url_bar.text()
    is_url= validators.url(search)

    if is_url:
      self.tabs.currentWidget().setUrl(QUrl(search))
    else:
      self.tabs.currentWidget().setUrl(QUrl('https://www.google.com/search?q=' + search))

  def update_title(self, browser):
    if browser != self.tabs.currentWidget():
      return 

    self.setWindowTitle(self.tabs.currentWidget().page().title())

  def update_url(self, url: QUrl, q, browser=None):
    if browser != self.tabs.currentWidget():
      return
      
    self.url_bar.setText(url.toString())

  def add_new_tab(self, _: bool = True, url: QUrl = QUrl('https://google.com/'), title='New tab'):
    if url is None or type(url) == bool:
      url = QUrl('')

    browser = QWebEngineView()
    browser.setUrl(url)
    index = self.tabs.addTab(browser, title)

    self.tabs.setCurrentIndex(index)

    browser.urlChanged.connect(lambda url, browser=browser: self.update_url(url, browser))
    browser.loadFinished.connect(lambda _, i=index, browser=browser: self.tabs.setTabText(i, browser.page().title()))

  def tab_open_doubleclick(self, i):
    if i == -1:
      self.add_new_tab()

  def current_tab_changed(self, i):
    url = self.tabs.currentWidget().url()
    self.update_url(url, self.tabs.currentWidget())
    self.update_title(self.tabs.currentWidget())

  def close_current_tab(self, i):
    if self.tabs.count() < 2:
      self.add_new_tab()

    self.tabs.removeTab(i)

  def main(self):
    self.tabs = QTabWidget()
    self.tabs.setMovable(False)
    self.tabs.setDocumentMode(True)
    self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
    self.tabs.currentChanged.connect(self.current_tab_changed)
    self.tabs.setTabsClosable(True)
    self.tabs.tabCloseRequested.connect(self.close_current_tab)

    self.setCentralWidget(self.tabs)
    self.showMaximized()

    self.navbar = QToolBar()
    self.navbar.setMovable(False)
    self.addToolBar(self.navbar)

    self.add_new_tab()

    self.add_to_navbar('←', self.tabs.currentWidget().back)
    self.add_to_navbar('→', self.tabs.currentWidget().forward)
    self.add_to_navbar('🗘', self.tabs.currentWidget().reload)
    self.add_to_navbar('Home', self.navigate_home)

    self.url_bar = QLineEdit()
    self.url_bar.returnPressed.connect(self.navigate_url)
    self.navbar.addWidget(self.url_bar)

    self.add_to_navbar('+', self.add_new_tab)

    self.show()
    

app = QApplication(sys.argv)
QApplication.setApplicationName('Internet')

window = MainWindow()

app.exec()
