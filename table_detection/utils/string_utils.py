def strip_value(text):
    """

    :param text:
    :return:
    """
    currencies = u'$¢£¤¥֏؋৲৳৻૱௹฿៛₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾꠸﷼﹩＄￠￡￥￦'
    text = text.strip('\n\r\t ' + currencies + "'+*/%^_:;'\"\\|").rstrip('-')
    return text