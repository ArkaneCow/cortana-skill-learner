import inspect
import re

import util
import d_time
import d_weather
import d_email
import d_stock
import d_words

micro_states = {}

def say(command_string, out_stack):
    return command_string[command_string.find("say") + 4:], True

def get_time(command_string, out_stack):
    return d_time.getTime(), True

def get_date(command_string, out_stack):
    return d_time.getDate(), True

def get_weather(command_string, out_stack):
    return d_weather.getWeather(), True

def combine(command_string, out_stack):
    m1 = re.search("(.+)last ([0-9]+)", command_string)
    if (m1 is not None):
        try:
            count = int(m1.group(2))
            if (count > len(out_stack) or count == 0):
                return ("Invalid input", True)
            else:
                return "\n".join(out_stack[-count:]), True
        except:
            return ("Invalid input", True)
    else:
        return ("Unable to combine", True)
    

def send_email(command_string, out_stack):
    frame = inspect.currentframe()
    state_key = str(inspect.getframeinfo(frame).function)
    def get_email(query):
        names = util.loadJSON("contacts.json")
        toField = None
        for x in range(len(names)):
            if names[x]["name"] in query:
                toField = names[x]["email"]
                break
        return toField

    DEFAULT_STATE = (False, None, None, None)
    if state_key not in micro_states:
        m1 = re.search("(.+)to (.+) about (.+) containing (.+)", command_string)
        m2 = re.search("(.+)to (.+) about (.+)", command_string)
        m3 = re.search("(.+)to (.+)", command_string)
        m4 = re.search("(.+)it to (.+)", command_string)
        m5 = re.search("(.+)that to (.+)", command_string)

        if m1 is not None:
            get_field = m1.group(2)
            to_field = get_email(get_field)
            if to_field is None:
                micro_states[state_key] = DEFAULT_STATE
            else:
                subject_field = m1.group(3)
                body_field = m1.group(4)
                if "that" in body_field or "it" in body_field:
                    body_field = out_stack[-1]
                micro_states[state_key] = (True, to_field, subject_field, body_field)
        elif m2 is not None:
            get_field = m2.group(2)
            to_field = get_email(get_field)
            if to_field is None:
                micro_states[state_key] = DEFAULT_STATE
            else:
                subject_field = m2.group(3)
                micro_states[state_key] = (True, to_field, subject_field, None)
                return "What is the message?", False
        elif m4 is not None:
            get_field = m4.group(2)
            to_field = get_email(get_field)
            print("out stack is " + str(out_stack[-1]))
            body_field = out_stack[-1]
            micro_states[state_key] = (True, to_field, None, body_field)
            return "What is the subject?", False
        elif m5 is not None:
            get_field = m5.group(2)
            to_field = get_email(get_field)
            print("out stack is " + str(out_stack[-1]))
            body_field = out_stack[-1]
            micro_states[state_key] = (True, to_field, None, body_field)
            return "What is the subject?", False
        elif m3 is not None:
            get_field = m3.group(2)
            to_field = get_email(get_field)
            if to_field is None:
                micro_states[state_key] = DEFAULT_STATE
            else:
                micro_states[state_key] = (True, to_field, None, None)
                return "What is the subject?", False
        else:
            micro_states[state_key] = DEFAULT_STATE
    current_state = micro_states[state_key]
    def param_complete():
        ms = micro_states[state_key]
        return ms[0] and ms[1] is not None and ms[2] is not None and ms[3] is not None
    def state_response():
        ms = micro_states[state_key]
        if param_complete():
            ms = micro_states[state_key]
            to_field = ms[1]
            subject_field = ms[2]
            bodymsg_field = ms[3]
            d_email.sendEmail(to_field, subject_field, bodymsg_field)
            del micro_states[state_key]
            return "Email sent!", True
        if ms[1] is None:
            return "Who do I send the email to?", False
        elif ms[2] is None:
            return "What is the subject?", False
        elif ms[3] is None:
            return "What is the body?", False

    if not current_state[0]:
        # The prompt has been asked
        micro_states[state_key] = (True, current_state[1], current_state[2], current_state[3])
        if current_state[1] is None:
            return "Who do I send the email to?", False
        elif current_state[2] is None:
            return "What is the subject?", False
        elif current_state[3] is None:
            return "What is the body?", False

    elif current_state[1] is None:
        # missing to field
        toField = get_email(command_string)
        if toField is None:
            return "I didn't get that. Could you repeat?", False
        else:
            micro_states[state_key] = (current_state[0], toField, current_state[2], current_state[3])
    elif current_state[2] is None:
        # missing subject field
        subject_field = command_string
        micro_states[state_key] = (current_state[0], current_state[1], subject_field, current_state[3])
    elif current_state[3] is None:
        # missing bodymsg
        body_message = command_string
        if "last thing" in body_message:
            body_message = out_stack[-1]
        micro_states[state_key] = (current_state[0], current_state[1], current_state[2], body_message)
    return state_response()

