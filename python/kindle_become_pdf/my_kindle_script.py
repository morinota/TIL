import os
import subprocess
import time

import pyautogui
from loguru import logger
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def main(
    output_pdf="kindle_output.pdf",
    total_pages=10,
) -> None:
    os.makedirs("screenshots", exist_ok=True)
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    _activate_kindle()  # Kindleアプリをアクティブにする

    logger.info(f"スクショ開始！全部で{total_pages}ページ分やるよ〜📸")
    for i in range(total_pages):
        filepath = f"/tmp/screenshots/page_{i:03}.png"
        logger.debug(f"{i+1}ページ目のスクショ撮るよ！保存先: {filepath}")
        os.system(f"screencapture -R0,0,1280,800 -x {filepath}")  # 範囲は必要に応じて調整！

        time.sleep(1)  # 安全にスクショ取れるまで待つ

        # ページめくり
        pyautogui.press("right")
        logger.debug("ページめくったよ→")
        time.sleep(0.5)

        # 画像をPDFに貼り付け
        img = Image.open(filepath)
        img = img.convert("RGB")
        img = img.resize((int(width), int(height)))  # A4にフィット
        img_path_jpg = filepath.replace(".png", ".jpg")
        img.save(img_path_jpg)

        c.drawImage(img_path_jpg, 0, 0, width=width, height=height)
        c.showPage()
        logger.info(f"{i+1}ページ目完了！")

    c.save()
    logger.success(f"PDF保存完了！{output_pdf}に出力したよ〜✨")


def _activate_kindle() -> None:
    """Kindleアプリをアクティブにする"""
    subprocess.run(["osascript", "-e", 'tell application "Kindle" to activate'])
    time.sleep(0.5)  # 少し待ってから操作しないとダメなことある


if __name__ == "__main__":
    input("Kindleを開いて、スクショ撮りたいページを表示してEnter押してね📖✨")
    logger.info("ユーザーの操作待ち中...準備できたらEnter押してね！")
    main(total_pages=5)
