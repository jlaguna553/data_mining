# author:      Javier Laguna
#
#------------------------------------------------------------

from _actions import * #import actions to do

__data__ = 'data' #data route

if __name__ == '__main__':

    content = {} #here collect data
    content_hour = {}

    #get file list
    file_list = f_get_file_list(dir=__data__)

    #for each file read json data
    for file in file_list:
        json_content = f_get_json(data=__data__+d+file)

        for e in json_content:
            # if is the first time of this ip we create counts in set 0s
            if not e['ip'] in content:
                content[e['ip']] = {"total_time": 0,
                                    "start_time": e['timestamp'],
                                    "start_time_format": "",
                                    "end_time_format": "",
                                    "end_time":  e['timestamp'],
                                    "up": 0,
                                    "down": 0,
                                    "left": 0,
                                    "right": 0,
                                    "idle": 0,
                                    "total_events": 0,
                                    "used_direction": 0,
                                    "ip": e['ip']
                                    }
            #calculate data for that ip
            content[e['ip']]["total_time"] += eval('+'.join([str(dur['duration']) for dur in e['actions']]))
            content[e['ip']]["start_time"] = e['timestamp'] if e['timestamp'] < content[e['ip']]["start_time"] else content[e['ip']]["start_time"]
            content[e['ip']]["end_time"] = e['timestamp'] if e['timestamp'] > content[e['ip']]["start_time"] else content[e['ip']]["start_time"]
            content[e['ip']]["total_events"] += len(e['actions'])
            content[e['ip']]["start_time_format"] = datetime.datetime.fromtimestamp(
                int(content[e['ip']]["start_time"])).strftime('%Y-%m-%d %H:%M:%S')
            content[e['ip']]["end_time_format"] = datetime.datetime.fromtimestamp(
                int(content[e['ip']]["end_time"])).strftime('%Y-%m-%d %H:%M:%S')

            content[e['ip']]["used_direction"] += 1

            #making action times
            for element in e['actions']:
                content[e['ip']][element['direction']] += element['duration']

            #making content for  date and hour
            if not str(datetime.datetime.fromtimestamp(int(e['timestamp'])).strftime('%Y%m%d%H')) in content_hour:
                content_hour[str(datetime.datetime.fromtimestamp(int(e['timestamp'])).strftime('%Y%m%d%H'))] = {
                    "timestamp": datetime.datetime.fromtimestamp(int(e['timestamp'])).strftime('%Y-%m-%d %H'),
                    "cout_total_event": 0
                }


            content_hour[str(datetime.datetime.fromtimestamp(int(e['timestamp'])).strftime('%Y%m%d%H'))]['cout_total_event'] += len(e['actions'])


    max_value = max([content[x]['used_direction'] for x in content if content[x]['ip'] != '127.0.0.1'])
    most_ips = [content[ips]['ip'] for ips in content if content[ips]['used_direction'] == max_value]

    _json_final = {"events_per_ip": []}

    for i in content:

        _json_final['events_per_ip'].append({
            "ip": content[e['ip']]['ip'],
            "total_time": content[e['ip']]['total_time'],
            "start_time": content[e['ip']]['start_time_format'],
            "end_time": content[e['ip']]['end_time_format'],
            "total_direction_time": {
                "up": content[e['ip']]['up'],
                "down": content[e['ip']]['down'],
                "left": content[e['ip']]['left'],
                "right": content[e['ip']]['right'],
            },
            "total_idle_time": content[e['ip']]['idle'],
            "total_events": content[e['ip']]['total_events']
        })

    print("total events per hour: %s" % content_hour)
    print("most used publics ips: %s" % most_ips)
    print("127.0.0.1 ip total duration movements: %s" % content['127.0.0.1']['idle'])
    print("total events per ip format json: %s" % json.dumps(_json_final))

