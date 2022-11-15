# FLASK DEVELOPER - MEMORISATION PROJECT  from JetBrains Academy  by Chris Freeman
# https://hyperskill.org/projects/159
# Version History
# 0.1 13-Nov-2022 stage 1/4 menu structure with cards in volatile list
# 0.2 14-Nov-2022 stage 2/4 Flashcards stored in SQL via SQLAlchemy v1.4 ORM v?
# 0.3 14-Nov-2022 stage 3/4 include update and delete of flashcards during practice
# 0.4 14-Nov-2022 stage 4/4 implement Leitner system. DB includes box# for cards

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    qn = Column(String)
    ans = Column(String)
    box = Column(Integer)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def invalid(choice):
    print()
    print(choice, 'is not an option')
    print()


def get_choice(prompt_string, valids_list):
    complete = False
    while not complete:
        print(prompt_string)
        choice = ''
        while len(choice) == 0:
            choice = input().strip()
        if choice in valids_list:
            complete = True
        else:
            invalid(choice)
    return choice


def do_get_flash():
    qn = ''
    while len(qn) == 0:
        print('\nQuestion:')
        qn = input().strip()
    ans = ''
    while len(ans) == 0:
        print('Answer:')
        ans = input().strip()
    card = Flashcard(qn=qn, ans=ans, box=0)
    try:
        session.add(card)
        session.commit()
    except Exception as e:
        print('Error writing to database:', e)


def do_add_flash():
    add_prompts = '\n1. Add a new flashcard\n2. Exit'
    add_choices = ['1', '2']
    fin = False
    while not fin:
        choice = get_choice(add_prompts, add_choices)
        if choice == '1':
            do_get_flash()
        else:
            fin = True


def do_update(card):
    update_prompts = 'press "d" to delete the flashcard:\npress "e" to edit the flashcard:'
    update_choices = ['d', 'e']
    choice = get_choice(update_prompts, update_choices)
    if choice == 'd':
        session.delete(card)
        session.commit()
    elif choice == 'e':
        print('\ncurrent question:', card.qn)
        qn = ''
        while len(qn) == 0:
            print('please write a new question:')
            qn = input().strip()
        print('\ncurrent answer:', card.ans)
        ans = ''
        while len(ans) == 0:
            print('please write a new answer:')
            ans = input().strip()
        card.qn = qn
        card.ans = ans
        try:
            session.commit()
        except Exception as e:
            print('error in update of flashcard', card.id, '- ', e)


def do_box_placement(card):
    box_prompts = 'press "y" if your answer is correct:\npress "n" if your answer is wrong:'
    box_choices = ['y', 'n']
    know_it = get_choice(box_prompts, box_choices)
    if know_it == 'y':
        card.box += 1
    elif know_it == 'n':
        card.box -= 1
    else:
        invalid(know_it)
    if card.box < 0:
        card.box = 0
    if card.box > 2:
        session.delete(card)
    session.commit()


def do_practice():
    cardlist = session.query(Flashcard).all()
    if not cardlist:
        print('\nThere is no flashcard to practice!')
    else:
        for card in cardlist:
            print('\nQuestion:', card.qn)
            prac_prompt = 'press "y" to see the answer:\npress "n" to skip:\npress "u" to update:'
            prac_choices = ['y', 'n', 'u']
            resp = get_choice(prac_prompt, prac_choices)
            if resp == 'y':
                print("\nAnswer:", card.ans)
                do_box_placement(card)
            elif resp == 'u':
                do_update(card)
            elif resp == 'n':
                print()
            else:
                invalid(resp)


def menu():
    fin = False
    while not fin:
        menu_prompts = '1. Add flashcards\n2. Practice flashcards\n3. Exit'
        menu_choices = ['1', '2', '3']
        choice = get_choice(menu_prompts, menu_choices)
        if choice == '1':
            do_add_flash()
        elif choice == '2':
            do_practice()
        elif choice == '3':
            fin = True
        else:
            invalid(choice)


if __name__ == '__main__':
    menu()
    print('\nBye!')
