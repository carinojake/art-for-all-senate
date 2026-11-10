#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Senate & Art for All Video Production Pipeline
Produces broadcast-ready 1080p MP4 presentation videos with:
1. Natural Neural AI Thai Narration (edge-tts th-TH-PremwadeeNeural, fallback macOS Kanya)
2. Warm cinematic harmonic ambient soundtrack (synthesized via numpy/wave)
3. Luxury glassmorphic typography & vector iconography (PIL with SukhumvitSet)
4. Silky-smooth Ken Burns motion & crossfade transitions (ffmpeg)
"""

import asyncio
import os
import subprocess
import unicodedata
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = "/Users/jake/Desktop/สว"
ASSETS_IMG = os.path.join(BASE_DIR, "assets", "images")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
TEMP_WORK = "/tmp/senate_video_work"
FFMPEG_BIN = "/opt/homebrew/bin/ffmpeg"
FFPROBE_BIN = "/opt/homebrew/bin/ffprobe"

FONT_PATH = "/System/Library/Fonts/Supplemental/SukhumvitSet.ttc"
FONTS = {
    "bold": ImageFont.truetype(FONT_PATH, 44, index=5),
    "semibold": ImageFont.truetype(FONT_PATH, 32, index=4),
    "badge": ImageFont.truetype(FONT_PATH, 21, index=4),
    "body": ImageFont.truetype(FONT_PATH, 26, index=3),
    "footer": ImageFont.truetype(FONT_PATH, 19, index=2),
    "micro": ImageFont.truetype(FONT_PATH, 17, index=3),
}

# Thai combining vowels & tone marks that must never start a wrapped line
THAI_NON_BREAKING_MARKS = set(
    "\u0e31\u0e34\u0e35\u0e36\u0e37\u0e38\u0e39\u0e3a"
    "\u0e47\u0e48\u0e49\u0e4a\u0e4b\u0e4c\u0e4d\u0e4e"
)

CLIPS_DATA = [
    {
        "id": "clip_1_art_for_all_expo",
        "chapter": "ตอนที่ 1 / 3",
        "title": "คลิปที่ 1: Art for All 2569: สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ",
        "output_file": os.path.join(VIDEOS_DIR, "clip_1_art_for_all_expo.mp4"),
        "infographic": os.path.join(ASSETS_IMG, "art-for-all-opportunity.png"),
        "theme_color": (245, 158, 11),  # Amber Gold
        "scenes": [
            {
                "badge": "โครงการระดับชาติ • วุฒิสภาไทย",
                "title": "Art for All: สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ",
                "subtitle": "ขอเชิญร่วมสัมผัสพลังแห่งการสร้างสรรค์ ก้าวข้ามขีดจำกัดด้วยศิลปะ เพื่อพัฒนาศักยภาพคนพิการสู่ระดับสากล",
                "voice": "ขอเชิญร่วมสัมผัสพลังแห่งการสร้างสรรค์ ในโครงการ Art for All สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ",
            },
            {
                "badge": "กำหนดการจัดงาน • รัฐสภาไทย",
                "title": "26 - 28 พฤศจิกายน 2569",
                "subtitle": "ณ อาคารรัฐสภา (สัปปายะสภาสถาน) ศูนย์กลางแห่งการรวมพลัง ส่งเสริมสิทธิ เสรีภาพ และโอกาสแห่งการเติบโต",
                "voice": "จัดขึ้นระหว่างวันที่ 26 ถึง 28 พฤศจิกายน 2569 ณ อาคารรัฐสภา สัปปายะสภาสถาน",
            },
            {
                "badge": "เป้าหมายหลัก • การพัฒนาที่ยั่งยืน",
                "title": "จากผืนผ้าใบ สู่การสร้างอาชีพและรายได้",
                "subtitle": "ใช้ศิลปะบำบัด ฟื้นฟู และยกระดับผลงานสร้างสรรค์คนพิการ 10,000 คน สู่ตลาดมืออาชีพและศักดิ์ศรีที่มั่นคง",
                "voice": "พบกับการใช้ศิลปะเป็นเครื่องมือพัฒนาศักยภาพคนพิการ และต่อยอดผลงานสู่การสร้างอาชีพและรายได้จริง",
            },
            {
                "badge": "ร่วมขับเคลื่อน • พลังความเสมอภาค",
                "title": "เปิดพื้นที่แห่งโอกาส ก้าวข้ามข้อจำกัดไปด้วยกัน",
                "subtitle": "วุฒิสภา และ มูลนิธิ Art for All ขอเชิญชวนทุกท่านร่วมเป็นพลังสำคัญ ขับเคลื่อนสังคมที่ไม่ทิ้งใครไว้ข้างหลัง",
                "voice": "ร่วมเปิดพื้นที่แห่งโอกาส และสร้างความภาคภูมิใจไปด้วยกัน กับวุฒิสภา และมูลนิธิ Art for All",
            },
        ],
    },
    {
        "id": "clip_2_five_in_one_genius",
        "chapter": "ตอนที่ 2 / 3",
        "title": "คลิปที่ 2: มหัศจรรย์ 5 รวมเป็น 1 อัจฉริยะ: พลังแห่งการก้าวข้ามข้อจำกัด",
        "output_file": os.path.join(VIDEOS_DIR, "clip_2_five_in_one_genius.mp4"),
        "infographic": os.path.join(ASSETS_IMG, "channarong-art-for-all.png"),
        "theme_color": (168, 85, 247),  # Royal Purple
        "scenes": [
            {
                "badge": "ปรัชญาโครงการ • ศ.ดร.ชาญณรงค์ พรรุ่งโรจน์",
                "title": "ความพิการไม่ใช่ข้อจำกัด",
                "subtitle": "“ความพิการอาจสร้างข้อจำกัดทางกายภาพ แต่โอกาสต่างหาก คือสิ่งที่กำหนดขีดความสามารถของมนุษย์”",
                "voice": "ความพิการไม่ใช่ข้อจำกัด แต่โอกาสต่างหาก คือสิ่งที่กำหนดขีดความสามารถ",
            },
            {
                "badge": "โมเดลนวัตกรรมสังคม • 5 In 1 Genius",
                "title": "โมเดล “5 รวมเป็น 1 อัจฉริยะ”",
                "subtitle": "ริเริ่มตั้งแต่ พ.ศ. 2540 และได้รับรางวัลเกียรติยศระดับชาติ “ค่าของแผ่นดิน” จากสำนักนายกรัฐมนตรี",
                "voice": "โมเดล 5 รวมเป็น 1 อัจฉริยะ ริเริ่มโดย ศาสตราจารย์ ดร.ชาญณรงค์ พรรุ่งโรจน์ สมาชิกวุฒิสภา",
            },
            {
                "badge": "การผสานพลัง • จุดแข็ง 5 ศักยภาพ",
                "title": "ปาก หู ตา ปัญญา แรงกาย และผู้ประสานงาน",
                "subtitle": "คนตาบอดสื่อสาร คนหูหนวกบรรจงแต้มสี กายภาพวางกลยุทธ์ สติปัญญาทุ่มเทแรงกาย ผสานผู้ประสานงาน",
                "voice": "ผสานพลัง ตาบอดเป็นปาก หูหนวกเป็นตา กายภาพเป็นปัญญา สติปัญญาเป็นแรงกาย ร่วมกับผู้ประสานงาน",
            },
            {
                "badge": "ผลลัพธ์เชิงประจักษ์ • ศักดิ์ศรีความเป็นมนุษย์",
                "title": "หลอมรวมเป็นหนึ่งอัจฉริยะ ไร้ขีดจำกัด",
                "subtitle": "สร้างสรรค์ผลงานระดับมาสเตอร์พีซ เพื่อพิสูจน์คุณค่า และศักดิ์ศรีความเป็นมนุษย์ที่พึ่งพาตนเองได้อย่างยั่งยืน",
                "voice": "หลอมรวมเป็นหนึ่งผลงานสร้างสรรค์ เพื่อพิสูจน์คุณค่า และศักดิ์ศรีความเป็นมนุษย์อย่างยั่งยืน",
            },
        ],
    },
    {
        "id": "clip_3_senate_legislative_power",
        "chapter": "ตอนที่ 3 / 3",
        "title": "คลิปที่ 3: พลังนิติบัญญัติเพื่อความยั่งยืน: วุฒิสภาเคียงข้างผู้พิการไทย",
        "output_file": os.path.join(VIDEOS_DIR, "clip_3_senate_legislative_power.mp4"),
        "infographic": os.path.join(ASSETS_IMG, "senate-legislative-power.png"),
        "theme_color": (16, 185, 129),  # Emerald
        "scenes": [
            {
                "badge": "วิสัยทัศน์นิติบัญญัติ • วุฒิสภาไทย",
                "title": "พลังนิติบัญญัติ สู่การพัฒนาที่ยั่งยืน",
                "subtitle": "บทบาท หน้าที่ และความมุ่งมั่นของวุฒิสภา ในการกลั่นกรองกฎหมายและขับเคลื่อนนโยบายเพื่อคนพิการ",
                "voice": "วุฒิสภาไทย มุ่งมั่นขับเคลื่อนพลังนิติบัญญัติ เพื่อยกระดับคุณภาพชีวิตคนพิการอย่างเป็นรูปธรรม",
            },
            {
                "badge": "เสาหลักที่ 1 • ด้านนโยบายและกฎหมาย",
                "title": "คุ้มครองสิทธิ สวัสดิการ และ Universal Design",
                "subtitle": "กลั่นกรองกฎหมาย ผลักดันความเสมอภาค และสร้างมาตรฐานอารยสถาปัตย์ในพื้นที่สาธารณะทั่วประเทศ",
                "voice": "เสาหลักที่ 1 กลั่นกรองกฎหมาย ผลักดันสิทธิ สวัสดิการ และมาตรฐาน อารยสถาปัตย์ ยูนิเวอร์แซล ดีไซน์",
            },
            {
                "badge": "เสาหลักที่ 2 & 3 • ศักยภาพและการสร้างงาน",
                "title": "พัฒนาศักยภาพผ่านศิลปะ สู่การสร้างอาชีพจริง",
                "subtitle": "บูรณาการภาครัฐ ภาคเอกชน และเครือข่ายศิลปิน ยกระดับผลงานสร้างสรรค์สู่ตลาด สร้างรายได้ที่มั่นคงและมีศักดิ์ศรี",
                "voice": "เสาหลักที่ 2 และ 3 ส่งเสริมการใช้ศิลปะฟื้นฟูศักยภาพ พร้อมบูรณาการเครือข่ายสร้างงาน สร้างอาชีพที่มั่นคง",
            },
            {
                "badge": "พันธกิจเพื่อสังคม • ไม่ทิ้งใครไว้ข้างหลัง",
                "title": "สังคมแห่งความเสมอภาค และโอกาสที่เท่าเทียม",
                "subtitle": "วุฒิสภาเคียงข้างคนพิการไทย ร่วมสร้างอนาคตที่ยั่งยืนและภาคภูมิใจไปด้วยกัน",
                "voice": "วุฒิสภา ร่วมสร้างสังคมแห่งความเสมอภาค ไม่ทิ้งใครไว้ข้างหลัง ผ่านพลังแห่งศิลปะและโอกาส",
            },
        ],
    },
]


async def _edge_tts_save(text: str, output_mp3: str, voice: str = "th-TH-PremwadeeNeural", rate: str = "-4%"):
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_mp3)


def get_audio_duration(audio_path: str) -> float:
    ffprobe_cmd = [
        FFPROBE_BIN,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        audio_path,
    ]
    return float(subprocess.check_output(ffprobe_cmd).decode().strip())


def synthesize_voice(text: str, output_wav: str) -> float:
    """Synthesize Thai AI neural narration via edge-tts, with offline macOS Kanya fallback."""
    temp_mp3 = output_wav.replace(".wav", ".mp3")
    used_neural = False
    try:
        asyncio.run(_edge_tts_save(text, temp_mp3))
        if os.path.exists(temp_mp3) and os.path.getsize(temp_mp3) > 1024:
            conv_cmd = [
                FFMPEG_BIN,
                "-y",
                "-i",
                temp_mp3,
                "-af",
                "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar",
                "44100",
                "-ac",
                "2",
                output_wav,
            ]
            subprocess.run(conv_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            used_neural = True
    except Exception:
        used_neural = False
    finally:
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

    if not used_neural:
        temp_aiff = output_wav.replace(".wav", ".aiff")
        subprocess.run(["say", "-v", "Kanya", "-r", "158", text, "-o", temp_aiff], check=True)
        conv_cmd = [FFMPEG_BIN, "-y", "-i", temp_aiff, "-ar", "44100", "-ac", "2", output_wav]
        subprocess.run(conv_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(temp_aiff):
            os.remove(temp_aiff)

    return get_audio_duration(output_wav)


def generate_ambient_music(duration: float, output_wav: str):
    """Synthesize a warm cinematic harmonic ambient pad bed."""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    chords = [
        [261.63, 329.63, 392.00, 493.88],        # Cmaj7
        [220.00, 261.63, 329.63, 392.00, 493.88], # Am9
        [174.61, 261.63, 329.63, 392.00],        # Fmaj7
        [196.00, 261.63, 293.66, 392.00],        # Gsus4
    ]
    chord_len = duration / len(chords)
    signal = np.zeros_like(t)

    for i, chord in enumerate(chords):
        t_start = i * chord_len
        t_end = min((i + 1) * chord_len, duration)
        idx_mask = (t >= t_start) & (t < t_end)
        t_segment = t[idx_mask] - t_start
        segment_len = len(t_segment)
        if segment_len == 0:
            continue

        segment_sig = np.zeros(segment_len)
        for f in chord:
            segment_sig += 0.14 * np.sin(2 * np.pi * f * t_segment)
            segment_sig += 0.04 * np.sin(2 * np.pi * (f * 2) * t_segment)

        attack = int(sample_rate * 0.8)
        decay = int(sample_rate * 0.8)
        env = np.ones(segment_len)
        if segment_len > attack:
            env[:attack] = np.linspace(0.1, 1.0, attack)
        if segment_len > decay:
            env[-decay:] = np.linspace(1.0, 0.2, decay)
        signal[idx_mask] += segment_sig * env

    total_len = len(signal)
    master_fade = min(int(sample_rate * 1.5), total_len // 4)
    if master_fade > 0:
        signal[:master_fade] *= np.linspace(0.0, 1.0, master_fade)
        signal[-master_fade:] *= np.linspace(1.0, 0.0, master_fade)

    signal = signal * 0.20
    audio = (signal * 32767).astype(np.int16)

    with wave.open(output_wav, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())


def _split_long_token(token: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    """Break an unspaced Thai string cleanly without orphaning combining vowels/tone marks."""
    chunks = []
    buf = ""
    i = 0
    while i < len(token):
        cluster = token[i]
        i += 1
        while i < len(token) and (
            token[i] in THAI_NON_BREAKING_MARKS or unicodedata.category(token[i]).startswith("M")
        ):
            cluster += token[i]
            i += 1
        candidate = buf + cluster
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if (bbox[2] - bbox[0]) <= max_width or not buf:
            buf = candidate
        else:
            chunks.append(buf)
            buf = cluster
    if buf:
        chunks.append(buf)
    return chunks


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    """Wrap Thai & English text cleanly within max_width."""
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if not word:
            continue
        test_line = f"{current_line} {word}".strip() if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = ""
            wbbox = draw.textbbox((0, 0), word, font=font)
            if (wbbox[2] - wbbox[0]) <= max_width:
                current_line = word
            else:
                sub_chunks = _split_long_token(word, font, max_width, draw)
                lines.extend(sub_chunks[:-1])
                current_line = sub_chunks[-1]
    if current_line:
        lines.append(current_line)
    return lines


def draw_diamond_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, fill):
    pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(pts, fill=fill)


def draw_mic_icon(draw: ImageDraw.ImageDraw, x: int, y: int, color):
    draw.rounded_rectangle([(x + 4, y), (x + 12, y + 13)], radius=4, fill=color)
    draw.arc([(x + 1, y + 5), (x + 15, y + 17)], start=0, end=180, fill=color, width=2)
    draw.line([(x + 8, y + 17), (x + 8, y + 21)], fill=color, width=2)
    draw.line([(x + 4, y + 21), (x + 12, y + 21)], fill=color, width=2)


def draw_calendar_icon(draw: ImageDraw.ImageDraw, x: int, y: int, color):
    draw.rounded_rectangle([(x, y + 3), (x + 18, y + 19)], radius=3, outline=color, width=2)
    draw.line([(x, y + 8), (x + 18, y + 8)], fill=color, width=2)
    draw.line([(x + 5, y), (x + 5, y + 5)], fill=color, width=2)
    draw.line([(x + 13, y), (x + 13, y + 5)], fill=color, width=2)


def _rounded_mask(width: int, height: int, radius: int) -> Image.Image:
    mask = Image.new("L", (width, height), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=radius, fill=255)
    return mask


def create_scene_frame(
    scene_data: dict,
    infographic_path: str,
    theme_color: tuple[int, int, int],
    scene_idx: int,
    total_scenes: int,
    chapter_label: str,
) -> Image.Image:
    """Render a 1920x1080 broadcast-grade presentation slide."""
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), color=(10, 15, 28))
    draw = ImageDraw.Draw(im)

    # 1. Ambient Radial Theme Glow
    glow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_overlay)
    gdraw.ellipse([(-220, -220), (820, 820)], fill=(*theme_color, 32))
    gdraw.ellipse([(W - 760, H - 760), (W + 220, H + 220)], fill=(*theme_color, 26))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(90))
    im.paste(glow_overlay, (0, 0), glow_overlay)

    # 2. Top Header Navigation Bar
    draw.rectangle([(0, 0), (W, 74)], fill=(15, 23, 42))
    draw.line([(0, 74), (W, 74)], fill=(38, 50, 72), width=1)

    draw_diamond_icon(draw, 92, 37, 8, theme_color)
    draw.text((114, 21), f"SENATE OF THAILAND  ×  ART FOR ALL 2569   |   {chapter_label}", font=FONTS["badge"], fill=(226, 232, 240))

    # Scene Step Counter & Pills
    step_text = f"ฉากที่ {scene_idx + 1} / {total_scenes}"
    sbbox = draw.textbbox((0, 0), step_text, font=FONTS["micro"])
    sw = sbbox[2] - sbbox[0]
    pills_start_x = W - 235
    draw.text((pills_start_x - sw - 18, 25), step_text, font=FONTS["micro"], fill=(148, 163, 184))
    for i in range(total_scenes):
        px = pills_start_x + (i * 36)
        pcolor = theme_color if i == scene_idx else (51, 65, 85)
        draw.rounded_rectangle([(px, 33), (px + 28, 40)], radius=3, fill=pcolor)

    # 3. Left Panel: High-Res Infographic in Museum Glass Frame
    card_x, card_y, card_w, card_h = 80, 118, 780, 868
    draw.rounded_rectangle(
        [(card_x - 2, card_y - 2), (card_x + card_w + 2, card_y + card_h + 2)],
        radius=24,
        outline=(*theme_color, 150),
        width=2,
    )
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=22, fill=(15, 23, 42))

    if os.path.exists(infographic_path):
        info_img = Image.open(infographic_path).convert("RGB")
        info_ratio = info_img.width / info_img.height
        inner_pad = 16
        target_w = card_w - (inner_pad * 2)
        target_h = card_h - (inner_pad * 2)
        target_ratio = target_w / target_h

        # For landscape infographics inside vertical card, add blurred ambient art backdrop + museum header/footer
        if info_ratio > 1.15:
            bg_fill = info_img.resize((card_w, card_h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(28))
            dark_tint = Image.new("RGBA", (card_w, card_h), (10, 15, 28, 185))
            bg_rgba = bg_fill.convert("RGBA")
            bg_composited = Image.alpha_composite(bg_rgba, dark_tint).convert("RGB")
            im.paste(bg_composited, (card_x, card_y), _rounded_mask(card_w, card_h, 22))
            draw.rounded_rectangle(
                [(card_x, card_y), (card_x + card_w, card_y + card_h)],
                radius=22,
                outline=(*theme_color, 140),
                width=2,
            )
            draw_diamond_icon(draw, card_x + 34, card_y + 34, 6, theme_color)
            draw.text(
                (card_x + 50, card_y + 20),
                "INFOGRAPHIC  •  สื่อประชาสัมพันธ์โครงการ",
                font=FONTS["micro"],
                fill=(226, 232, 240),
            )
            draw.text(
                (card_x + 28, card_y + card_h - 42),
                "วุฒิสภาไทย  ×  มูลนิธิศิลปะเพื่อมวลมนุษย์ (Art for All)",
                font=FONTS["micro"],
                fill=(180, 195, 215),
            )
            usable_h = card_h - 110
            nw = target_w
            nh = min(int(nw / info_ratio), usable_h)
            nw = int(nh * info_ratio)
        else:
            if info_ratio > target_ratio:
                nw = target_w
                nh = int(nw / info_ratio)
            else:
                nh = target_h
                nw = int(nh * info_ratio)

        resized_info = info_img.resize((nw, nh), Image.Resampling.LANCZOS)
        px = card_x + (card_w - nw) // 2
        py = card_y + (card_h - nh) // 2
        # Subtle frame around embedded artwork
        draw.rounded_rectangle(
            [(px - 3, py - 3), (px + nw + 3, py + nh + 3)],
            radius=14,
            outline=(255, 255, 255, 70),
            width=2,
        )
        im.paste(resized_info, (px, py), _rounded_mask(nw, nh, 12))

    # 4. Right Panel: Content Card & Typography
    rx, ry, rw, rh = 900, 118, 940, 868
    draw.rounded_rectangle(
        [(rx, ry), (rx + rw, ry + rh)],
        radius=24,
        fill=(17, 24, 39),
        outline=(51, 65, 85),
        width=1,
    )

    # Top-right theme accent strip inside card
    draw.rounded_rectangle([(rx + 50, ry + 48), (rx + 120, ry + 54)], radius=3, fill=theme_color)

    # Badge Pill
    badge_text = scene_data["badge"]
    bbox = draw.textbbox((0, 0), badge_text, font=FONTS["badge"])
    bw = (bbox[2] - bbox[0]) + 56
    badge_y = ry + 74
    draw.rounded_rectangle(
        [(rx + 50, badge_y), (rx + 50 + bw, badge_y + 42)],
        radius=21,
        fill=(26, 36, 56),
        outline=theme_color,
        width=2,
    )
    draw_diamond_icon(draw, rx + 72, badge_y + 21, 6, theme_color)
    draw.text((rx + 88, badge_y + 7), badge_text, font=FONTS["badge"], fill=theme_color)

    # Title
    title_lines = wrap_text(scene_data["title"], FONTS["bold"], rw - 100, draw)
    ty = badge_y + 64
    for tline in title_lines:
        draw.text((rx + 50, ty), tline, font=FONTS["bold"], fill=(255, 255, 255))
        ty += 60

    # Accent Divider
    ty += 12
    draw.line([(rx + 50, ty), (rx + 250, ty)], fill=theme_color, width=3)
    ty += 28

    # Subtitle / Narrative
    sub_lines = wrap_text(scene_data["subtitle"], FONTS["semibold"], rw - 105, draw)
    for sline in sub_lines:
        draw.text((rx + 50, ty), sline, font=FONTS["semibold"], fill=(226, 232, 240))
        ty += 48

    # Spoken Narration Box (Auto-sized so text never overflows)
    vlines = wrap_text(f"“{scene_data['voice']}”", FONTS["body"], rw - 135, draw)
    box_h = max(145, 72 + len(vlines) * 38)
    box_y = ry + rh - 65 - box_h
    draw.rounded_rectangle(
        [(rx + 42, box_y), (rx + rw - 42, box_y + box_h)],
        radius=18,
        fill=(25, 35, 54),
        outline=theme_color,
        width=1,
    )
    draw_mic_icon(draw, rx + 66, box_y + 19, theme_color)
    draw.text((rx + 94, box_y + 17), "บทบรรยายประกอบภาพ (AI Voiceover):", font=FONTS["badge"], fill=(165, 180, 200))

    vy = box_y + 54
    voice_text_color = (254, 240, 138) if theme_color[0] > 200 else (241, 245, 249)
    for vl in vlines:
        draw.text((rx + 66, vy), vl, font=FONTS["body"], fill=voice_text_color)
        vy += 38

    # Bottom Card Footer
    footer_y = ry + rh - 44
    draw_calendar_icon(draw, rx + 50, footer_y + 3, theme_color)
    foot_text = "กำหนดการจัดงาน: 26 - 28 พฤศจิกายน 2569   |   ณ อาคารรัฐสภา (สัปปายะสภาสถาน)"
    draw.text((rx + 78, footer_y), foot_text, font=FONTS["footer"], fill=(148, 163, 184))

    return im


def build_single_clip(clip_data: dict) -> str:
    """Build a single 1080p MP4 clip with 4 scenes, neural TTS narration, ambient bed & smooth transitions."""
    clip_id = clip_data["id"]
    print(f"\n=======================================================")
    print(f"🎬 กำลังผลิต: {clip_data['title']}")
    print(f"=======================================================")

    clip_work = os.path.join(TEMP_WORK, clip_id)
    if os.path.exists(clip_work):
        import shutil
        shutil.rmtree(clip_work)
    os.makedirs(clip_work, exist_ok=True)

    scene_videos = []
    scene_durations = []
    total_scenes = len(clip_data["scenes"])
    xfade_dur = 0.45

    for s_idx, scene in enumerate(clip_data["scenes"]):
        scene_wav = os.path.join(clip_work, f"scene_{s_idx}_voice.wav")
        dur = synthesize_voice(scene["voice"], scene_wav)
        # Add brief intro & outro pause so transitions never clip speech
        lead_silence = 0.35
        pad_dur = max(dur + lead_silence + 1.1, 6.2)
        scene_durations.append(pad_dur)

        slide_img = create_scene_frame(
            scene,
            clip_data["infographic"],
            clip_data["theme_color"],
            s_idx,
            total_scenes,
            clip_data["chapter"],
        )
        slide_png = os.path.join(clip_work, f"scene_{s_idx}.png")
        slide_img.save(slide_png, "PNG")

        # Shift voice by 350ms and pad to exact scene duration
        padded_wav = os.path.join(clip_work, f"scene_{s_idx}_padded.wav")
        pad_cmd = [
            FFMPEG_BIN,
            "-y",
            "-i",
            scene_wav,
            "-af",
            f"adelay=350|350,apad=whole_dur={pad_dur:.2f}",
            "-ar",
            "44100",
            "-ac",
            "2",
            padded_wav,
        ]
        subprocess.run(pad_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Render silky-smooth Ken Burns motion (upscale first to prevent subpixel text shimmer)
        scene_mp4 = os.path.join(clip_work, f"scene_{s_idx}.mp4")
        total_frames = int(round(pad_dur * 30))
        vf_filter = (
            f"scale=2880:1620:flags=lanczos,"
            f"zoompan=z='1+0.025*on/{total_frames}':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={total_frames}:s=1920x1080:fps=30"
        )
        vid_cmd = [
            FFMPEG_BIN,
            "-y",
            "-loop",
            "1",
            "-i",
            slide_png,
            "-i",
            padded_wav,
            "-vf",
            vf_filter,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "19",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-t",
            f"{pad_dur:.2f}",
            scene_mp4,
        ]
        subprocess.run(vid_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        scene_videos.append(scene_mp4)
        print(f"  ✓ ฉากที่ {s_idx + 1}/{total_scenes}: {scene['badge']} ({pad_dur:.1f} วินาที)")

    # Join scenes with smooth crossfade transitions
    raw_joined_mp4 = os.path.join(clip_work, "raw_joined.mp4")
    inputs = []
    for sv in scene_videos:
        inputs.extend(["-i", sv])

    v_filters = []
    a_filters = []
    curr_v = "[0:v]"
    curr_a = "[0:a]"
    offset = scene_durations[0] - xfade_dur
    for i in range(1, len(scene_videos)):
        next_v = f"[v{i}]"
        next_a = f"[a{i}]"
        v_filters.append(f"{curr_v}[{i}:v]xfade=transition=fade:duration={xfade_dur}:offset={offset:.3f}{next_v}")
        a_filters.append(f"{curr_a}[{i}:a]acrossfade=d={xfade_dur}:c1=tri:c2=tri{next_a}")
        curr_v = next_v
        curr_a = next_a
        if i < len(scene_videos) - 1:
            offset += scene_durations[i] - xfade_dur

    filter_complex = ";".join(v_filters + a_filters)
    join_cmd = [
        FFMPEG_BIN,
        "-y",
        *inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        curr_v,
        "-map",
        curr_a,
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "19",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        raw_joined_mp4,
    ]
    subprocess.run(join_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    joined_dur = get_audio_duration(raw_joined_mp4)
    music_wav = os.path.join(clip_work, "ambient_bed.wav")
    generate_ambient_music(joined_dur, music_wav)

    # Mix voice narration with warm subtle ambient bed
    final_output = clip_data["output_file"]
    mix_cmd = [
        FFMPEG_BIN,
        "-y",
        "-i",
        raw_joined_mp4,
        "-i",
        music_wav,
        "-filter_complex",
        "[0:a]volume=1.05[voice];[1:a]volume=0.22[music];[voice][music]amix=inputs=2:duration=first:normalize=0[aout]",
        "-map",
        "0:v",
        "-map",
        "[aout]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        final_output,
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    fsize_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"  🎉 เรนเดอร์สำเร็จ: {os.path.basename(final_output)} ({fsize_mb:.2f} MB, ความยาว {joined_dur:.1f} วินาที)")
    return final_output


def build_master_combined_video(clip_outputs: list[str], master_path: str):
    """Combine all 3 clips into one full presentation master MP4 with crossfades."""
    print(f"\n=======================================================")
    print("🎞️  กำลังรวมคลิปฉบับเต็มพร้อมพรีเซนต์ (Full Master Presentation)")
    print("=======================================================")
    xfade_dur = 0.65
    durations = [get_audio_duration(p) for p in clip_outputs]

    inputs = []
    for p in clip_outputs:
        inputs.extend(["-i", p])

    v_filters = []
    a_filters = []
    curr_v = "[0:v]"
    curr_a = "[0:a]"
    offset = durations[0] - xfade_dur
    for i in range(1, len(clip_outputs)):
        next_v = f"[mv{i}]"
        next_a = f"[ma{i}]"
        v_filters.append(f"{curr_v}[{i}:v]xfade=transition=fadeblack:duration={xfade_dur}:offset={offset:.3f}{next_v}")
        a_filters.append(f"{curr_a}[{i}:a]acrossfade=d={xfade_dur}:c1=tri:c2=tri{next_a}")
        curr_v = next_v
        curr_a = next_a
        if i < len(clip_outputs) - 1:
            offset += durations[i] - xfade_dur

    cmd = [
        FFMPEG_BIN,
        "-y",
        *inputs,
        "-filter_complex",
        ";".join(v_filters + a_filters),
        "-map",
        curr_v,
        "-map",
        curr_a,
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "19",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        master_path,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    total_dur = get_audio_duration(master_path)
    fsize_mb = os.path.getsize(master_path) / (1024 * 1024)
    print(f"  🏆 คลิปฉบับเต็มพร้อมพรีเซนต์สำเร็จ: {os.path.basename(master_path)} ({fsize_mb:.2f} MB, ความยาว {total_dur:.1f} วินาที)")


def main():
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(TEMP_WORK, exist_ok=True)

    clip_outputs = []
    for clip in CLIPS_DATA:
        out_mp4 = build_single_clip(clip)
        clip_outputs.append(out_mp4)

    master_output = os.path.join(VIDEOS_DIR, "art_for_all_senate_full_presentation.mp4")
    build_master_combined_video(clip_outputs, master_output)

    print("\n✨ ผลิตคลิปวิดีโอระดับผู้บริหารครบทั้งหมด (3 คลิปย่อย + 1 คลิปฉบับเต็ม) เสร็จสมบูรณ์ 100% ✨")


if __name__ == "__main__":
    main()
