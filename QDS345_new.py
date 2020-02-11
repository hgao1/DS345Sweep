# -*- coding: utf-8 -*-

from common.QSettingsWidget import QSettingsWidget
from .DS345Settings_UI import Ui_DS345Settings
from .DS345SettingsSweep_UI import Ui_DS345SettingsSweep

class QDS345SettingsSweep(QSettingsWidget):

    '''Configuration for a Stanford Research Systems
    DS345 Function Generator With Sweep Function
    '''

    def __init__(self, parent=None, device=None):
        super(QDS345SettingsSweep, self).__init__(parent=parent,
                                             device=device,
                                             ui=Ui_DS345SettingsSweep())


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    from DS345 import DS345

    app = QApplication(sys.argv)
    try:
        device = DS345()
    except ValueError:
        device = None
    wid = QDS345SettingsSweep(device=device)
    wid.show()
    sys.exit(app.exec_())
