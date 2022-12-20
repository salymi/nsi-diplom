# forms.py
# -*- coding: cp1251 -*-
from wtforms import Form, StringField, SelectField



# ��� ������
# ������� TURN_OFF_NODE
class TurnSearchForm(Form):
    choices = [('NAME', '�����'),
               ('IP_NODE', 'IP'),
               ('COMMENT', '����������')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')


# ������� LINKS
class LinkSearch(Form):
    choices = [('LINK', '�����e')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')

# ������� NODE
class NodeSearch(Form):
    choices = [('NODE_NAME', '�����'),
               ('IP', 'IP')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')

# ������� EVENTMAP
class SituatSearch(Form):
    choices = [('SITUATION_ID', '��������'),
               ('MSG', '������ ����������'),
               ('APP_LABEL', '�������')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')

# ������� GROUP
class GroupSearch(Form):
    choices = [('NAME_GROUP', '����� ������'),
               ('FLAG', '�����'),
               ('NOTES', '�����������')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')

# ������� SERV_AUD
class AuditSearch(Form):
    choices = [('AGENT_NAME', '����� ������'),
               ('NODE_NAME', '����� �������'),
               ('IP', 'IP'),
               ('EMAIL', 'email'),
               ('TELEPHONE', '��������'),
               ('DEAPRT', '������'),
               ('INCIDENT_FLAG', '�������� �����'),
               ('TELEGRAM', '���������')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')


# ������� SERV_SIT
class FTsitSearch(Form):
    choices = [('AGENT_NAME', '����� ������'),
               ('SITUATION_ID', '��������'),
               ('EMAIL', 'email'),
               ('TELEPHONE', '��������'),
               ('DEOART', '������'),
               ('FLAG_GRAFANA', '�����(�������)'),
               ('TELEGRAM', '���������'),
               ('DEPART_GRAFAN', '������(�������)')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')

# ������� ICMP
class IcmpSearch(Form):
    choices = [('SERVER', '����� ������'),
               ('DESCRIPTION', '��������'),
               ('EMAIL', 'email'),
               ('TELEPHONE', '��������'),
               ('DEPART', '������'),
               ('INCIDENT_FLAG', '�������� �����'),
               ('TELEGRAM', '���������'),
               ('PROFILE', '�������'),
               ('FLAG_GRAFANA', '�����(�������)'),
               ('DEPART_GRAFAN', '������(�������)')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')

class TcpportSearch(Form):
    choices = [('SERVER', '����� ������'),
               ('PORT', '�����'),
               ('PROFILE', '�������'),
               ('DESCRIPTION', '��������'),
               ('EMAIL', 'email'),
               ('TELEPHONE', '��������'),
               ('DEPART', '������'),
               ('INCIDENT_FLAG', '�������� �����'),
               ('TELEGRAM', '���������'),
               ('FLAG_GRAFANA', '�����(�������)'),
               ('DEPART_GRAFAN', '������(�������)')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')

class WeblSearch(Form):
    choices = [('URL', '����� ������'),
               ('PROFILE', '�������'),
               ('DESCRIPTION', '��������'),
               ('TABLE', '��������'),
               ('EMAIL', 'email'),
               ('TELEPHONE', '��������'),
               ('DEPART', '������'),
               ('INCIDENT_FLAG', '�������� �����'),
               ('TELEGRAM', '���������'),
               ('FLAG_GRAFANA', '�����(�������)'),
               ('DEPART_GRAFAN', '������(�������)')]
    select = SelectField('����� ��:', choices=choices)
    search = StringField('')


# ����������, ���������, ��������
class TurnForm(Form):
    __tablename__ = 'TURN_OFF_NODE'
    __table_args__ = {'schema': 'ITMDATA'}
    NAME = StringField('���')
    IP_NODE = StringField('IP')
    COMMENT = StringField('����������(����������� � ����������!)')


class LinksFrom(Form):
    __tablename__ = "LINKS"
    __table_args__ = {'schema': 'ITMDATA'}
    LINK = StringField('������')
    ID_GROUP = SelectField('����')
    ID_LINK = StringField('id ������')

class NodeFrom(Form):
    __tablename__ = "NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_NODE = StringField('id �������')
    NODE_NAME = StringField('���')
    IP = StringField('IP')
    ID_GROUP = StringField('id ������')

class SituatFrom(Form):
    __tablename__ = "EVENTMAP"
    __table_args__ = {'schema': 'ITMDATA'}
    SITUATION_ID = StringField('��������')
    MSG = StringField('����� ����������')
    APP_LABLE = StringField('�������')

class GroupFrom(Form):
    __tablename__ = "GROUP"
    __table_args__ = {'schema': 'ITMDATA'}
    NAME_GROUP = StringField('��� ������')
    FLAG = [('0', '0'),
            ('1', '1')]
    FLAG = SelectField('����', choices=FLAG)
    NOTES = StringField('�����������')


class AuditForm(Form):
    __tablename__ = "SERV_AUD"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = StringField('��� ������')
    NODE_NAME = StringField('��� �������')
    IP = StringField('IP')
    HOST_INFO = StringField('���������� � �������')
    PRODUCT = StringField('�������')
    THRUNODE = StringField('�� ����� RTEMSE �����������')
    VERSION = StringField('������')
    STATUS = [('Y', '�������'),
              ('N', '��������')]
    STATUS = SelectField('������ ������', choices=STATUS)
    EMAIL = StringField('email')
    TELEPHONE = StringField('�������')
    EMAIL_VID_ENG = StringField('email ��������������')
    TELEP_VID_ENG = StringField('������� ��������������')
    DEPART = StringField('�����')
    SERVICE_KE = StringField('������')
    WORGROUP = StringField('������� ������')
    INCIDENT_FLAG = [('0', '0'),
                    ('1', '1')]
    INCIDENT_FLAG = SelectField('�������� ����', choices=INCIDENT_FLAG)
    TELEGRAM = StringField('��������')
    TELEG_VID_ENG = StringField('�������� ��������������')


class FTsitForm(Form):
    __tablename__ = "SERV_SIT"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = StringField('��� ������')

    SITUATION_ID = StringField('��������')
    EMAIL = StringField('email')
    TELEPHONE = StringField('�������')
    EMAIL_VID_ENG = StringField('email ��������������')
    TELEP_VID_ENG = StringField('������� ��������������')
    DEPART = StringField('�����')
    SERVICE_KE = StringField('������')
    WORGROUP = StringField('������')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('����(�������)', choices=FLAG_GRAFANA)
    TELEGRAM = StringField('��������')
    TELEG_VID_ENG = StringField('�������� ��������������')
    DEPART_GRAF = StringField('�����(�������)')

class IcmpForm(Form):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = StringField('������')
    DESCRIPTION = StringField('��������')
    EMAIL = StringField('email')
    TELEPHONE = StringField('�������')
    EMAIL_VID_ENG = StringField('email ��������������')
    TELEP_VID_ENG = StringField('email ��������������')
    DEPART = StringField('�����')
    SERVICE_KE = StringField('������')
    WORGROUP = StringField('������� ������')
    INCIDENT_FLAG = [('0', '0'),
                    ('1', '1')]
    INCIDENT_FLAG = SelectField('�������� ����', choices=INCIDENT_FLAG)
    TELEGRAM = StringField('��������')
    TELEG_VID_ENG = StringField('�������� ��������������')
    PROFILE = StringField('�������')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('����(�������)', choices=FLAG_GRAFANA)
    DEPART_GRAF = StringField('�����(�������)')

class TcpportForm(Form):
    __tablename__ = "TCPPORT"
    __table_args__ = {'schema': 'ITMDATA'}
    SERVER = StringField('������')
    PORT = StringField('����')
    PROFILE = StringField('�������')
    DESCRIPTION = StringField('��������')
    EMAIL = StringField('email')
    TELEPHONE = StringField('�������')
    EMAIL_VID_ENG = StringField('email ��������������')
    TELEP_VID_ENG = StringField('������� ��������������')
    DEPART = StringField('�����')
    SERVICE_KE = StringField('������')
    WORGROUP = StringField('������� ������')
    INCIDENT_FLAG = [('0', '0'),
                    ('1', '1')]
    INCIDENT_FLAG = SelectField('�������� ����', choices=INCIDENT_FLAG)
    TELEGRAM = StringField('��������')
    TELEG_VID_ENG = StringField('�������� ��������������')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('����(�������)', choices=FLAG_GRAFANA)
    DEPART_GRAF = StringField('�����(�������)')

class WeblForm(Form):
    __tablename__ = "WEBLIN"
    __table_args__ = {'schema': 'ITMDATA'}
    URL = StringField('������')
    PROFILE = StringField('�������')
    DESCRIPTION = StringField('��������')
    TABLE = StringField('��������')
    EMAIL = StringField('email')
    TELEPHONE = StringField('�������')
    SERVICE_KE = StringField('������')
    DEPART = StringField('�����')
    INCIDENT_FLAG = [('0', '0'),
                     ('1', '1')]
    INCIDENT_FLAG = SelectField('�������� ����', choices=INCIDENT_FLAG)
    EMAIL_VID_ENG = StringField('email ��������������')
    TELEP_VID_ENG = StringField('������� ��������������')
    TELEGRAM = StringField('��������')
    TELEG_VID_ENG = StringField('�������� ��������������')
    FLAG_GRAFANA = [('0', '0'),
                    ('1', '1')]
    FLAG_GRAFANA = SelectField('����(�������)', choices=FLAG_GRAFANA)
    DEPART_GRAF = StringField('�����(�������)')
