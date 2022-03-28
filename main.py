import imdb
import random
import pandas

score = 0
ia = imdb.IMDb()
Top250 = ia.get_top250_movies()
firstMovie = Top250[random.randint(0,249)]
secondMovie = Top250[random.randint(0,249)]
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
    secondMovie = Top250[random.randint(0,249)]
print(f"score:{score}")
if score > highscore:
    data._set_value(user_csv_id, 'Score', score)
data.to_csv('scores.csv', index=False)
