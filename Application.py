import sys
import WhatsAppMessageParser as wa
import WhatsAppMessageStatisticVisualizer as viz

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWin = viz.MainWindow()
    
    msgListReader = wa.WhatsAppMessageParser()

    msgListReader.emojiSignal.connect(mainWin.onData)
    msgListReader.wordSignal.connect(mainWin.onData)
    msgListReader.messageByPersonSignal.connect(mainWin.onData)
    msgListReader.mediaMessageByPersonSignal.connect(mainWin.onData)

    msgListReader.minDateSignal.connect(mainWin.setMinDateInCalendar)
    msgListReader.maxDateSignal.connect(mainWin.setMaxDateInCalendar)

    mainWin.loadNewFileSignal.connect(msgListReader.loadFile)
    mainWin.acquireDataSignal.connect(msgListReader.onJob)
    mainWin.setMinDateSignal.connect(msgListReader.setMinDate)
    mainWin.setMaxDateSignal.connect(msgListReader.setMaxDate)
    
    mainWin.show()
    sys.exit( app.exec_())