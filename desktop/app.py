"""FrameDrop desktop: browser-independent public-video downloads."""
import sys
from pathlib import Path
from PySide6.QtCore import QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar, QFileDialog, QFrame, QScrollArea)
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
        self.setWindowIcon(QIcon(str(Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) / 'icon-128.png')))
        self.resize(1000, 790)
        self.setMinimumSize(660, 650)
        self.folder = str(Path.home() / 'Downloads' / 'FrameDrop')
        self.info = None
        self.task = None
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        root.addWidget(scroll)
        canvas = QWidget()
        scroll.setWidget(canvas)
        layout = QVBoxLayout(canvas)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(16)

        def label(text, name='muted'):
            w = QLabel(text)
            w.setObjectName(name)
            w.setWordWrap(name not in ('eyebrow', 'darkeyebrow'))
            w.setTextFormat(__import__('PySide6.QtCore', fromlist=['Qt']).Qt.PlainText)
            return w

        def card(name='card'):
            w = QFrame()
            w.setObjectName(name)
            box = QVBoxLayout(w)
            box.setContentsMargins(22, 16, 22, 16)
            box.setSpacing(10)
            return w, box

        top = QHBoxLayout()
        top.addWidget(label('✦  FrameDrop', 'brand'))
        top.addStretch()
        top.addWidget(label('BY INIEXE  /  DESKTOP PREVIEW', 'eyebrow'))
        layout.addLayout(top)
        heading = label('Good finds. Yours to keep.', 'heading')
        layout.addWidget(heading)
        layout.addWidget(label('Save a video or just the audio. Everything happens on your computer.'))

        source, box = card()
        box.addWidget(label('01  /  START WITH A LINK', 'eyebrow'))
        row = QHBoxLayout()
        row.setSpacing(10)
        self.url = QLineEdit()
        self.url.setPlaceholderText('Paste a public video URL')
        self.url.setAccessibleName('Public video URL')
        self.url.setMinimumWidth(220)
        self.url.textChanged.connect(self.invalidate)
        self.url.returnPressed.connect(self.inspect)
        row.addWidget(self.url, 1)
        self.analyze = QPushButton('Analyze link  ↗')
        self.analyze.setObjectName('primary')
        self.analyze.clicked.connect(self.inspect)
        row.addWidget(self.analyze)
        box.addLayout(row)
        box.addWidget(label('YouTube · Supported video pages · Direct media links', 'small'))
        layout.addWidget(source)

        options, box = card()
        box.addWidget(label('02  /  MAKE IT YOURS', 'eyebrow'))
        self.title = label('Your next good find goes here.', 'title')
        box.addWidget(self.title)
        row = QHBoxLayout()
        left = QVBoxLayout()
        left.addWidget(label('OUTPUT', 'eyebrow'))
        self.mode = QComboBox()
        self.mode.addItems(['Video', 'MP3 audio'])
        self.mode.setAccessibleName('Output type')
        self.mode.currentIndexChanged.connect(self.fill_formats)
        left.addWidget(self.mode)
        right = QVBoxLayout()
        right.addWidget(label('QUALITY', 'eyebrow'))
        self.quality = QComboBox()
        self.quality.setMinimumWidth(220)
        self.quality.setAccessibleName('Download quality')
        self.quality.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        right.addWidget(self.quality)
        row.addLayout(left, 1)
        row.addLayout(right, 2)
        box.addLayout(row)
        self.note = label('Analyze a link to see the formats available from its source.', 'small')
        box.addWidget(self.note)
        self.destination = QPushButton('Save folder · Downloads / FrameDrop')
        self.destination.setToolTip(self.folder)
        self.destination.clicked.connect(self.choose_folder)
        box.addWidget(self.destination)
        layout.addWidget(options)

        transfer, box = card('transfer')
        row = QHBoxLayout()
        row.addWidget(label('03  /  BRING IT HOME', 'darkeyebrow'))
        row.addStretch()
        self.download = QPushButton('Download  ↓')
        self.download.setObjectName('download')
        self.download.setEnabled(False)
        self.download.clicked.connect(self.start_download)
        row.addWidget(self.download)
        box.addLayout(row)
        self.status = label('Ready when you are.', 'status')
        box.addWidget(self.status)
        self.bar = QProgressBar()
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(7)
        box.addWidget(self.bar)
        self.open_folder = QPushButton('Open downloads folder  ↗')
        self.open_folder.setObjectName('folderLink')
        self.open_folder.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(self.folder)))
        box.addWidget(self.open_folder)
        layout.addWidget(transfer)
        layout.addWidget(label('LOCAL PROCESSING     /     NO ACCOUNT NEEDED     /     BY INIEXE', 'eyebrow'))
        layout.addStretch()
        self.setStyleSheet("""
QWidget {background:#f5f4f1;color:#202020;font:14px 'Segoe UI';}
QScrollArea {border:0;} QScrollArea > QWidget > QWidget {background:#f5f4f1;}
QLabel {background:transparent;}
QLabel#brand {font-size:22px;font-weight:700;}
QLabel#heading {font-size:34px;font-weight:700;}
QLabel#eyebrow {font-size:11px;font-weight:600;color:#65635e;}
QLabel#muted {color:#64625d;} QLabel#small {font-size:12px;color:#64625d;}
QLabel#title {font-size:20px;font-weight:600;}
QFrame#card {background:#ffffff;border:1px solid #e2e0db;border-radius:18px;}
QFrame#transfer {background:#19191e;border-radius:18px;}
QLabel#darkeyebrow {font-size:11px;color:#b9b9c0;font-weight:600;}
QLabel#status {font-size:17px;color:#ffffff;}
QLineEdit,QComboBox,QPushButton {min-height:22px;border:1px solid #deddd7;border-radius:9px;padding:11px 14px;background:#f8f8f6;}
QLineEdit:focus,QComboBox:focus,QPushButton:focus {border:2px solid #777466;}
QPushButton {font-weight:600;} QPushButton:hover {background:#eae9e3;}
QPushButton:pressed {background:#dddcd4;}
QPushButton:disabled,QComboBox:disabled {color:#92918b;background:#eeede9;}
QPushButton#primary {background:#202024;color:white;border:1px solid #202024;}
QPushButton#primary:hover {background:#414147;}
QPushButton#download {background:#e4ecd7;color:#22291c;border:0;min-width:130px;}
QPushButton#download:hover {background:#f0f6e7;}
QPushButton#download:disabled {background:#35353c;color:#a5a5ac;}
QPushButton#folderLink {color:#d0d0d6;background:transparent;border:1px solid #48484f;}
QPushButton#folderLink:hover {background:#33333b;}
QProgressBar {background:#3c3c44;border:0;border-radius:3px;}
QProgressBar::chunk {background:#dce9cb;border-radius:3px;}
QComboBox QAbstractItemView {background:white;color:#202020;selection-background-color:#e5e8dc;selection-color:#202020;padding:4px;}
""")
        self.mode.setEnabled(False)
        self.quality.setEnabled(False)

    def invalidate(self):
        self.info = None
        self.download.setEnabled(False)
        self.quality.clear()
        self.title.setText('Your next good find goes here.')
        self.mode.setEnabled(False)
        self.quality.setEnabled(False)
        self.bar.setValue(0)

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
        self.mode.setEnabled(not enabled and self.info is not None)
        self.quality.setEnabled(not enabled and self.info is not None)
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
        if self.task and self.task.isRunning():
            return
        url = self.url.text().strip()
        if not url:
            self.status.setText('Paste a public video link to get started.')
            self.url.setFocus()
            return
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
            self.destination.setText('Save folder selected · Change…')
            self.destination.setToolTip(folder)

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
    if '--self-test' in sys.argv:
        import unittest
        import test_download
        with open('framedrop-self-test.txt', 'w', encoding='utf-8') as report:
            result = unittest.TextTestRunner(stream=report).run(unittest.defaultTestLoader.loadTestsFromModule(test_download))
        sys.exit(0 if result.wasSuccessful() else 1)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    if '--smoke-test' in sys.argv:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(500, app.quit)
    sys.exit(app.exec())
