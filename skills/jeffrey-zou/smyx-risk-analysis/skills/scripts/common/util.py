#!/usr/bin/env python3

import os
import traceback

# current_dir = os.path.dirname(os.path.abspath(__file__))  # .../src

import requests
from .config import ApiEnum, ConstantEnum, sys, YamlUtil

# if current_dir not in sys.path:
#     sys.path.insert(0, current_dir)

from .base import BaseUtil
import time
import logging
from typing import Any, Callable, Optional, TypeVar, Dict

if ConstantEnum.IS_DEBUG:
    print("*********====>>>> beign ligns e!!!!!!!!!!!")
    import http.client

    # 【关键代码】开启调试模式
    http.client.HTTPConnection.debuglevel = 1
    # 可选：如果你希望日志更整洁，可以配合 logging 模块（否则打印会比较乱）
    import logging

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


class CommonUtil(BaseUtil):

    @staticmethod
    def trace_exception_stack(e):
        if ConstantEnum.IS_DEBUG:
            print(f"❌ 错误描述: {str(e)}, 堆栈跟踪:")
            traceback.print_stack()

    @staticmethod
    def polling(
            action: Callable[[], Any],
            check_condition: Callable[[Any], bool],
            on_success: Optional[Callable[[Any], None]] = None,
            on_retry: Optional[Callable[[Any, int], None]] = None,
            on_error: Optional[Callable[[Exception], None]] = None,
            interval: float = 1.0,
            max_attempts: int = 5,
            description: str = "轮询任务"
    ) -> Optional[Any]:
        """
        通用的轮询处理函数

        :param action:
            [必填] 执行动作的回调函数。
            例如：发送 HTTP 请求、查询数据库状态等。
            必须返回一个结果对象供 check_condition 使用。

        :param check_condition:
            [必填] 检查是否结束的回调函数。
            接收 action 的返回值，返回 True 表示“满足结束条件”，False 表示“继续轮询”。
            例如：lambda res: res.get('need_refresh') is False

        :param on_success:
            [可选] 当 check_condition 返回 True 时执行的回调（通常用于记录日志或处理最终数据）。

        :param on_retry:
            [可选] 当需要继续轮询时执行的回调。
            参数：(当前结果, 当前尝试次数)。可用于打印进度。

        :param on_error:
            [可选] 当 action 抛出异常时执行的回调。
            参数：(异常对象)。

        :param interval:
            每次轮询之间的等待时间（秒）。

        :param max_attempts:
            最大尝试次数，防止死循环。

        :param description:
            任务描述，用于日志输出。

        :return:
            如果成功，返回 action 的最后一次返回值；如果超时或失败，返回 None。
        """

        attempts = 0
        last_result = None

        print(f"🚀 开始执行 [{description}]...")

        while attempts < max_attempts:
            attempts += 1
            # print(f"[{description}] 第 {attempts}/{max_attempts} 次尝试...")

            try:
                # 1. 执行动作
                result = action()
                last_result = result

                # 2. 检查条件
                if check_condition(result):
                    print(f"✅ [{description}] 成功！条件已满足 (尝试次数: {attempts}, 耗时{interval * attempts}秒)")
                    if on_success:
                        on_success(result)
                    return result

                # 3. 条件未满足，准备重试
                if on_retry:
                    on_retry(result, attempts)
                else:
                    # 默认日志行为
                    print(
                        f"⏳ [{description}] 条件未满足，{interval}秒后重试... ({attempts}/{max_attempts}, 耗时{interval * attempts}秒)")

                time.sleep(interval)

            except Exception as e:
                # 4. 异常处理
                if on_error:
                    on_error(e)
                else:
                    # 默认错误行为：打印错误并继续
                    logging.error(f"❌ [{description}] 发生异常: {e}")
                    print(f"⚠️ [{description}] 遇到错误，{interval}秒后重试...")

                time.sleep(interval)

        # 5. 超时处理
        print(f"⚠️ [{description}] 失败：达到最大尝试次数 ({max_attempts})，强制停止。")
        return None

    @staticmethod
    def is_empty(data):
        # 1. 如果是 None (对应 JSON 的 null)
        if data is None:
            return True

        # 2. 如果是字典或列表，且长度为 0 (对应 {} 或 [])
        if isinstance(data, (dict, list)) and len(data) == 0:
            return True


