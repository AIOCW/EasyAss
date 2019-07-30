import urllib
import ssl
import json
import random

# # client_id 为官网获取的AK， client_secret 为官网获取的SK
# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ak&client_secret=sk'
# request = urllib.request.Request(host)
# request.add_header('Content-Type', 'application/json; charset=UTF-8')
# response = urllib.request.urlopen(request)
# content = response.read()
# if (content):
#     print(content)
#
#     content.decode('utf-8')
#     content = json.loads(content)
#     print(content['access_token'])

#-*- version: Python3.0 -*
#-*- coding: UTF-8      -*
import urllib.request

headers = {'Content-Type':'application/json'}
# access_token = content['access_token']
access_token = '24.28cff53af4acb2cf08649af5802eac0e.2592000.1567086565.282335-16920155'
print(access_token)


def get_result(question, session_id):
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token
    post_data = '{"log_id":"try_again88888888",' \
                '"version":"2.0",' \
                '"service_id":"S20770",' \
                '"session_id":"' + session_id + '",' \
                '"request":{"query":"' + question + '","user_id":"88888"},' \
                '"dialog_state":{"contexts":{"SYS_REMEMBERED_SKILLS":["1057"]}}}'
    try:
        request = urllib.request.Request(url,data=post_data.encode('utf-8'),headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")
        content = json.loads(content)
    except:
        return "哦哦，我卡住了", None
    if content:
        print(content)
        result = content['result']
        print(result)
        session_id = result['session_id']
        print(session_id)
        response = result['response_list'][0]
        print(response)
        action_list = response['action_list']
        action = action_list[random.randint(0, len(action_list))]
        print(action)
        say = action['say']
        print(say)
        return say, session_id
    return "哦哦，我卡住了", None


"{'result': " \
    "{" \
    "'version': '2.0'," \
    " 'timestamp': '2019-07-30 22:00:25.715'," \
    " 'service_id': 'S20770', " \
    "'log_id': 'try_again88888888'," \
    " 'session_id': 'service-session-id-1564495225715-0504cdd87fa54fad91e29012428bf5b4'," \
    " 'interaction_id': 'service-interactive-id-1564495225715-e69daa6019654b8c862a35dfc87d0123', " \
    "'response_list': " \
        "[{'status': 0," \
        " 'msg': 'ok'," \
        " 'origin': '71559'," \
        " 'schema': {'intent_confidence': 1.0, 'intent': 'BUILT_CHAT'}," \
        "'action_list':" \
            " [" \
            "{'action_id': '','refine_detail': {},'confidence': 1.0,  'custom_reply': '', 'say': '你好，想聊什么呢。~','type': 'chat'}, " \
            "{'action_id': '', 'refine_detail': {}, 'confidence': 1.0, 'custom_reply': '', 'say': '有礼貌的好孩子', 'type': 'chat'}, " \
            "{'action_id': '', 'refine_detail': {}, 'confidence': 1.0, 'custom_reply': '', 'say': '你好。咱们聊一会呀', 'type': 'chat'}" \
            "]," \
        " 'qu_res': {}}" \
        "], " \
    "'dialog_state': " \
    "{'contexts': {'SYS_REMEMBERED_SKILLS': []}, 'skill_states': {}}}, 'error_code': 0}"


if __name__ == "__main__":
    response, session_id = get_result("现在几点了", "")
    print(response, session_id)