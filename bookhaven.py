from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    PhoneNumber = Column(String, nullable=False)

    
    transactions = relationship("Transaction", back_populates="customer")


class Author(Base):
    __tablename__ = 'author'
    AuthorID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'book'
    BookID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Genre = Column(String, nullable=False)
    Price = Column(Float, nullable=False)
    AuthorID = Column(Integer, ForeignKey('author.AuthorID'), nullable=False)

   
    author = relationship("Author", back_populates="books")

    
    transactions = relationship("TransactionBook", back_populates="book")


class Transaction(Base):
    __tablename__ = 'transaction'
    TransactionID = Column(Integer, primary_key=True, autoincrement=True)
    TransactionDate = Column(Date, nullable=False)
    CustomerID = Column(Integer, ForeignKey('customer.CustomerID'), nullable=False)

    
    customer = relationship("Customer", back_populates="transactions")

   
    books = relationship("TransactionBook", back_populates="transaction")


class TransactionBook(Base):
    __tablename__ = 'transaction book'
    TransactionID = Column(Integer, ForeignKey('transaction.TransactionID'), primary_key=True)
    BookID = Column(Integer, ForeignKey('book.BookID'), primary_key=True)

   
    transaction = relationship("Transaction", back_populates="books")
    book = relationship("Book", back_populates="transactions")



engine = create_engine('sqlite:///bookhaven.db')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def add_sample_data():
    author1 = Author(FirstName='J.K.', LastName='Rowling')
    book1 = Book(Title='Harry Potter and the Philosopher\'s Stone', Genre='Fantasy', Price=19.99, author=author1)
    
    author2 = Author(FirstName='Dale', LastName='Carnegie')
    book2 = Book(Title='How to Win Friends and Influence People', Genre='Self-Help', Price=14.99, author=author2)
    
    author3 = Author(FirstName='Stephen R.', LastName='Covey')
    book3 = Book(Title='The 7 Habits of Highly Effective People', Genre='Self-Help', Price=16.99, author=author3)
    
    author4 = Author(FirstName='James', LastName='Clear')
    book4 = Book(Title='Atomic Habits', Genre='Self-Help', Price=18.99, author=author4)
    
    customer1 = Customer(FirstName='John', LastName='Doe', Email='john.doe@example.com', PhoneNumber='1234567890')
    customer2 = Customer(FirstName='Jane', LastName='Smith', Email='jane.smith@example.com', PhoneNumber='0987654321')
    
    transaction1 = Transaction(TransactionDate='2024-05-16', customer=customer1)
    transaction2 = Transaction(TransactionDate='2024-05-17', customer=customer2)
    
    transaction_book1 = TransactionBook(transaction=transaction1, book=book1)
    transaction_book2 = TransactionBook(transaction=transaction1, book=book2)
    transaction_book3 = TransactionBook(transaction=transaction2, book=book3)
    transaction_book4 = TransactionBook(transaction=transaction2, book=book4)
    
    session.add(author1)
    session.add(book1)
    session.add(author2)
    session.add(book2)
    session.add(author3)
    session.add(book3)
    session.add(author4)
    session.add(book4)
    session.add(customer1)
    session.add(customer2)
    session.add(transaction1)
    session.add(transaction2)
    session.add(transaction_book1)
    session.add(transaction_book2)
    session.add(transaction_book3)
    session.add(transaction_book4)
    
    session.commit()

