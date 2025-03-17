from flask import Flask, render_template, request

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





#java FirstName firstName
#python first_name firstname

if __name__ == "__main__":
    #True = kun til debug , False = til en udgivelse af koden for at være mere sikker
    app.run("0.0.0.0",debug=True)
