#recordings_manager
import json
import argparse
import configparser
from zoomus import ZoomClient

#Def Var
api_key = 'DBHJyNYcSAi7sasvQmuzLw'
api_secret = 'HYHPChXQzuq1NWJvR65itW0dDDIWLZlWBlZo'
debug = True

#Def Func
def init_parser():
    parser = argparse.ArgumentParser(description='recordings_manager.py')
    parser.add_argument("get", nargs="?")
    parser.add_argument('-u', '--userid')
    parser.add_argument('-m', '--meeting')

    args = parser.parse_args()
    return(args)

def init_config():
    config = configparser.ConfigParser()
    #with open ('recordman_D.ini', 'r') as configfile:
    config.read('recordman_D.ini')
    print(config.sections())
        #if config['API']['api_key']:
        #    api_key = config['API']['api_key']
        #if config['API']['api_secret']:
        #    api_key = config['API']['api_secret']
    return(config)

def init_client(key, secret):
    client = ZoomClient(api_key, api_secret)
    return(client)

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
    response = client.recording.list(user_id=host_user_id).content
    recording_list = json.loads(response)
    if debug:
        print("Recording List: \n %".format(recording_list))
    for meeting in recording_list['meetings']:
        for file in meeting['recording_files']:
            topic = str(meeting['topic'])
            this_meeting_id = str(meeting['id'])
            share_url = str(meeting['share_url'])
            if this_meeting_id == str(meeting_id):
                    for file in meeting['recording_files']:
                        parent_meeting = str(file['meeting_id'])
                        start_time = str(file['recording_start'])
                        end_time = str(file['recording_end'])
                        share_url = str(file['play_url'])
                        print("'" + parent_meeting + "', '" + start_time + "', '" + end_time + "', '" + share_url + "'")
                        #inc counter after
    #Because zoom's dumb api thinks only end users use API written apps?
    #We have to look up the meeting separately, then make the meeting calls based on that users id
    #This sucks. the 'meetings' endpoint will only return one recording? and it's not parsing well
    #The zoomus lib only supports meeting searches by user ID...
    #maybe take meeting ID, resolve user ID, list all recordings by user ID, then match by meeting_id again?
    endpoint = 'meetings/' + str(meeting_id) + '/recordings'
    print(endpoint)
    response = client.get_request(endpoint)
    #print(response)
    #print(response.content)
    recordings = json.loads(response.content)
    print(recordings)
    print(type(recordings))
    #for meeting in recording_list['meetings']:
        #write meeting header
        #ifile = 1
        #topic = str(meeting['topic'])
        #meeting_id = str(meeting['id'])
        #share_url = str(meeting['share_url'])
        #print("'" + topic + "', '" + meeting_id + "', '" + share_url + "'")
    for file in recordings:
        type(file)
        #retrieve actual meeting files
        parent_meeting = str(file['meeting_id'])
        start_time = str(file['recording_start'])
        end_time = str(file['recording_end'])
        share_url = str(file['share_url'])
        print("'" + str(ifile) + "', '" + parent_meeting + "', '" + start_time + "', '" + end_time + "', '" + redist_url + "'")
        #inc counter after
        ifile + 1

def get_recordings_from_config(config):
    for user in config['Users']:
        meetings = config['Users'][user].split(',')
        print(meetings)
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
    if args.get:
        #by host ID
        get_recordings_by_host_id(args.userid)
        #by meetind ID
    else:
        get_recordings_from_config(config)
        
