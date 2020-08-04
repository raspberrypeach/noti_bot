from multiprocessing import Lock, Process, Queue
import crawling
import bot

if __name__ == '__main__':
    # queue, lock 설정
    queue = Queue()
    lock = Lock()

    # msg_thd 초기화
    Message_thd = Process(target=bot.msg_thd, args=(queue, lock))
    Message_thd.start()

    send_thd = Process(target=crawling, args=(queue, lock))
    send_thd.start()
