import os

# =======================================
#  빌드 및 경로 구성
# =======================================
# 소스 폰트 파일이 다운로드되는 디렉터리입니다.
DOWNLOAD_PATH: str = "assets"
# 최종 폰트 파일이 저장될 디렉터리입니다.
BUILT_FONTS_PATH: str = "built_fonts"
OLD_FONT_NAME: str = "Fira Code"
NEW_FONT_NAME: str = "FiraD2"

# =======================================
#  한글 모노스페이스 폰트 구성
# =======================================
KOREAN_FONT_VERSION: str = "1.3.2"
KOREAN_FONT_RELEASE_DATE: str = "20180524"
KOREAN_FONT_WIDTH: int = 1000
# 압축 해제 후 D2Coding TTF 원본 파일의 경로입니다.
KOREAN_FONT_PATH: str = os.path.join(
    DOWNLOAD_PATH,
    "D2Coding",
    f"D2Coding-Ver{KOREAN_FONT_VERSION}-{KOREAN_FONT_RELEASE_DATE}.ttf",
)


# =======================================
#  영문 모노스페이스 폰트 구성
# =======================================
ENGLISH_FONT_WIDTH: int = 1200
# 압축 해제된 JetBrains Mono TTF 파일이 포함된 디렉터리 경로입니다.
ENGLISH_FONT_PATH: str = os.path.join(DOWNLOAD_PATH, "ttf")


# =======================================
#  영문 너드 폰트 구성
# =======================================
ENGLISH_FONT_NF_WIDTH: int = 1200
# 압축 해제된 JetBrains Mono Nerd Font TTF 파일이 포함된 디렉터리 경로입니다.
# DOWNLOAD_PATH의 루트에 압축 해제됩니다.
ENGLISH_FONT_NF_PATH: str = DOWNLOAD_PATH
