# 链接: https://pan.baidu.com/s/1JoB5E1PLtKVsePVNJOlJtg  密码: mtaj
import os
from pathlib import Path

DIRECTORIES = {
    "图片": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "视频": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "文档": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx",".csv",",pdf"],
    "压缩文件": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "影音": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "文本": [".txt", ".in", ".out"],
    "编程": [".py",".html5", ".html", ".htm", ".xhtml",".c",".cpp",".java",".css"],
    "可执行程序": [".exe"],
}

FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}

def auto_organize(dirval):
    # 整理对应的文件夹下的文件
    for entry in os.scandir(dirval):
        if entry.is_dir():
            # 如果是文件夹则跳过
            continue
        file_path = Path(dirval + "\\" + entry.name)
        file_format = file_path.suffix.lower()
        # 避免后缀大小写判断问题，全转为小写
        if file_format in FILE_FORMATS:
            directory_path = Path(dirval + "\\" + FILE_FORMATS[file_format])
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(entry.name))

    try:
        os.mkdir(dirval + "\\" +"其他文件")
    except:
        pass

    for dir in os.scandir(dirval):
        try:
            if dir.is_dir():
                # 删除空文件夹
                os.rmdir(dir)
            else:
                temp = str(Path(dir)).split('\\')
                # 分割文件路径
                path = '\\'.join(temp[:-1])
                print(path + '\\其他文件\\' + str(temp[-1]))
                os.rename(str(Path(dir)), path + '\\其他文件\\' + str(temp[-1]))
        except:
            pass


if __name__ == "__main__":
    auto_organize(r"C:\Users\83493\Downloads")
