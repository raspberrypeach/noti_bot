import telepot
import parameter


def msg_thd(queue, lock):  # message thread
    defaultMsg = "공지사항 알리미 입니다.\n공지사항에 새로운글이 업로드되면 알림이 전송됩니다!"  # default message
    bot = telepot.Bot(parameter.token)  # 봇 초기화

    def Check_user(vid):  # DB에 등록된 ID인지 확인합니다.
        for index in user_data:
            if index['user_id'] == vid:  # 등록된 경우
                return True  # DB에 등록된 정보(라즈베리파이 번호)를 반환
        return -1  # 사전에 등록된 정보가 아닌경우 -1를 반환합니다

    def my_callback_query(msg):  # interrupt 메시지의 버튼을 클릭하였을떄 열기/거부를 처리하는 함수
        queryID, id, contents = telepot.glance(msg, flavor='callback_query')  # 메시지를 수신하면 queryID, id, query내용으로 반환
        print('[msg_thd]수신한 메시지: ', contents, ' 사용자 ID: ', id)

        mlock.acquire()  # critical section
        try:
            if contents == '!허가':  # 문 열때
                msgTemp = {'1. sender': id, '2. receiver': Check_user(id), '3. DataType': 'instruction',
                           '4. DataSize': -1, '5. DataName': -1, '6. description': 'OPEN THE DOOR',
                           '7. count': Param.DEFAULT_COUNT}

                mqueue.put(msgTemp)
                bot.sendMessage(id, '문을 여는중입니다!')
                print('[msg_thd]DOOR_OPEN request sent')

            elif contents == '!거부':  # 문 닫을때
                bot.sendMessage(id, '거부되었습니다!')
                print('[msg_thd]DOOR noti rejected')

            else:
                print('error')

        except Exception as e:  # 예외처리
            print(e)
        finally:
            mlock.release()

    def Message(msg):  # 사용자메시지 수신하여 처리하는 함수입니다.
        content, chat, id = telepot.glance(msg)  # 메시지를 수신하면 내용, chat, id로 반환

        if Check_user(id) is True:  # 사용자 정보가 등록되지 않은 경우
            bot.sendMessage(id, '등록되지 않았습니다.\n알림을 수신하려면 !등록 명령어를 먼저 입력해주세요!')
            bot.sendMessage(id, defaultMsg)
            print('[msg_thd]등록되지 않았습니다. 사용자 ID: ', id)

        else:  # 사용자 정보가 등록된 경우
            if content == 'text':
                print('[msg_thd]수신한 메시지: ', msg['text'], ' 사용자 ID: ', id)

                lock.acquire()  # critical section
                try:
                    if msg['text'] == '!사진':  # 사진 요청
                        bot.sendMessage(id, '사진 전송을 요청하였습니다. ')
                        mqueue.put(msgTemp)
                        print('[msg_thd]photo request sent')

                    else:  # 등록되지않은 문자열인경우
                        bot.sendMessage(id, '무슨 말인지 모르겠어요')
                        bot.sendMessage(id, infoMsg)
                        print('[msg_thd]content error')

                except Exception as e3:  # 예외처리
                    print('[msg_thd]', e3)
                finally:
                    print("msg inner release")
                    mlock.release()

    bot.message_loop({'chat': Message, 'callback_query': my_callback_query})  # loop으로 동작하며 사용자메시지에 응답

    while True:
        time.sleep(1)
