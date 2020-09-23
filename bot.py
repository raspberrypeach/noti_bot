import telepot
import param
import time
from database import *
from crawling import *

bot = telepot.Bot(param.token)  # initialize bot


def Message(msg):
    defaultMsg = "정보통신공학과 공지사항 알림봇 입니다.\n공지사항에 새로운글이 업로드되면 알림이 전송됩니다!"  # default message
    helpmsg = "!등록: 알림시작\n!종료: 알림종료\n!최근글: 최근에 등록된 게시글(2개)"
    content, chat, id = telepot.glance(msg)  # 메시지를 수신하면 내용, chat, id로 반환

    try:
        if database('check', id=id) is False:  # 사용자 정보가 등록되지 않은 경우
            if msg['text'] == '/start' or msg['text'] == '!등록':  # 등록
                bot.sendMessage(id, defaultMsg)
                bot.sendMessage(id, '이제부터 알림서비스가 제공됩니다.')
                database('register', id=id)
            else:
                bot.sendMessage(id, '등록되지 않았습니다.\n알림을 수신하려면 !등록 명령어를 먼저 입력해주세요!')
                print('등록되지 않았습니다. 사용자 ID: ', id)

        else:  # 사용자 정보가 등록된 경우
            if content == 'text':
                print('수신한 메시지: ', msg['text'], ' 사용자 ID: ', id)
                if msg['text'] == '!종료':  # 삭제
                        bot.sendMessage(id, '알림 종료!')
                        database('delete', id=id)

                elif msg['text'] == '/start' or msg['text'] == '!등록':  # 등록
                    bot.sendMessage(id, '이미 등록된 계정입니다!')

                elif msg['text'] == '!최근글':  # 최근글
                    bot.sendMessage(id, '최근글 2개 불러오는중...')

                    # WEB crawling
                    crawling()
                    feed = feedparser.parse('rssList.xml')

                    for i in range(param.message_num):
                        bot.sendMessage(id, feed['entries'][i]['title'])
                        bot.sendMessage(id, feed['entries'][i]['link'])

                else:
                    bot.sendMessage(id, '무슨 말인지 모르겠어요')
                    bot.sendMessage(id, helpmsg)
                    print('unknown message')
            else:
                bot.sendMessage(id, defaultMsg)
                bot.sendMessage(id, helpmsg)

    except Exception as e:  # 예외처리
        bot.sendMessage(857044101, 'error!:  ' + str(e))



bot.message_loop(Message)

if __name__ == '__main__':
    while True:
        time.sleep(1)
