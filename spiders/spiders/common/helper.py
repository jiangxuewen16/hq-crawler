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
