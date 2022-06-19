# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 08:52:55 2022

@author: ahmet
"""

from PyQt5 import uic

with open('AnaSayfaUI.py', 'w', encoding="utf-8") as fout:
    uic.compileUi('AnaSayfaUI.ui', fout)  