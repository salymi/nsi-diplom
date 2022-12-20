# -*- coding: cp1251 -*-
from flask_table import Table, Col, LinkCol


# ��� �������� �������

# ������� TURN_OFF_NODE
class Results(Table):
    NAME = Col('���')
    IP_NODE = Col('IP')
    COMMENT = Col('����������')
    edit = LinkCol('��������', 'turnedit', url_kwargs=dict(NAME='NAME'))
    delete = LinkCol('�������', 'deleteturn', url_kwargs=dict(NAME='NAME'))

# ������� LINKS
class ResultsLinks(Table):
    ID_LINK = Col('ID')
    LINK = Col('������')
    ID_GROUP = Col('id ������')
    edit = LinkCol('��������', 'linksedit', url_kwargs=dict(ID_LINK='ID_LINK'))
    delete = LinkCol('�������', 'deletelinks', url_kwargs=dict(ID_LINK='ID_LINK'))

# ������� NODE
class ResultsNode(Table):
    ID_NODE = Col('ID')
    NODE_NAME = Col('���')
    IP = Col('IP')
    ID_GROUP = Col('id ������')
    edit = LinkCol('��������', 'nodeedit', url_kwargs=dict(ID_NODE='ID_NODE'))
    delete = LinkCol('�������', 'deletenode', url_kwargs=dict(ID_NODE='ID_NODE'))

# ������� EVENTMAP
class ResultsSituat(Table):
    SITUATION_ID = Col('��������')
    MSG = Col('����� ����������')
    APP_LABLE = Col('�������')
    edit = LinkCol('��������', 'situatedit', url_kwargs=dict(SITUATION_ID='SITUATION_ID'))
    delete = LinkCol('�������', 'deletesituat', url_kwargs=dict(SITUATION_ID='SITUATION_ID'))

# ������� GROUP
class ResultsGroup(Table):
    ID_GROUP = Col('id')
    NAME_GROUP = Col('��� ������')
    FLAG = Col('�������� ����')
    NOTES = Col('����������')
    edit = LinkCol('��������', 'groupedit', url_kwargs=dict(ID_GROUP='ID_GROUP'))
    delete = LinkCol('�������', 'deletegroup', url_kwargs=dict(ID_GROUP='ID_GROUP'))

class ResultAudit(Table):
    __tablename__ = "SERV_AUD"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = Col('��� ������')
    NODE_NAME = Col('��� �������')
    IP = Col('IP')
    HOST_INFO = Col('���������� � �������')
    PRODUCT = Col('�������')
    THRUNODE = Col('RTEMS')
    VERSION = Col('������')
    STATUS = Col('������ ������')
    EMAIL = Col('email')
    TELEPHONE = Col('�������')
    EMAIL_VID_ENG = Col('email ��������������')
    TELEP_VID_ENG = Col('������� ��������������')
    DEPART = Col('�����')
    SERVICE_KE = Col('������')
    WORGROUP = Col('������� ������')
    INCIDENT_FLAG = Col('�������� ����')
    TELEGRAM = Col('��������')
    TELEG_VID_ENG = Col('�������� ��������������')
    edit = LinkCol('��������', 'auditedit', url_kwargs=dict(AGENT_NAME='AGENT_NAME'))
    delete = LinkCol('�������', 'deleteaudit', url_kwargs=dict(AGENT_NAME='AGENT_NAME'))

class ResultFTsit(Table):
    __tablename__ = "SERV_SIT"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = Col('��� ������')
    SITUATION_ID = Col('��������')
    EMAIL = Col('email')
    TELEPHONE = Col('�������')
    EMAIL_VID_ENG = Col('email ��������������')
    TELEP_VID_ENG = Col('������� ��������������')
    DEPART = Col('�����')
    SERVICE_KE = Col('������')
    WORGROUP = Col('������� ������')
    FLAG_GRAFANA = Col('����(�������)')
    TELEGRAM = Col('��������')
    TELEG_VID_ENG = Col('�������� ��������������')
    DEPART_GRAF = Col('�����(�������)')
    edit = LinkCol('��������', 'ftsitedit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('�������', 'deleteftsit', url_kwargs=dict(ID='ID'))


class ResultIcmp(Table):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = Col('������')
    DESCRIPTION = Col('��������')
    EMAIL = Col('email')
    TELEPHONE = Col('�������')
    EMAIL_VID_ENG = Col('email ��������������')
    TELEP_VID_ENG = Col('������� ��������������')
    DEPART = Col('�����')
    SERVICE_KE = Col('������')
    WORGROUP = Col('������� ������')
    INCIDENT_FLAG = Col('�������� ����')
    TELEGRAM = Col('��������')
    TELEG_VID_ENG = Col('�������� ��������������')
    PROFILE = Col('�������')
    FLAG_GRAFANA = Col('����(�������)')
    DEPART_GRAF = Col('�����(�������)')
    edit = LinkCol('��������', 'icmpedit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('�������', 'deleteicmp', url_kwargs=dict(ID='ID'))

class ResultTcpport(Table):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = Col('������')
    PORT = Col('����')
    PROFILE = Col('�������')
    DESCRIPTION = Col('��������')
    EMAIL = Col('email')
    TELEPHONE = Col('�������')
    EMAIL_VID_ENG = Col('email ��������������')
    TELEP_VID_ENG = Col('������� ��������������')
    DEPART = Col('�����')
    SERVICE_KE = Col('������')
    WORGROUP = Col('������� ������')
    INCIDENT_FLAG = Col('�������� ����')
    TELEGRAM = Col('��������')
    TELEG_VID_ENG = Col('�������� ��������������')
    FLAG_GRAFANA = Col('����(�������)')
    DEPART_GRAF = Col('�����(�������)')
    edit = LinkCol('��������', 'tcpportedit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('�������', 'deletetcpport', url_kwargs=dict(ID='ID'))

class ResultWebl(Table):
    __tablename__ = "WEBLIN"
    __table_args__ = {'schema': 'ITMDATA'}
    URL = Col('������')
    PROFILE = Col('�������')
    DESCRIPTION = Col('��������')
    TABLE = Col('��������')
    EMAIL = Col('email')
    TELEPHONE = Col('�������')
    SERVICE_KE = Col('������')
    DEPART = Col('�����')
    INCIDENT_FLAG = Col('�������� ����')
    EMAIL_VID_ENG = Col('email ��������������')
    TELEP_VID_ENG = Col('������� ��������������')
    TELEGRAM = Col('��������')
    TELEG_VID_ENG = Col('�������� ��������������')
    FLAG_GRAFANA = Col('����(�������)')
    DEPART_GRAF = Col('�����(�������)')
    edit = LinkCol('��������', 'webledit', url_kwargs=dict(ID='ID'))
    delete = LinkCol('�������', 'deletewebl', url_kwargs=dict(ID='ID'))