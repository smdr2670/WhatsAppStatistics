import sys
import random

import WhatsApp

###############################################################################

import numpy as np
import matplotlib.font_manager as fm
###############################################################################

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QAction, 
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QCalendarWidget, QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QDate, QSize, Qt, pyqtSignal, pyqtSlot

###############################################################################

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

###############################################################################

class MainWindow(QMainWindow):
    
    mySignal = pyqtSignal(dict)
    acquireDataSignal = pyqtSignal(str)

    acquireMostCommonEmojis = pyqtSignal()

    loadNewFileSignal = pyqtSignal(str)

    def makeConnections(self, otherObject):
        self.mySignal.connect(otherObject.onJob)
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        QMainWindow.__init__(self)

        self.currentData = {}
        self.indx = 0
        self.indxPlotTable = {0: 'emoji', 1: 'word', 2: 'msgByUser', 3: 'mediaMsgByUser'}
        self.currentFile = ""

        self.title = 'Whatsapp Statisic Application'
        self.left = 30
        self.top = 30
        self.width = 640
        self.height = 480

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')

        self.initMenubar()
        self.initToolBar()

        widget = QWidget(self)
        self.setCentralWidget(widget)
        vlay = QVBoxLayout(widget)
        hlay = QHBoxLayout()
        vlay.addLayout(hlay)

        self.nameLabel = QLabel('Name:', self)
        self.line = QLineEdit(self)
        self.nameLabel2 = QLabel('Result', self)

        hlay.addWidget(self.nameLabel)
        hlay.addWidget(self.line)
        hlay.addWidget(self.nameLabel2)
        hlay.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

        #pybutton = QPushButton('Click me', self)
        #pybutton.clicked.connect(self.clickMethod)

        pyCal = QCalendarWidget()
        pyCal.setGridVisible(True)
        pyCal.clicked[QDate].connect(self.showDate)

        hlay2 = QHBoxLayout()
        hlay2.addWidget(pyCal)
        hlay2.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        vlay.addLayout(hlay2)
        self.plotWidget = WidgetPlot(self)
        vlay.addWidget(self.plotWidget)

    def showDate(self, date):     
        print(date.toString())        

    def initMenubar(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')

        loadButton = QAction(QIcon('load24.png'), 'Load', self)
        loadButton.setShortcut('Ctrl+O')
        loadButton.setStatusTip('Load File')
        loadButton.triggered.connect(self.loadFile)
        fileMenu.addAction(loadButton)

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)


    def initToolBar(self):
        self.toolbar = self.addToolBar('Open')
        
        open_action = QAction(QIcon('F:\Projects\WhatsAppStatistics\Icons\Icon_New_File_256x256.png'), '&Save', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open File')
        open_action.triggered.connect(self.loadFile)
        self.toolbar.addAction(open_action)

        prevPlot_action = QAction(QIcon('F:\Projects\WhatsAppStatistics\Icons\iconfinder_arrow-left_227602.png'), '&Save', self)
        prevPlot_action.setShortcut('Left')
        prevPlot_action.setStatusTip('Previous Plot')
        prevPlot_action.triggered.connect(self.prevPlot)
        self.toolbar.addAction(prevPlot_action)

        nextPlot_action = QAction(QIcon('F:\Projects\WhatsAppStatistics\Icons\iconfinder_arrow-right_227601.png'), '&Save', self)
        nextPlot_action.setShortcut('Right')
        nextPlot_action.setStatusTip('Next Plot')
        nextPlot_action.triggered.connect(self.nextPlot)
        self.toolbar.addAction(nextPlot_action)

    def loadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Text files (*.txt)")
        self.currentFile = fname[0]
        self.plotWidget.canvas.clearPlot()
        self.loadNewFileSignal.emit(self.currentFile)
        
    def clickMethod(self):
        print('Clicked Pyqt button.')
        print('Emit signal')
        self.mySignal.emit(dict())
        
        if self.line.text() == '':
            self.statusBar().showMessage('Not a Number')
        else:
            print('Number: {}'.format(float(self.line.text())*2))
            self.statusBar().showMessage('Introduction of a number')
            self.nameLabel2.setText(str(float(self.line.text())*2))

    def nextPlot(self):
        print("Requesting next plot")
        self.plotWidget.canvas.clearPlot()
        
        if self.currentFile != "":
            if self.indx + 1 >= len(self.indxPlotTable):
                self.indx = 0
            else:
                self.indx = self.indx + 1
        
            self.acquireDataSignal.emit(self.indxPlotTable[self.indx])
            

    def prevPlot(self):
        print("Requesting previous plot")
        self.plotWidget.canvas.clearPlot()

        if self.currentFile != "":
            if self.indx - 1 < 0:
                self.indx = len(self.indxPlotTable) - 1
            else:
                self.indx = self.indx - 1
            
            self.acquireDataSignal.emit(self.indxPlotTable[self.indx])
        
    def clearPlot(self):
        print("Clear next plot")
        self.plotWidget.canvas.clearPlot()

    @pyqtSlot(dict)
    def onData(self, data):
        print('Receveived data')
        self.currentData = data
        self.plotWidget.canvas.plot(self.currentData, self.indxPlotTable[self.indx])


###############################################################################

class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self, width=10, height=8)
        # Toolbar for plot
        #self.toolbar = NavigationToolbar(self.canvas, self) 
        #self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data, title):
        ax = self.figure.add_subplot(111)

        group_data = list(data.values())[::-1]
        group_names = list(data.keys())[::-1]

        ax.title.set_text(title)    
        ax.barh(group_names, group_data)
        for i, v in enumerate(group_data):
            ax.text(v, i, " "+str(v), color='blue', va='center', fontweight='bold', fontsize=15)

        self.draw()
    
    def clearPlot(self):
        self.figure.clear()

    

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    
    msgListReader = WhatsApp.MessageListReader()

    msgListReader.emojiSignal.connect(mainWin.onData)
    msgListReader.wordSignal.connect(mainWin.onData)
    msgListReader.messageByPersonSignal.connect(mainWin.onData)
    msgListReader.mediaMessageByPersonSignal.connect(mainWin.onData)

    mainWin.loadNewFileSignal.connect(msgListReader.loadFile)
    mainWin.acquireDataSignal.connect(msgListReader.onJob)
    
    mainWin.show()
    sys.exit( app.exec_())