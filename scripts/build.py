import os
import sys
import shutil

from config import (
    BUILT_FONTS_PATH,
    EN_FONT_PATH,
    KO_FONT_PATH,
    EN_NERD_FONT_PATH,
)
from hangulify import build_fonts


def print_usage():
    """사용법 안내 메시지를 출력합니다."""
    print(f"python {sys.argv[0]} <subcommand>\n")
    print("subcommand:")
    print("    build  : assets 디렉터리의 폰트를 병합하고 출력합니다.")
    print("    test   : 폰트 빌드 프로세스를 테스트합니다.")
    print("    clean  : 출력 파일을 삭제합니다.")




def check_font_directories():
    """필요한 폰트 디렉터리들이 존재하는지 확인합니다."""
    directories = {
        "영문 폰트": EN_FONT_PATH,
        "한글 폰트": KO_FONT_PATH,
        "너드 폰트": EN_NERD_FONT_PATH
    }
    
    missing_dirs = []
    for name, path in directories.items():
        if not os.path.exists(path):
            missing_dirs.append((name, path))
        else:
            ttf_files = [f for f in os.listdir(path) if f.lower().endswith('.ttf')]
            if not ttf_files:
                print(f"[WARNING] {name} 디렉터리({path})에 TTF 파일이 없습니다.")
            else:
                print(f"[INFO] {name} 디렉터리 확인: {len(ttf_files)}개 폰트 파일 발견")
    
    if missing_dirs:
        print("[ERROR] 다음 디렉터리들이 누락되었습니다:")
        for name, path in missing_dirs:
            print(f"  - {name}: {path}")
        return False
    
    return True


def test_font_build():
    """폰트 빌드 프로세스를 테스트합니다."""
    print("[INFO] 폰트 빌드 테스트 시작")
    
    if not check_font_directories():
        print("[ERROR] 필요한 폰트 디렉터리가 누락되었습니다.")
        return False
    
    try:
        # FontForge 모듈 임포트 테스트
        import fontforge
        print("[INFO] FontForge 모듈 로드 성공")
        
        # 각 디렉터리에서 첫 번째 폰트 파일 로드 테스트
        test_dirs = [EN_FONT_PATH, KO_FONT_PATH, EN_NERD_FONT_PATH]
        for test_dir in test_dirs:
            ttf_files = [f for f in os.listdir(test_dir) if f.lower().endswith('.ttf')]
            if ttf_files:
                test_file = os.path.join(test_dir, ttf_files[0])
                try:
                    font = fontforge.open(test_file)
                    print(f"[INFO] 폰트 로드 테스트 성공: {ttf_files[0]} (Family: {font.familyname})")
                    font.close()
                except Exception as e:
                    print(f"[ERROR] 폰트 로드 테스트 실패 ({ttf_files[0]}): {e}")
                    return False
        
        print("[INFO] 모든 테스트가 성공했습니다. 폰트 빌드를 진행할 수 있습니다.")
        return True
        
    except ImportError as e:
        print(f"[ERROR] FontForge 모듈을 찾을 수 없습니다: {e}")
        print("[INFO] FontForge 설치: pip install fontforge-python 또는 시스템 패키지 관리자 사용")
        return False
    except Exception as e:
        print(f"[ERROR] 테스트 중 오류 발생: {e}")
        return False


def clean():
    """출력 파일을 삭제합니다."""
    print("[INFO] 출력 파일 삭제 중")
    if os.path.exists(BUILT_FONTS_PATH):
        shutil.rmtree(BUILT_FONTS_PATH)
        print(f"[INFO] {BUILT_FONTS_PATH} 디렉터리를 삭제했습니다.")
    else:
        print(f'[INFO] "{BUILT_FONTS_PATH}" 디렉터리를 찾을 수 없어 건너뜁니다.')




def main():
    if len(sys.argv) == 1:
        print_usage()
        exit(1)

    subcommand = sys.argv[1]

    if subcommand == "build":
        print("[INFO] 폰트 디렉터리 확인 중")
        if check_font_directories():
            print("[INFO] 폰트 빌드 시작")
            build_fonts()
        else:
            print("[ERROR] 폰트 빌드에 필요한 파일이 준비되지 않았습니다.")
            exit(1)
    elif subcommand == "test":
        success = test_font_build()
        if not success:
            exit(1)
    elif subcommand == "clean":
        clean()
    else:
        print_usage()
        exit(1)


if __name__ == "__main__":
    main()
