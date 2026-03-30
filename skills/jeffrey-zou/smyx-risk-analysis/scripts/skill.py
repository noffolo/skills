#!/usr/bin/env python3

from .config import ApiEnum, ConstantEnum

# import_path_common()
from skills.scripts.common.config import ApiEnum as ApiEnumBase
from skills.scripts.common.base import BaseSkill
from skills.scripts.common.api_service import ApiService as ApiServiceBase

from skills.face_analysis.scripts.skill import Skill as SkillParent


class Skill(SkillParent):
    def __init__(self):
        super().__init__()
        self.analysis_url = ApiEnum.ANALYSIS_URL

    def get_output_analysis(self, input_path, params={}):
        params.setdefault("scene", ConstantEnum.DEFAULT__SCENE_CODE)
        response = self.get_analysis(
            input_path, params
        )

        output_content = self.get_output_analysis_content(response)
        return output_content

    def get_output_analysis_content_body(self, result=None):
        import json
        result_json = result
        result_json = json.dumps(result_json,
                                 ensure_ascii=False, indent=2)
        return result_json if result_json else "⚠️暂未无发现风险"

    def get_output_analysis_content_head(self, result=None):
        return f"📊 风险分析结构化结果"

    def get_output_analysis_content_foot(self, result):
        pass


skill = Skill()
