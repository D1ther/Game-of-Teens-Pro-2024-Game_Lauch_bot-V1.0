import sqlite3 as sq


# Під'єднання до дб
def base_connect():

     with sq.connect('game_launch.db') as con:
        
        global cur   

        cur = con.cursor()

        # таблиця юзерів
        cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    name TEXT,
                    tg_id INTEGER NOT NULL
                    )''')
        
        # таблиця ігор
        cur.execute('''CREATE TABLE IF NOT EXISTS games(
                    game_name TEXT NOT NULL,
                    photo TEXT,
                    plot TEXT NOT NULL,
                    tg_id INTEGER NOT NULL
                    )''')

        # таблиця історії запитів до ШІ
        cur.execute('''CREATE TABLE IF NOT EXISTS sinnbo(
                    history1 TEXT,
                    tg_id INTEGER NOT NULL
                    )''')
        
        con.commit()


# реєстрація нового користувача
async def reg(tg_name, tg_id):
    with sq.connect('game_launch.db') as con:
      
        cur = con.cursor()
        
        cur.execute('''INSERT OR IGNORE INTO users VALUES(?, ?)''', (tg_name, tg_id))

        con.commit()

# Функція додавання гри
async def create_game(game_name:str=None, photo:str=None, plot:str=None, tg_id:int=None ):
    with sq.connect('game_launch.db') as con:

        cur = con.cursor()

        cur.execute('''INSERT INTO games VALUES(?, ?, ?, ?)''', (game_name, photo, plot, tg_id))
   
        con.commit()
        
# Функція перегляду усіх ігор людини, працює не до кінця

# Перегляд імені
async def show_game_name(tg_id:int=None):
        
        with sq.connect('game_launch.db') as con:
        
            cur = con.cursor()

            name_game = cur.execute('''SELECT game_name FROM games WHERE tg_id = ?''', (tg_id,)).fetchall()
            plot_game = cur.execute('''SELECT plot FROM games WHERE tg_id = ?''', (tg_id,)).fetchall()

            con.commit()

            return(name_game)

# Перегляд фото
async def show_game_photo(tg_id:int=None):
        
        with sq.connect('game_launch.db') as con:
        
            cur = con.cursor()
 
            photo_game = cur.execute('''SELECT photo FROM games WHERE tg_id = ?''', (tg_id,)).fetchall()

            con.commit()

            return(photo_game)

# Перегляд опису
async def show_game_plot(tg_id:int=None):
        
        with sq.connect('game_launch.db') as con:
        
            cur = con.cursor()

            plot_game = cur.execute('''SELECT plot FROM games WHERE tg_id = ?''', (tg_id,)).fetchall()

            con.commit()

            return(plot_game)


# select опису гри по id, та назві гри
async def select_game_plot_for_id(title:str, tg_id:int):
     with sq.connect('game_launch.db') as con:
        cur = con.cursor()

        plot_game = cur.execute('''SELECT plot FROM games WHERE game_name = ? AND tg_id = ?''', (title, tg_id)).fetchall()

        plot_of_game = None

        for plot in plot_game:
            plot_of_game = plot[0]

        if plot_of_game is not None:
            return plot_of_game
        else:
            return 'опису нема'
    
# select фото гри
async def select_game_photo_for_id(title:str, tg_id:int):
     with sq.connect('game_launch.db') as con:
          cur = con.cursor()

          game_photo = cur.execute('''SELECT photo FROM games WHERE game_name = ? AND tg_id = ?''', (title, tg_id)).fetchone()
          
          return(game_photo)
     
# Оновлення назви гри 
async def update_game_name(new_game_title:str, title:str, tg_id:int):
     
     with sq.connect('game_launch.db') as con:
          cur = con.cursor()

          updated_name = cur.execute('''UPDATE games SET game_name = ? WHERE game_name = ? AND tg_id = ?''', (new_game_title, title, tg_id)).fetchone()

          con.commit()

          return(updated_name)
     
# Оновлення опису гри
async def update_game_plot(new_plot:str, title:str, tg_id:int):
     with sq.connect('game_launch.db') as con:
          cur = con.cursor()

          cur.execute('''UPDATE games SET plot = ? WHERE game_name = ? AND tg_id = ?''', (new_plot, title, tg_id))

          con.commit()

# оновлення фото
async def update_game_photo(new_photo:str, title:str, tg_id:int):
     with sq.connect('game_launch.db') as con:
          cur = con.cursor()

          updated_game_photo = cur.execute('''UPDATE games SET photo = ? WHERE game_name = ? AND tg_id = ?''', (new_photo, title, tg_id)).fetchone()

          con.commit()

          return(updated_game_photo)

# Видалення гри зі списку ігор
async def game_removed(name:str, tg_id:int):
     with sq.connect('game_launch.db') as con:
          cur = con.cursor()

          cur.execute('''DELETE FROM games WHERE game_name = ? AND tg_id = ?''', (name, tg_id))

          con.commit()

# отримання гри по імені гри 
async def select_game_name(tg_id:int, name:str):
     with sq.connect('game_launch.db') as con:
          cur = con.cursor()

          title = cur.execute('''SELECT game_name FROM games WHERE tg_id = ? AND game_name = ?''', (tg_id, name)).fetchone()

          return(title)