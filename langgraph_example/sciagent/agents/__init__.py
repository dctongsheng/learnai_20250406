# agents/__init__.py
"""
科研助手系统的专业agent模块
"""

from .chat_agent import chat_agent
from .bioinformatics_agent import bioinformatics_agent
from .bioinfo_interpret_agent import bioinfo_interpret_agent
from .literature_agent import literature_agent
from .research_image_agent import research_image_agent
from .deep_research_agent import deep_research_agent

# 导出所有agent
__all__ = [
    'chat_agent',
    'bioinformatics_agent',
    'bioinfo_interpret_agent',
    'literature_agent',
    'research_image_agent',
    'deep_research_agent',
]
