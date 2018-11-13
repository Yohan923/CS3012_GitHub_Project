from github import Github
import MySQLdb


class PopulateDB:

    def populate(self, dataBase, auth, db_password):

        g = Github(auth)

        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd=db_password,
                             db=dataBase)
        cur = db.cursor()

        for repo in g.search_repositories("stars:>500", "stars", "desc"):
            name = repo.name
            id = repo.id
            owner = repo.owner
            owner_name = owner.login
            stars = repo.stargazers_count
            forks = repo.forks_count
            contributors = repo.get_contributors()
            contributor_ids = list()
            for c in contributors:
                list.append(c.id)
                query = "INSERT INTO contributer(id, login, contribution, location, company) " + \
                        "VALUES (%d, %s, %d, %s, %s)"
                val = (c.id, c.login, c.contributions, c.location, c.company)
                cur.execute(query, val)

            query = "INSERT INTO repositories(id, owner, name, stars, forks, contributors) " + \
                    "VALUES (%d, %s, %s, %d, %d, %s)"
            val = (id, owner_name, name, stars, forks, str(contributor_ids))
            cur.execute(query, val)
