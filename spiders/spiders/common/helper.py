from spiders.items import marketing


class String(object):
    """
    字符串列表在某个字符串出现的次数列表
    """

    @classmethod
    def str_count_list(cls, base_str: str, str_list: list, is_filter: bool = False) -> dict:
        counts = {}
        for item in str_list:
            num = base_str.count(item)
            if not is_filter or (is_filter and num != 0):
                counts[item] = base_str.count(item)
        return counts


def get_media_account(cls):
    account_list = marketing.Account.objects(platform=cls.we_media_id).all()
    if len(account_list):
        for account in account_list:
            if account.authorization_information is not None:
                for item in account.authorization_information.split(';'):
                    kv = item.strip().split('=')
                    cls.cookie_list[kv[0]] = kv[1]
                account.type = cls.we_media_type
                account.platform = cls.we_media_id
                return [account, cls.cookie_list]
            else:
                # todo::报错给推广部
                pass
    else:
        # todo::报错给推广部
        pass
