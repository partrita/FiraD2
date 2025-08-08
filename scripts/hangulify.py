import os
from typing import Any
import re
import fontforge

from config import (
    BUILT_FONTS_PATH,
    EN_FONT_PATH,
    KO_FONT_PATH,
    EN_NERD_FONT_PATH,
    ENGLISH_FONT_NF_WIDTH,
    ENGLISH_FONT_WIDTH,
    OLD_FONT_NAME,
    NEW_FONT_NAME,
)

# 글리프의 사이드 베어링을 조정하는 값입니다.
BEARING_ADJUSTMENT: int = 200

# TARGET em 단위, 키울수록 D2Coding 폰트(기본 1000)가 더 커집니다.
TARGET_EM: int = 1400


def _get_cleaned_name(name: str) -> str:
    """이름에서 공백을 제거합니다."""
    return name.replace(" ", "")


def update_family_name(original_family_name: str, old_str: str, new_str: str) -> str:
    """
    폰트 이름을 변경합니다.

    Args:
        original_family_name (str): 원래 폰트 이름.
        old_str (str): 변경하려는 이전 문자열. 공백과 대소문자는 무시됩니다.
        new_str (str): 변경할 새로운 문자열.

    Returns:
        str: 변경된 폰트 이름.
    """
    cleaned_original_name = _get_cleaned_name(original_family_name)
    cleaned_old_str = _get_cleaned_name(old_str)

    # old_str의 공백을 제거하고 대소문자를 무시하는 정규표현식으로 만듭니다.
    pattern = re.compile(re.escape(cleaned_old_str), re.IGNORECASE)

    # 정규표현식을 사용해 변경합니다.
    return pattern.sub(new_str, cleaned_original_name)


def adjust_glyph_bearing(glyph: Any, adjustment: int) -> Any:
    """글리프의 왼쪽 및 오른쪽 사이드 베어링을 조정합니다."""
    glyph.left_side_bearing += adjustment // 2
    glyph.right_side_bearing += adjustment // 2
    return glyph


def _is_jetbrains_font_width(width: int) -> bool:
    """주어진 너비가 JetBrains Mono 폰트의 너비와 일치하는지 확인합니다."""
    return width in (ENGLISH_FONT_WIDTH, ENGLISH_FONT_NF_WIDTH)


def _process_and_adjust_glyph(font: fontforge.font, glyph_id: int) -> None:
    """
    단일 글리프 또는 참조 글리프의 베어링을 조정합니다.
    """
    glyph = font[glyph_id]

    if not glyph.references:
        # 일반 글리프 처리
        if _is_jetbrains_font_width(int(glyph.width)):
            adjust_glyph_bearing(glyph, BEARING_ADJUSTMENT)
    else:
        # 참조(composite) 글리프 처리
        for ref in glyph.references:
            ref_glyph_id = ref[0]
            ref_glyph = font[ref_glyph_id]
            if _is_jetbrains_font_width(int(ref_glyph.width)):
                adjust_glyph_bearing(ref_glyph, BEARING_ADJUSTMENT)


def process_hangul_glyphs(font: fontforge.font) -> fontforge.font:
    """한글 글리프를 선택하고 베어링을 조정합니다."""
    hangul_range_start = 0x3131
    hangul_range_end = 0xD7A3

    # 폰트의 한글 범위 글리프들을 순회합니다.
    for glyph_id in range(hangul_range_start, hangul_range_end + 1):
        if glyph_id in font:
            _process_and_adjust_glyph(font, glyph_id)

    print("[INFO] 한글 글리프의 사이드 베어링 조정을 완료했습니다.")
    return font


def get_font_style(font: fontforge.font, original_filename: str = None) -> str:
    """
    폰트 객체나 파일명에서 폰트 스타일을 추출합니다.
    """
    # 1. 파일명에서 스타일 추출
    if original_filename:
        base_name = os.path.splitext(original_filename)[0]
        if "Regular" in base_name:
            return "Regular"
        style_parts = base_name.split("-")
        if len(style_parts) > 1:
            return style_parts[-1]

    # 2. 폰트 객체의 메타데이터에서 스타일 추출
    style_parts = []

    if hasattr(font, "weight") and font.weight:
        weight = font.weight.lower()
        if "bold" in weight:
            style_parts.append("Bold")
        elif "light" in weight:
            style_parts.append("Light")
        elif "medium" in weight:
            style_parts.append("Medium")

    if hasattr(font, "italicangle") and font.italicangle != 0:
        style_parts.append("Italic")

    try:
        if (
            hasattr(font, "os2_weight")
            and font.os2_weight >= 700
            and "Bold" not in style_parts
        ):
            style_parts.append("Bold")
    except Exception:
        pass

    if not style_parts:
        return "Regular"

    return "".join(style_parts)


