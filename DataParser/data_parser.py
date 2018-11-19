import MySQLdb
import json


class DataParser:

    def parse(self, db_name, db_password):

        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd=db_password,
                             db=db_name,
                             charset='utf8')

        cur = db.cursor()

        cur.execute("SELECT * FROM repositories")
        result = cur.fetchall()

        repo_names = open("../visualization/data/repo_names.json", "w")
        vis_data = open("../visualization/data/repo_info.json", "w")

        for i in result:
            repo_name = i[2] + "/" + i[3]
            json.dump({"name": repo_name}, repo_names)

            cur.execute("SELECT login, contribution FROM contributor WHERE repository_id = " + str(i[1]))
            repo_data = cur.fetchall()
            total_contributions = 0

            if len(repo_data) > 0:
                for j in repo_data:
                    total_contributions += j[1]

                json.dump(
                    {"name": repo_name,
                     "top_1": repo_data[0][0],
                     "top_1_value": int((repo_data[0][1] / total_contributions) * 10000),
                     "top_2": repo_data[1][0],
                     "top_2_value": int((repo_data[1][1] / total_contributions) * 10000),
                     "top_3": repo_data[2][0],
                     "top_3_value": int((repo_data[2][1] / total_contributions) * 10000),
                     "top_4": repo_data[3][0],
                     "top_4_value": int((repo_data[3][1] / total_contributions) * 10000),
                     "top_5": repo_data[4][0],
                     "top_5_value": int((repo_data[4][1] / total_contributions) * 10000)
                     }, vis_data)
            else:
                json.dump({"name": repo_name,
                           "note": "Contributor list was to big to retrieve through api"
                           }, vis_data)

            repo_names.close()
            vis_data.close()




