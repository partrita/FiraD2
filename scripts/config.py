import os

# =======================================
#  빌드 및 경로 구성
# =======================================
# 에셋 디렉터리 경로
ASSETS_PATH: str = "assets"
# 최종 폰트 파일이 저장될 디렉터리입니다.
BUILT_FONTS_PATH: str = os.path.join(ASSETS_PATH, "built_fonts")
# 폰트 이름 설정
OLD_FONT_NAME: str = "Fira Code"
NEW_FONT_NAME: str = "FiraD2"

# =======================================
#  폰트 디렉터리 경로 구성
# =======================================
# 영문 폰트 디렉터리 경로
EN_FONT_PATH: str = os.path.join(ASSETS_PATH, "en_font")
# 한글 폰트 디렉터리 경로
KO_FONT_PATH: str = os.path.join(ASSETS_PATH, "ko_font")
# 영문 너드 폰트 디렉터리 경로
EN_NERD_FONT_PATH: str = os.path.join(ASSETS_PATH, "en_nerd_font")

# =======================================
#  폰트 설정
# =======================================
KOREAN_FONT_WIDTH: int = 1000
ENGLISH_FONT_WIDTH: int = 1200
ENGLISH_FONT_NF_WIDTH: int = 1200
