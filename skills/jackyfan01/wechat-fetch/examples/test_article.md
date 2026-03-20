# 测试文章示例

这是一个测试用的微信文章抓取示例。

## 测试命令

```bash
# 测试基本抓取
python3 scripts/wechat_fetch.py "https://mp.weixin.qq.com/s/xxxxx" --output /tmp/test.md

# 测试 JSON 输出
python3 scripts/wechat_fetch.py "https://mp.weixin.qq.com/s/xxxxx" --format json --output /tmp/test.json

# 测试文本输出
python3 scripts/wechat_fetch.py "https://mp.weixin.qq.com/s/xxxxx" --format txt --output /tmp/test.txt
```

## 预期输出

抓取成功后会输出：
- 文章标题
- 公众号名称
- 发布时间
- 内容长度
- 图片数量
- 保存位置