def format_style_name(style: str) -> str:
    """스타일 이름을 포맷팅합니다(예: 'BoldItalic' -> 'Bold Italic')."""
    return re.sub(r"(?<!^)(?=[A-Z])", " ", style).strip()


def update_font_metadata(
    font: fontforge.font, style: str, old_name: str, new_name: str
) -> None:
    """
    폰트의 메타데이터(패밀리 이름, 폰트 이름, 스타일 등)를 업데이트합니다.
    """
    new_family_name = update_family_name(font.familyname, old_name, new_name)

    formatted_style = format_style_name(style)

    font.familyname = new_family_name
    font.fontname = f"{new_family_name}-{style}"
    font.fullname = f"{new_family_name} {formatted_style}"

    font.appendSFNTName("English (US)", "Preferred Family", new_family_name)
    font.appendSFNTName("English (US)", "Family", new_family_name)
    font.appendSFNTName("English (US)", "Compatible Full", font.fullname)
    font.appendSFNTName("English (US)", "SubFamily", formatted_style)

    print(f"[INFO] 폰트 메타데이터를 '{new_family_name}'로 업데이트했습니다.")


def re_encode_for_nerd_font(font: fontforge.font) -> None:
    """Nerd Font의 특정 글리프 매핑 문제를 수정합니다(예: 하트, 오른쪽 삼각형 아이콘)."""
    mappings = {
        0xF08D0: 0x2665,  # heart
        0x25BA: 0x22B2,  # tringled right
    }

    for src_codepoint, dest_codepoint in mappings.items():
        try:
            if src_codepoint in font and dest_codepoint in font:
                font.selection.select(src_codepoint)
                font.copy()
                font.selection.select(dest_codepoint)
                font.paste()
                font.selection.select(src_codepoint)
                font.clear()
                print(
                    f"[INFO] 글리프 매핑을 수정했습니다: {hex(src_codepoint)} -> {hex(dest_codepoint)}"
                )
        except Exception as e:
            print(
                f"[WARNING] 글리프 매핑 수정 중 오류 발생 ({hex(src_codepoint)}): {e}"
            )


def generate_font_files(font: fontforge.font, style: str) -> None:
    """최종 TTF 및 WOFF2 폰트 파일을 생성하고 내보냅니다."""
    output_filename_base = f"{_get_cleaned_name(font.familyname)}-{style}"

    for ext in ["ttf", "woff2"]:
        output_path = os.path.join(BUILT_FONTS_PATH, f"{output_filename_base}.{ext}")

        try:
            font.generate(output_path)
            print(f"[INFO] {output_path} 내보내기 완료")
        except Exception as e:
            print(f"[ERROR] {font.fontname}에 대한 {ext.upper()} 생성 실패: {e}")


def scale_font_em_units(font: fontforge.font, target_em: int) -> None:
    """
    폰트의 Em 단위를 조정하고 모든 글리프를 스케일링합니다.
    """
    if font.em == target_em:
        return

    scale_factor = target_em / font.em

    font.em = target_em
    font.selection.all()
    font.transform((scale_factor, 0, 0, scale_factor, 0, 0))

    print(
        f"[INFO] 폰트 Em 단위를 {int(target_em / scale_factor)}에서 {target_em}로 조정했습니다."
    )


def merge_korean_glyphs(
    target_font: fontforge.font, source_font: fontforge.font
) -> None:
    """
    한국어 글리프를 소스 폰트에서 타겟 폰트로 복사합니다.
    """
    try:
        # 한글 범위의 글리프들을 복사
        hangul_ranges = [
            (0x1100, 0x11FF),
            (0x3130, 0x318F),
            (0xA960, 0xA97F),
            (0xAC00, 0xD7AF),
            (0xD7B0, 0xD7FF),
        ]

        copied_count = 0
        for start, end in hangul_ranges:
            for codepoint in range(start, end + 1):
                if codepoint in source_font:
                    source_glyph = source_font[codepoint]
                    if source_glyph.isWorthOutputting():
                        source_font.selection.select(codepoint)
                        source_font.copy()
                        target_font.selection.select(codepoint)
                        target_font.paste()
                        copied_count += 1

        print(f"[INFO] {copied_count}개의 한글 글리프를 복사했습니다.")

    except Exception as e:
        print(f"[ERROR] 한글 글리프 병합 중 오류 발생: {e}")


