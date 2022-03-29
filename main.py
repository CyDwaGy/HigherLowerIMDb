import imdb
import random
import pandas
from tkinter import *
from tkinter.ttk import *
import urllib.request
import os


def change_images(url):
    os.remove('first_movie_cover.jpg')
    os.rename('second_movie_cover.jpg', 'first_movie_cover.jpg')
    urllib.request.urlretrieve(url, 'second_movie_cover.jpg')

score = 0
ia = imdb.IMDb()
Top250Movies = ia.get_top250_movies()
firstMovie = ia.get_movie(Top250Movies[random.randint(0, 249)].movieID)
secondMovie = ia.get_movie(Top250Movies[random.randint(0, 249)].movieID)
print("Podaj swoja nazwe")
name = input()
data = pandas.read_csv("scores.csv")
try:
    user_csv_id = data.index[data['Name'].str.match(name)].tolist()[0]
except IndexError:
    tmp = pandas.DataFrame({'Name': [name], 'Score': [0]})
    data = data.append(tmp, ignore_index=True)
    print(data)
    user_csv_id = data.tail(1).index.item()
print(user_csv_id)
highscore = data._get_value(user_csv_id, 'Score')
print(f"highscore: {highscore}")
urllib.request.urlretrieve(firstMovie['cover url'], 'first_movie_cover.jpg')
urllib.request.urlretrieve(secondMovie['cover url'], 'second_movie_cover.jpg')
while 1:
    print(f"{firstMovie['title']}  {firstMovie['rating']},\n{secondMovie}")
    x = input()
    if x == '1' and firstMovie['rating'] >= secondMovie['rating']:
        print("gz")
        score += 1
    elif x == '2' and firstMovie['rating'] <= secondMovie['rating']:
        print("gz")
        score += 1
    else:
        print("lose")
        print(f"{firstMovie['rating']}, {secondMovie['rating']}")
        break
    firstMovie = secondMovie
    secondMovie = ia.get_movie(Top250Movies[random.randint(0,249)].movieID)
    change_images(secondMovie['cover url'])
print(f"score:{score}")
if score > highscore:
    data._set_value(user_csv_id, 'Score', score)
data.to_csv('scores.csv', index=False)
