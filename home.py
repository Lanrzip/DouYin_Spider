import os
import time
import json
import requests
from dy_utils.dy_util import (
    get_cpu_usage,
    norm_str, download_media, check_and_create_path, get_headers,
    get_list_params, splice_url, handle_list_video_info_each,
    js, save_video_detail, check_info,
    download_media_from_server
)
from profile import Profile
import paramiko


server_user = "root"
server_host = "region-42.seetacloud.com"
server_path = "/root/"
server_port = 27691
server_password = "8VGQlBc7XbQU"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server_host, port=server_port, username=server_user, password=server_password)

transport = paramiko.Transport((server_host, server_port))
transport.connect(username=server_user, password=server_password)
sftp = paramiko.SFTPClient.from_transport(transport)

class Home:
    def __init__(self, info=None):
        if info is None:
            self.info = check_info()
        else:
            self.info = info
        self.profile = Profile(self.info)
        self.list_url = "https://www.douyin.com/aweme/v1/web/aweme/post/"
        self.headers = get_headers()
        if not os.path.exists("./static/header_and_cookie.json"):
            with open("./static/header_and_cookie.json", "w", encoding="utf-8") as f:
                f.write(json.dumps({
                    'headers': self.headers,
                    'cookies': self.info['cookies']
                }))
        sftp.put("./static/header_and_cookie.json", server_path+'main/'+'header_and_cookie.json')
    # 主页
    def get_all_video_info(self, url):
        profile = self.profile.get_profile_info(url)
        video_list = []
        sec_user_id = url.split('/')[-1]
        max_cursor = '0'
        while True:
            params = get_list_params()
            params['webid'] = self.info['webid']
            params['msToken'] = self.info['msToken']
            params['max_cursor'] = max_cursor
            params['sec_user_id'] = sec_user_id
            splice_url_str = splice_url(params)
            xs = js.call('get_dy_xb', splice_url_str)
            params['X-Bogus'] = xs
            post_url = self.list_url + '?' + splice_url(params)
            response = requests.get(post_url, headers=self.headers, cookies=self.info['cookies'])
            res_json = response.json()
            max_cursor = str(res_json['max_cursor'])
            has_more = res_json['has_more']
            for item in res_json['aweme_list']:
                video_detail = handle_list_video_info_each(item)
                video_list.append(video_detail)
            print(f'已经获取到 {len(video_list)} 条视频信息，共 {profile.aweme_count} 条视频信息（数量可能不准确）（未开始下载）')
            if has_more == 0:
                break
        return video_list, profile

    # 主页
    def save_all_video_info(self, url, need_cover=False):
        profile = self.profile.save_profile_info(url)
        nickname = norm_str(profile.nickname)
        aweme_count = profile.aweme_count
        user_path = f'./datas/{nickname}_{profile.sec_uid}'
        sec_user_id = profile.sec_uid
        max_cursor = '0'
        index = 1
        batch = 1
        while batch < 1000:
            video_list = []
            params = get_list_params()
            params['webid'] = self.info['webid']
            params['msToken'] = self.info['msToken']
            params['max_cursor'] = max_cursor
            params['sec_user_id'] = sec_user_id
            splice_url_str = splice_url(params)
            xs = js.call('get_dy_xb', splice_url_str)
            params['X-Bogus'] = xs
            post_url = self.list_url + '?' + splice_url(params)
            while True:
                try:
                    response = requests.get(post_url, headers=self.headers, cookies=self.info['cookies'])
                    res_json = response.json()
                except requests.exceptions.JSONDecodeError:
                    print('JSONDecodeError 重试中...')
                    time.sleep(5)
                    continue
                break
            max_cursor = str(res_json['max_cursor'])
            has_more = res_json['has_more']
            for item in res_json['aweme_list']:
                video_detail = handle_list_video_info_each(item)
                video_list.append(video_detail)
            self.save_videos_info(video_list, index, nickname, user_path, aweme_count, need_cover)
            index += len(video_list)
            batch += 1
            print(f'已经获取到 {index - 1} 条视频信息，共 {profile.aweme_count} 条视频信息（如果存在共创视频，数量可能更多！）')
            if has_more == 0:
                break
            # break
        print(f'用户 {profile.nickname} 全部视频信息保存成功')

    # 工具类，用于保存信息
    def save_videos_info(self, video_list, index, nickname, user_path, aweme_count, need_cover):
        for video in video_list:
            try:
                title = norm_str(video.title)
                if len(title) > 50:
                    title = title[:50]
                if title.strip() == '':
                    title = f'无标题'
                path = f'{user_path}/{title}_{video.awemeId}'
                
                print(f'用户: {nickname}, 第{index}条视频: 标题: {title}')

                # 从服务器下载视频并检查该视频是否已经存在
                while True:
                    cpu_usage = get_cpu_usage(ssh)
                    if cpu_usage < 80:
                        # print('path: ', path)
                        # print('url: ', video.video_addr)
                        # print('nickname: ', nickname)
                        # print('index: ', index)
                        # print('title: ', title)
                        stdout, stderr = download_media_from_server(path, video.video_addr, nickname, index, title, ssh)
                        break
                    else:
                        print(f"CPU usage is {cpu_usage}%, waiting for CPU usage to drop below 80%")
                        time.sleep(5)  # 等待 5 秒后重新检查 CPU 使用率

                # exit_status = stdout.channel.recv_exit_status()
                print(stdout.read().decode())
                print(stderr.read().decode())
                # if exit_status == 0:
                #     print(f"    - 服务器端下载视频成功: {title}")
                # else:
                #     print(f"Download failed: {title}, Error: {stderr.read().decode()}")
                
                # 检查本地是否已经存在该视频相关文件
                exist = check_and_create_path(path)
                if exist and not need_cover:
                    print(f'    ---本地机--- 用户: {nickname}, 第{index}条视频: 标题: {title} 本地已存在，跳过保存')
                    print('============================================================================================================')
                    continue
                save_video_detail(path, video)
                if len(video.images) > 0:
                    for img_index, image in enumerate(video.images):
                        download_media(path, f'image_{img_index}', image['url_list'][0], 'image', f'第{img_index}张图片', headers=self.headers, cookies=self.info['cookies'])
                else:
                    download_media(path, 'cover', video.video_cover, 'image', '视频封面', headers=self.headers, cookies=self.info['cookies'])
                # download_media(path, 'video', video.video_addr, 'video', headers=self.headers, cookies=self.info['cookies'])
                # print(self.headers)
                # print(self.info['cookies'])
         
                print(f'用户: {nickname}, 第{index}条视频, 标题: {title} 保存成功, 共 {aweme_count} 条视频信息（如果存在共创视频，数量可能更多！）')
                print('============================================================================================================')
            except Exception as e:
                raise e
                print(f'用户: {nickname}, 第{index}条视频, 标题: {norm_str(video.title)} 保存失败')
            finally:
                index += 1

    def main(self, url_list):
        for url in url_list:
            try:
                self.save_all_video_info(url)
            except Exception as e:
                raise e
                print(f'用户 {url} 查询失败')


if __name__ == '__main__':
    home = Home()
    url_list = [
        'https://www.douyin.com/user/MS4wLjABAAAAp2OG100fRV13HqBbRnbPM_l7DU0eTOaxgL-4_l07fQo',
        'https://www.douyin.com/user/MS4wLjABAAAAigSKToDtKeC5cuZ3YsDrHfYuvpLqVSygIZ0m0yXfUAI',
    ]
    home.main(url_list)


