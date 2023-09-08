# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import sys
import sysrsync

from PySide6.QtCore import QFile, QIODevice, QTextStream, Qt, Slot
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
                               QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMessageBox, QPushButton, QRadioButton, QCheckBox, QTextEdit,
                               QVBoxLayout, QWidget)


class SortedDict(dict):
    class Iterator(object):
        def __init__(self, sorted_dict):
            self._dict = sorted_dict
            self._keys = sorted(self._dict.keys())
            self._nr_items = len(self._keys)
            self._idx = 0

        def __iter__(self):
            return self

        def next(self):
            if self._idx >= self._nr_items:
                raise StopIteration

            key = self._keys[self._idx]
            value = self._dict[key]
            self._idx += 1

            return key, value

        __next__ = next

    def __iter__(self):
        return SortedDict.Iterator(self)

    iterkeys = __iter__


class destBook(QWidget):
    NavigationMode, AddingMode, EditingMode = range(3)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.contacts = SortedDict()
        self._old_name = ''
        self._old_dest = ''
        self._current_mode = self.NavigationMode

        src_label = QLabel("* Source:")
        self._src_text = QLineEdit()

        self._load_button = QPushButton("&Load...")
        self._load_button.setToolTip("Load file/folder")
        
        srv_label = QLabel("* User@SSH_server:")
        self._srv_text = QLineEdit()

        dest_label = QLabel("* Destination:")
        self._dest_text = QLineEdit()

        pkey_label = QLabel("Private key:")
        self._pkey_text = QLineEdit()

        self._load2_button = QPushButton("&Load...")
        self._load2_button.setToolTip("Load private key")

        sync_label = QLabel("Sync:")
        self._wf_button = QRadioButton("Whole folder")
        self._co_button = QRadioButton("Contents only")
        
        options_label = QLabel("Options:")
        self._option0 = QCheckBox("Archive (-a)")
        self._option0.setToolTip("Recursive, symlinked, preserved perms, mod times, groups, owners")
        
        self._option1 = QCheckBox("Verbose (-v)")
        self._option1.setToolTip("Increase output verbosity")
        
        rsh_label = QLabel("RSH Port:")
        self._rsh_text = QLineEdit()
        
        host_label = QLabel("Host key checking: ")
        self._host_button = QCheckBox("on / off")
        
        self._send_button = QPushButton("&Send...")
        self._send_button.setToolTip("Send file/folder")
                
        self._load_button.clicked.connect(self.load_file_folder)
        self._load2_button.clicked.connect(self.load_pkey)
        self._send_button.clicked.connect(self.send)
        
        button_layout_1 = QHBoxLayout()
        button_layout_1.addWidget(self._co_button)
        button_layout_1.addWidget(self._wf_button)
        
        button_layout_2 = QHBoxLayout()
        button_layout_2.addWidget(self._option0)
        button_layout_2.addWidget(self._option1)        

        main_layout = QGridLayout()
        main_layout.addWidget(src_label, 0, 0)
        main_layout.addWidget(self._src_text, 0, 1)
        main_layout.addWidget(srv_label, 1, 0)
        main_layout.addWidget(self._srv_text, 1, 1)
        main_layout.addWidget(dest_label, 2, 0)
        main_layout.addWidget(self._dest_text, 2, 1)
        main_layout.addWidget(pkey_label, 3, 0)
        main_layout.addWidget(self._pkey_text, 3, 1)
        main_layout.addWidget(rsh_label, 4, 0)
        main_layout.addWidget(self._rsh_text, 4, 1)
        main_layout.addWidget(sync_label, 5, 0)
        main_layout.addWidget(options_label, 6, 0)      
        main_layout.addWidget(host_label, 7, 0)
        
        main_layout.addWidget(self._load_button, 0, 2)
        main_layout.addWidget(self._load2_button, 3, 2)
        main_layout.addWidget(self._host_button, 7, 1)
        main_layout.addWidget(self._send_button, 7, 2)
        main_layout.addLayout(button_layout_1, 5, 1)
        main_layout.addLayout(button_layout_2, 6, 1)

        self.setLayout(main_layout)
        self.setWindowTitle("Rsync GUI")

    def load_file_folder(self):
        file_name = QFileDialog.getOpenFileName(
            self, "Load file / folder")
        
        self._src_text.setText(file_name[0])
    
    def load_pkey(self):
        file_name = QFileDialog.getOpenFileName(
            self, "Load private key")
        
        self._pkey_text.setText(file_name[0])
    
    def send(self):
        if self._co_button.isChecked():
            sync = True
        elif self._wf_button.isChecked():
            sync = False
            
        options = []
        if self._option0.isChecked():
            options.append('-a')
        if self._option1.isChecked():
            options.append('-v')
        print(options)
        
        if self._host_button.isChecked():
            key = True
        else: key = False
            
        sysrsync.run(source = self._src_text.text(),
             destination = self._dest_text.text(),
             destination_ssh = self._srv_text.text(),
             exclusions = [],
             sync_source_contents = sync,
             options = options,
             private_key = self._pkey_text.text(),
             rsh_port = self._rsh_text.text(),
             strict_host_key_checking = key
            )
            
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    dest_book = destBook()
    dest_book.show()

    sys.exit(app.exec())