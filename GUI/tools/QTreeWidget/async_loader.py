import asyncio
from PyQt5.QtWidgets import QFileSystemModel
import os
import env




async def async_show_all_tabs(geo_tw, mark_tw, proj_tw, other_tw):
    await asyncio.gather(geo(geo_tw),
                         mark(mark_tw),
                         proj(proj_tw),
                         other(other_tw))

async def async_show_geo_other_tabs(geo_tw, other_tw):
    await asyncio.gather(bm_geo(geo_tw), bm_other(other_tw))



async def geo(treewidget):
    'Загрузка дерева проводника Геология с учетом заданных фильтров'
    print('Загружено дерево: geo')
    # try:
        

    # except Exception as e:
    #     print(e)

        
async def mark(treewidget):
    'Загрузка дерева проводника Маркшейдерия с учетом заданных фильтров'
    print('Загружено дерево: mark')


async def proj(treewidget):
    'Загрузка дерева проводника Проектирование с учетом заданных фильтров'
    print('Загружено дерево: proj')


async def other(treewidget):
    'Загрузка дерева проводника Прочее/другое с учетом заданных фильтров, по умолчанию корень - Рабочий стол'
    print('Загружено дерево: other')

    

async def bm_other(treewidget):
    'Загрузка дерева проводника Прочее/другое с учетом заданных фильтров (только БМ), по умолчанию корень - Рабочий стол'
    print('Загружено дерево: bm_other')


async def bm_geo(treewidget):
    'Загрузка дерева проводника Геология с учетом заданных фильтров (только БМ), по умолчанию корень - Рабочий стол'
    print('Загружено дерево: bm_geo')