def process_font_file(
    en_font: fontforge.font,
    ko_font: fontforge.font,
    is_nerd_font: bool,
    font_filename: str,
) -> None:
    """
    단일 폰트 파일을 처리하여 한글 글리프를 병합하고 메타데이터를 업데이트합니다.
    """
    if is_nerd_font:
        re_encode_for_nerd_font(en_font)

    merge_korean_glyphs(en_font, ko_font)

    style = get_font_style(en_font, font_filename)
    update_font_metadata(en_font, style, old_name=OLD_FONT_NAME, new_name=NEW_FONT_NAME)

    generate_font_files(en_font, style)


def find_font_files(directory: str, weight: str = None) -> list:
    """
    지정된 디렉터리에서 폰트 파일을 찾습니다.
    
    Args:
        directory: 폰트 파일을 찾을 디렉터리
        weight: 찾을 폰트 웨이트 ("Regular" 또는 "Bold")
        
    Returns:
        폰트 파일 경로의 리스트
    """
    if not os.path.exists(directory):
        return []
    
    font_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(".ttf"):
            if weight is None:
                font_files.append(os.path.join(directory, filename))
            elif weight.lower() in filename.lower():
                font_files.append(os.path.join(directory, filename))
    
    return font_files


def build_fonts() -> None:
    """
    메인 폰트 빌드 프로세스입니다.
    새로운 디렉터리 구조에서 Regular와 Bold 폰트를 로드하고 병합합니다.
    """
    os.makedirs(BUILT_FONTS_PATH, exist_ok=True)

    # 한글 폰트 로드
    ko_regular_files = find_font_files(KO_FONT_PATH, "regular")
    ko_bold_files = find_font_files(KO_FONT_PATH, "bold")
    
    if not ko_regular_files:
        print(f"[ERROR] {KO_FONT_PATH}에서 Regular 한글 폰트를 찾을 수 없습니다.")
        return
    
    # 영문 폰트 로드
    en_regular_files = find_font_files(EN_FONT_PATH, "regular")
    en_bold_files = find_font_files(EN_FONT_PATH, "bold")
    
    # 너드 폰트 로드
    nerd_regular_files = find_font_files(EN_NERD_FONT_PATH, "regular")
    nerd_bold_files = find_font_files(EN_NERD_FONT_PATH, "bold")
    
    # 폰트 조합 정의
    font_combinations = [
        ("Regular", ko_regular_files, en_regular_files, False),
        ("Bold", ko_bold_files, en_bold_files, False),
        ("NerdFont-Regular", ko_regular_files, nerd_regular_files, True),
        ("NerdFont-Bold", ko_bold_files, nerd_bold_files, True),
    ]
    
    for style, ko_files, en_files, is_nerd_font in font_combinations:
        if not ko_files:
            print(f"[WARNING] {style}용 한글 폰트 파일을 찾을 수 없습니다. 건너뜁니다.")
            continue
        if not en_files:
            print(f"[WARNING] {style}용 영문 폰트 파일을 찾을 수 없습니다. 건너뜁니다.")
            continue
            
        # 첫 번째 파일 사용 (여러 파일이 있을 경우)
        ko_font_path = ko_files[0]
        en_font_path = en_files[0]
        
        try:
            print(f"[INFO] {style} 폰트 처리 중: {os.path.basename(ko_font_path)} + {os.path.basename(en_font_path)}")
            
            # 한글 폰트 로드 및 처리
            ko_font = fontforge.open(ko_font_path)
            scale_font_em_units(ko_font, TARGET_EM)
            process_hangul_glyphs(ko_font)
            
            # 영문 폰트 로드 및 처리
            en_font = fontforge.open(en_font_path)
            process_font_file(en_font, ko_font, is_nerd_font, os.path.basename(en_font_path))
            
            # 폰트 닫기
            en_font.close()
            ko_font.close()
            
        except Exception as e:
            print(f"[ERROR] {style} 폰트 처리 중 오류 발생: {e}")
            continue


if __name__ == "__main__":
    build_fonts()
