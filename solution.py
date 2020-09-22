import elv

user_key = 'lktgt'
problem_id = 2
elvs = 4

startStat = elv.start(user_key, problem_id, elvs)
token = startStat['token']
# token = 'KHZby'

print(token)

def floorCall(floor,calls,start = True):
    ret = []
    if start:
        for Call in calls:
            if floor == Call['start']:
                ret.append(Call)
    elif not start:
        for Call in calls:
            if floor == Call['end']:
                ret.append(Call)
    return ret

def upOrdown(floor,calls,end = True):
    ret = []
    if end:
        for Call in calls:
            if Call['end'] > floor:
                ret.append('UP')
            elif Call['end'] < floor:
                ret.append('DOWN')
            else:
                ret.append('STOP')
    else:
        for Call in calls:
            if Call['start'] > floor:
                ret.append('UP')
            elif Call['start'] < floor:
                ret.append('DOWN')
            else:
                ret.append('STOP')
    return ret

def solve():
    while 1:
        curStats = elv.onCall(token)
        if curStats['is_end']:
            return
        elvs = elv.allelvs(curStats)
        oncalls = curStats['calls']
        allcalls = []
        for Elevator in elvs:
            for Call in Elevator['passengers']:
                allcalls.append(Call['id'])
        nxtCmds = []
        for i,Elevator in enumerate(elvs):
            ElvStat = Elevator['status']
            ElvFloor = Elevator['floor']
            ElvPassengers = Elevator['passengers']
            fcall_end = floorCall(ElvFloor,ElvPassengers,False)
            fcall_enter = floorCall(ElvFloor,oncalls,True)
            cmd = {}
            cmd['elevator_id'] = i

            passengers = upOrdown(ElvFloor,ElvPassengers)
            enters = upOrdown(ElvFloor,fcall_enter)
            calls = upOrdown(ElvFloor,oncalls,False)

            if ElvStat == 'STOPPED':
                #OPEN
                if fcall_end: # 내리는 사람이 있다.
                    cmd['command'] = 'OPEN'
                elif fcall_enter and len(ElvPassengers) < 8: # 타려는 사람이 있고 엘리베이터에 수용된다.
                    if not passengers or passengers[0] in enters: # 타려는 사람이 엘리베이터에 타있는 사람과 방향이 같다.
                        cmd['command'] = 'OPEN'
                    else: # 타려는 사람이 엘리베이터에 타있는 사람과 방향이 같지않다.
                        if passengers: # 현재 고객이 있다.
                            cmd['command'] = passengers[0]
                        else: # 현재 고객이 없다.
                            cmd['command'] = calls[0]
                else: # 타려는 사람이 없거나 엘리베이터에 수용할 수 없다.
                    if passengers:
                        cmd['command'] = passengers[0]
                    elif calls:
                        cmd['command'] = calls[0]
                    else:
                        cmd['command'] = 'STOP'
            elif ElvStat == 'OPENED':
                if fcall_end: # 내리는 사람이 있다.
                    cmd['command'] = 'EXIT'
                    cmd['call_ids'] = []
                    for Call in fcall_end:
                        cmd['call_ids'].append(Call['id'])
                        allcalls.append(Call['id'])
                elif fcall_enter and len(ElvPassengers) < 8: # 타려는 사람이 있고 엘리베이터에 수용된다.
                    if not passengers or passengers[0] in enters: # 타려는 사람이 타있는 사람과 방향이 같다.
                        cmd['command'] = 'ENTER'
                        cmd['call_ids'] = []
                        for j, Call in enumerate(fcall_enter):
                            tmp = 0
                            if not passengers:
                                tmp = 0
                            else:
                                tmp = passengers[0]
                            if len(cmd['call_ids']) + len(ElvPassengers) < 8 and (not passengers or enters[j] == passengers[0]) and Call['id'] not in allcalls:
                                cmd['call_ids'].append(Call['id'])
                                allcalls.append(Call['id'])
                    else:
                        cmd['command'] = 'CLOSE'
                else: # 타려는 사람이 없거나 엘리베이터에 수용할 수 없다.
                    cmd['command'] = 'CLOSE'
            elif ElvStat == 'UPWARD':
                if fcall_end: # 내리는 사람이 있다.
                    cmd['command'] = 'STOP'
                elif fcall_enter and len(ElvPassengers) < 8: # 타려는 사람이 있고 엘리베이터에 수용된다.
                    if not passengers or passengers[0] in enters: # 타있는 사람과 타려는 사람의 방향이 같다.
                        cmd['command'] = 'STOP'
                    else:
                        if passengers[0] == 'DOWN':
                            cmd['command'] = 'STOP'
                        else:
                            cmd['command'] = 'UP'
                else:
                    cmd['command'] = 'UP'
            elif ElvStat == 'DOWNWARD':
                if fcall_end:
                    cmd['command'] = 'STOP'
                elif fcall_enter and len(ElvPassengers) < 8:
                    if not passengers or passengers[0] in enters:
                        cmd['command'] = 'STOP'
                    else:
                        if passengers[0] == 'UP':
                            cmd['command'] = 'STOP'
                        else:
                            cmd['command'] = 'DOWN'
                else:
                    cmd['command'] = 'DOWN'
            nxtCmds.append(cmd)
        elv.Action(token, nxtCmds)

solve()
