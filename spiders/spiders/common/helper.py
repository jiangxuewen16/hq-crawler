class String(object):
    """
    字符串列表在某个字符串出现的次数列表
    """
    @classmethod
    def str_count_list(cls, base_str: str, str_list: list) -> dict:
        counts = {}
        for item in str_list:
            counts[item] = base_str.count(item)
        return counts
