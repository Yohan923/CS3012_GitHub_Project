from github import Github
import MySQLdb
import time
import ssl


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

        """
        import urllib.request
        context = ssl._create_unverified_context()
        contents = urllib.request.urlopen("https://api.github.com/repos/torvalds/linux/contributors&per_page=50", context=context).\
            read()

        d = g.get_repo(2325298).get_contributors()

        for c in d:
            c_id = c.id
            c_login = c.login
            c_contributions = c.contributions
            c_location = c.location if c.location is not None else "N/A"
            c_company = c.company if c.company is not None else "N/A"
            query = "INSERT INTO contributor" + \
                    "(contributor_id, repository_id, login, contribution, location, company)" + \
                    "VALUES (%s, %s, %s, %s, %s, %s)"
            val = (c_id, 9384267, c_login, c_contributions, c_location, c_company)
            cur.execute(query, val)
            db.commit()
        """

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
            f = open("test.txt", "r")
            progress = f.readlines()
            for i in range(len(progress), 100):
                repos.append(int(stored_ids[i].replace("\n", "")))
            f.close()

        f = open('test.txt', 'a')

        for i in repos:
            l = g.rate_limiting
            if l[0] < 10:
                time.sleep(4000)
            cur.execute("DELETE FROM contributor WHERE repository_id = "+str(i))
            db.commit()
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
            f.write(str(i) + "\n")
        f.close()
