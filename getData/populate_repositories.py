from github import Github
import MySQLdb


class PopulateRepositories:

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
            fullname = repo.full_name
            stars = repo.stargazers_count
            forks = repo.forks_count
            contributers = repo.get_contributors()
            branches = repo.get_branches()


