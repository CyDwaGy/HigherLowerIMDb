import tkinter

import imdb
import random
import pandas
from tkinter import *
from tkinter.ttk import *
import urllib.request
import os
from PIL import Image, ImageTk
higher_lower = 0
name = ''


def leaderboard(data):
    data = data.sort_values(by=['Score'], ascending=False)
    i = 1
    window1 = Tk()
    for row in data.iterrows():
        Label(window1, text=i).grid(row=i, column=0)
        Label(window1, text=row[1].Name).grid(row=i, column=1)
        Label(window1, text=row[1].Score).grid(row=i, column=2)
        i+=1
    Button(window1, text="Ok", command=window1.destroy).grid(row=i, column=0, columnspan=3)
    mainloop()


def lost_popup():
    window = Tk()
    img = ImageTk.PhotoImage(Image.open('lost.jpg').resize((360, 170)))
    (Label(window, image=img)).grid(row=0, column=0)
    Button(window, text="Close", command=window.destroy).grid(row=1, column=0)
    mainloop()


def name_popup():
    window = Tk()
    e = Entry(window)
    Label(window, text="Name: ").grid(row=1, column=0, ipady=15)
    e.grid(row=1, column=1)
    b = Button(window, text="Ok", command=lambda *args: give_name_value(e.get(), window))
    b.grid(row=2, column=0, columnspan=2)
    mainloop()


def change_images(url):
    url = f"{url.split('_V1_', 1)[0]}.jpg"
    os.remove('first_movie_cover.jpg')
    os.rename('second_movie_cover.jpg', 'first_movie_cover.jpg')
    urllib.request.urlretrieve(url, 'second_movie_cover.jpg')


def give_higher_lower_value(value, window):
    global higher_lower
    higher_lower = value
    window.destroy()

def give_name_value(value, window):
    global name
    name = value
    window.destroy()


score = 0
ia = imdb.IMDb()
Top250Movies = ia.get_top250_movies()
firstMovie = ia.get_movie(Top250Movies[random.randint(0, 249)].movieID)
secondMovie = ia.get_movie(Top250Movies[random.randint(0, 249)].movieID)
data = pandas.read_csv("scores.csv")
name_popup()
try:
    user_csv_id = data.index[data['Name'].str.match(name)].tolist()[0]
except IndexError:
    tmp = pandas.DataFrame({'Name': [name], 'Score': [0]})
    data = data.append(tmp, ignore_index=True)
    user_csv_id = data.tail(1).index.item()
highscore = data._get_value(user_csv_id, 'Score')
final_url1 = f"{firstMovie['cover url'].split('_V1_', 1)[0]}.jpg"
final_url2 = f"{secondMovie['cover url'].split('_V1_', 1)[0]}.jpg"
urllib.request.urlretrieve(final_url1, 'first_movie_cover.jpg')
urllib.request.urlretrieve(final_url2, 'second_movie_cover.jpg')
while 1:
    window = Tk()
    Label(window, text=firstMovie['title']).grid(row=0, column=0, columnspan=2)
    Label(window, text=secondMovie['title']).grid(row=0, column=2, columnspan=2)
    img1 = ImageTk.PhotoImage(Image.open('first_movie_cover.jpg').resize((300, 450)))
    img2 = ImageTk.PhotoImage(Image.open('second_movie_cover.jpg').resize((300, 450)))
    (Label(window, image=img1)).grid(row=1, column=0, columnspan=2)
    (Label(window, image=img2)).grid(row=1, column=2, columnspan=2)
    Label(window, text=f"Rating: {firstMovie['rating']}").grid(row=2, column=0,columnspan=2)
    Label(window, text=f"Your score: {score}").grid(row=3, column=1)
    Label(window, text=f"Highscore: {highscore}").grid(row=3, column=0)
    Button(window, text="Higher", command=lambda *args: give_higher_lower_value('2',window)).grid(row=2, column=2)
    Button(window, text="Lower", command=lambda *args: give_higher_lower_value('1',window)).grid(row=2, column=3)
    Button(window, text="Leaderboard", command=lambda *args: leaderboard(data)).grid(row=4, column=0, columnspan=2)
    Button(window, text="Close", command=window.destroy).grid(row=4, column=2, columnspan=2)
    mainloop()
    if (higher_lower == '1' and firstMovie['rating'] >= secondMovie['rating']) or \
    (higher_lower == '2' and firstMovie['rating'] <= secondMovie['rating']):
        score += 1
        higher_lower = '0'
        firstMovie = secondMovie
        secondMovie = ia.get_movie(Top250Movies[random.randint(0, 249)].movieID)
        change_images(secondMovie['cover url'])
    else:
        lost_popup()
        break
if score > highscore:
    data._set_value(user_csv_id, 'Score', score)
data.to_csv('scores.csv', index=False)