def getStockInfo(command_string, outStack):
    frame = inspect.currentframe()
    state_key = str(inspect.getframeinfo(frame).function)
    DEFAULT_STATE = False
    if (state_key not in micro_states):
        micro_states[state_key] = DEFAULT_STATE
    current_state = micro_states[state_key]
    m1 = re.search("(.*)stock ([a-z]+)", command_string)
    if (m1 is not None):
        ticker = m1.group(2)
        if(state_key in micro_states):
            del micro_states[state_key]
        if (d_stock.isValid(ticker)):
            return (d_stock.getPrice(ticker), True)
        else:
            return "Invalid Ticker", True
    else:
        if (current_state):
            ticker = command_string
            if(state_key in micro_states):
                del micro_states[state_key]
            if (d_stock.isValid(ticker)):
                return (d_stock.getPrice(ticker), True)
            else:
                return "Invalid Ticker", True
        else:
            micro_states[state_key] = True
            return "Specify valid ticker", False
    
def teach_command(command_string, out_stack):
    print("DEBUG" + command_string)
    frame = inspect.currentframe()
    state_key = str(inspect.getframeinfo(frame).function)
    DEFAULT_STATE = (None, [])
    if state_key not in micro_states:
        m1 = re.search("(.+)called (.+)", command_string)
        if m1 is None:
            micro_states[state_key] = DEFAULT_STATE
            return "What should I call this?", False
        else:
            command_name = m1.group(2)
            micro_states[state_key] = (command_name, [])
            cmds = util.loadJSON("cmd.json")
            conflict = False
            for x in cmds:
                x_trigger = cmds[x]["trigger"]
                if x_trigger in command_name or command_name in x_trigger:
                    conflict = True
            if conflict:
                del micro_states[state_key]
                return "Invalid command name.", True
            return "How do I do this?", False
    else:
        if "cancel" in command_string:
            del micro_states[state_key]
            return "Teaching cancelled", True
        current_state = micro_states[state_key]
        if current_state[0] is None:
            command_name = command_string
            cmds = util.loadJSON("cmd.json")
            conflict = False
            for x in cmds:
                x_trigger = cmds[x]["trigger"]
                if x_trigger in command_name or command_name in x_trigger:
                    conflict = True
            if conflict:
                del micro_states[state_key]
                return "Invalid command name.", True
            micro_states[state_key] = (command_name, [])
            return "How do I do this?", False
        else:
            if "finish" in command_string:
                if len(micro_states[state_key][1]) > 0:
                    seq_id = [i[0] for i in micro_states[state_key][1]]
                    seq_str = [i[1] for i in micro_states[state_key][1]]
                    util.saveFunction(micro_states[state_key][0], seq_id, seq_str)
                    del micro_states[state_key]
                    return "New command saved", True
                else:
                    del micro_states[state_key]
                    return "Incorrect number of steps", True
            else:
                command_step = command_string
                cmds = util.loadJSON("cmd.json")
                step_id = None
                step_str = command_string
                for x in cmds:
                    x_trigger = cmds[x]["trigger"]
                    if x_trigger in command_step:
                        if x_trigger == "teach":
                            continue
                        x_id = cmds[x]["id"]
                        step_id = x_id
                        break
                if step_id is None:
                    return "Sorry. I didn't get that", False
                else:
                    micro_states[state_key][1].append((step_id, step_str))
                    return "OK. What next?", False

def define_command(command_string, outStack):
    frame = inspect.currentframe()
    state_key = str(inspect.getframeinfo(frame).function)
    DEFAULT_STATE = False
    if (state_key not in micro_states):
        micro_states[state_key] = DEFAULT_STATE
    current_state = micro_states[state_key]
    m1 = re.search("(.*)define ([a-z]+)", command_string)
    if (m1 is not None):
        word = m1.group(2)
        if(state_key in micro_states):
            del micro_states[state_key]
        return d_words.define_word(word), True
    else:
        if (current_state):
            word = command_string
            if(state_key in micro_states):
                del micro_states[state_key]
            return d_words.define_word(word), True
        else:
            micro_states[state_key] = True
            return "Specify a word", False

def synonym_command(command_string, outStack):
    frame = inspect.currentframe()
    state_key = str(inspect.getframeinfo(frame).function)
    DEFAULT_STATE = False
    if (state_key not in micro_states):
        micro_states[state_key] = DEFAULT_STATE
    current_state = micro_states[state_key]
    m1 = re.search("(.*)synonym of ([a-z]+)", command_string)
    if (m1 is not None):
        word = m1.group(2)
        if(state_key in micro_states):
            del micro_states[state_key]
        return d_words.synonym(word), True
    else:
        if (current_state):
            word = command_string
            if(state_key in micro_states):
                del micro_states[state_key]
            return d_words.synonym(word), True
        else:
            micro_states[state_key] = True
            return "Specify a word", False

def antonym_command(command_string, outStack):
    frame = inspect.currentframe()
    state_key = str(inspect.getframeinfo(frame).function)
    DEFAULT_STATE = False
    if (state_key not in micro_states):
        micro_states[state_key] = DEFAULT_STATE
    current_state = micro_states[state_key]
    m1 = re.search("(.*)antonym of ([a-z]+)", command_string)
    if (m1 is not None):
        word = m1.group(2)
        if(state_key in micro_states):
            del micro_states[state_key]
        return d_words.antonym(word), True
    else:
        if (current_state):
            word = command_string
            if(state_key in micro_states):
                del micro_states[state_key]
            return d_words.antonym(word), True
        else:
            micro_states[state_key] = True
            return "Specify a word", False