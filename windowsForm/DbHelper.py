import psycopg2
import config
connection=None
try:
    connection=psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        print(cursor.fetchone())

    with connection.cursor() as cursor:
        cursor.execute(
            """

            CREATE TABLE IF NOT EXISTS users (
                id TEXT,
                login text,
                password text,
                textHeaders text[],
                textDescriptions text[],
                textDates text[]
            );"""
        )
        connection.commit()


except Exception as _ex:
    print("null")
    print(_ex)

def add_user(id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (id) VALUES('{id}')"""
        )
        connection.commit()
def registration(login,password,id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE users SET login='{login}',password='{password}' WHERE id='{id}';"""
        )
        connection.commit()
def getData(id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM users WHERE id ='{id}';"""
            )
            result=cursor.fetchone()
            return result
    except:
        print("null")
def getAllData():
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT * FROM users;"""
        )
        result=cursor.fetchall()
        return result
    
def history(textHeaders,textDescriptions,textDates,id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE users SET textHeaders=array_append(textHeaders,'{textHeaders}'),textDescriptions=array_append(textDescriptions,'{textDescriptions}'),textDates=array_append(textDates,'{textDates}') WHERE id='{id}';"""
            )
            connection.commit()


def GetId():
        result=""
        with open('id.txt', 'r') as f:
            for line in f:
                result+=line.strip()
            
        return result

# def WriteComment(comment,counter,id):
#     with connection.cursor() as cursor:

#         cursor.execute(f"UPDATE users SET textComments[{counter}] = '{comment}' WHERE id = '{id}'")

#             # Подтверждение изменений
#         connection.commit()
# def getAllComments():
#         commentsHistoies=[]
#         data=getAllData()
#         comments=[[]]
#         for i in data:
#             if(i[6]!=None):
#                 for j in i[6]:
#                     commentsHistoies.append(j)
#             comments[0].append(commentsHistoies[1].split("\n"))
#         print(comments[0])
# getAllComments()
   
