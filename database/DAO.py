from database.DB_connect import DBConnect
from model.teams import Team


class DAO():
    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT year as year
                            FROM teams t
                            WHERE year >1979
                            ORDER by year ASC
                             """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @classmethod
    def getTeams(self, year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
                        FROM teams t
                        WHERE year = %s
                        ORDER by t.name
                         """
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(Team(**row))
            cursor.close()
            cnx.close()
        return result

    @classmethod
    def getTeamsSalary(self, idMap, year):   #l'anno ci serve come parametro mentre l'idMap la
                                            # usiamo per trovare la squadra usando l'id
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)    # in questa query trovo l'id della squadra,
                                                    # quindi passerò un id map e userò l'id come chiave
            query = """SELECT t.teamCode , t.ID , sum(s.salary) as totSalary 
                        FROM salaries s , teams t , appearances a 
                        WHERE s.`year` = t.`year` and t.`year` = a.`year` 
                        and a.`year` = %s
                        and t.ID = a.teamID 
                        and s.playerID = a.playerID 
                        GROUP by t.teamCode
                         """
            cursor.execute(query, (year,))
            result = {}
            for row in cursor:
                result[idMap[row["ID"]]] = row["totSalary"]
               # result.append(idMap[row["ID"]], row["totSalary"])
            cursor.close()
            cnx.close()
        return result
