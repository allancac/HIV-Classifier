from DbConnection import TweetsDatabse

connection = TweetsDatabse()

objeto = connection.getTwitter("1280522339474685954")

print(objeto["text"])
