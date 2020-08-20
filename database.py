from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///scrape.db')
Base = declarative_base()

class ScrapedURLs(Base):
    __tablename__ = 'scrapedurl'

    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)
    scraped = Column(Boolean, nullable=False)
    
Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def DeleteDatabaseData():
    session.query(ScrapedURLs).delete()

def SaveURLs(urlList):
    for url in urlList:
        isItUnique = session.query(ScrapedURLs).filter_by(url = url).first()
        if str(isItUnique) ==  "None":			
            data = ScrapedURLs(url = url, scraped = False)
            session.add(data)
    session.commit()
    session.close()

def GetFirstUncrawled():
    firstUnique = session.query(ScrapedURLs).filter_by(scraped = False).first()
    url = firstUnique.url
    return url

def SetAsScraped():
    firstUnique = session.query(ScrapedURLs).filter_by(scraped = False).first()
    firstUnique.scraped = True
    session.commit()
    session.close()