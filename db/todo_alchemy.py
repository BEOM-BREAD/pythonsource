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
class Todo(Base):

    __tablename__ = "todos"

    todo_id: Mapped[int] = mapped_column(Numeric(10, 0), Identity(start=1, increment=1), primary_key=True)
    title:Mapped[str] = mapped_column(String(200))
    is_done:Mapped[bool] = mapped_column(default=False)
    # Optional[datetime] : None or datetime 일수도 있음
    created_at:Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now)
    # created_at:Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.sysdate())

    
    def __repr__(self):
        status = "완료" if self.is_done else "미완료"
        return f"{self.todo_id}. {self.title}[{status}] {self.created_at}"

Base.metadata.create_all(engine)


# todo 추가
def add_todo():
    '''create'''
    # 할 일 내용을 입력하세요 : 내용입력...
    title = input("할 일 내용을 입력하세요: ").strip()
    # insert 구문 실행
    # sql = "insert into todos(title, created_at) values(:1,sysdate)"
    with Session(engine) as session:
        todo = Todo(title=title)
        session.add(todo)
        session.commit()
        
        print(f"{todo.todo_id} 가 등록되었습니다.\n")


def list_todos():
    '''select'''

    with Session(engine) as session:
        stmt = select(Todo).order_by(Todo.todo_id)
        todos = session.scalars(stmt).all()

    # todo 내용이 없는경우
    if not todos:
        print("등록된 할 일 목록은 없습니다.\n")
        return
    print("-"*50)
    for todo in todos:
        print(todo)
    print("-"*50)
    print()

def update_todo():
    '''완료처리'''
    # 목록 보여주기
    list_todos()
    todo_id = input("완료 처리할 일 번호를 입력하세요: ").strip()

    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if todo is None:
            print("해당 번호가 없습니다.")
            return 

        todo.is_done = True
        session.commit()

    print("완료 처리 되었습니다.\n")

def delete_todo():
    '''삭제처리 - delete'''
    # 목록 보여주기
    list_todos()
    todo_id = input("삭제 처리할 일 번호를 입력하세요: ").strip()
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if todo is None:
            print("해당 번호가 없습니다.")
            return
        
        session.delete(todo)
        session.commit()
    print("삭제 처리 되었습니다.\n")


def menu():
    while True:
        print("=== Todo 관리 ===")
        print("1. 추가 2. 목록 3. 완료처리 4. 삭제 5. 종료")

        choice = input("선택 : ")

        if choice == "1":
            add_todo()
        elif choice == "2":
            list_todos()
        elif choice == "3":
            update_todo()
        elif choice == "4":
            delete_todo()
        elif choice == "5":
            print("종료합니다")
            break
        else:
            print("번호를 확인해 주세요")

if __name__ == "__main__":
    menu()