from baguio_mc import scrape_bmc_news
from baguio_news import scrape_baguio_news
from lda import initiate_topic_modelling

from multiprocessing import Process, Manager

compiled_data = {
    "title": [],
    "date": [],
    "content": []
}

if __name__ == '__main__':
    # bn = subprocess.run(['python', 'baguio_news.py', "2023-04-30"], capture_output=True, text=True).stdout.strip()
    # bmc = subprocess.run(['python', 'baguio_mc.py', "2023-04-30"], capture_output=True, text=True).stdout.strip()

    manager = Manager()
    return_dict = manager.dict()

    p1 = Process(target=scrape_baguio_news, args=("2023-04-30", return_dict))
    p2 = Process(target=scrape_bmc_news, args=("2023-04-30", return_dict))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    merged_dict = {k: return_dict['baguio_news'].get(k, []) + return_dict['baguio_mc'].get(k, []) for k in set(return_dict['baguio_news'].keys()) | set(return_dict['baguio_mc'].keys())}
    print(merged_dict)