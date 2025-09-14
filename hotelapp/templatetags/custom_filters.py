from django import template

# 创建一个模板库对象
register = template.Library()


# 定义一个自定义过滤器
@register.filter
def length_is(value, arg):
    """
    此过滤器用于检查 value 的长度是否等于 arg
    :param value: 要检查长度的对象
    :param arg: 期望的长度
    :return: 如果 value 的长度等于 arg，则返回 True；否则返回 False
    """
    return len(value) == int(arg)