from datetime import date, datetime


class DatetimeUtil(BaseUtil):
    FORMAT__DATETIME = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def today():
        return DatetimeUtil.now().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def format(date):
        return date.strftime('%Y-%m-%d %H:%M:%S') if type(date) == datetime else date

    @staticmethod
    def parse(date_str):
        return datetime.strptime(date_str, DatetimeUtil.FORMAT__DATETIME) if type(date_str) == str else date_str

    @staticmethod
    def timestamp(date=now()):
        return int(date.timestamp() * 1000)


class RequestUtil(BaseUtil):
    BASE_URL = ApiEnum.BASE_URL_OPEN_API

    @classmethod
    def http_post(cls, url, data=None, params=None, headers=None, *args, **argss):
        return cls.http_request("post", url, data=data, params=params, headers=headers, *args, **argss)

    @classmethod
    def http_put(cls, url, data=None, params=None, headers=None, *args, **argss):
        return cls.http_request("put", url, data=data, params=params, headers=headers, *args, **argss)

    @classmethod
    def http_delete(cls, url, data=None, params=None, headers=None, *args, **argss):
        return cls.http_request("delete", url, data=data, params=params, headers=headers, *args, **argss)

    @classmethod
    def http_get(cls, url, params=None, headers=None, *args, **argss):
        return cls.http_request("get", url, params=params, headers=headers, *args, **argss)

    @classmethod
    def http_request(cls, method, url, data=None, params=None, headers=None, options=None, *args,
                     timeout=ApiEnum.DEFAULT__REQUEST_TIMEOUT, **argss):
        def _get_or_create_user(username):
            _url = ApiEnum.BASE_URL_HEALTH + "/sys/phoneLogin"
            open_id = username
            print("\n1. 创建用户 ConstantEnum.CURRENT__U**** 开始openToen begin creae: " + username + ",url" + _url)
            _data = {
                "silent": 1,
                "register": 1,
                "openId": open_id,
                "mobile": username
            }
            try:
                # _response = _get_or_create_user(username)
                _response = requests.post(_url, json=_data)
                print("******______====>>> get newUser and get create and user, respinse:", _response)
                if _response.status_code == 200:
                    # raise requests.exceptions.RequestException(
                    #     response, response=response)
                    _response_json = _response.json()
                    # if _response_json:
                    if _response_json and _response_json.get("success"):
                        return _response_json and _response_json.get("result")
                # return _response
            except Exception as _e:
                CommonUtil.trace_exception_stack(_e)
            return {}
            # return {
            #     "open_token": "AAA1___" + ApiEnum.OPEN_TOKEN,
            #     "token": "AAA222222___" + ApiEnum.TOKEN
            # }

        try:
            headers = headers or {}
            if not url.startswith("https://") and not url.startswith("http://"):
                url = cls.BASE_URL + url
            headers['App-Id'] = ConstantEnum.APP__ID
            print("******=-=====>>>>> get apiToken:", ApiEnum.TOKEN, "CURRENT__USER_NAME:",
                  ConstantEnum.CURRENT__USER_NAME)
            print("******=-=====>>>>> get api+_++open.Token:", ApiEnum.OPEN_TOKEN)

            current__user_name = ConstantEnum.CURRENT__USER_NAME or ConstantEnum.CURRENT__OPEN_ID
            print("⚠️******=-=====>>>>> get api+_++open.Token:", ApiEnum.OPEN_TOKEN, "current__user_name",
                  current__user_name)
            if (not ApiEnum.TOKEN or not ApiEnum.OPEN_TOKEN) and current__user_name:
                try:
                    from .dao import UserDao, User
                    user_dao = UserDao()
                    # article_dao = ArticleDao()

                    # 1. 创建用户
                    print(
                        "\n1. 创建用户 ConstantEnum.CURRENT__USER_NAME  and new *****____+===>>>>>> : " + current__user_name)
                    found_user = user_dao.get_by_username(current__user_name)
                    # print("*****+====>>>> get foundUser and user Iname:", found_user, "user.id", "__userName:",
                    #       "__found_user:", found_user.username, found_user.token[:20], found_user.open_token[:20])
                    if found_user:
                        ApiEnum.TOKEN = found_user.token
                        ApiEnum.OPEN_TOKEN = found_user.open_token
                    else:
                        new_current_user = _get_or_create_user(current__user_name)
                        if new_current_user:
                            ApiEnum.TOKEN = new_current_user.get("token")
                            ApiEnum.OPEN_TOKEN = new_current_user.get("openToken")
                            new_found_user = user_dao.update_by_username(current__user_name, token=ApiEnum.TOKEN,
                                                                         open_token=ApiEnum.OPEN_TOKEN,
                                                                         source=ConstantEnum.APP__SOURCE)
                except Exception as e:
                    ApiEnum.TOKEN = ApiEnum.OPEN_TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ0ZW5hbnROYW1lIjoi55Sf5ZG95raM546w5Lqn56CU5Zui6ZifIiwidXNlclJlYWxOYW1lIjoi55Sf5ZG95raM546w5Lqn56CU5Zui6ZifIiwidGVuYW50SWQiOjE3Njk2MTM3NzgyMjcxMDAwMDAsInJvbGVDb2RlcyI6WyJST0xFX1NNWVhfQURNSU4iLCJST0xFX1BBVElFTlQiLCJST0xFX0RPQ1RPUiIsIlJPTEVfQUlfQU5BTFlTSVMiXSwidGVuYW50Q29kZSI6IjEzMjYwNjU3MDA4IiwicGVybWlzc2lvbkNvZGVzIjpbXSwidXNlcklkIjoxNzY5NjEzNzc4MjI3MTAwMDA4LCJ1c2VybmFtZSI6MTc2OTYxMzc3ODIyNzEwMDAwMCwic3ViIjoiMTMyNjA2NTcwMDgiLCJpYXQiOjE3NzMzODIzNjcsImV4cCI6MTc3Mzk4NzE2N30.C129EZR9NCaNZNOu11uCE8N5qYoGuo3QBpC-fjwQyepXifFJIyEtdx0RU3LRH8GXtNiq67a6AixAxP7tukGoQA"
                    print("******=-=====>>>>> get api+_++open.Token 22232212111 ge terror :", ApiEnum.OPEN_TOKEN)
                    CommonUtil.trace_exception_stack(e)
                    print("******=-=====>>>>> get apiTokenan error:", ApiEnum.TOKEN, "CURRENT__USER_NAME:",
                          ConstantEnum.CURRENT__USER_NAME)
                    # raise

            print("******=-=====>>>>> get api+_++open.Token 44444444444:", ApiEnum.OPEN_TOKEN)

            headers.setdefault("X-Access-Token", ApiEnum.TOKEN)
            headers.setdefault("Authorization", ApiEnum.OPEN_TOKEN)

            data = data or {}
            params = params or {}
            options = options or {}
            data.setdefault('tenantCode', ConstantEnum.CURRENT__TENTANT_CODE)
            if current__user_name:
                data.setdefault('pnaUserName', current__user_name)

            if bool(options.get("data_as_params")):
                params.update(data)

            # print("*****+++++====>>>> get usr:", argss, "options", options)

            print(f"请求拦截URL: {url}", "method", method, "params", params, "data", data, "headers", headers,
                  "options", options,
                  "timeout",
                  timeout)
            response = requests.request(method, url, *args, json=data, params=params, headers=headers,
                                        timeout=int(timeout), **argss)
            responseText = response.text if ConstantEnum.is_debug() else response
            print(f"请求拦截URL: 返回:{responseText}, {url}", "method", method, "params", params,
                  "data",
                  data,
                  "headers",
                  headers,
                  "timeout",
                  timeout)
            if response.status_code != 200:
                raise requests.exceptions.RequestException(
                    response, response=response)
            response_json = response.json()
            if not bool(response_json['success']):
                raise requests.exceptions.RequestException(
                    response, response=response)
            response_json_data = response_json.get("data", response_json.get("result"))
            response_json_data = response_json_data.get("records") if response_json_data and type(
                response_json_data) == dict and "records" in response_json_data else response_json_data
            return response_json_data
        except Exception as e:
            import pydash as _
            CommonUtil.trace_exception_stack(e)
            responseText = _.get(e.args, '0.text')
            print(
                f"请求拦截URL, 失败, e: {e}, e.response.text: {responseText}, url:{url}",
                "method",
                method,
                "params",
                params,
                "data", data, "headers",
                "response", hasattr(e, 'response') and e.response,
                headers,
                "timeout",
                timeout)
            raise
