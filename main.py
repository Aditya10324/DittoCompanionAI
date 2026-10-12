import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
import threading
from health_advisor import listen_and_respond
from screen_monitor import detect_screen_event

class DittoCompanion(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel(self)
        self.current_emotion = "idle"
        self.load_emotion(self.current_emotion)
        self.label.resize(200, 200)

        # Task reminder timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.remind_task)
        self.timer.start(60000)

        # DB setup
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (task TEXT)")
        self.conn.commit()

        # Screen monitoring thread
        threading.Thread(target=self.monitor_screen, daemon=True).start()

    def load_emotion(self, emotion):
        movie = QtGui.QMovie(f"assets/ditto_{emotion}.PNG")
        self.label.setMovie(movie)
        movie.start()

    def remind_task(self):
        self.cursor.execute("SELECT task FROM tasks LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            task = row[0]
            self.load_emotion("angry")
            msg = QtWidgets.QMessageBox()
            msg.setText(f"⚠️ Reminder: {task}")
            msg.exec_()
        else:
            self.load_emotion("happy")

    def monitor_screen(self):
        while True:
            event = detect_screen_event()
            if event == "win":
                self.load_emotion("happy")
            elif event == "pause":
                self.load_emotion("sad")
            elif event == "focus":
                self.load_emotion("focus")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    companion = DittoCompanion()
    companion.show()
    threading.Thread(target=listen_and_respond, daemon=True).start()
    sys.exit(app.exec_())
