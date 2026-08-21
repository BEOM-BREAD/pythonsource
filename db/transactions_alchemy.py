import oracledb
from sqlalchemy import Numeric,String, func
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Identity
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, DateTime
from dotenv import load_dotenv
from typing import Optional
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

load_dotenv()
password = os.getenv("ORACLE_PASSWORD")

engine = create_engine(f"oracle+oracledb://python_user:{password}@localhost:1521/?service_name=xe",echo=True,)

# 테이블 생성 => 클래스 생성
Base = declarative_base()
class Transaction(Base):

    __tablename__ = "transactions"
    
    tx_id: Mapped[int] = mapped_column(Numeric(10, 0), Identity(start=1, increment=1), primary_key=True)
    tx_type:Mapped[str] = mapped_column(String(10))
    amount:Mapped[int] = mapped_column(Numeric(10,0))
    memo:Mapped[str] = mapped_column(String(2000))
    # Optional[datetime] : None or datetime 일수도 있음
    # created_at:Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now)
    reg_date:Mapped[str] = mapped_column(String(20))

    def __repr__(self):
        return f"{self.tx_id}. [{self.tx_type}] {self.amount}원 - {self.memo} ({self.reg_date})"
    
Base.metadata.create_all(engine)

def add_transaction():
    tx_type = input('구분을 입력하세요 (수입/지출): ').strip()
    amount = input('금액을 입력하세요: ').strip()
    memo = input('내역을 입력하세요: ').strip()
    reg_date = input('날짜를 입력하세요 (YYYY-MM-DD,엔터 시 오늘): ').strip()

    if not reg_date:
        reg_date = datetime.now().strftime("%Y-%m-%d")

    with Session(engine) as session:
        transaction = Transaction(tx_type=tx_type, amount = amount, memo=memo, reg_date=reg_date)
        session.add(transaction)
        session.commit()
            
        print(f"{transaction.tx_id} 가 등록되었습니다.\n")


def list_transaction():
    """reg_date asc"""
    # 번호 [지출] 300000원 = 용돈(2026-08-18)
    with Session(engine) as session:
        stmt = select(Transaction).order_by(Transaction.reg_date)
        transactions = session.scalars(stmt).all()
    
    if not transactions:
        print("등록된 할 일 목록은 없습니다.\n")
        return
    print("-"*50)
    for t in transactions:
        print((f"{t.tx_id}. [{t.tx_type}] {t.amount}원 - {t.memo}({t.reg_date})"))
    print("-"*50)
    print()

def monthly_summary():

    month = input("조회 할 월을 입력하세요 (YYYY-MM): ").strip()

    with Session(engine) as session:
        # label() : 별칭 붙이기
        # stmt = select(Transaction.tx_type, func.sum(Transaction.amount).label("total")).where(Transaction.reg_date.like(month+'%')).group_by(Transaction.reg_date)
        stmt = select(Transaction.tx_type, func.sum(Transaction.amount)).where(Transaction.reg_date.like(month+'%')).group_by(Transaction.tx_type)
        transactions = session.execute(stmt).all()
        
    if not transactions:
        print("요청하신 해당 월 가계부 내역은 없습니다.\n")
        return
    print("-"*50)
    for tx_type, total in transactions:
        print(f"{tx_type} : {total}")

    # 별칭을 썼다면
    # for t in results:
    #   print(f"{t.tx_type} : {t.total}")
    print("-"*50)
    print()

def menu():
    # 1. 내역 추가 2. 전체 조회 3. 월별 합계 4. 종료
    while True:
        print("=== 가계부 ===")
        print("1. 내역 추가 2. 전체 조회 3. 월별 합계 4. 종료")
    
        choice = input("선택 : ")
    
        if choice == "1":
            add_transaction()
        elif choice == "2":
            list_transaction()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            print("종료합니다")
            break
        else:
            print("번호를 확인해 주세요")


if __name__ == "__main__":
    menu()
