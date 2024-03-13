This project is a backend application for a corporate microblogging service. The application is designed to work exclusively within a Docker environment and can be launched using `docker-compose up` command.

The functionality of the application is tailored to meet the requirements of a corporate network.

* FastAPI
* Docker
* PostgreSQL
* SQLAlchemy

## Functional

1. **Adding a New Tweet** : User can create new tweets.
2. **Deleting Own Tweet** : User can delete their own tweets.
3. **Following Other Users** : User can follow other users.
4. **Unfollowing Other Users** : User can unfollow other users.
5. **Liking Tweets** : User can like tweets.
6. **Removing Likes** : User can remove likes from tweets.
7. **Tweet Images** : Tweet may contain an image.

🚀**Getting Started**

To run the project locally, follow the steps below:

1. Make sure you have Docker and Docker-compose installed on your machine.
2. Clone the repository.
3. Navigate to the project directory.
4. Open a terminal and run the following command to start the application:

```shell
docker-compose up
```

5. The application will be up and running at `http://localhost:80`
