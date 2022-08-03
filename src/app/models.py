from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class context(Base):
    __tablename__ = 'contexts'

    id = Column(Integer, primary_key=True)

    context_id = Column(String)
    context_type = Column(String)
    context_title = Column(String)


class assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True)

    assignment_id = Column(String)
    assignment_type = Column(String)
    assignment_title = Column(String)

    context_id = Column(Integer, ForeignKey('contexts.id'))
    context = relationship('context', backref='assignments')



class user(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    user_id = Column(String)
    roles = Column(String)


class account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)

    issuer = Column(String)
    client_id = Column(String)
    deployment_id = Column(String)


class session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)

    issuer = Column(String)
    login_hint = Column(String)
    target_link_uri = Column(String)
