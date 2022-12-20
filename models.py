# -*- coding: cp1251 -*-
from flask_login import UserMixin

from app import db, manager


class Turn(db.Model):
    __tablename__ = "TURN_OFF_NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    NAME = db.Column(db.String(64), primary_key=True)
    IP_NODE = db.Column(db.String(64))
    COMMENT = db.Column(db.String(128), nullable=False)

class Links(db.Model):
    __tablename__ = "LINKS"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_LINK = db.Column(db.Integer, primary_key=True)
    LINK = db.Column(db.String(512))
    ID_GROUP = db.Column(db.Integer)

    def __repr__(self):
        return "<{}>".format(self.ID_GROUP)

class Node(db.Model):
    __tablename__ = "NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_NODE = db.Column(db.Integer, primary_key=True)
    NODE_NAME = db.Column(db.String(64))
    IP = db.Column(db.String(64))
    ID_GROUP = db.Column(db.Integer)

    def __repr__(self):
        return "<{}>".format(self.ID_GROUP)

class Situat(db.Model):
    __tablename__ = "EVENTMAP"
    __table_args__ = {'schema': 'ITMDATA'}
    SITUATION_ID = db.Column(db.String(512), primary_key=True)
    MSG = db.Column(db.String(1000))
    APP_LABLE = db.Column(db.String(1000))


class Group(db.Model):
    __tablename__ = "GROUP"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_GROUP = db.Column(db.Integer, primary_key=True)
    NAME_GROUP = db.Column(db.String(64))
    FLAG = db.Column(db.Integer, nullable=False)
    NOTES = db.Column(db.String(64))

class GRLink(db.Model):
    __tablename__ = "GROUP_LINK"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_ST_LINK = db.Column(db.Integer, primary_key=True)
    ID_GROUP = db.Column(db.Integer)

    ID_LINK = db.Column(db.Integer, db.ForeignKey("ITMDATA.LINKS.ID_LINK"))
    link = db.relationship("Links", backref=db.backref(
        "ITMDATA.GROUP_LINK"), lazy=True)

class GRNode(db.Model):
    __tablename__ = "GROUP_NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_STR = db.Column(db.Integer, primary_key=True)
    ID_GROUP = db.Column(db.Integer)

    ID_NODE = db.Column(db.Integer, db.ForeignKey("ITMDATA.NODE.ID_NODE"))
    nod = db.relationship("Node", backref=db.backref(
        "ITMDATA.GROUP_NODE"), lazy=True)

class Audit(db.Model):
    __tablename__ = "SERV_AUD"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = db.Column(db.String(512), primary_key=True)
    NODE_NAME = db.Column(db.String(512), primary_key=True)
    IP = db.Column(db.String(512))
    HOST_INFO = db.Column(db.String(512))
    PRODUCT = db.Column(db.String(512))
    THRUNODE = db.Column(db.String(512))
    VERSION = db.Column(db.String(512))
    STATUS = db.Column(db.String(512))
    EMAIL = db.Column(db.String(1000))
    TELEPHONE = db.Column(db.String(1000))
    EMAIL_VID_ENG = db.Column(db.String(512))
    TELEP_VID_ENG = db.Column(db.String(512))
    DEPART = db.Column(db.String(512))
    SERVICE_KE = db.Column(db.String(512))
    WORGROUP = db.Column(db.String(512))
    INCIDENT_FLAG = db.Column(db.Integer, nullable=False)
    TELEGRAM = db.Column(db.String(1000))
    TELEG_VID_ENG = db.Column(db.String(512))

class FTsit(db.Model):
    __tablename__ = "SERV_SIT"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = db.Column(db.Integer, primary_key=True)
    AGENT_NAME = db.Column(db.String(512), nullable=False)
    SITUATION_ID = db.Column(db.String(128), nullable=False)
    EMAIL = db.Column(db.String(1000))
    TELEPHONE = db.Column(db.String(1000))
    EMAIL_VID_ENG = db.Column(db.String(512))
    TELEP_VID_ENG = db.Column(db.String(512))
    DEPART = db.Column(db.String(512))
    SERVICE_KE = db.Column(db.String(512))
    WORGROUP = db.Column(db.String(512))
    FLAG_GRAFANA = db.Column(db.Integer, nullable=False)
    TELEGRAM = db.Column(db.String(1000))
    TELEG_VID_ENG = db.Column(db.String(512))
    DEPART_GRAF = db.Column(db.String(512))

class Icmp(db.Model):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = db.Column(db.Integer, primary_key=True)
    SERVER = db.Column(db.String(512), nullable=False)
    DESCRIPTION = db.Column(db.String(64), nullable=False)
    EMAIL = db.Column(db.String(512))
    TELEPHONE = db.Column(db.String(512))
    EMAIL_VID_ENG = db.Column(db.String(128))
    TELEP_VID_ENG = db.Column(db.String(128))
    DEPART = db.Column(db.String(50))
    SERVICE_KE = db.Column(db.String(128))
    WORGROUP = db.Column(db.String(50))
    INCIDENT_FLAG = db.Column(db.Integer, nullable=False)
    TELEGRAM = db.Column(db.String(512))
    TELEG_VID_ENG = db.Column(db.String(512))
    PROFILE = db.Column(db.String(512))
    FLAG_GRAFANA = db.Column(db.Integer, nullable=False)
    DEPART_GRAF = db.Column(db.String(512))

class Tcpport(db.Model):
    __tablename__ = "TCPPORT"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = db.Column(db.Integer, primary_key=True)
    SERVER = db.Column(db.String(512), nullable=False)
    PORT = db.Column(db.String(10), nullable=False)
    PROFILE = db.Column(db.String(512))
    DESCRIPTION = db.Column(db.String(64))
    EMAIL = db.Column(db.String(512))
    TELEPHONE = db.Column(db.String(512))
    EMAIL_VID_ENG = db.Column(db.String(128))
    TELEP_VID_ENG = db.Column(db.String(128))
    DEPART = db.Column(db.String(50))
    SERVICE_KE = db.Column(db.String(128))
    WORGROUP = db.Column(db.String(50))
    INCIDENT_FLAG = db.Column(db.Integer, nullable=False)
    TELEGRAM = db.Column(db.String(512))
    TELEG_VID_ENG = db.Column(db.String(512))
    FLAG_GRAFANA = db.Column(db.Integer, nullable=False)
    DEPART_GRAF = db.Column(db.String(512))

class Webl(db.Model):
    __tablename__ = "WEBLIN"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(512), nullable=False)
    PROFILE = db.Column(db.String(512))
    DESCRIPTION = db.Column(db.String(64))
    TABLE = db.Column(db.String(512))
    EMAIL = db.Column(db.String(512))
    TELEPHONE = db.Column(db.String(512))
    SERVICE_KE = db.Column(db.String(128))
    DEPART = db.Column(db.String(50))
    INCIDENT_FLAG = db.Column(db.Integer, nullable=False)
    EMAIL_VID_ENG = db.Column(db.String(128))
    TELEP_VID_ENG = db.Column(db.String(128))
    TELEGRAM = db.Column(db.String(512))
    TELEG_VID_ENG = db.Column(db.String(512))
    FLAG_GRAFANA = db.Column(db.Integer, nullable=False)
    DEPART_GRAF = db.Column(db.String(512))

class User (db.Model, UserMixin):
    __tablename__ = "USER"
    __table_args__ = {'schema': 'ITMDATA'}
    id = db.Column(db.Integer, primary_key=True)
    LOGIN = db.Column(db.String(128), nullable=False, unique=True)
    PASSWORD = db.Column(db.String(128), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
