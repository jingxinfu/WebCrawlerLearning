import channel_list, pageCrawl
from multiprocessing import Pool


if __name__ == '__main__':
    pool = Pool(processes=5)
    pool.map(pageCrawl.get_all_url_from,channel_list.channel_list)
    pool.close()
    pool.join()