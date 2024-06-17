import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

from crypto_password import check_password
from models import User, Message
from db_settings import DB_USER, DB_PASSWORD, DB_HOST
from db_create import DB_NAME


parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min 8 characters)')
parser.add_argument('-n', '--new_password', help='new password (min 8 characters)')
parser.add_argument('-l', '--list', help='list all users', action='store_true')
parser.add_argument('-d', '--delete', help='delete user', action='store_true')
parser.add_argument('-m', '--messages', help='list all messages', action='store_true')
parser.add_argument('-t', '--to', help='to user')
parser.add_argument('-s', '--send', help='text message (maximum 255 characters)')

args = parser.parse_args()


def create_user(cursor, username, password):

    if len(password) < 8:
        print('Password is too short, it should have minimum 8 characters')
    
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor=cursor)
            print('User created')
        except UniqueViolation:
            print('User already exists')


def edit_user(cursor, username, password, new_password):
    
    user = User.load_user_by_username(cursor=cursor, username=username)

    if not user:
        print('User does not exist')
    
    elif check_password(pass_to_check=password, hashed=user.hashed_password):

        if len(new_password) < 8:
            print('Password is too short, it should have minimum 8 characters')

        else:
            user.hashed_password =  new_password
            user.save_to_db(cursor=cursor)
            print('Password changed')
    
    else:
        print('Incorrect password')


def delete_user(cursor, username, password):

    user = User.load_user_by_username(cursor=cursor, username=username)

    if not user:
        print('User does not exist')
    
    elif check_password(pass_to_check=password, hashed=user.hashed_password):
        user.delete(cursor=cursor)
        print('User deleted')
    
    else:
        print('Incorrect password')


def list_users(cursor):

    users = User.load_all_users(cursor=cursor)

    if users:

        for user in users:
            print(user.username)
    
    else:
        print('Any user does not exist')


def user_messages(cursor, username, password):

    user = User.load_user_by_username(
        cursor=cursor,
        username=username
    )

    if not user:
        print('User does not exist')

    elif check_password(pass_to_check=password, hashed=user.hashed_password):
        messages = Message.load_all_messages(
            cursor=cursor,
            to_id=user.id
        )

        if messages:

            for message in messages:
                print(20 * '-')
                from_username = User.load_user_by_id(
                    cursor=cursor,
                    user_id=message.from_id
                ).username
                print(f'From: {from_username}')
                print(f'Date: {message.date_of_created}')
                print(message.text)
                print(20 * '-')

            else:
                print('User does have any messages')
    
    else:
        print('Incorrect password')


def send_message(cursor, username, password, to_username, text):

    user = User.load_user_by_username(
        cursor=cursor,
        username=username
    )

    if not user:
        print('User does not exist')

    elif check_password(pass_to_check=password, hashed=user.hashed_password):
        
        to_user = User.load_user_by_username(
            cursor=cursor,
            username=to_username
        )

        if len(text) > 255:
            print('Message is too long')
        
        elif to_user:
            message = Message(
                from_id=user.id,
                to_id=to_user.id,
                text=text
            )
            message.save_to_db(cursor=cursor)
            print('Message send')
        
        else:
            print('User to send does not exist')
        
    else:
        print('Incorrect password')


if __name__ == '__main__':
    try:
        cnx = connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        
        if args.username and args.password and args.to and args.send:
            send_message(
                cursor=cursor,
                username=args.username,
                password=args.password,
                to_username=args.to,
                text=args.send
            )
        
        elif args.username and args.password and args.new_password:
            edit_user(
                cursor=cursor,
                username=args.username,
                password=args.password,
                new_password=args.new_password
            )
        
        elif args.username and args.password and args.messages:
            user_messages(
                cursor=cursor,
                username=args.username,
                password=args.password
            )

        elif args.username and args.password and args.delete:
            delete_user(
                cursor=cursor,
                username=args.username,
                password=args.password
            )
        
        elif args.username and args.password:
            create_user(
                cursor=cursor,
                username=args.username,
                password=args.password
            )
        
        elif args.list:
            list_users(cursor=cursor)
        
        else:
            parser.print_help()
        
        cursor.close()
        cnx.close()
    
    except OperationalError as e:
        print('Connection error: ', e)