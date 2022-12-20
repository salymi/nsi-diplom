# -*- coding: cp1251 -*-
from flask_table import Table, Col, LinkCol


# Для создания таблицы

# таблица TURN_OFF_NODE
class Results(Table):
    NAME = Col('Имя')
    IP_NODE = Col('IP')
    COMMENT = Col('Коментарий')
    edit = LinkCol('Изменить', 'turnedit', url_kwargs=dict(NAME='NAME'))
    delete = LinkCol('Удалить', 'deleteturn', url_kwargs=dict(NAME='NAME'))

# таблица LINKS
class ResultsLinks(Table):
    ID_LINK = Col('ID')
    LINK = Col('Ссылка')
    ID_GROUP = Col('id группы')
    edit = LinkCol('Изменить', 'linksedit', url_kwargs=dict(ID_LINK='ID_LINK'))
    delete = LinkCol('Удалить', 'deletelinks', url_kwargs=dict(ID_LINK='ID_LINK'))

# таблица NODE
class ResultsNode(Table):
    ID_NODE = Col('ID')
    NODE_NAME = Col('Имя')
    IP = Col('IP')
    ID_GROUP = Col('id группы')
    edit = LinkCol('Изменить', 'nodeedit', url_kwargs=dict(ID_NODE='ID_NODE'))
    delete = LinkCol('Удалить', 'deletenode', url_kwargs=dict(ID_NODE='ID_NODE'))

# таблица EVENTMAP
class ResultsSituat(Table):
    SITUATION_ID = Col('Ситуация')
    MSG = Col('Текст оповещения')
    APP_LABLE = Col('Система')
    edit = LinkCol('Изменить', 'situatedit', url_kwargs=dict(SITUATION_ID='SITUATION_ID'))
    delete = LinkCol('Удалить', 'deletesituat', url_kwargs=dict(SITUATION_ID='SITUATION_ID'))

# таблица GROUP
class ResultsGroup(Table):
    ID_GROUP = Col('id')
    NAME_GROUP = Col('Имя группы')
    FLAG = Col('Инцедент флаг')
    NOTES = Col('Коментарий')
    edit = LinkCol('Изменить', 'groupedit', url_kwargs=dict(ID_GROUP='ID_GROUP'))
    delete = LinkCol('Удалить', 'deletegroup', url_kwargs=dict(ID_GROUP='ID_GROUP'))

class ResultAudit(Table):
    __tablename__ = "SERV_AUD"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = Col('Имя агента')
    NODE_NAME = Col('Имя сервера')
    IP = Col('IP')
    HOST_INFO = Col('Информация о сервере')
    PRODUCT = Col('Продукт')
    THRUNODE = Col('RTEMS')
    VERSION = Col('Версия')
    STATUS = Col('статус агента')
    EMAIL = Col('email')
    TELEPHONE = Col('телефон')
    EMAIL_VID_ENG = Col('email видеоинженеров')
    TELEP_VID_ENG = Col('телефон видеоинженеров')
    DEPART = Col('Отдел')
    SERVICE_KE = Col('Сервис')
    WORGROUP = Col('Рабочая группа')
    INCIDENT_FLAG = Col('Инцидент флаг')
    TELEGRAM = Col('Телеграм')
    TELEG_VID_ENG = Col('Телеграм видеоинженеров')
    edit = LinkCol('Изменить', 'auditedit', url_kwargs=dict(AGENT_NAME='AGENT_NAME'))
    delete = LinkCol('Удалить', 'deleteaudit', url_kwargs=dict(AGENT_NAME='AGENT_NAME'))

class ResultFTsit(Table):
    __tablename__ = "SERV_SIT"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = Col('Имя агента')
    SITUATION_ID = Col('Ситуация')
    EMAIL = Col('email')
    TELEPHONE = Col('телефон')
    EMAIL_VID_ENG = Col('email видеоинженеров')
    TELEP_VID_ENG = Col('телефон видеоинженеров')
    DEPART = Col('Отдел')
    SERVICE_KE = Col('Сервис')
    WORGROUP = Col('Рабочая группа')
    FLAG_GRAFANA = Col('Флаг(дашборд)')
    TELEGRAM = Col('Телеграм')
    TELEG_VID_ENG = Col('Телеграм видеоинженеров')
    DEPART_GRAF = Col('Отдел(дашборд)')
    edit = LinkCol('Изменить', 'ftsitedit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('Удалить', 'deleteftsit', url_kwargs=dict(ID='ID'))


class ResultIcmp(Table):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = Col('Сервер')
    DESCRIPTION = Col('Описание')
    EMAIL = Col('email')
    TELEPHONE = Col('Телефон')
    EMAIL_VID_ENG = Col('email видеоинженеров')
    TELEP_VID_ENG = Col('Телефон видеоинженеров')
    DEPART = Col('Отдел')
    SERVICE_KE = Col('Сервис')
    WORGROUP = Col('Рабочая группа')
    INCIDENT_FLAG = Col('Инцидент флаг')
    TELEGRAM = Col('Телеграм')
    TELEG_VID_ENG = Col('Телеграм видеоинженеров')
    PROFILE = Col('Профиль')
    FLAG_GRAFANA = Col('Флаг(дашборд)')
    DEPART_GRAF = Col('Отдел(дашборд)')
    edit = LinkCol('Изменить', 'icmpedit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('Удалить', 'deleteicmp', url_kwargs=dict(ID='ID'))

class ResultTcpport(Table):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = Col('Сервер')
    PORT = Col('Порт')
    PROFILE = Col('Профиль')
    DESCRIPTION = Col('Описание')
    EMAIL = Col('email')
    TELEPHONE = Col('Телефон')
    EMAIL_VID_ENG = Col('email видеоинженеров')
    TELEP_VID_ENG = Col('Телефон видеоинженеров')
    DEPART = Col('Отдел')
    SERVICE_KE = Col('Сервис')
    WORGROUP = Col('Рабочая группа')
    INCIDENT_FLAG = Col('Инцидент флаг')
    TELEGRAM = Col('Телеграм')
    TELEG_VID_ENG = Col('Телеграм видеоинженеров')
    FLAG_GRAFANA = Col('Флаг(дашборд)')
    DEPART_GRAF = Col('Отдел(дашборд)')
    edit = LinkCol('Изменить', 'tcpportedit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('Удалить', 'deletetcpport', url_kwargs=dict(ID='ID'))

class ResultWebl(Table):
    __tablename__ = "WEBLIN"
    __table_args__ = {'schema': 'ITMDATA'}
    URL = Col('Ссылка')
    PROFILE = Col('Профиль')
    DESCRIPTION = Col('Описпние')
    TABLE = Col('Протокол')
    EMAIL = Col('email')
    TELEPHONE = Col('Телефон')
    SERVICE_KE = Col('Сервис')
    DEPART = Col('Отдел')
    INCIDENT_FLAG = Col('Инцидент флаг')
    EMAIL_VID_ENG = Col('email видеоинженеров')
    TELEP_VID_ENG = Col('Телефон видеоинженеров')
    TELEGRAM = Col('Телеграм')
    TELEG_VID_ENG = Col('Телеграм видеоинженеров')
    FLAG_GRAFANA = Col('Флаг(дашборд)')
    DEPART_GRAF = Col('Отдел(дашборд)')
    edit = LinkCol('Изменить', 'webledit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('Удалить', 'deletewebl', url_kwargs=dict(ID='ID'))