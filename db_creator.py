# -*- coding: cp1251 -*-
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('ibm_db_sa://db2admin:jesus@192.168.1.99:53590/TOOLSDB?charset=cp1251',
                       convert_unicode=True, encoding='cp1251', echo=True)
Base = declarative_base()


class Turn(Base):
    """
    Создание таблицы
    """
    __tablename__ = "TURN_OFF_NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    NAME = Column(String(64), primary_key=True)
    IP_NODE = Column(String(64))
    COMMENT = Column(String(128), nullable=False)


class Links(Base):
    __tablename__ = "LINKS"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_LINK = Column(Integer, primary_key=True)
    LINK = Column(String(512))
    ID_GROUP = Column(Integer)

    def __repr__(self):
        return "<Links: {}>".format(self.ID_GROUP)

class Situat(Base):
    __tablename__ = "EVENTMAP"
    __table_args__ = {'schema': 'ITMDATA'}
    SITUATION_ID = Column(String(512), primary_key=True)
    MSG = Column(String(1000))
    APP_LABLE = Column(String(1000))

class Group(Base):
    __tablename__ = "GROUP"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_GROUP = Column(Integer, primary_key=True)
    NAME_GROUP = Column(String(64))
    FLAG = Column(Integer, nullable=False)
    NOTES = Column(String(64))

class Node(Base):
    __tablename__ = "NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_NODE = Column(Integer, primary_key=True)
    NODE_NAME = Column(String(64))
    IP = Column(String(64))
    ID_GROUP = Column(Integer)

    def __repr__(self):
        return "<Node: {}>".format(self.ID_GROUP)

class GRLink(Base):
    __tablename__ = "GROUP_LINK"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_ST_LINK = Column(Integer, primary_key=True)
    ID_GROUP = Column(Integer)

    ID_LINK = Column(Integer, ForeignKey("ITMDATA.LINKS.ID_LINK"))
    link = relationship("Links", backref=backref(
        "ITMDATA.GROUP_LINK"))

class GRNode(Base):
    __tablename__ = "GROUP_NODE"
    __table_args__ = {'schema': 'ITMDATA'}
    ID_STR = Column(Integer, primary_key=True)
    ID_GROUP = Column(Integer)

    ID_NODE = Column(Integer, ForeignKey("ITMDATA.NODE.ID_NODE"))
    nod = relationship("Node", backref=backref(
        "ITMDATA.GROUP_NODE"))

class Audit(Base):
    __tablename__ = "SERV_AUD"
    __table_args__ = {'schema': 'ITMDATA'}
    AGENT_NAME = Column(String(512), primary_key=True)
    NODE_NAME = Column(String(512), primary_key=True)
    IP = Column(String(512))
    HOST_INFO = Column(String(512))
    PRODUCT = Column(String(512))
    THRUNODE = Column(String(512))
    VERSION = Column(String(512))
    STATUS = Column(String(512))
    EMAIL = Column(String(1000))
    TELEPHONE = Column(String(1000))
    EMAIL_VID_ENG = Column(String(512))
    TELEP_VID_ENG = Column(String(512))
    DEPART = Column(String(512))
    SERVICE_KE = Column(String(512))
    WORGROUP = Column(String(512))
    INCIDENT_FLAG = Column(Integer, nullable=False)
    TELEGRAM = Column(String(1000))
    TELEG_VID_ENG = Column(String(512))

class FTsit(Base):
    __tablename__ = "SERV_SIT"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = Column(Integer, primary_key=True)
    AGENT_NAME = Column(String(512), nullable=False)
    SITUATION_ID = Column(String(128), nullable=False)
    EMAIL = Column(String(1000))
    TELEPHONE = Column(String(1000))
    EMAIL_VID_ENG = Column(String(512))
    TELEP_VID_ENG = Column(String(512))
    DEPART = Column(String(512))
    SERVICE_KE = Column(String(512))
    WORGROUP = Column(String(512))
    FLAG_GRAFANA = Column(Integer, nullable=False)
    TELEGRAM = Column(String(1000))
    TELEG_VID_ENG = Column(String(512))
    DEPART_GRAF = Column(String(512))

class Icmp(Base):
    __tablename__ = "ICMP"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = Column(Integer, primary_key=True)
    SERVER = Column(String(512), nullable=False)
    DESCRIPTION = Column(String(64), nullable=False)
    EMAIL = Column(String(512))
    TELEPHONE = Column(String(512))
    EMAIL_VID_ENG = Column(String(128))
    TELEP_VID_ENG = Column(String(128))
    DEPART = Column(String(50))
    SERVICE_KE = Column(String(128))
    WORGROUP = Column(String(50))
    INCIDENT_FLAG = Column(Integer, nullable=False)
    TELEGRAM = Column(String(512))
    TELEG_VID_ENG = Column(String(512))
    PROFILE = Column(String(512))
    FLAG_GRAFANA = Column(Integer, nullable=False)
    DEPART_GRAF = Column(String(512))

class Tcpport(Base):
    __tablename__ = "TCPPORT"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = Column(Integer, primary_key=True)
    SERVER = Column(String(512), nullable=False)
    PORT = Column(String(10), nullable=False)
    PROFILE = Column(String(512))
    DESCRIPTION = Column(String(64))
    EMAIL = Column(String(512))
    TELEPHONE = Column(String(512))
    EMAIL_VID_ENG = Column(String(128))
    TELEP_VID_ENG = Column(String(128))
    DEPART = Column(String(50))
    SERVICE_KE = Column(String(128))
    WORGROUP = Column(String(50))
    INCIDENT_FLAG = Column(Integer, nullable=False)
    TELEGRAM = Column(String(512))
    TELEG_VID_ENG = Column(String(512))
    FLAG_GRAFANA = Column(Integer, nullable=False)
    DEPART_GRAF = Column(String(512))

class Webl(Base):
    __tablename__ = "WEBLIN"
    __table_args__ = {'schema': 'ITMDATA'}
    ID = Column(Integer, primary_key=True)
    URL = Column(String(512), nullable=False)
    PROFILE = Column(String(512))
    DESCRIPTION = Column(String(64))
    TABLE = Column(String(512))
    EMAIL = Column(String(512))
    TELEPHONE = Column(String(512))
    SERVICE_KE = Column(String(128))
    DEPART = Column(String(50))
    INCIDENT_FLAG = Column(Integer, nullable=False)
    EMAIL_VID_ENG = Column(String(128))
    TELEP_VID_ENG = Column(String(128))
    TELEGRAM = Column(String(512))
    TELEG_VID_ENG = Column(String(512))
    FLAG_GRAFANA = Column(Integer, nullable=False)
    DEPART_GRAF = Column(String(512))

# для авторизации
class User (Base, UserMixin):
    __tablename__ = "USER"
    __table_args__ = {'schema': 'ITMDATA'}
    id = Column(Integer, primary_key=True)
    LOGIN = Column(String(512), nullable=False, unique=True)
    PASSWORD = Column(String(50), nullable=False)

# Создание таблиц
Base.metadata.create_all(engine)