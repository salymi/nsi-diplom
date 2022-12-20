# forms.py
# -*- coding: cp1251 -*-
from wtforms import Form, StringField, SelectField



# для поиска
# таблица TURN_OFF_NODE
class TurnSearchForm(Form):
    choices = [('NAME', 'Имени'),
               ('IP_NODE', 'IP'),
               ('COMMENT', 'Коментарию')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')


# таблица LINKS
class LinkSearch(Form):
    choices = [('LINK', 'Ссылкe')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')

# таблица NODE
class NodeSearch(Form):
    choices = [('NODE_NAME', 'Имени'),
               ('IP', 'IP')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')

# таблица EVENTMAP
class SituatSearch(Form):
    choices = [('SITUATION_ID', 'Ситуации'),
               ('MSG', 'Тексту оповещения'),
               ('APP_LABEL', 'Системе')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')

# таблица GROUP
class GroupSearch(Form):
    choices = [('NAME_GROUP', 'Имени группы'),
               ('FLAG', 'Флагу'),
               ('NOTES', 'Комментарию')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')

# таблица SERV_AUD
class AuditSearch(Form):
    choices = [('AGENT_NAME', 'Имени агента'),
               ('NODE_NAME', 'Имени сервера'),
               ('IP', 'IP'),
               ('EMAIL', 'email'),
               ('TELEPHONE', 'Телефону'),
               ('DEAPRT', 'Отделу'),
               ('INCIDENT_FLAG', 'Инцидент флагу'),
               ('TELEGRAM', 'Телеграму')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')


# таблица SERV_SIT
class FTsitSearch(Form):
    choices = [('AGENT_NAME', 'Имени агента'),
               ('SITUATION_ID', 'Ситуации'),
               ('EMAIL', 'email'),
               ('TELEPHONE', 'Телефону'),
               ('DEOART', 'Отделу'),
               ('FLAG_GRAFANA', 'Флагу(дашборд)'),
               ('TELEGRAM', 'Телеграму'),
               ('DEPART_GRAFAN', 'Отделу(Дашборд)')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')

# таблица ICMP
class IcmpSearch(Form):
    choices = [('SERVER', 'Имени агента'),
               ('DESCRIPTION', 'Описанию'),
               ('EMAIL', 'email'),
               ('TELEPHONE', 'Телефону'),
               ('DEPART', 'Отделу'),
               ('INCIDENT_FLAG', 'Инцидент флагу'),
               ('TELEGRAM', 'Телеграму'),
               ('PROFILE', 'Профаил'),
               ('FLAG_GRAFANA', 'Флагу(дашборд)'),
               ('DEPART_GRAFAN', 'Отделу(Дашборд)')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')

class TcpportSearch(Form):
    choices = [('SERVER', 'Имени агента'),
               ('PORT', 'Порту'),
               ('PROFILE', 'Профилю'),
               ('DESCRIPTION', 'Описанию'),
               ('EMAIL', 'email'),
               ('TELEPHONE', 'Телефону'),
               ('DEPART', 'Отделу'),
               ('INCIDENT_FLAG', 'Инцидент флагу'),
               ('TELEGRAM', 'Телеграму'),
               ('FLAG_GRAFANA', 'Флагу(дашборд)'),
               ('DEPART_GRAFAN', 'Отделу(Дашборд)')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')

class WeblSearch(Form):
    choices = [('URL', 'Имени агента'),
               ('PROFILE', 'Профилю'),
               ('DESCRIPTION', 'Описанию'),
               ('TABLE', 'Протокол'),
               ('EMAIL', 'email'),
               ('TELEPHONE', 'Телефону'),
               ('DEPART', 'Отделу'),
               ('INCIDENT_FLAG', 'Инцидент флагу'),
               ('TELEGRAM', 'Телеграму'),
               ('FLAG_GRAFANA', 'Флагу(дашборд)'),
               ('DEPART_GRAFAN', 'Отделу(Дашборд)')]
    select = SelectField('Поиск по:', choices=choices)
    search = StringField('')


# добавления, изменения, удаления
class TurnForm(Form):
    __tablename__ = 'TURN_OFF_NODE'
    __table_args__ = {'schema': 'ITMDATA'}
    NAME = StringField('Имя')
    IP_NODE = StringField('IP')
    COMMENT = StringField('Коментарий(обязательно к заполнению!)')


class LinksFrom(Form):
    __tablename__ = "LINKS"
    __table_args__ = {'schema': 'ITMDATA'}
    LINK = StringField('Ссылка')
    ID_GROUP = SelectField('флаг')
    ID_LINK = StringField('id ссылки')

class NodeFrom(Form):
    __tablename__ = "NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_NODE = StringField('id сервера')
    NODE_NAME = StringField('Имя')
    IP = StringField('IP')
    ID_GROUP = StringField('id группы')

class SituatFrom(Form):
    __tablename__ = "EVENTMAP"
    __table_args__ = {'schema': 'ITMDATA'}
    SITUATION_ID = StringField('Ситуация')
    MSG = StringField('Текст оповещения')
    APP_LABLE = StringField('Система')

class GroupFrom(Form):
    __tablename__ = "GROUP"
    __table_args__ = {'schema': 'ITMDATA'}
    NAME_GROUP = StringField('Имя группы')
    FLAG = [('0', '0'),
            ('1', '1')]
    FLAG = SelectField('флаг', choices=FLAG)
    NOTES = StringField('Комментарий')


class AuditForm(Form):
    __tablename__ = "SERV_AUD"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = StringField('Имя агента')
    NODE_NAME = StringField('Имя сервера')
    IP = StringField('IP')
    HOST_INFO = StringField('Информация о сервере')
    PRODUCT = StringField('Продукт')
    THRUNODE = StringField('На каком RTEMSE мониторится')
    VERSION = StringField('Версия')
    STATUS = [('Y', 'включен'),
              ('N', 'выключен')]
    STATUS = SelectField('Статус агента', choices=STATUS)
    EMAIL = StringField('email')
    TELEPHONE = StringField('Телефон')
    EMAIL_VID_ENG = StringField('email видеоинженеров')
    TELEP_VID_ENG = StringField('Телефон видеоинженеров')
    DEPART = StringField('Отдел')
    SERVICE_KE = StringField('Сервис')
    WORGROUP = StringField('Рабочая группа')
    INCIDENT_FLAG = [('0', '0'),
                    ('1', '1')]
    INCIDENT_FLAG = SelectField('Инцидент флаг', choices=INCIDENT_FLAG)
    TELEGRAM = StringField('Телеграм')
    TELEG_VID_ENG = StringField('Телеграм видеоинженеров')


class FTsitForm(Form):
    __tablename__ = "SERV_SIT"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = StringField('Имя агента')

    SITUATION_ID = StringField('Ситуация')
    EMAIL = StringField('email')
    TELEPHONE = StringField('телефон')
    EMAIL_VID_ENG = StringField('email видеоинженеров')
    TELEP_VID_ENG = StringField('Телефон видеоинженеров')
    DEPART = StringField('Отдел')
    SERVICE_KE = StringField('Сервис')
    WORGROUP = StringField('Сервис')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('Флаг(дашборд)', choices=FLAG_GRAFANA)
    TELEGRAM = StringField('Телеграм')
    TELEG_VID_ENG = StringField('Телеграм видеоинженеров')
    DEPART_GRAF = StringField('Отдел(дашборд)')

class IcmpForm(Form):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = StringField('Сервер')
    DESCRIPTION = StringField('Описание')
    EMAIL = StringField('email')
    TELEPHONE = StringField('Телефон')
    EMAIL_VID_ENG = StringField('email видеоинжинеров')
    TELEP_VID_ENG = StringField('email видеоинжинеров')
    DEPART = StringField('Отдел')
    SERVICE_KE = StringField('Сервис')
    WORGROUP = StringField('Рабочая группа')
    INCIDENT_FLAG = [('0', '0'),
                    ('1', '1')]
    INCIDENT_FLAG = SelectField('Инцидент флаг', choices=INCIDENT_FLAG)
    TELEGRAM = StringField('Телеграм')
    TELEG_VID_ENG = StringField('Телеграм видеоинженеров')
    PROFILE = StringField('Профаил')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('флаг(дашборд)', choices=FLAG_GRAFANA)
    DEPART_GRAF = StringField('Отдел(дашборд)')

class TcpportForm(Form):
    __tablename__ = "TCPPORT"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = StringField('Сервер')
    PORT = StringField('Порт')
    PROFILE = StringField('Профиль')
    DESCRIPTION = StringField('Описание')
    EMAIL = StringField('email')
    TELEPHONE = StringField('Телефон')
    EMAIL_VID_ENG = StringField('email видеоинжинеров')
    TELEP_VID_ENG = StringField('Телефон видеоинжинеров')
    DEPART = StringField('Отдел')
    SERVICE_KE = StringField('Сервис')
    WORGROUP = StringField('Рабочая группа')
    INCIDENT_FLAG = [('0', '0'),
                    ('1', '1')]
    INCIDENT_FLAG = SelectField('Инцидент флаг', choices=INCIDENT_FLAG)
    TELEGRAM = StringField('Телеграм')
    TELEG_VID_ENG = StringField('Телеграм видеоинженеров')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('Флаг(дашборд)', choices=FLAG_GRAFANA)
    DEPART_GRAF = StringField('Отдел(дашборд)')

class WeblForm(Form):
    __tablename__ = "WEBLIN"
    __table_args__ = {'schema': 'ITMDATA'}
    URL = StringField('Сервер')
    PROFILE = StringField('Профиль')
    DESCRIPTION = StringField('Описание')
    TABLE = StringField('Протокол')
    EMAIL = StringField('email')
    TELEPHONE = StringField('Телефон')
    SERVICE_KE = StringField('Сервис')
    DEPART = StringField('Отдел')
    INCIDENT_FLAG = [('0', '0'),
                     ('1', '1')]
    INCIDENT_FLAG = SelectField('Инцидент флаг', choices=INCIDENT_FLAG)
    EMAIL_VID_ENG = StringField('email видеоинжинеров')
    TELEP_VID_ENG = StringField('Телефон видеоинжинеров')
    TELEGRAM = StringField('Телеграм')
    TELEG_VID_ENG = StringField('Телеграм видеоинженеров')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('Флаг(дашборд)', choices=FLAG_GRAFANA)
    DEPART_GRAF = StringField('Отдел(дашборд)')
