from github import Github
import MySQLdb
import time


class PopulateDB:

    def populate(self, db_name, auth, db_password):

        f = open('info.txt', 'r')
        stored_ids = f.readlines()
        f.close()

        g = Github(auth)

        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd=db_password,
                             db=db_name,
                             charset='utf8')

        cur = db.cursor()
        repos = list()

        if len(stored_ids) != 100:
            f = open('info.txt', 'w')
            limit = 0
            for repo in g.search_repositories("stars:>500", "stars", "desc"):
                l = g.rate_limiting
                if l[0] < 2:
                    time.sleep(150)
                name = repo.name
                id = repo.id

                repos.append(id)
                f.write(str(id) + "\n")

                owner = repo.owner
                owner_name = owner.login
                stars = repo.stargazers_count
                forks = repo.forks_count

                query = "INSERT INTO repositories(repository_id, owner, name, stars, forks) " + \
                        "VALUES (%s, %s, %s, %s, %s)"
                val = (id, owner_name, name, stars, forks)
                cur.execute(query, val)

                limit += 1
                if limit >= 100:
                    break
            db.commit()
        else:
            progress = open("test.txt", "r").readlines()
            for i in range(max(0, len(progress) - 1), 100):
                repos.append(int(stored_ids[i].replace("\n", "")))

        f = open('test.txt', 'a')
        cur.execute("DELETE FROM contributor WHERE repository_id = " + str(repos[0]))
        db.commit()

        for i in repos:
            f.write(str(i) + "\n")
            l = g.rate_limiting
            if l[0] < 10:
                time.sleep(4000)
            repo = g.get_repo(i)
            contributors = repo.get_contributors()
            for c in contributors:
                c_id = c.id
                c_login = c.login
                c_contributions = c.contributions
                c_location = c.location if c.location is not None else "N/A"
                c_company = c.company if c.company is not None else "N/A"
                query = "INSERT INTO contributor" + \
                        "(contributor_id, repository_id, login, contribution, location, company)" + \
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                val = (c_id, i, c_login, c_contributions, c_location, c_company)
                cur.execute(query, val)
                db.commit()
        f.close()
