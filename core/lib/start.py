import os
import platform

from core.common.helper import get_scrapyd_cli
from hq_crawler import settings


def deploy_scrapy(scrapyd_deploy: str = ''):
    scrapyd_project_list = get_scrapyd_cli().list_projects()
    scrapy_project_name = settings.SCRAPY_PROJECT

    if scrapy_project_name not in scrapyd_project_list:
        if platform.system() == 'Windows':
            if scrapyd_deploy != '':
                cmd = f'cd {settings.SPIDER_PATH} && python {scrapyd_deploy} -p {scrapy_project_name}'
            else:
                cmd = f'cd {settings.SPIDER_PATH} && python {settings.BASE_DIR}\\venv\Scripts\\scrapyd-deploy -p {scrapy_project_name}'

            status = os.system(cmd)
            if status != 0:
                raise Exception('windows环境执行注册scrapyd项目错误，请检查目录路径、python环境，是否已安装scrapyd、scrapyd client')
        else:
            os.system(f'scrapyd-deploy -p {scrapy_project_name}')
