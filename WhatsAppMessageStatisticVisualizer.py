
import emoji
import WhatsAppMessageParser as wa

###############################################################################

import numpy as np
import matplotlib.pyplot as plt

from datetime import date

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

###############################################################################

from PyQt5.QtWidgets import (QWidget, QMainWindow, QAction, 
    QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QCalendarWidget, QFileDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QObject, QDate, QSize, Qt, pyqtSignal, pyqtSlot

###############################################################################

class MainWindow(QMainWindow):
    
    mySignal = pyqtSignal(dict)
    acquireDataSignal = pyqtSignal(str)

    acquireMostCommonEmojis = pyqtSignal()

    loadNewFileSignal = pyqtSignal(str)

    setMinDateSignal = pyqtSignal(object)  
    setMaxDateSignal = pyqtSignal(object)  

    def makeConnections(self, otherObject):
        self.mySignal.connect(otherObject.onJob)
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        QMainWindow.__init__(self)

        self.currentData = {}
        self.indx = 0
        self.indxPlotTable = {0: 'Emojis', 1: 'Words', 2: 'Messages by user', 3: 'Media messages by user'}
        self.currentFile = ""

        self.title = 'Whatsapp Statisic Application'

        self.mindataToDisplay = date(1900, 1, 1)
        self.currentMinData = date(1900, 1, 1)

        self.maxdataToDisplay = date(2100, 12, 31)      
        self.currentMaxData = date(2100, 12, 31)      

        self.setWindowTitle(self.title)
        self.setGeometry(30, 30, 1280, 1024)
        self.statusBar().showMessage('Ready')

        self.initMenubar()
        self.initToolBar()
        self.plotWidget = WidgetPlot(self)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        vlay = QVBoxLayout(widget)
        
        self.nameLabel = QLabel('Min Date', self)
        self.nameLabel2 = QLabel('Max Date', self)

        self.nameLabel.setFont(QFont('Arial', 20))
        self.nameLabel2.setFont(QFont('Arial', 20))

        self.pyCal = QCalendarWidget()
        self.pyCal.setGridVisible(True)
        self.pyCal.clicked[QDate].connect(self.sendMinDate)

        self.pyCal2 = QCalendarWidget()
        self.pyCal2.setGridVisible(True)
        self.pyCal2.clicked[QDate].connect(self.sendMaxDate)

        grid = QGridLayout()
        grid.addWidget(self.nameLabel, 0, 0, Qt.AlignCenter)
        grid.addWidget(self.nameLabel2, 0, 1, Qt.AlignCenter)
        grid.addWidget(self.pyCal, 1, 0)
        grid.addWidget(self.pyCal2, 1, 1)
        
        vlay.addLayout(grid)
        vlay.addWidget(self.plotWidget)


    def sendMinDate(self, date):
        self.currentMinData = date.toPyDate()    
        self.setMinDateSignal.emit(self.currentMinData)
            
    def sendMaxDate(self, date):
        self.currentMaxData = date.toPyDate()    
        self.setMaxDateSignal.emit(self.currentMaxData)


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
        
        open_action = QAction(QIcon('resources\Icons\Icon_New_File_256x256.png'), '&Save', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open File')
        open_action.triggered.connect(self.loadFile)
        self.toolbar.addAction(open_action)

        prevPlot_action = QAction(QIcon('resources\Icons\iconfinder_arrow-left_227602.png'), '&Save', self)
        prevPlot_action.setShortcut('Left')
        prevPlot_action.setStatusTip('Previous Plot')
        prevPlot_action.triggered.connect(self.prevPlot)
        self.toolbar.addAction(prevPlot_action)

        nextPlot_action = QAction(QIcon('resources\Icons\iconfinder_arrow-right_227601.png'), '&Save', self)
        nextPlot_action.setShortcut('Right')
        nextPlot_action.setStatusTip('Next Plot')
        nextPlot_action.triggered.connect(self.nextPlot)
        self.toolbar.addAction(nextPlot_action)

    def loadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Text files (*.txt)")
        if fname[0]:
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
        self.plotWidget.canvas.clearPlot()     
        if self.currentFile != "":
            if self.indx + 1 >= len(self.indxPlotTable):
                self.indx = 0
            else:
                self.indx = self.indx + 1
        
            self.acquireDataSignal.emit(self.indxPlotTable[self.indx])
            

    def prevPlot(self):
        self.plotWidget.canvas.clearPlot()
        if self.currentFile != "":
            if self.indx - 1 < 0:
                self.indx = len(self.indxPlotTable) - 1
            else:
                self.indx = self.indx - 1
            
            self.acquireDataSignal.emit(self.indxPlotTable[self.indx])
        
    def clearPlot(self):
        self.plotWidget.canvas.clearPlot()

    @pyqtSlot(dict)
    def onData(self, data):
        self.currentData = data
        self.plotWidget.canvas.clearPlot()
        title = self.indxPlotTable[self.indx] + " between " + self.currentMinData.strftime("%d.%m.%Y") + " and " + self.currentMaxData.strftime("%d.%m.%Y")
        self.plotWidget.canvas.plot(self.currentData, title)

    @pyqtSlot(object)
    def setMinDateInCalendar(self, minData):
        self.mindataToDisplay = minData
        self.currentMinData = minData
        self.pyCal.setMinimumDate(QDate(minData.year, minData.month, minData.day))
        self.pyCal2.setMinimumDate(QDate(minData.year, minData.month, minData.day))
        self.pyCal.setSelectedDate(QDate(minData.year, minData.month, minData.day))
        
    @pyqtSlot(object)
    def setMaxDateInCalendar(self, maxData):
        self.maxdataToDisplay = maxData
        self.currentMaxData = maxData
        self.pyCal.setMaximumDate(QDate(maxData.year, maxData.month, maxData.day))
        self.pyCal2.setMaximumDate(QDate(maxData.year, maxData.month, maxData.day))
        self.pyCal2.setSelectedDate(QDate(maxData.year, maxData.month, maxData.day))

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
        #self.figure.tight_layout()

        isEmojiPlot = "Emojis" in title

        group_data = list(data.values())[::-1]
        group_names = list(data.keys())[::-1]

        ax.title.set_text(title) 

        if isEmojiPlot:
            emojiNames = []
            for mostCommonEmoji in group_names:
                for emojiInList, name in emoji.UNICODE_EMOJI.items():   
                    if mostCommonEmoji == emojiInList:
                        emojiNames.append(name)
            #group_names = emojiNames
            ax.barh(emojiNames, group_data)
        else:
            ax.barh(group_names, group_data)

        for i, v in enumerate(group_data):
            ax.text(v, i, " "+str(v), color='blue', va='center', fontweight='bold', fontsize=15)
            
            if isEmojiPlot:
                currentEmoji = group_names[i]
                filename = str(emoji.UNICODE_EMOJI[currentEmoji]).strip(':')
                fileFilePath = "resources\Emojis"

                arr_img = plt.imread(fileFilePath + "\\" + filename + ".jpg" , format='jpg')

                imagebox = OffsetImage(arr_img, zoom=0.3)
                imagebox.image.axes = ax
                # Define a 1st position to annotate (display it with a marker)
                xy = (v, i)

                ab = AnnotationBbox(imagebox, 
                                    xy,
                                    xybox=(60, 0),
                                    xycoords='data',
                                    boxcoords="offset points")
                ax.add_artist(ab)

        self.draw()
    
    def clearPlot(self):
        self.figure.clear()

    