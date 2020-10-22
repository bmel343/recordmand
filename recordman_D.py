#recordings_manager
import json
import argparse
import configparser
from zoomus import ZoomClient

#Def Var
api_key = 'DBHJyNYcSAi7sasvQmuzLw'
api_secret = 'HYHPChXQzuq1NWJvR65itW0dDDIWLZlWBlZo'
debug = False

#Def Func
def init_parser():
    parser = argparse.ArgumentParser(description='recordings_manager.py')
    parser.add_argument("get", nargs="?")
    parser.add_argument("--debug", action='store_true')
    parser.add_argument('-u', '--userid')
    parser.add_argument('-m', '--meeting')

    args = parser.parse_args()
    return(args)

def init_config():
    config = configparser.ConfigParser()
    #with open ('recordman_D.ini', 'r') as configfile:
    config.read('recordman_D.ini')
    if debug:
        print('Config Sections: \r\n {0}'.format(config.sections()))
    return(config)

def init_client(key, secret):
    client = ZoomClient(api_key, api_secret)
    return(client)

def get_localtime_str(time_string):
    #This is only for Zoom time strings in this format: 2020-10-15T17:20:04Z
    try:
        start_date, start_time = time_string.split('T')
    except:
        if debug:
            print('I could not process this time string: {0}'.format(time_string))
        return(time_string)
    hour, minute, second = start_time.split(':')
    start_time = "{0}:{1}".format(
        str(int(hour) - 5), str(minute))
    localtime_str = '{0}-{1}'.format(
        start_date, start_time)
    return(localtime_str)

def get_meeting_details(meeting_id):
    endpoint = 'meetings/%s' % meeting_id
    response = client.get_request(endpoint)
    meeting_json = json.loads(response.content)
    return(meeting_json)

def get_recordings_by_host_id(userid):
    response = client.recording.list(user_id=userid).content
    recording_list = json.loads(response)
    ## do stuf
    outlist = []
    for meeting in recording_list['meetings']:
        #write meeting header
        ifile = 1
        topic = str(meeting['topic'])
        meeting_id = str(meeting['id'])
        share_url = str(meeting['share_url'])
        print("'" + topic + "', '" + meeting_id + "', '" + share_url + "'")
        for file in meeting['recording_files']:
            #retrieve actual meeting files
            parent_meeting = str(file['meeting_id'])
            start_time = str(file['recording_start'])
            end_time = str(file['recording_end'])
            share_url = str(file['share_url'])
            print("'" + str(ifile) + "', '" + parent_meeting + "', '" + start_time + "', '" + end_time + "', '" + redist_url + "'")
            #inc counter after
            ifile + 1

def get_recordings_by_meeting_id(meeting_id):
    #Starting Over
    meeting_details = get_meeting_details(meeting_id)
    host_user_id = meeting_details['host_id']
    topic = meeting_details['topic']
    response = client.recording.list(user_id=host_user_id).content
    recording_list = json.loads(response)
    
    print('\nMeeting: {0}, ID: {1}\n Available recordings: '.format(topic, meeting_id))
    if debug:
        print("Recording List: \n {0}".format(recording_list))
    for meeting in recording_list['meetings']:
        uuid = meeting['uuid']
        count = meeting['recording_count']
        if count != 0:
            if debug:
                print(uuid)
            recordings_password = get_recording_password(uuid)
            for file in meeting['recording_files']:
                topic = str(meeting['topic'])
                this_meeting_id = str(meeting['id'])
                share_url = str(meeting['share_url'])
                if this_meeting_id == str(meeting_id):
                        for file in meeting['recording_files']:
                            #recording_id = str(file['id'])
                            start_time = get_localtime_str(file['recording_start'])
                            end_time = get_localtime_str(file['recording_end'])
                            play_url = str(file['play_url'])
                            download_url = str(file['download_url'])
                            print('\t{0}, {1},Password: {2}, {3}'.format(
                                start_time, end_time,
                                recordings_password, play_url))

def get_recording_password(meeting_id):
    endpoint = '/meetings/{0}/recordings/settings'.format(meeting_id)
    response = client.get_request(endpoint)
    settings_json = json.loads(response.content)
    if debug:
        print(endpoint)
        print(response)
        print(settings_json)
    password = settings_json["password"]
    return(password)

def get_recordings_from_config(config):
    for user in config['Users']:
        meetings = config['Users'][user].split(',')
        print('\nFetching recordings for {0}'.format(user))
        if debug:
            print('\\CONFIG PASS \r\n config_user: {0}, config_meetings: {1}'.format(user, meetings))
        for meeting_id in meetings:
            get_recordings_by_meeting_id(meeting_id)
            
    
#def get_recordings_by_meeting_id(meeting_id)

#def get_recordings_by_topic(topic)

#Def Main
if __name__ == "__main__":
    config = init_config()
    args = init_parser()
    client = init_client(api_key, api_secret)

    #Get
    if args.debug:
        debug = True
    if args.get:
        #by host ID
        get_recordings_by_host_id(args.userid)
        #by meetind ID
    else:
        get_recordings_from_config(config)
        
