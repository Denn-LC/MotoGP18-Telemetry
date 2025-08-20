def format_time(t_s):
    mins = int(t_s // 60)
    secs = t_s - 60 * mins
    return f"{mins:d}:{secs:06.3f}"
