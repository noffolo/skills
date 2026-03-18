#!/usr/bin/env python3
"""
智能备忘录系统 - Smart Memo System
支持：导入、分类、搜索、快速记录
"""

import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import hashlib

class SmartMemoSystem:
    """智能备忘录主类"""
    
    def __init__(self, data_dir: str = None):
        """初始化备忘录系统"""
        if data_dir is None:
            data_dir = os.path.expanduser("~/.qclaw/workspace/memos")
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 数据库文件
        self.db_path = self.data_dir / "memos.db"
        self._init_database()
        
        # 分类关键词映射 - 优化版本，增加权重和更多关键词
        self.category_keywords = {
            "工作": {
                "keywords": ["会议", "项目", "任务", "deadline", "进度", "汇报", "客户", "需求", "bug", "修复", "上线", "发布", "工作总结", "周报", "月报", "汇报", "述职", "绩效", "考核", "团队", "协作", "审批", "流程", "合同", "协议", "商务", "合作", "交付", "验收", "排期", "里程碑", "okr", "kpi"],
                "weight": 1.5
            },
            "学习": {
                "keywords": ["教程", "课程", "学习", "笔记", "阅读", "书籍", "知识", "技能", "培训", "考证", "考试", "学习笔记", "读书笔记", "知识点", "总结", "复习", "预习", "作业", "练习", "题库", "教材", "课件", "网课", "在线学习", "慕课", "mooc", "学习方法", "学习资料", "学习资源", "专业", "学位", "学历", "证书", "资格", "认证"],
                "weight": 1.5
            },
            "生活": {
                "keywords": ["购物", "超市", "买菜", "做饭", "家务", "缴费", "账单", "快递", "预约", "医院", "健康", "体检", "药品", "饮食", "菜谱", "食谱", "穿搭", "护肤", "保养", "运动", "健身", "瑜伽", "跑步", "睡眠", "休息", "日常", "起居", "收纳", "整理", "清洁", "洗衣", "打扫", "维修", "物业", "水电", "燃气", "房租", "房贷"],
                "weight": 1.0
            },
            "旅行": {
                "keywords": ["机票", "酒店", "景点", "攻略", "行程", "旅游", "度假", "签证", "护照", "出行", "游玩", "门票", "导游", "路线", "交通", "高铁", "火车", "自驾", "租车", "民宿", "旅馆", "住宿", "打卡", "拍照", "风景", "美食", "特产", "纪念品", "行李箱", "打包", "出发", "到达", "返程"],
                "weight": 1.5
            },
            "财务": {
                "keywords": ["收入", "支出", "预算", "投资", "理财", "股票", "基金", "账单", "报销", "工资", "薪资", "奖金", "福利", "补贴", "费用", "成本", "利润", "亏损", "存款", "储蓄", "信用卡", "贷款", "借款", "还款", "利息", "汇率", "税务", "发票", "收据", "记账", "对账", "审计", "保险", "养老金", "公积金"],
                "weight": 1.5
            },
            "灵感": {
                "keywords": ["想法", "创意", "灵感", "构思", "设计", "方案", "计划", "目标", "愿景", "梦想", "思考", "感悟", "心得", "体会", "发现", "观察", "联想", "想象", "创新", "改进", "优化", "突破", "尝试", "实验", "探索", "研究", "分析", "总结", "反思", "复盘", "展望", "规划", "策略", "方向"],
                "weight": 1.0
            },
            "待办": {
                "keywords": ["todo", "待办", "待处理", "待确认", "待审核", "待回复", "提醒", "记得", "别忘了", "记得做", "记得去", "记得买", "记得带", "记得说", "记得问", "必须", "需要", "应该", "得去", "得做", "得买", "截止", "期限", "最后期限", "deadline", "到期", "过期", "逾期", "紧急", "重要", "优先", "尽快", "马上", "立即", "今天", "明天", "后天", "下周", "下个月"],
                "weight": 2.0
            },
            "联系人": {
                "keywords": ["电话", "手机号", "手机号码", "邮箱", "电子邮件", "地址", "联系人", "名片", "社交", "微信", "微信号", "qq", "qq号", "钉钉", "飞书", "linkedin", "领英", "facebook", "twitter", "微博", "抖音", "小红书", "好友", "朋友", "同事", "同学", "老师", "领导", "下属", "合作伙伴", "客户", "供应商", "厂家", "商家", "客服", "销售", "经理", "主任", "总监", "老板"],
                "weight": 1.5
            },
            "技术": {
                "keywords": ["代码", "编程", "程序", "开发", "api", "接口", "框架", "库", "工具", "git", "github", "gitlab", "版本控制", "服务器", "云服务器", "vps", "数据库", "db", "sql", "nosql", "缓存", "redis", "算法", "数据结构", "前端", "后端", "全栈", "web", "app", "移动端", "ios", "android", "flutter", "react", "vue", "angular", "node", "python", "java", "go", "golang", "rust", "c++", "javascript", "typescript", "html", "css", "部署", "上线", "发布", "测试", "debug", "调试", "日志", "监控", "运维", "devops", "ci/cd", "docker", "kubernetes", "k8s", "容器", "微服务", "架构", "设计模式", "重构", "性能", "优化", "安全", "漏洞", "加密", "认证", "授权"],
                "weight": 1.5
            },
            "娱乐": {
                "keywords": ["电影", "影片", "电视剧", "剧集", "综艺", "节目", "音乐", "歌曲", "歌手", "专辑", "乐队", "游戏", "手游", "网游", "单机", "steam", "switch", "ps5", "xbox", "追剧", "追剧", "番剧", "动漫", "动画", "漫画", "小说", "书籍", "读书", "推荐", "评分", "影评", "剧评", "书评", "乐评", "娱乐", "明星", "八卦", "八卦", "新闻", "热点", "话题", "讨论", "吐槽", "安利", "种草", "拔草"],
                "weight": 1.0
            },
            "健康": {
                "keywords": ["健康", "医疗", "医院", "医生", "看病", "就诊", "挂号", "体检", "检查", "化验", "报告", "诊断", "治疗", "吃药", "用药", "药品", "药方", "处方", "手术", "住院", "康复", "护理", "保健", "养生", "中医", "西医", "症状", "疼痛", "不舒服", "发烧", "感冒", "咳嗽", "过敏", "慢性病", "急性病", "疫苗", "接种", "防疫", "口罩", "消毒", "卫生", "饮食", "营养", "膳食", "健身", "运动", "锻炼", "减肥", "增肌", "瑜伽", "冥想", "睡眠", "休息", "心理健康", "情绪", "压力", "焦虑", "抑郁", "心理咨询"],
                "weight": 1.5
            },
            "美食": {
                "keywords": ["美食", "餐厅", "饭店", "吃饭", "用餐", "聚餐", "请客", "约会", "下午茶", "早餐", "午餐", "晚餐", "夜宵", "小吃", "零食", "甜品", "蛋糕", "面包", "奶茶", "咖啡", "茶", "饮料", "酒水", "菜谱", "食谱", "做法", "烹饪", "烘焙", "料理", "食材", "原料", "调料", "酱料", "推荐", "好评", "踩雷", "避雷", "打卡", "探店", "网红店", "老字号", "特色", "招牌", "必点"],
                "weight": 1.0
            }
        }
    
    def _init_database(self):
        """初始化 SQLite 数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建备忘录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT DEFAULT '未分类',
                tags TEXT,
                source TEXT DEFAULT 'manual',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                importance INTEGER DEFAULT 0,
                is_archived BOOLEAN DEFAULT 0,
                search_vector TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON memos(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created ON memos(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_search ON memos(search_vector)')
        
        conn.commit()
        conn.close()
    
    def add_memo(self, title: str, content: str, category: str = None,
                 tags: List[str] = None, importance: int = 0, source: str = 'manual') -> int:
        """添加新备忘录"""
        # 自动分类
        if category is None:
            category = self._auto_categorize(title + " " + content)

        # 生成搜索向量
        search_vector = self._generate_search_vector(title, content, tags)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO memos (title, content, category, tags, importance, source, search_vector)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, category, json.dumps(tags or []), importance, source, search_vector))

        memo_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return memo_id
    
    def _auto_categorize(self, text: str) -> str:
        """根据内容自动分类 - 优化版本，支持权重和上下文分析"""
        text_lower = text.lower()
        scores = {}

        # 1. 关键词匹配（带权重）
        for category, config in self.category_keywords.items():
            keywords = config["keywords"]
            weight = config.get("weight", 1.0)

            # 计算匹配得分
            match_count = 0
            for keyword in keywords:
                # 完全匹配得分更高
                if keyword in text_lower:
                    # 检查是否是完整单词/词组
                    if self._is_word_boundary(text_lower, keyword):
                        match_count += 1.5  # 完整词匹配加分
                    else:
                        match_count += 1

            if match_count > 0:
                # 应用权重，并考虑匹配密度
                score = match_count * weight * (1 + match_count / len(keywords))
                scores[category] = score

        # 2. 标题加权（标题中的关键词权重更高）
        title_lines = text.split('\n')[:3]  # 取前3行作为标题区域
        title_text = ' '.join(title_lines).lower()

        for category, config in self.category_keywords.items():
            keywords = config["keywords"]
            weight = config.get("weight", 1.0)

            title_matches = sum(1 for keyword in keywords if keyword in title_text)
            if title_matches > 0:
                # 标题匹配额外加权
                bonus = title_matches * weight * 2.0
                scores[category] = scores.get(category, 0) + bonus

        # 3. 特殊规则判断
        # 如果包含明确的时间+动作，可能是待办
        if self._is_todo_pattern(text):
            scores["待办"] = scores.get("待办", 0) + 3.0

        # 如果包含金额、数字+元/块，可能是财务
        if self._is_finance_pattern(text):
            scores["财务"] = scores.get("财务", 0) + 3.0

        # 如果包含人名+联系方式，可能是联系人
        if self._is_contact_pattern(text):
            scores["联系人"] = scores.get("联系人", 0) + 3.0

        # 4. 选择最高分的分类
        if scores:
            # 找到最高分
            max_score = max(scores.values())
            # 如果有多个相同最高分，选择权重更高的
            best_categories = [cat for cat, score in scores.items() if score == max_score]
            if len(best_categories) == 1:
                return best_categories[0]
            else:
                # 多个相同分数，选择权重最高的
                return max(best_categories, key=lambda cat: self.category_keywords[cat].get("weight", 1.0))

        return "未分类"

    def _is_word_boundary(self, text: str, keyword: str) -> bool:
        """检查关键词是否是完整词边界"""
        import re
        # 构建正则，检查词边界
        pattern = r'(?:^|[\s\b])' + re.escape(keyword) + r'(?:[\s\b]|$)'
        return bool(re.search(pattern, text))

    def _is_todo_pattern(self, text: str) -> bool:
        """检查是否是待办模式"""
        todo_patterns = [
            r'记得\s*[:：]?\s*',
            r'别忘了\s*[:：]?\s*',
            r'todo\s*[:：]?\s*',
            r'待办\s*[:：]?\s*',
            r'\d{1,2}[月/]\d{1,2}[日/号]',
            r'(今天|明天|后天|下周|下个月)',
            r'(截止|期限|deadline)',
        ]
        import re
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in todo_patterns)

    def _is_finance_pattern(self, text: str) -> bool:
        """检查是否是财务模式"""
        finance_patterns = [
            r'\d+[\d,]*\.?\d*\s*[元块刀]',
            r'(收入|支出|花费|消费|报销|工资|奖金)',
            r'(预算|成本|费用|价格|金额)',
            r'(\d+\.?\d*\s*%|\d+\s*折)',
        ]
        import re
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in finance_patterns)

    def _is_contact_pattern(self, text: str) -> bool:
        """检查是否是联系人模式"""
        contact_patterns = [
            r'1[3-9]\d{9}',  # 手机号
            r'[\w.-]+@[\w.-]+\.\w+',  # 邮箱
            r'(微信|微信号|wx|wechat)[:：]?\s*\w+',
            r'(qq|qq号)[:：]?\s*\d+',
            r'(电话|手机|联系方式)[:：]?\s*\d+',
        ]
        import re
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in contact_patterns)
    
    def _generate_search_vector(self, title: str, content: str, tags: List[str] = None) -> str:
        """生成搜索向量（简化版）"""
        # 提取关键词
        text = f"{title} {content}"
        # 移除标点，分词
        words = re.findall(r'\b[\u4e00-\u9fa5a-zA-Z0-9]+\b', text.lower())
        # 添加标签
        if tags:
            words.extend([t.lower() for t in tags])
        return " ".join(words)
    
    def search_memos(self, query: str, category: str = None, 
                     limit: int = 20) -> List[Dict]:
        """搜索备忘录（支持语义匹配）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 构建查询
        if category:
            sql = '''
                SELECT * FROM memos 
                WHERE is_archived = 0 
                AND category = ?
                AND (title LIKE ? OR content LIKE ? OR search_vector LIKE ?)
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            '''
            params = (category, f'%{query}%', f'%{query}%', f'%{query}%', limit)
        else:
            sql = '''
                SELECT * FROM memos 
                WHERE is_archived = 0 
                AND (title LIKE ? OR content LIKE ? OR search_vector LIKE ?)
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            '''
            params = (f'%{query}%', f'%{query}%', f'%{query}%', limit)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_memos_by_category(self, category: str = None, limit: int = 50) -> List[Dict]:
        """按分类获取备忘录"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if category:
            cursor.execute('''
                SELECT * FROM memos
                WHERE is_archived = 0 AND category = ?
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT * FROM memos
                WHERE is_archived = 0
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_memo_by_id(self, memo_id: int) -> Optional[Dict]:
        """根据ID获取单个备忘录详情"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM memos
            WHERE id = ? AND is_archived = 0
        ''', (memo_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def update_memo(self, memo_id: int, title: str = None, content: str = None,
                    category: str = None, tags: List[str] = None, importance: int = None) -> bool:
        """更新备忘录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 获取当前数据
        cursor.execute('SELECT * FROM memos WHERE id = ? AND is_archived = 0', (memo_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return False

        # 构建更新字段
        updates = []
        params = []

        if title is not None:
            updates.append('title = ?')
            params.append(title)

        if content is not None:
            updates.append('content = ?')
            params.append(content)

        if category is not None:
            updates.append('category = ?')
            params.append(category)

        if tags is not None:
            updates.append('tags = ?')
            params.append(json.dumps(tags))

        if importance is not None:
            updates.append('importance = ?')
            params.append(importance)

        if not updates:
            conn.close()
            return True

        # 更新搜索向量
        new_title = title if title is not None else row[1]
        new_content = content if content is not None else row[2]
        new_tags = tags if tags is not None else json.loads(row[4]) if row[4] else []
        search_vector = self._generate_search_vector(new_title, new_content, new_tags)
        updates.append('search_vector = ?')
        params.append(search_vector)

        updates.append('updated_at = CURRENT_TIMESTAMP')

        # 执行更新
        sql = f"UPDATE memos SET {', '.join(updates)} WHERE id = ?"
        params.append(memo_id)

        cursor.execute(sql, params)
        conn.commit()
        affected = cursor.rowcount
        conn.close()

        return affected > 0

    def get_categories(self) -> List[Tuple[str, int]]:
        """获取所有分类及数量"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM memos 
            WHERE is_archived = 0
            GROUP BY category 
            ORDER BY count DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def import_from_notes_app(self, export_path: str = None) -> int:
        """
        从 macOS Notes 应用导入
        支持格式：PDF, Markdown (.md), HTML, TXT, JSON
        """
        imported_count = 0
        
        if export_path and os.path.exists(export_path):
            file_lower = export_path.lower()
            # 处理导出的文件
            if file_lower.endswith('.pdf'):
                imported_count = self._import_from_pdf(export_path)
            elif file_lower.endswith('.md') or file_lower.endswith('.markdown'):
                imported_count = self._import_from_markdown(export_path)
            elif file_lower.endswith('.html') or file_lower.endswith('.htm'):
                imported_count = self._import_from_html(export_path)
            elif file_lower.endswith('.txt'):
                imported_count = self._import_from_txt(export_path)
            elif file_lower.endswith('.json'):
                imported_count = self._import_from_json(export_path)
            else:
                print(f"不支持的文件格式: {export_path}")
                print("支持的格式: PDF, Markdown(.md), HTML, TXT, JSON")
        else:
            print(f"文件不存在: {export_path}")
        
        return imported_count
    
    def _import_from_html(self, html_path: str) -> int:
        """从 HTML 文件导入"""
        from html.parser import HTMLParser
        
        class NotesHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.notes = []
                self.current_note = {}
                self.in_note = False
                self.current_tag = None
                self.current_data = []
            
            def handle_starttag(self, tag, attrs):
                if tag == 'div' and any(attr == ('class', 'note') for attr in attrs):
                    self.in_note = True
                    self.current_note = {}
                self.current_tag = tag
            
            def handle_data(self, data):
                if self.in_note and data.strip():
                    self.current_data.append(data.strip())
            
            def handle_endtag(self, tag):
                if tag == 'div' and self.in_note:
                    if self.current_data:
                        content = ' '.join(self.current_data)
                        if len(content) > 50:
                            self.current_note['title'] = content[:50] + '...'
                        else:
                            self.current_note['title'] = content
                        self.current_note['content'] = content
                        self.notes.append(self.current_note)
                    self.in_note = False
                    self.current_data = []
        
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            parser = NotesHTMLParser()
            parser.feed(html_content)
            
            for note in parser.notes:
                self.add_memo(
                    title=note.get('title', '无标题'),
                    content=note.get('content', ''),
                    source='notes_app'
                )
            
            return len(parser.notes)
        except Exception as e:
            print(f"导入失败: {e}")
            return 0
    
    def _import_from_txt(self, txt_path: str) -> int:
        """从 TXT 文件导入（每行一个备忘录）"""
        count = 0
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if len(line) > 50:
                            title = line[:50] + '...'
                        else:
                            title = line
                        self.add_memo(title=title, content=line, source='txt_import')
                        count += 1
            return count
        except Exception as e:
            print(f"导入失败: {e}")
            return 0
    
    def _import_from_json(self, json_path: str) -> int:
        """从 JSON 文件导入"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            count = 0
            if isinstance(data, list):
                for item in data:
                    self.add_memo(
                        title=item.get('title', '无标题'),
                        content=item.get('content', ''),
                        category=item.get('category'),
                        tags=item.get('tags'),
                        source='json_import'
                    )
                    count += 1
            return count
        except Exception as e:
            print(f"导入失败: {e}")
            return 0

    def _extract_tags_from_content(self, content: str) -> Tuple[str, List[str]]:
        """从内容中提取 #标签，返回 (清理后的内容, 标签列表)"""
        import re

        # 匹配 #开头的标签（支持中文、英文、数字、下划线）
        tag_pattern = r'#([\u4e00-\u9fa5a-zA-Z0-9_]+)'
        tags = re.findall(tag_pattern, content)

        # 移除内容中的标签标记
        cleaned_content = re.sub(tag_pattern, '', content)
        # 清理多余空格和空行
        cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content).strip()

        return cleaned_content, tags

    def _import_from_markdown(self, md_path: str) -> int:
        """从 Markdown 文件导入 - 支持 #标签"""
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析 Markdown 结构
            # 支持格式：
            # 1. 每个 H1/H2 标题作为一个备忘录
            # 2. 列表项作为独立备忘录
            # 3. 提取 #标签

            memos = []
            import re

            # 匹配 # 或 ## 开头的标题
            sections = re.split(r'\n(?=#{1,2}\s)', content)

            if len(sections) > 1:
                # 按标题分割
                for section in sections:
                    section = section.strip()
                    if not section:
                        continue

                    lines = section.split('\n')
                    title_line = lines[0].strip()

                    # 移除标题标记
                    title = re.sub(r'^#{1,2}\s*', '', title_line).strip()
                    body = '\n'.join(lines[1:]).strip()

                    # 提取标签
                    full_content = title + '\n' + body if body else title
                    cleaned_content, tags = self._extract_tags_from_content(full_content)

                    # 重新分割清理后的内容
                    cleaned_lines = cleaned_content.split('\n')
                    cleaned_title = cleaned_lines[0][:100] if cleaned_lines else title
                    cleaned_body = '\n'.join(cleaned_lines[1:]).strip() if len(cleaned_lines) > 1 else cleaned_content

                    if cleaned_title:
                        memos.append({
                            'title': cleaned_title,
                            'content': cleaned_body if cleaned_body else cleaned_title,
                            'tags': tags
                        })
            else:
                # 尝试按列表项分割
                list_items = re.findall(r'^[\s]*[-*+][\s]+(.+)$', content, re.MULTILINE)
                if list_items:
                    for item in list_items:
                        item = item.strip()
                        # 提取标签
                        cleaned_content, tags = self._extract_tags_from_content(item)

                        if len(cleaned_content) > 50:
                            title = cleaned_content[:50] + '...'
                        else:
                            title = cleaned_content
                        memos.append({
                            'title': title,
                            'content': cleaned_content,
                            'tags': tags
                        })
                else:
                    # 整个文件作为一个备忘录
                    lines = content.strip().split('\n')
                    title = lines[0][:100] if lines else "Markdown导入"

                    # 提取标签
                    cleaned_content, tags = self._extract_tags_from_content(content)
                    cleaned_lines = cleaned_content.split('\n')
                    cleaned_title = cleaned_lines[0][:100] if cleaned_lines else title

                    memos.append({
                        'title': cleaned_title,
                        'content': cleaned_content,
                        'tags': tags
                    })

            # 添加到数据库
            for memo in memos:
                self.add_memo(
                    title=memo['title'],
                    content=memo['content'],
                    tags=memo.get('tags', []),
                    source='markdown_import'
                )

            return len(memos)

        except Exception as e:
            print(f"Markdown导入失败: {e}")
            return 0

    def _import_from_pdf(self, pdf_path: str) -> int:
        """从 PDF 文件导入"""
        try:
            # 尝试使用 PyPDF2 或 pdfplumber
            try:
                import pdfplumber
                return self._import_pdf_with_pdfplumber(pdf_path)
            except ImportError:
                pass
            
            try:
                import PyPDF2
                return self._import_pdf_with_pypdf2(pdf_path)
            except ImportError:
                pass
            
            # 如果没有安装 PDF 库，使用系统命令 pdftotext
            return self._import_pdf_with_pdftotext(pdf_path)
            
        except Exception as e:
            print(f"PDF导入失败: {e}")
            print("提示: 可安装 pdfplumber (pip install pdfplumber) 获得更好的 PDF 支持")
            return 0

    def _import_pdf_with_pdfplumber(self, pdf_path: str) -> int:
        """使用 pdfplumber 导入 PDF"""
        import pdfplumber
        
        memos = []
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # 尝试识别备忘录结构
            # 按段落分割，每个段落可能是一个备忘录
            paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
            
            if len(paragraphs) > 1:
                for para in paragraphs[:50]:  # 限制数量避免过多
                    lines = para.split('\n')
                    if len(lines[0]) > 100:
                        title = lines[0][:100] + '...'
                    else:
                        title = lines[0]
                    
                    memos.append({
                        'title': title,
                        'content': para
                    })
            else:
                # 整个 PDF 作为一个备忘录
                title = os.path.basename(pdf_path).replace('.pdf', '')
                memos.append({
                    'title': title,
                    'content': full_text[:2000]  # 限制长度
                })
        
        for memo in memos:
            self.add_memo(
                title=memo['title'],
                content=memo['content'],
                source='pdf_import'
            )
        
        return len(memos)

    def _import_pdf_with_pypdf2(self, pdf_path: str) -> int:
        """使用 PyPDF2 导入 PDF"""
        import PyPDF2
        
        memos = []
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            full_text = ""
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # 按段落分割
            paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
            
            if len(paragraphs) > 1:
                for para in paragraphs[:50]:
                    lines = para.split('\n')
                    title = lines[0][:100] if len(lines[0]) <= 100 else lines[0][:100] + '...'
                    memos.append({
                        'title': title,
                        'content': para
                    })
            else:
                title = os.path.basename(pdf_path).replace('.pdf', '')
                memos.append({
                    'title': title,
                    'content': full_text[:2000]
                })
        
        for memo in memos:
            self.add_memo(
                title=memo['title'],
                content=memo['content'],
                source='pdf_import'
            )
        
        return len(memos)

    def _import_pdf_with_pdftotext(self, pdf_path: str) -> int:
        """使用系统 pdftotext 命令导入 PDF"""
        import subprocess
        import tempfile
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # 使用 pdftotext 转换
            result = subprocess.run(
                ['pdftotext', pdf_path, tmp_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # 尝试使用 pdf2txt.py
                result = subprocess.run(
                    ['pdf2txt.py', '-o', tmp_path, pdf_path],
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0 and os.path.exists(tmp_path):
                # 读取转换后的文本
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 按段落分割
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                
                memos = []
                if len(paragraphs) > 1:
                    for para in paragraphs[:50]:
                        lines = para.split('\n')
                        title = lines[0][:100] if len(lines[0]) <= 100 else lines[0][:100] + '...'
                        memos.append({
                            'title': title,
                            'content': para
                        })
                else:
                    title = os.path.basename(pdf_path).replace('.pdf', '')
                    memos.append({
                        'title': title,
                        'content': content[:2000]
                    })
                
                for memo in memos:
                    self.add_memo(
                        title=memo['title'],
                        content=memo['content'],
                        source='pdf_import'
                    )
                
                return len(memos)
            else:
                print("PDF 转换失败，请安装 pdftotext (poppler) 或 pdfplumber")
                return 0
                
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def export_to_json(self, output_path: str = None) -> str:
        """导出所有备忘录为 JSON"""
        if output_path is None:
            output_path = self.data_dir / f"memos_export_{datetime.now().strftime('%Y%m%d')}.json"
        
        memos = self.get_memos_by_category(limit=10000)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(memos, f, ensure_ascii=False, indent=2)
        
        return str(output_path)
    
    def delete_memo(self, memo_id: int) -> bool:
        """删除备忘录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM memos WHERE id = ?', (memo_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    def archive_memo(self, memo_id: int) -> bool:
        """归档备忘录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE memos SET is_archived = 1 WHERE id = ?', (memo_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute('SELECT COUNT(*) FROM memos WHERE is_archived = 0')
        total = cursor.fetchone()[0]
        
        # 分类统计
        cursor.execute('SELECT category, COUNT(*) FROM memos WHERE is_archived = 0 GROUP BY category')
        categories = dict(cursor.fetchall())
        
        # 今日新增
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM memos WHERE date(created_at) = ?', (today,))
        today_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'categories': categories,
            'today_added': today_count
        }


# CLI 接口
if __name__ == '__main__':
    import sys
    
    memo_system = SmartMemoSystem()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python memos.py add '标题' '内容' [分类] [标签1,标签2]")
        print("  python memos.py search '关键词' [分类]")
        print("  python memos.py list [分类] [数量]")
        print("  python memos.py view <ID>          - 查看备忘录详情")
        print("  python memos.py edit <ID> [选项]   - 编辑备忘录")
        print("    选项: --title '新标题' --content '新内容' --category '分类' --tags '标签1,标签2'")
        print("  python memos.py categories")
        print("  python memos.py import <文件路径>")
        print("  python memos.py export [输出路径]")
        print("  python memos.py delete <ID>        - 删除备忘录")
        print("  python memos.py archive <ID>       - 归档备忘录")
        print("  python memos.py stats")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 4:
            print("用法: python memos.py add '标题' '内容' [分类] [标签]")
            sys.exit(1)
        title = sys.argv[2]
        content = sys.argv[3]
        category = sys.argv[4] if len(sys.argv) > 4 else None
        tags = sys.argv[5].split(',') if len(sys.argv) > 5 else None
        memo_id = memo_system.add_memo(title, content, category, tags)
        print(f"✅ 备忘录已添加 (ID: {memo_id})")
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("用法: python memos.py search '关键词' [分类]")
            sys.exit(1)
        query = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else None
        results = memo_system.search_memos(query, category)
        print(f"🔍 找到 {len(results)} 条结果:")
        for memo in results:
            print(f"  [ID:{memo['id']}] [{memo['category']}] {memo['title']}")
    
    elif command == 'list':
        category = sys.argv[2] if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        results = memo_system.get_memos_by_category(category, limit)
        print(f"📋 备忘录列表 ({len(results)} 条):")
        for memo in results:
            print(f"  [ID:{memo['id']}] [{memo['category']}] {memo['title']}")
    
    elif command == 'view':
        if len(sys.argv) < 3:
            print("用法: python memos.py view <ID>")
            print("  查看指定ID的备忘录详情")
            sys.exit(1)
        try:
            memo_id = int(sys.argv[2])
            memo = memo_system.get_memo_by_id(memo_id)
            if memo:
                print(f"\n📝 备忘录详情 (ID: {memo['id']})")
                print(f"{'=' * 50}")
                print(f"📌 标题: {memo['title']}")
                print(f"🏷️  分类: {memo['category']}")
                if memo['tags']:
                    tags = json.loads(memo['tags']) if isinstance(memo['tags'], str) else memo['tags']
                    print(f"🔖 标签: {', '.join(tags)}")
                print(f"📅 创建: {memo['created_at']}")
                print(f"{'=' * 50}")
                print(f"\n{memo['content']}")
                print(f"\n{'=' * 50}\n")
            else:
                print(f"❌ 未找到备忘录 (ID: {memo_id})")
        except ValueError:
            print("❌ ID 必须是数字")

    elif command == 'edit':
        if len(sys.argv) < 3:
            print("用法: python memos.py edit <ID> [选项]")
            print("  选项:")
            print("    --title '新标题'       修改标题")
            print("    --content '新内容'     修改内容")
            print("    --category '分类'      修改分类")
            print("    --tags '标签1,标签2'   修改标签")
            print("  示例:")
            print("    python memos.py edit 5 --title '新标题' --category '工作'")
            sys.exit(1)
        try:
            memo_id = int(sys.argv[2])

            # 解析参数
            new_title = None
            new_content = None
            new_category = None
            new_tags = None

            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == '--title' and i + 1 < len(sys.argv):
                    new_title = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--content' and i + 1 < len(sys.argv):
                    new_content = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--category' and i + 1 < len(sys.argv):
                    new_category = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == '--tags' and i + 1 < len(sys.argv):
                    new_tags = sys.argv[i + 1].split(',')
                    i += 2
                else:
                    i += 1

            if memo_system.update_memo(memo_id, new_title, new_content, new_category, new_tags):
                print(f"✏️  备忘录 (ID: {memo_id}) 已更新")
            else:
                print(f"❌ 未找到备忘录 (ID: {memo_id})")
        except ValueError:
            print("❌ ID 必须是数字")

    elif command == 'categories':
        cats = memo_system.get_categories()
        print("📁 分类统计:")
        for cat, count in cats:
            print(f"  {cat}: {count} 条")
    
    elif command == 'import':
        if len(sys.argv) < 3:
            print("用法: python memos.py import <文件路径>")
            print("支持的格式: PDF, Markdown(.md), HTML, TXT, JSON")
            sys.exit(1)
        count = memo_system.import_from_notes_app(sys.argv[2])
        print(f"📥 成功导入 {count} 条备忘录")
    
    elif command == 'export':
        path = sys.argv[2] if len(sys.argv) > 2 else None
        output = memo_system.export_to_json(path)
        print(f"📤 已导出到: {output}")
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("用法: python memos.py delete <ID>")
            print("  删除指定ID的备忘录")
            sys.exit(1)
        try:
            memo_id = int(sys.argv[2])
            if memo_system.delete_memo(memo_id):
                print(f"🗑️  备忘录 (ID: {memo_id}) 已删除")
            else:
                print(f"❌ 未找到备忘录 (ID: {memo_id})")
        except ValueError:
            print("❌ ID 必须是数字")

    elif command == 'archive':
        if len(sys.argv) < 3:
            print("用法: python memos.py archive <ID>")
            print("  归档指定ID的备忘录")
            sys.exit(1)
        try:
            memo_id = int(sys.argv[2])
            if memo_system.archive_memo(memo_id):
                print(f"📦 备忘录 (ID: {memo_id}) 已归档")
            else:
                print(f"❌ 未找到备忘录 (ID: {memo_id})")
        except ValueError:
            print("❌ ID 必须是数字")

    elif command == 'stats':
        stats = memo_system.get_stats()
        print("📊 备忘录统计:")
        print(f"  总计: {stats['total']} 条")
        print(f"  今日新增: {stats['today_added']} 条")
        print("  分类分布:")
        for cat, count in stats['categories'].items():
            print(f"    {cat}: {count} 条")

    else:
        print(f"未知命令: {command}")
