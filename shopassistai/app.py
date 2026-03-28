from flask import Flask, redirect, url_for, render_template,request
app = Flask(__name__)

conversation = []
conversation.append({'bot': 'Please input your name'})
@app.route('/')
def default_route():
   global output
   return render_template('index.html', name_xyz=conversation)
# @app.route('/hello/<name>')
# def hello(name):
#     return render_template('index.html', name_xyz=output)

@app.route('/end_conv', methods=['POST'])
def end_conv():
    global conversation
    conversation = []
    conversation.append({'bot': 'Please input your name'})
    return redirect(url_for('default_route'))  

@app.route('/bye/<name>')
def bye(name):
    return f"bye {name}"

@app.route("/invite", methods=['POST'])
def invite():
    global conversation
    name = request.form['user_input_message']
    conversation.append({'user':name})
    if name == 'nikhil':
        output = 'bye, you are not inivited to the event,'+name
    else:
        output = ' welcome to the event' + name
    conversation.append({'bot':output})       
    return redirect(url_for('default_route'))  


if __name__ == "__main__":
    app.run(debug=True)