from pathlib import Path

ORODAEL_TURRIM_ROOT = Path(__file__).parent.absolute()
EXPERT_SYSTEM_ROOT = (Path(__file__).parent.parent / 'ExpertSystem').absolute()
USER_ROOT = (Path(__file__).parent.parent / 'User').absolute()

RESOURCES_ROOT = ORODAEL_TURRIM_ROOT / 'res'
UI_ROOT = RESOURCES_ROOT / 'ui'
IMAGES_ROOT = RESOURCES_ROOT / 'images'
ICONS_ROOT = IMAGES_ROOT / 'icons'

__version__ = '1.2.3'

DEBUG = False
GENERATE_BUG_REPORTS = True
AI_CONSOLE_OUTPUT = True
