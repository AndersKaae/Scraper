from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///scrape.db')
Base = declarative_base()

class ScrapedURLs(Base):
    __tablename__ = 'scrapedurl'

    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)
    scraped = Column(UnicodeText(length=2**31), nullable=True)
    
Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def InserScraped(url, scraped):
    inserted = False
    isItUnique = session.query(ScrapedURLs).filter_by(url = url).first()
    if str(isItUnique) ==  "None":			
        company = ScrapedURLs(url = url, scraped = str(scraped))
        session.add(company)
        session.commit()
        inserted = True 
    session.close()
    return inserted

def UpdateScraped(url, scraped):
    oldItem = session.query(ScrapedURLs).filter_by(url = url).first()
    session.delete(oldItem)
    #company = ScrapedURLs(url = url, scraped = str(scraped))
    #session.add(company)
    session.commit()
    session.close()

def GetFirstUncrawled():
    firstUnique = session.query(ScrapedURLs).filter_by(scraped = 'NULL').first()
    url = firstUnique.url
    #firstUnique = session.query(ScrapedURLs).filter(scraped != None).all()
    return url
