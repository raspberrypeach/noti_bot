import telepot
import param
import time
import feedparser
from database import *

bot = telepot.Bot(param.token)  # 봇 초기화


def Message(msg):
    defaultMsg = "공지사항 알리미 입니다.\n공지사항에 새로운글이 업로드되면 알림이 전송됩니다!"  # default message
    content, chat, id = telepot.glance(msg)  # 메시지를 수신하면 내용, chat, id로 반환

    if database('check', id) is False:  # 사용자 정보가 등록되지 않은 경우
        if msg['text'] == '!등록':  # 등록
            database('register', id)
        else:
            bot.sendMessage(id, '등록되지 않았습니다.\n알림을 수신하려면 !등록 명령어를 먼저 입력해주세요!')
            bot.sendMessage(id, defaultMsg)
            print('등록되지 않았습니다. 사용자 ID: ', id)

    else:  # 사용자 정보가 등록된 경우
        if content == 'text':
            print('수신한 메시지: ', msg['text'], ' 사용자 ID: ', id)

            try:
                if msg['text'] == '!삭제':  # 삭제
                    database('delete', id)

                elif msg['text'] == '!최근글':  # 최근글
                    feed = feedparser.parse('rssList.xml')
                    bot.sendMessage(id, feed['entries'][0]['title'])
                    bot.sendMessage(id, feed['entries'][0]['link'])

                else:
                    bot.sendMessage(id, '무슨 말인지 모르겠어요')
                    print('unknown message')

            except Exception as e3:  # 예외처리
                print('error: ', e3)


bot.message_loop(Message)

if __name__ == '__main__':
    while True:
        time.sleep(1)
