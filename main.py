
DB = {}
DB_TRANS = {}

def parse_command(data):
    key = ""
    val = ""
    command = ""
    res = data.split(" ")
    if len(res) == 3 and res[0] == "SET":
        command, key, val = data.split(" ")
    elif len(res) == 2 and res[0] in ('GET', 'UNSET'):
        command, key = data.split(" ")
    elif len(res) == 2 and res[0] in ('COUNTS', 'FIND'):
        command, val = data.split(" ")
    return command, key, val

def get(key, tran=False):
    if tran:
        if key in DB_TRANS.keys():
            print(DB_TRANS[key])
        else:
            print("NULL")
    else:
        if key in DB.keys():
            print(DB[key])
        else:
            print("NULL")

def unset(key, tran=False):
    if tran:
        if key in DB_TRANS.keys():
            DB_TRANS[key] = "NULL"
    else:
        if key in DB.keys():
            del DB[key]

def counts(val, tran=False):
    if tran:
        v = [i for i in DB_TRANS.values() if i == val]
        print len(v)
    else:
        v = [i for i in DB.values() if i == val]
        print len(v)

def finds(val, tran=False):
    if tran:
        res = [i for i in DB_TRANS if DB_TRANS[i] == val]
        print(', '.join(res))
    else:
        res = [i for i in DB if DB[i] == val]
        print(', '.join(res))

def sets(key, val, tran=False):
    if tran:
        DB_TRANS[key] = val
    else:
        DB[key] = val

COMMANDS = {'GET': get, 'UNSET': unset, 'COUNTS': counts,
            'FIND': finds, 'SET': sets}

def main_loop(command, key, val, trans):
    if trans:
        if command in ('GET', 'UNSET'):
            COMMANDS[command](key, tran=True)
        elif command in ('COUNTS', 'FIND'):
            COMMANDS[command](val, tran=True)
        elif command in ('SET',):
            COMMANDS[command](key, val, tran=True)
        else:
            print('Unknown command')
    else:
        if command in ('GET', 'UNSET'):
            COMMANDS[command](key)
        elif command in ('COUNTS', 'FIND'):
            COMMANDS[command](val)
        elif command in ('SET',):
            COMMANDS[command](key, val)
        else:
            print('Unknown command')

def main():
    trans = False
    global DB_TRANS
    while True:
        data = raw_input()
        command, key, val = parse_command(data.strip())
        if data.strip() == "EXIT":
            break
        elif data.strip() == 'BEGIN':
            trans = True
            DB_TRANS = DB.copy()
            continue
        elif data.strip() == 'ROLLBACK':
            trans = False
            DB_TRANS.clear()
            continue
        elif data.strip() == 'COMMIT':
            trans = False
            DB.update(DB_TRANS)
            continue
        else:
            main_loop(command, key, val, trans)

if __name__ == '__main__':
    main()

