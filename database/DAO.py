from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getRangeCoordinate():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT MIN(Lat) as minLat, MAX(Lat) as maxLat,
                           MIN(Lng) as minLng, MAX(Lng) as maxLng
                            FROM state"""

        cursor.execute(query)
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return row["minLat"], row["maxLat"], row["minLng"], row["maxLng"]

    @staticmethod
    def getAllShape():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape 
                    from sighting s 
                    where s.shape is not null
                    and s.shape != ''
                    and s.shape != 'unknown'
                    order by s.shape desc"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["shape"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(lat,lng,shape):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.id, s.Name, s.Capital, s.Lat, s.Lng, s.Area, s.Population, s.Neighbors
                    from state s, sighting si
                    where s.id = si.state
                    and s.lat > %s
                    and s.lng > %s
                    and si.shape = %s"""

        cursor.execute(query, (lat,lng,shape))

        for row in cursor:
            results.append(State(row["id"], row["Name"], row["Capital"], row["Lat"], row["Lng"], row["Area"], row["Population"], row["Neighbors"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppie(idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        results = []

        query = """SELECT DISTINCT s1.id as id1, s2.id as id2
                    FROM state s1, state s2, neighbor n
                    WHERE ((s1.id = n.state1 and s2.id = n.state2) or
                        (s1.id = n.state2 and s2.id = n.state1))
                    and s1.id < s2.id"""

        cursor.execute(query, )

        for row in cursor:
            if row["id1"] in idMap and row["id2"] in idMap:
                n1 = idMap[row["id1"]]
                n2 = idMap[row["id2"]]
                results.append((n1, n2))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getDurate(shape):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        results = []

        query = """SELECT st.id as id, SUM(s.duration) as peso
                        FROM sighting s, state st
                        WHERE s.state = st.id
                        and s.shape = %s
                        GROUP BY st.id"""

        cursor.execute(query, (shape,))

        for row in cursor:
            results.append((row["id"], row["peso"]))

        cursor.close()
        conn.close()
        return results









