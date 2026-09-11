"""FrameDrop desktop: browser-independent public-video downloads."""
import sys
from pathlib import Path
from PySide6.QtCore import QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar, QFileDialog)
from engine import Engine, choices


class Task(QThread):
    result = Signal(object)
    error = Signal(str)
    progress = Signal(object)

    def __init__(self, operation):
        super().__init__()
        self.operation = operation

    def run(self):
        try:
            self.result.emit(self.operation(Engine(self.progress.emit)))
        except Exception as exc:
            self.error.emit(str(exc)[:600])


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FrameDrop • by iniexe')
        self.resize(570, 640)
        self.folder = str(Path.home() / 'Downloads' / 'FrameDrop')
        self.info = None
        self.task = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)
        brand = QLabel('✦  FRAMEDROP\n     by iniexe')
        layout.addWidget(brand)
        heading = QLabel('Worth keeping.')
        heading.setStyleSheet('font-size:36px;font-weight:700;')
        layout.addWidget(heading)
        layout.addWidget(QLabel('Your video. Your quality. One neat download.'))
        self.url = QLineEdit()
        self.url.setPlaceholderText('Paste a public video link…')
        self.url.textChanged.connect(self.invalidate)
        layout.addWidget(self.url)
        self.analyze = QPushButton('Analyze link  ↗')
        self.analyze.clicked.connect(self.inspect)
        layout.addWidget(self.analyze)
        self.title = QLabel('YouTube, supported video pages, and direct media links.')
        self.title.setWordWrap(True)
        layout.addWidget(self.title)
        row = QHBoxLayout()
        self.mode = QComboBox()
        self.mode.addItems(['Video', 'MP3 audio'])
        self.mode.currentIndexChanged.connect(self.fill_formats)
        self.quality = QComboBox()
        row.addWidget(self.mode)
        row.addWidget(self.quality, 1)
        layout.addLayout(row)
        self.note = QLabel('Video keeps original codecs; separate tracks merge into MKV.')
        self.note.setWordWrap(True)
        layout.addWidget(self.note)
        self.destination = QPushButton('Choose save folder')
        self.destination.clicked.connect(self.choose_folder)
        layout.addWidget(self.destination)
        self.download = QPushButton('✦  Download')
        self.download.setObjectName('primary')
        self.download.setEnabled(False)
        self.download.clicked.connect(self.start_download)
        layout.addWidget(self.download)
        self.bar = QProgressBar()
        self.bar.setValue(0)
        layout.addWidget(self.bar)
        self.status = QLabel('Ready when you are.')
        self.status.setWordWrap(True)
        self.status.setTextFormat(__import__('PySide6.QtCore', fromlist=['Qt']).Qt.PlainText)
        self.title.setTextFormat(__import__('PySide6.QtCore', fromlist=['Qt']).Qt.PlainText)
        layout.addWidget(self.status)
        self.open_folder = QPushButton('Open downloads folder')
        self.open_folder.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(self.folder)))
        layout.addWidget(self.open_folder)
        layout.addStretch()
        layout.addWidget(QLabel('Local processing · Public, unprotected videos · Desktop preview'))
        self.setStyleSheet('''QWidget {background:#fffaf3;color:#191715;font:14px sans-serif;}
QLineEdit,QComboBox,QPushButton {border:1px solid #292522;border-radius:14px;padding:12px;}
QPushButton:hover {background:#eee3d4;} QPushButton:disabled {color:#958b80;border-color:#cfc4b8;}
QPushButton#primary {background:#191715;color:#fffaf3;font-weight:700;}
QProgressBar {border:1px solid #292522;border-radius:6px;text-align:center;}
QProgressBar::chunk {background:#a99a85;}
''')

    def invalidate(self):
        self.info = None
        self.download.setEnabled(False)
        self.quality.clear()

    def fill_formats(self):
        self.quality.clear()
        if self.mode.currentIndex():
            for value in ('320', '192', '128'):
                self.quality.addItem(value+' kbps · MP3', value)
            self.note.setText('Converted locally. A higher bitrate cannot improve the source.')
        else:
            for f in choices(self.info or {}):
                self.quality.addItem(f['label'], f['id'])
            self.note.setText('Video keeps original codecs; separate tracks merge into MKV.')

    def busy(self, enabled):
        for widget in (self.url, self.analyze, self.mode, self.quality, self.destination):
            widget.setEnabled(not enabled)
        self.download.setEnabled(not enabled and self.info is not None)
        self.bar.setRange(0, 0 if enabled else 100)

    def launch(self, operation, callback):
        self.busy(True)
        self.task = Task(operation)
        self.task.result.connect(callback)
        self.task.error.connect(self.status.setText)
        self.task.progress.connect(self.on_progress)
        self.task.finished.connect(lambda: self.busy(False))
        self.task.start()

    def inspect(self):
        url = self.url.text().strip()
        self.invalidate()
        self.status.setText('Finding available video formats…')
        self.launch(lambda engine: engine.inspect(url), self.inspected)

    def inspected(self, info):
        self.info = info
        self.title.setText(info.get('title', 'Video'))
        self.fill_formats()
        self.status.setText('Choose a quality and make it yours.')

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Save downloads', self.folder)
        if folder:
            self.folder = folder
            self.destination.setText('Save to: '+folder)

    def start_download(self):
        url, mode, quality, folder = self.url.text().strip(), ('audio' if self.mode.currentIndex() else 'video'), self.quality.currentData(), self.folder
        self.status.setText('Preparing download…')
        self.launch(lambda engine: engine.download(url, mode, quality, folder), self.completed)

    def completed(self, _):
        self.status.setText('Saved to '+self.folder)
        self.bar.setRange(0, 100)
        self.bar.setValue(100)

    def on_progress(self, data):
        total = data.get('total_bytes') or data.get('total_bytes_estimate')
        if total:
            self.bar.setRange(0, 100)
            self.bar.setValue(int(data.get('downloaded_bytes', 0)*100/total))
        self.status.setText('Merging or converting locally…' if data['status'] == 'finished' else 'Downloading…')

    def closeEvent(self, event):
        if self.task and self.task.isRunning():
            self.status.setText('Wait for the current operation to finish before closing.')
            event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    if '--smoke-test' in sys.argv:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(500, app.quit)
    sys.exit(app.exec())
