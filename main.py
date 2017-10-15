from flask import Flask
from flask import request

import util
import micro

app = Flask(__name__)

state = 0
ins_stack = [] # instruction stack
com_stack = [] # command stack
out_stack = [] # output stack

def breakdown(stack, loc, funcs):
    macro_ins_id = stack.pop(loc)
    loc -= 1
    for f in funcs:
        if funcs[f]["id"] == macro_ins_id:
            return (funcs[f]["s_id"], funcs[f]["s_str"])

def call(id, string, stack):
    if id == 0:
        return micro.get_time(string, stack)
    elif id == 1:
        return micro.get_date(string, stack)
    elif id == 2:
        return micro.get_weather(string, stack)
    elif id == 3:
        return micro.send_email(string, stack)
    elif id == 4:
        return micro.getStockInfo(string, stack)
    elif id == 5:
        return micro.combine(string, stack)
    elif id == 6:
        return micro.say(string, stack)
    elif id == 7:
        return micro.define_command(string, stack)
    elif id == 8:
        return micro.synonym_command(string, stack)
    elif id == 9:
        return micro.antonym_command(string, stack)    
    elif id == 10:
        return micro.teach_command(string, stack)

def internal(id):
    if (id > 10):
        return False
    else:
        return True

@app.route('/')
def hello_world():
  return 'Hello!'

@app.route('/process')
def process():
    global state
    global ins_stack
    global com_stack
    global out_stack

    result = ""
    query = request.args.get("query").lower()

    if state == 0:
        command = None
        funcs = util.loadJSON("cmd.json")
        for f in funcs:
                if funcs[f]["trigger"] in query:
                    command = funcs[f]
                    break
        if command == None:
            if query == "":
                return "Hello."
            elif "reset" in query:
                util.writeJSON("cmd.json", (util.loadJSON("backup.json")))
                micro.micro_states = {}
            else:
                return "I couldn't understand."
        else:
            ins_stack.append(command["id"])
            if (command["internal"] == True):
                state = 1
            else:
                x = 0
                t_i_s = [ins_stack.pop()]
                t_c_s = []
                while x < len(t_i_s):
                    while internal(t_i_s[x]) == False:
                        tuple = breakdown(t_i_s, x, funcs)
                        t_i_s = tuple[0] + t_i_s
                        t_c_s = tuple[1] + t_c_s
                    x += 1
                ins_stack = t_i_s
                com_stack = t_c_s
                state = 2

    if state == 1:
        feedback = call(ins_stack[0], query, out_stack)
        if (feedback[1] == True):
            ins_stack.pop(0)
            state = 0
            out_stack.append(feedback[0])
        result = feedback[0]
    elif state == 2:
        feedback = call(ins_stack[0], com_stack[0], out_stack)
        while  (feedback[1] == True and len(ins_stack) > 0):
            ins_stack.pop(0)
            com_stack.pop(0)
            out_stack.append(feedback[0])
            if len(ins_stack) > 0:
                feedback = call(ins_stack[0], com_stack[0], out_stack)
        result = feedback[0]

        if (len(ins_stack) == 0 and feedback[1] == True):
            state = 0
            
    return result

if __name__ == '__main__':
  app.run()
