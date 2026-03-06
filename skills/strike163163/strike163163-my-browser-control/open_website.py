# /Users/mac/Desktop/my-browser-skill/open_website.py
import webbrowser
import sys

# 核心函数：支持接收外部传入的网址参数
def open_website(url="https://www.baidu.com"):
    """
    打开指定网址的函数，Agent 调用时会传url参数进来
    :param url: 要打开的网址，默认打开百度
    """
    try:
        # 调用Mac默认浏览器打开网址
        webbrowser.open(url)
        # 返回Agent能识别的成功结果（JSON格式）
        return {
            "success": True,
            "url": url,
            "message": f"已成功在默认浏览器中打开：{url}"
        }
    except Exception as e:
        # 异常处理，返回错误信息
        return {
            "success": False,
            "error": str(e),
            "message": "打开网页失败，请检查网址是否正确"
        }

# 支持终端传参（比如 python3 open_website.py https://zhihu.com）
if __name__ == "__main__":
    # 如果终端传了网址参数，就用传的；没传就用默认百度
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "https://www.baidu.com"
    result = open_website(target_url)
    print(result)