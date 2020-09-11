# -*- coding: utf-8 -*-


def format_time(seconds):
    """格式化时间"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    seconds *= 1.0

    if hours:
        return f"{hours}h {minutes}m {seconds:.3}s"
    elif minutes:
        return f"{minutes}m {seconds:.3}s"
    else:
        return f"{seconds:.3}s"
