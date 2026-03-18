#!/usr/bin/env python3
"""
智能备忘录系统测试脚本
"""

import os
import sys
import tempfile
import shutil

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.memos import SmartMemoSystem


def test_basic_operations():
    """测试基本操作"""
    print("🧪 测试基本操作...")

    # 使用临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        memos = SmartMemoSystem(data_dir=tmpdir)

        # 测试添加
        memo_id = memos.add_memo(
            title="测试备忘录",
            content="这是一条测试内容",
            category="测试",
            tags=["测试", "单元测试"]
        )
        assert memo_id > 0, "添加失败"
        print("  ✅ 添加备忘录成功")

        # 测试查询
        memo = memos.get_memo_by_id(memo_id)
        assert memo is not None, "查询失败"
        assert memo['title'] == "测试备忘录", "标题不匹配"
        print("  ✅ 查询备忘录成功")

        # 测试更新
        success = memos.update_memo(memo_id, title="更新后的标题")
        assert success, "更新失败"
        memo = memos.get_memo_by_id(memo_id)
        assert memo['title'] == "更新后的标题", "标题未更新"
        print("  ✅ 更新备忘录成功")

        # 测试删除
        success = memos.delete_memo(memo_id)
        assert success, "删除失败"
        memo = memos.get_memo_by_id(memo_id)
        assert memo is None, "备忘录未删除"
        print("  ✅ 删除备忘录成功")


def test_categorization():
    """测试自动分类"""
    print("\n🧪 测试自动分类...")

    with tempfile.TemporaryDirectory() as tmpdir:
        memos = SmartMemoSystem(data_dir=tmpdir)

        # 测试工作分类
        id1 = memos.add_memo("会议记录", "今天下午3点项目进度会议")
        m1 = memos.get_memo_by_id(id1)
        print(f"  📌 '会议记录' -> {m1['category']}")

        # 测试待办分类
        id2 = memos.add_memo("待办事项", "记得明天去买菜")
        m2 = memos.get_memo_by_id(id2)
        print(f"  📌 '记得明天...' -> {m2['category']}")

        # 测试学习分类
        id3 = memos.add_memo("Python学习", "今天学习了装饰器和元类")
        m3 = memos.get_memo_by_id(id3)
        print(f"  📌 'Python学习' -> {m3['category']}")

        print("  ✅ 自动分类测试通过")


def test_search():
    """测试搜索功能"""
    print("\n🧪 测试搜索功能...")

    with tempfile.TemporaryDirectory() as tmpdir:
        memos = SmartMemoSystem(data_dir=tmpdir)

        # 添加测试数据
        memos.add_memo("会议1", "项目进度会议")
        memos.add_memo("会议2", "团队周会")
        memos.add_memo("学习", "Python教程")

        # 搜索
        results = memos.search_memos("会议")
        assert len(results) == 2, f"应该找到2条，实际找到{len(results)}条"
        print(f"  ✅ 搜索 '会议' 找到 {len(results)} 条结果")


def test_import_tags():
    """测试标签提取"""
    print("\n🧪 测试标签提取...")

    with tempfile.TemporaryDirectory() as tmpdir:
        memos = SmartMemoSystem(data_dir=tmpdir)

        content = "项目会议记录 #工作 #会议\n今天下午3点开会 #紧急"
        cleaned, tags = memos._extract_tags_from_content(content)

        assert "工作" in tags, "未提取到标签 '工作'"
        assert "会议" in tags, "未提取到标签 '会议'"
        assert "紧急" in tags, "未提取到标签 '紧急'"
        assert "#工作" not in cleaned, "标签未从内容中清理"
        print(f"  ✅ 提取标签: {tags}")
        print("  ✅ 标签提取测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("智能备忘录系统 - 单元测试")
    print("=" * 50)

    try:
        test_basic_operations()
        test_categorization()
        test_search()
        test_import_tags()

        print("\n" + "=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
