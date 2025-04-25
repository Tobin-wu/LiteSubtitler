# coding: utf8
from typing import List, Tuple

import openai


class OpenAiChecker:
    """OpenAI 检查工具类，用于测试 OpenAI API 和获取支持的模型列表。

    该类提供了两个静态方法：
    1. `test_openai`: 测试 OpenAI API 的连接和响应。
    2. `get_openai_models`: 获取支持的模型列表并按权重排序。
    """

    @staticmethod
    def test_openai(base_url: str, api_key: str, model: str) -> Tuple[bool, str]:
        """测试 OpenAI API 的连接和响应。

        Args:
            base_url (str): OpenAI API 的基础 URL。
            api_key (str): OpenAI API 的密钥。
            model (str): 使用的模型名称。

        Returns:
            Tuple[bool, str]: 返回一个元组，包含：
                - bool: 是否成功。
                - str: 错误信息或 AI 助手的回复。
        """
        try:
            # 创建 OpenAI 客户端并发送请求，timeout需要长一点，加载模型可能需要不少时间
            client = openai.OpenAI(base_url=base_url, api_key=api_key, timeout=180)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello!"}
                ],
                max_tokens=100,
                timeout=30
            )
            # 返回 AI 助手的回复
            return True, response.choices[0].message.content
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_openai_models(base_url: str, api_key: str) -> List[str]:
        """获取支持的模型列表并按权重排序。

        Args:
            base_url (str): OpenAI API 的基础 URL。
            api_key (str): OpenAI API 的密钥。

        Returns:
            List[str]: 排序后的模型名称列表。
        """
        try:
            # 创建 OpenAI 客户端并获取模型列表
            client = openai.OpenAI(base_url=base_url, api_key=api_key, timeout=10)
            models = client.models.list()

            def get_model_weight(model_name: str) -> int:
                """根据模型名称计算权重。

                Args:
                    model_name (str): 模型名称。

                Returns:
                    int: 模型的权重值。
                """
                model_name = model_name.lower()
                if model_name.startswith('gemma2'):
                    return 10
                if model_name.startswith(('gpt-4o', 'claude-3-5')):
                    return 8
                elif model_name.startswith('gpt-4'):
                    return 5
                elif model_name.startswith('claude-3'):
                    return 6
                elif model_name.startswith(('deepseek', 'glm')):
                    return 3
                return 0

            # 按权重和名称排序模型列表
            sorted_models = sorted(
                [model.id for model in models],
                key=lambda x: (-get_model_weight(x), x)
            )
            return sorted_models
        except Exception as e:
            raise f"{e}"
