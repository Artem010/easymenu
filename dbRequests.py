import os, sqlite3

pathDB = os.getcwd() + '/EasyMenu.db'

def addUserDB(id, first_name):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()

        sqlite_query = """SELECT * from Users where Id = ? """
        cursor.execute(sqlite_query, (id,))
        records = cursor.fetchone()
        # Если в таблице нет пользователя с таким id, то добавляем нового
        if(records == None):
            sqlite_insert_query = """INSERT INTO Users
                                    (Id, FirstName)
                                    VALUES (?, ?);"""

            data_tuple = (id, first_name)

            cursor.execute(sqlite_insert_query, data_tuple)
            sqlite_connection.commit()
            print("Row added to table Users ", cursor.rowcount)
            return 1
        else:
            print("User exist!")
            return 0

        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getUserIngredients(id):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()

        sqlite_query = """SELECT Ingredients.*
                          FROM UserIngredients JOIN Ingredients ON UserIngredients.IngredientId=Ingredients.Id
                          WHERE UserIngredients.UserId = ?"""
        cursor.execute(sqlite_query, (id,))
        return cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getCategories():
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        sqlite_query = """SELECT * FROM Categories"""
        cursor.execute(sqlite_query)
        return cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getIngredientsForCategory(categoryId,userId):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        # sqlite_query = """SELECT Ingredients.Id, Ingredients.IngredientName
        #                 FROM Ingredients
        #                 WHERE Ingredients.CategoryId = ?"""
        sqlite_query = """SELECT Ingredients.Id, Ingredients.IngredientName 
                            FROM Ingredients
                            WHERE Id NOT IN (SELECT UserIngredients.IngredientId
                                            FROM UserIngredients
                                            WHERE UserIngredients.UserId = ?)
                                    AND Ingredients.CategoryId = ?"""
        cursor.execute(sqlite_query, (userId,categoryId))
        return cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def addInredientToUser(userId, ingredientId):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        sqlite_query = """SELECT 0 FROM UserIngredients WHERE UserId = ? AND IngredientId = ?"""
        cursor.execute(sqlite_query, (userId, ingredientId))
        records = cursor.fetchone()
        # Если такого ингредиента нет, то добавляем
        if(records == None):
            sqlite_insert_query = """INSERT INTO UserIngredients
                                    (UserId, IngredientId)
                                    VALUES (?, ?);"""


            cursor.execute(sqlite_insert_query, (userId, ingredientId))
            sqlite_connection.commit()
            print("Row added to table UserIngredients ")
            return 1
        else:
            print("Ingr exists in table UserIngredients!")
            return 0
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
        return 0
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def delIngedientToUser(userId, ingredientId):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """DELETE FROM UserIngredients
                                 WHERE UserId = ? AND IngredientId = ?"""

        cursor.execute(sqlite_insert_query, (userId,ingredientId))
        sqlite_connection.commit()
        print("Row del to table UserIngredients!")
        cursor.close()
        return 1
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
        return 0
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getAllIngredients():
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        sqlite_query = """SELECT * FROM Ingredients"""
        cursor.execute(sqlite_query)
        return cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def addIngredintForRecipe(recipeId, ingredientId):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()

        sqlite_insert_query = """INSERT INTO IngredientsForRecipe
                                (RecipeId, IngredientId)
                                VALUES (?, ?);"""


        cursor.execute(sqlite_insert_query, (recipeId, ingredientId))
        sqlite_connection.commit()
        print("Row added to table IngredientsForRecipe ")
        cursor.close()
        return 1
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
        return 0
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def getRecipe(recipeId):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        sqlite_query = """SELECT * 
                            FROM Recipes
                            WHERE Recipes.Id=?;"""
        cursor.execute(sqlite_query, (recipeId,))
        return cursor.fetchone()
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getRecipeForIngredients(lisId):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()

        # sqlite_query = f"""
        #     SELECT Recipes.Id, Recipes.Title
        #     FROM Recipes
        #     JOIN IngredientsForRecipe ON Recipes.Id = IngredientsForRecipe.RecipeId
        #     JOIN Ingredients ON IngredientsForRecipe.IngredientId = Ingredients.Id
        #     WHERE IngredientsForRecipe.IngredientId in ({lisId})
        #     GROUP BY Recipes.Title
        #     HAVING COUNT(*) >= 2
        # """

        sqlite_query = f"""SELECT Recipes.*, COUNT(*) AS N
            FROM Recipes 
            JOIN IngredientsForRecipe ON IngredientsForRecipe.RecipeId = Recipes.Id
            JOIN Ingredients ON Ingredients.Id = IngredientsForRecipe.IngredientId
            WHERE Ingredients.Id IN ({lisId})
            GROUP BY Recipes.Title
            HAVING N >= 2"""
        cursor.execute(sqlite_query)
        return cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def getRandomRecipe():
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()

        sqlite_query = f"""
            SELECT *
            FROM Recipes
            ORDER BY RANDOM() LIMIT 1;
        """
        cursor.execute(sqlite_query)
        return cursor.fetchone()
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def addNewRecipe(title, desc, cTime, videoLink):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()

        sqlite_query = """SELECT Id FROM Recipes WHERE Title LIKE ?"""
        cursor.execute(sqlite_query, (title,))
        records = cursor.fetchone()
        # Если в таблице нет рецепта с таким навзание, то добавляем
        if (records == None):
            sqlite_insert_query = """INSERT INTO Recipes
                                    (Title,Description,CookingTime,VideoLink)
                                    VALUES (?,?,?,?);"""

            cursor.execute(sqlite_insert_query, (title, desc, cTime, videoLink))
            sqlite_connection.commit()
            print("Row added to table Recipes ", cursor.rowcount)
            return cursor.lastrowid
        else:
            return 0
        cursor.close()
    except sqlite3.Error as error:
        print("Error SQLite: ", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()



def delRecipe(title):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """DELETE FROM Recipes
                                 WHERE Title = ?"""

        cursor.execute(sqlite_insert_query, (title,))
        sqlite_connection.commit()
        print("Row del to table Recipes!")
        cursor.close()
        if(cursor.rowcount >0):
            return 1
        else:
            return 0
    except sqlite3.Error as error:
        print("Error SQLite: ", error)
        return 0
    finally:
        if sqlite_connection:
            sqlite_connection.close()

# 521369524	1
# 521369524	8
# 521369524	16
# 521369524	4
# 521369524	3
# 521369524	2
# 1603532193	26
# 1603532193	24
# 1603532193	23
# 1603532193	25
# 1603532193	1
# 1603532193	16