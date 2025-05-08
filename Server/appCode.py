from flask import Flask, render_template, request
import sqlite3
import json

app = Flask(__name__)

#test commit for github
@app.route("/Shooter")
def shooter():
    name = request.args.get("name", default="")
    return name*3
    s=""
    s += "<h1>Online Scoreboard for my Space Shooter game!</h1>"
    s += "<br>"
    s += "<table>"
    for u in range (3):
        s += "<tr>"
        s += "<td>[NAME]</td>"
        s += "<td>[SCORE]</td>"
        s+= "</tr>"
    s+="</tr> </table>"

    return s

@app.route("/Scores")
def scores():
    s = "<body style='font-size: 300%;'>"
    s += "<a href='/Scores/hard'>hard</a>"
    s += " <a href='/Scores/normal'>normal</a>"
    s += " <a href='/Scores/SUPER'>SUPER</a>"
    s += " <a href='/Scores/nightmare'>nightmare</a>"
    s += "</body>"
    return s

@app.route("/Scores/<difficulty>")
def getscore(difficulty):
    s = ""
    s += "<style> table, th, td {border:1px solid black;}</style>"
    connection = sqlite3.connect("dataTest.db")
    sql = (f"SELECT username, score from {difficulty}score order by score DESC;")
    cursor = connection.cursor()
    cursor.execute(sql)
    rest = cursor.fetchall()
    connection.commit()
    connection.close()
    s += f"Here is top 10 best players in the world on the {difficulty} difficulty:"
    s += "<table> <tr> <th> Username </th> <th> Score </th> </tr>"
    for i in range(10):
        s += "<tr>"
        s += "<th>" + rest[i][0] + "</th> <th>" + str(rest[i][1]) + "</th>" 
        s += "</tr>"
    s += "</table>"
    
    return render_template("index.html", data=rest)




#java FirstName firstName
#python first_name firstname

if __name__ == "__main__":
    #True = kun til debug , False = til en udgivelse af koden for at være mere sikker
    app.run("0.0.0.0",debug=True)
