from search import Search
from home import Home





if __name__ == '__main__':
    # search = Search()
    # query = '美食教学'
    # sort_type = '0'
    # number = 20
    # publish_time = '0'
    # info = {
    #     'query': query,
    #     'number': number,
    #     'sort_type': sort_type,
    #     'publish_time': publish_time
    # }

    # video_list = search.get_search_data(**info)

    # author_info_list = [
    #     {
    #         'nickname': video.nickname,
    #         'sec_uid': video.sec_uid

    #     }
    #     for video in video_list
    # ]
    author_info_list = [
        # {
        #     'nickname': '灭爸局长',
        #     'sec_uid': 'MS4wLjABAAAAsrB8awcgHz_JOjECwWm2_6tWHGsSCL_-JpXXexJ5k2kS8LTjRDZKQJeaJ6lkXlYQ'
        # },
        # {
        #     'nickname': '公考面试老梅',
        #     'sec_uid': 'MS4wLjABAAAApbYr5AV6Wxbtw2sPjFd58U6TjJgkxn0JCI_ifWLZZNM'
        # },
        # {
        #     'nickname': '毕上公考',
        #     'sec_uid': 'MS4wLjABAAAApfBs4gXZgp8QtBT4F_XPqRIfsnGvRrMfr3GxziEVXXs'
        # },
        {
            'nickname': '左岸讲公考',
            'sec_uid': 'MS4wLjABAAAAda4ZZRoK8NC56LdhusXP_kdGHRlYJDs67EiHuw64hGsyAThJoZ_FiTkam8fWh5fp'
        },
        # {
        #     'nickname': '公考江牧云',
        #     'sec_uid': 'MS4wLjABAAAAEd9fiLYWmKr0nx7MgGQcoesAyND61rJLibg7uIPNsZz0uq0oszjUUbjEWjGBTPjy'
        # },
        {
            'nickname': '老夏说公务员面试',
            'sec_uid': 'MS4wLjABAAAA5lSb0ZdMxcYGQv6p0oub5N38hKA1bpi58JA98pyWgcw'
        },
        {
            'nickname': '带你上岸的滕嘉嘉',
            'sec_uid': 'MS4wLjABAAAAfJDYFVs00EDbP0onrZLE5Wh4JkPL89JWkO9zZbkpSZFAAiEqXu9re1h42f3nEM5q'
        },
    ]
    print(author_info_list)

    home = Home()
    url_list = [
        f'https://www.douyin.com/user/{author_info["sec_uid"]}'
        for author_info in author_info_list
    ]
    home.main(url_list)