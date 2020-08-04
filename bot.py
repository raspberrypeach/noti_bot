def msg_thd(mqueue, mlock, user_data):  # message thread
    infoMsg = "등록된 명령어 목록\n!사진: 사진전송\n!온도: 온도출력\n!불켜: LED ON\n!불꺼: LED OFF\n!열기: 문열기\n!닫기: 문닫기"  # default message
    bot = telepot.Bot(Param.token)  # 봇 초기화



    def my_callback_query(msg):  # interrupt 메시지의 버튼을 클릭하였을떄 열기/거부를 처리하는 함수
        """
        text가 아니라 interrupt 발생후 버튼메시지가 전송되었을때는
        문자열파싱이 아니라 callback_query 함수에서 처리합니다.
        """
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
        receiver_id = Check_user(id)  # 사용자가 등록한 라즈베리파이번호 - linkded list의 index

        if receiver_id is -1:  # 사용자 정보가 등록되지 않은 경우
            bot.sendMessage(id, '등록되지 않았습니다')
            bot.sendMessage(id, infoMsg)
            print('[msg_thd]등록되지 않았습니다. 사용자 ID: ', id)

        else:  # 사용자 정보가 등록된 경우
            if content == 'text':
                print('[msg_thd]수신한 메시지: ', msg['text'], ' 사용자 ID: ', id)

                '''
                사용자가 고객센터에 문의 접수하기:
                !문의 채팅을 전송하면 Param.py파일의 ques_flag 변수가 True로 변경되어 
                DB에 고객문의사항을 등록하게 됩니다.
                등록된 문의사항은 직원이 웹페이지에서 확인이 가능하게 됩니다.

                table entityes: 5개
                num int, id int, contents varchar(250), time varchar(300), reply varchar(250), primary key(num)                
                '''
                if Param.ques_flag is True:  # <!문의> 메시지 수신 직후
                    c_time = datetime.datetime.now().strftime(' %Y년 %m월 %d일 %H시 %M분 %S초')  # time info

                    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='smartHome',
                                         charset='utf8')
                    dict = db.cursor(pymysql.cursors.DictCursor)

                    # DB table에서 num(문의 번호)는 현재 tuple 갯수 + 1개로 설정합니다
                    sql_count = 'SELECT COUNT(*) FROM smartHome.query_table'
                    dict.execute(sql_count)
                    sql_count = dict.fetchall()

                    print(sql_count)
                    sql_count = sql_count[0]['COUNT(*)'] + 1

                    # DB insert
                    sql_insert = 'insert into smartHome.query_table values(%s, %s, %s, %s, %s)'  # SQL
                    dict.execute(sql_insert, (sql_count, id, msg['text'], c_time, '아직 답변이 등록되지 않았습니다'))
                    db.commit()

                    # DB close
                    db.close()

                    bot.sendMessage(id, "고객센터에 문의사항이 제출되었습니다!")
                    print('고객센터에 문의사항이 제출되었습니다!')
                    Param.ques_flag = False  # 문의사항 접수 후 flag값 변경합니다

                else:  # 사용자로부터 메시지를 수신하고, 내용에 따라 응답합니다
                    mlock.acquire()  # critical section
                    print('msg inner lock')
                    try:
                        if msg['text'] == '!사진':  # 사진 요청
                            bot.sendMessage(id, '사진 전송을 요청하였습니다. ')
                            msgTemp = {'1. sender': id, '2. receiver': receiver_id, '3. DataType': 'instruction',
                                       '4. DataSize': -1, '5. DataName': -1, '6. description': 'IMG REQUEST',
                                       '7. count': Param.DEFAULT_COUNT}
                            mqueue.put(msgTemp)
                            print('[msg_thd]photo request sent')

                        elif msg['text'] == '!온도':  # 현재 온도 요청
                            msgTemp = {'1. sender': id, '2. receiver': receiver_id, '3. DataType': 'instruction',
                                       '4. DataSize': -1, '5. DataName': -1, '6. description': 'TEMP REQUEST',
                                       '7. count': Param.DEFAULT_COUNT}
                            mqueue.put(msgTemp)
                            print('[msg_thd]temperature request sent')

                        elif msg['text'] == '!불켜':  # LED 켜기
                            msgTemp = {'1. sender': id, '2. receiver': receiver_id, '3. DataType': 'instruction',
                                       '4. DataSize': -1, '5. DataName': -1, '6. description': 'LIGHT ON',
                                       '7. count': Param.DEFAULT_COUNT}
                            mqueue.put(msgTemp)
                            print('[msg_thd]LED_ON request sent')
                            bot.sendMessage(id, 'LED를 켰습니다.')

                        elif msg['text'] == '!불꺼':  # LED 끄기
                            msgTemp = {'1. sender': id, '2. receiver': receiver_id, '3. DataType': 'instruction',
                                       '4. DataSize': -1, '5. DataName': -1, '6. description': 'LIGHT OFF',
                                       '7. count': Param.DEFAULT_COUNT}
                            mqueue.put(msgTemp)
                            print('[msg_thd]LED_OFF request sent')
                            bot.sendMessage(id, 'LED를 껐습니다.')

                        elif msg['text'] == '!열기':  # 문 열때
                            msgTemp = {'1. sender': id, '2. receiver': receiver_id, '3. DataType': 'instruction',
                                       '4. DataSize': -1, '5. DataName': -1, '6. description': 'OPEN THE DOOR',
                                       '7. count': Param.DEFAULT_COUNT}
                            mqueue.put(msgTemp)
                            print('[msg_thd]DOOR_OPEN request sent')
                            bot.sendMessage(id, '문을 여는중입니다.')

                        elif msg['text'] == '!닫기':  # 문 닫을떄
                            msgTemp = {'1. sender': id, '2. receiver': receiver_id, '3. DataType': 'instruction',
                                       '4. DataSize': -1, '5. DataName': -1, '6. description': 'CLOSE THE DOOR',
                                       '7. count': Param.DEFAULT_COUNT}
                            mqueue.put(msgTemp)
                            print('[msg_thd]DOOR_CLOSE request sent')
                            bot.sendMessage(id, '문을 닫는중입니다.')

                        elif msg['text'] == '!문의':  # 사용자가 문의사항을 입력할떄
                            bot.sendMessage(id, '문의사항을 입력해주세요')
                            Param.ques_flag = True  # ques_flag값이 TRUE가 되어 다음 입력은 DB에 등록됩니다.
                            print('[msg_thd]customer inquiry')

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