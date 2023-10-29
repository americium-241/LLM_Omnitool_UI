
from sqlalchemy import create_engine, MetaData, Table, Column, String, select, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer

Base = declarative_base()
class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, unique=True)
    chat_history = relationship("ChatHistory", backref="session")
    session_name = relationship("SessionName", backref="session")

class ChatHistory(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String)
    content = Column(String)
    session_id = Column(Integer, ForeignKey('sessions.id'))

class SessionName(Base):
    __tablename__ = 'sessions_names'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    session_id = Column(Integer, ForeignKey('sessions.id'))

class PersistentStorage:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_chat_message(self, session_id, role, content,name):
        session = self.Session()
        # Check if session exists, if not, create new one
        existing_session = session.query(Session).filter_by(session_id=session_id).first()
        if not existing_session:
            existing_session = Session(session_id=session_id)
            session.add(existing_session)
            session.commit()

        # Add chat history with session reference
        chat_history_instance = ChatHistory(role=role, content=content, session=existing_session)
        session.add(chat_history_instance)
        session.commit()

    def save_session_name(self,session_id,name):
        session = self.Session()
        # Check if session exists, if not, create new one
        existing_session = session.query(Session).filter_by(session_id=session_id).first()
        session_name_instance = SessionName(name=name,session=existing_session)
        session.add(session_name_instance)
        session.commit()

    def get_chat_history(self, session_id):
        session = self.Session()
        session_instance = session.query(Session).filter_by(session_id=session_id).first()
        if not session_instance:
            return []
        result = session_instance.chat_history
        return [{"role": res.role, "content": res.content} for res in result]

    def get_all_sessions(self):
        session = self.Session()
        result = session.query(Session).all()
        return [res.session_id for res in result]

    def get_all_sessions_names(self):
        session = self.Session()
        # Perform a join between Session and SessionName tables on session_id
        join_query = session.query(Session.session_id, SessionName.name).join(SessionName, Session.id == SessionName.session_id).all()
        # Convert the result of join_query into a dictionary
        session_names_dict = {item[0]: item[1] for item in join_query}

        return session_names_dict

    
    def delete_session(self, session_id):
        session = self.Session()
        session_instance = session.query(Session).filter_by(session_id=session_id).first()
        if session_instance:
            session.delete(session_instance)
            session.commit()

    def reset_all_session_names_to_default(self):
        session = self.Session()
        # Fetch all session names
        all_session_names = session.query(SessionName).all()

        for session_name_instance in all_session_names:
            # Set the name attribute to its corresponding session_id
          
            related_session = session_name_instance.session
            session_name_instance.name = related_session.session_id

        session.commit()