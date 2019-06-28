import datetime


class News:
    news_id = 0
    title = ''
    text = ''
    image_link = ''
    date = datetime.datetime.now()
    favourites = 0


class NewsFull:
    news_id = 0
    title = ''
    blocks = []
    main_image_link = ''
    date = datetime.datetime.now()
    favourites = 0


class Block:
    text = ''
    images = []
