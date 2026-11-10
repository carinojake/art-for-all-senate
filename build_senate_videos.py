#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Senate & Art for All Video Production Pipeline (V2 Master Edition)
Produces broadcast-ready 1080p MP4 presentation videos with:
1. Bespoke AI Cinematic Scene Artworks (12 unique scenes across 3 clips) + Official Infographic PiP
2. Complete Senate Governance & Policy Integration across ALL 3 clips (Requirement 3)
3. Natural Thai Speech Narration (macOS Kanya) + Synthesized Harmonic Ambient Soundtrack
4. Luxury Glassmorphic Typography (PIL with SukhumvitSet & Thai non-breaking vowel protection)
5. Silky-smooth Ken Burns motion & crossfade transitions (ffmpeg)
"""

import os
import subprocess
import unicodedata
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = "/Users/jake/Desktop/สว"
ASSETS_IMG = os.path.join(BASE_DIR, "assets", "images")
AI_SCENES_DIR = os.path.join(BASE_DIR, "assets", "ai_scenes")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
TEMP_WORK = "/tmp/senate_video_work_v2"
FFMPEG_BIN = "/opt/homebrew/bin/ffmpeg"
FFPROBE_BIN = "/opt/homebrew/bin/ffprobe"

FONT_PATH = "/System/Library/Fonts/Supplemental/SukhumvitSet.ttc"
FONTS = {
    "bold": ImageFont.truetype(FONT_PATH, 42, index=5),
    "semibold": ImageFont.truetype(FONT_PATH, 29, index=4),
    "badge": ImageFont.truetype(FONT_PATH, 20, index=4),
    "pill": ImageFont.truetype(FONT_PATH, 21, index=4),
    "body": ImageFont.truetype(FONT_PATH, 25, index=3),
    "footer": ImageFont.truetype(FONT_PATH, 19, index=2),
    "micro": ImageFont.truetype(FONT_PATH, 16, index=4),
}

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
                "ai_image": os.path.join(AI_SCENES_DIR, "clip1_s1.jpg"),
                "badge": "โครงการระดับชาติ • วุฒิสภาไทย",
                "title": "Art for All: สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ",
                "subtitle": "ใช้ศิลปะเป็นเครื่องมือพัฒนาศักยภาพคนพิการ ก้าวข้ามข้อจำกัดทางกายภาพ สู่เวทีสร้างสรรค์ระดับสากล",
                "senate_pill": "บทบาทวุฒิสภา: ส่งเสริมและเปิดพื้นที่โอกาสให้คนพิการเข้าถึงศิลปะอย่างเท่าเทียม",
                "voice": "ขอเชิญร่วมสัมผัสพลังแห่งการสร้างสรรค์ ในโครงการ Art for All สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ ที่วุฒิสภาร่วมผลักดันเพื่อคนพิการไทย",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip1_s2.jpg"),
                "badge": "กำหนดการจัดงาน • รัฐสภาไทย",
                "title": "26 - 28 พฤศจิกายน 2569",
                "subtitle": "ณ อาคารรัฐสภา (สัปปายะสภาสถาน) ศูนย์กลางแห่งการรวมพลังนิติบัญญัติ ภาครัฐ เอกชน และภาคประชาชน",
                "senate_pill": "บทบาทวุฒิสภา: ผลักดันนโยบายด้านคุณภาพชีวิต สิทธิ และความเสมอภาคในสังคม",
                "voice": "จัดขึ้นระหว่างวันที่ 26 ถึง 28 พฤศจิกายน 2569 ณ อาคารรัฐสภา เพื่อผลักดันนโยบายสิทธิและความเสมอภาคของคนพิการ",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip1_s3.jpg"),
                "badge": "เป้าหมายหลัก • การพัฒนาที่ยั่งยืน",
                "title": "จากผืนผ้าใบ สู่การสร้างอาชีพและรายได้จริง",
                "subtitle": "ศิลปะบำบัด ฟื้นฟูจิตใจ และต่อยอดผลงานศิลปะสู่ผลิตภัณฑ์สร้างอาชีพให้คนพิการ 10,000 คน ภายใน 10 ปี",
                "senate_pill": "บทบาทวุฒิสภา: สนับสนุนการต่อยอดทักษะสู่ตลาดอาชีพและรายได้ที่มั่นคง",
                "voice": "พบกับการใช้ศิลปะพัฒนาศักยภาพคนพิการ และต่อยอดผลงานสู่การสร้างอาชีพและรายได้ที่มั่นคงอย่างเป็นรูปธรรม",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip1_s4.jpg"),
                "badge": "บูรณาการทุกภาคส่วน • ไม่ทิ้งใครไว้ข้างหลัง",
                "title": "เปิดพื้นที่แห่งโอกาส ก้าวข้ามข้อจำกัดไปด้วยกัน",
                "subtitle": "วุฒิสภา และ มูลนิธิ Art for All เชื่อมโยงทุกภาคส่วนร่วมสร้างสังคมแห่งศักดิ์ศรีความเป็นมนุษย์",
                "senate_pill": "บทบาทวุฒิสภา: ส่งเสริมการมีส่วนร่วมของทุกภาคส่วนในการพัฒนาศักยภาพคนพิการ",
                "voice": "วุฒิสภา และมูลนิธิ Art for All ขอเชิญทุกภาคส่วนร่วมสร้างความเสมอภาค และเปิดโอกาสให้คนพิการอย่างยั่งยืน",
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
                "ai_image": os.path.join(AI_SCENES_DIR, "clip2_s1.jpg"),
                "badge": "ปรัชญาหลัก • ศ.ดร.ชาญณรงค์ พรรุ่งโรจน์",
                "title": "ความพิการไม่ใช่ข้อจำกัด",
                "subtitle": "“ความพิการอาจสร้างข้อจำกัดทางกายภาพ แต่โอกาสต่างหาก คือสิ่งที่กำหนดขีดความสามารถของมนุษย์”",
                "senate_pill": "บทบาทวุฒิสภา: ขับเคลื่อนแนวคิดสากลเพื่อปลดล็อกศักยภาพคนพิการทุกประเภท",
                "voice": "ความพิการไม่ใช่ข้อจำกัด แต่โอกาสต่างหาก คือสิ่งที่กำหนดขีดความสามารถและคุณค่าของมนุษย์",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip2_s2.jpg"),
                "badge": "นวัตกรรมสังคม • 5 In 1 Genius",
                "title": "โมเดล “5 รวมเป็น 1 อัจฉริยะ”",
                "subtitle": "ริเริ่มโดย ศ.ดร.ชาญณรงค์ พรรุ่งโรจน์ สมาชิกวุฒิสภา การันตีด้วยรางวัลเกียรติยศ “ค่าของแผ่นดิน”",
                "senate_pill": "บทบาทวุฒิสภา: นำองค์ความรู้และนวัตกรรมศิลปะสู่การผลักดันเชิงนโยบายระดับชาติ",
                "voice": "โมเดล 5 รวมเป็น 1 อัจฉริยะ ริเริ่มโดย ศาสตราจารย์ ดร.ชาญณรงค์ พรรุ่งโรจน์ สมาชิกวุฒิสภา เจ้าของรางวัลค่าของแผ่นดิน",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip2_s3.jpg"),
                "badge": "การผสานพลัง • จุดแข็ง 5 ศักยภาพ",
                "title": "ปาก หู ตา ปัญญา แรงกาย และผู้ประสานงาน",
                "subtitle": "คนตาบอดสื่อสาร คนหูหนวกแต้มสี กายภาพวางกลยุทธ์ สติปัญญาทุ่มเทแรงกาย ผสานผู้ประสานงานเป็นหนึ่งเดียว",
                "senate_pill": "บทบาทวุฒิสภา: ส่งเสริมการมีส่วนร่วมของคนพิการและคนทั่วไปให้เติบโตเคียงข้างกัน",
                "voice": "ผสานพลัง ตาบอดเป็นปาก หูหนวกเป็นตา กายภาพเป็นปัญญา สติปัญญาเป็นแรงกาย ร่วมกับผู้ประสานงานอย่างเอื้ออาทร",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip2_s4.jpg"),
                "badge": "พลังนิติบัญญัติหนุนเสริม • ศักดิ์ศรีที่ยั่งยืน",
                "title": "หลอมรวมเป็นหนึ่งอัจฉริยะ ไร้ขีดจำกัด",
                "subtitle": "วุฒิสภาผลักดันนโยบายและสิทธิการเข้าถึงโอกาส ให้คนพิการต่อยอดงานศิลป์สู่อาชีพและพึ่งพาตนเองได้",
                "senate_pill": "บทบาทวุฒิสภา: คุ้มครองสิทธิ สร้างความเสมอภาค และยกระดับคุณภาพชีวิตอย่างยั่งยืน",
                "voice": "ด้วยแรงหนุนด้านนโยบายและสิทธิจากวุฒิสภา ช่วยให้คนพิการก้าวข้ามข้อจำกัด และสร้างอาชีพได้อย่างมีศักดิ์ศรี",
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
                "ai_image": os.path.join(AI_SCENES_DIR, "clip3_s1.jpg"),
                "badge": "วิสัยทัศน์นิติบัญญัติ • วุฒิสภาไทย",
                "title": "พลังนิติบัญญัติ สู่การพัฒนาที่ยั่งยืน",
                "subtitle": "บทบาท หน้าที่ และความมุ่งมั่นของวุฒิสภา ในการกลั่นกรองกฎหมายและขับเคลื่อนนโยบายเพื่อคนพิการ",
                "senate_pill": "เสาหลักนิติบัญญัติ: ยกระดับคุณภาพชีวิตคนพิการไทยอย่างเป็นระบบและยั่งยืน",
                "voice": "วุฒิสภาไทย มุ่งมั่นขับเคลื่อนพลังนิติบัญญัติ เพื่อยกระดับคุณภาพชีวิตคนพิการอย่างเป็นรูปธรรม",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip3_s2.jpg"),
                "badge": "เสาหลักที่ 1 • ด้านนโยบายและกฎหมาย",
                "title": "คุ้มครองสิทธิ สวัสดิการ และ Universal Design",
                "subtitle": "กลั่นกรองกฎหมาย ผลักดันความเสมอภาคในการเข้าถึงสิทธิ และสร้างมาตรฐานอารยสถาปัตย์ทั่วประเทศ",
                "senate_pill": "หน้าที่วุฒิสภา: ติดตามการบังคับใช้กฎหมายและขจัดอุปสรรคในการเข้าถึงสิทธิ",
                "voice": "เสาหลักที่ 1 กลั่นกรองกฎหมาย ผลักดันสิทธิ สวัสดิการ และมาตรฐาน อารยสถาปัตย์ ยูนิเวอร์แซล ดีไซน์",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip3_s3.jpg"),
                "badge": "เสาหลักที่ 2 & 3 • ศักยภาพและการสร้างงาน",
                "title": "พัฒนาศักยภาพผ่านศิลปะ สู่การสร้างอาชีพจริง",
                "subtitle": "บูรณาการภาครัฐ เอกชน และเครือข่ายศิลปิน ยกระดับผลงานสร้างสรรค์สู่ตลาด สร้างรายได้ที่มั่นคง",
                "senate_pill": "หน้าที่วุฒิสภา: เชื่อมโยงทุกภาคส่วนร่วมสร้างเศรษฐกิจสร้างสรรค์เพื่อคนพิการ",
                "voice": "เสาหลักที่ 2 และ 3 ส่งเสริมการใช้ศิลปะฟื้นฟูศักยภาพ พร้อมบูรณาการเครือข่ายสร้างงาน สร้างอาชีพที่มั่นคง",
            },
            {
                "ai_image": os.path.join(AI_SCENES_DIR, "clip3_s4.jpg"),
                "badge": "พันธกิจเพื่อสังคม • ไม่ทิ้งใครไว้ข้างหลัง",
                "title": "สังคมแห่งความเสมอภาค และโอกาสที่เท่าเทียม",
                "subtitle": "วุฒิสภาเคียงข้างคนพิการไทย ร่วมสร้างอนาคตที่ยั่งยืนและภาคภูมิใจไปด้วยกัน ในงาน 26-28 พ.ย. 2569",
                "senate_pill": "พันธกิจวุฒิสภา: ส่งเสริมการมีส่วนร่วมของทุกภาคส่วนเพื่อคุณภาพชีวิตที่ดีกว่า",
                "voice": "วุฒิสภา ร่วมสร้างสังคมแห่งความเสมอภาค ไม่ทิ้งใครไว้ข้างหลัง ผ่านพลังแห่งศิลปะและโอกาส",
            },
        ],
    },
]


def synthesize_voice(text, output_wav, rate=155):
    """Synthesize clean Thai voiceover using macOS Kanya voice."""
    temp_aiff = output_wav.replace(".wav", ".aiff")
    subprocess.run(["say", "-v", "Kanya", "-r", str(rate), text, "-o", temp_aiff], check=True)
    subprocess.run(
        [FFMPEG_BIN, "-y", "-i", temp_aiff, "-ar", "44100", "-ac", "2", output_wav],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    if os.path.exists(temp_aiff):
        os.remove(temp_aiff)

    dur_str = subprocess.check_output(
        [
            FFPROBE_BIN,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            output_wav,
        ]
    ).decode().strip()
    return float(dur_str)


def generate_ambient_music(duration, output_wav):
    """Synthesize a warm, dignified harmonic chord soundtrack."""
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
        mask = (t >= t_start) & (t < t_end)
        t_seg = t[mask] - t_start
        seg_len = len(t_seg)
        if seg_len == 0:
            continue

        seg_sig = np.zeros(seg_len)
        for f in chord:
            seg_sig += 0.14 * np.sin(2 * np.pi * f * t_seg)
            seg_sig += 0.04 * np.sin(2 * np.pi * (f * 2) * t_seg)

        attack = int(sample_rate * 0.8)
        decay = int(sample_rate * 0.8)
        env = np.ones(seg_len)
        if seg_len > attack:
            env[:attack] = np.linspace(0.15, 1.0, attack)
        if seg_len > decay:
            env[-decay:] = np.linspace(1.0, 0.25, decay)
        signal[mask] += seg_sig * env

    total_len = len(signal)
    fade_samples = min(int(sample_rate * 1.5), total_len // 4)
    signal[:fade_samples] *= np.linspace(0.0, 1.0, fade_samples)
    signal[-fade_samples:] *= np.linspace(1.0, 0.0, fade_samples)

    signal = signal * 0.20
    audio = (signal * 32767).astype(np.int16)

    with wave.open(output_wav, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())


def wrap_thai_text(text, font, max_width, draw):
    """Wrap Thai/English text safely without splitting Thai combining vowels."""
    text = unicodedata.normalize("NFC", text)
    words = text.split(" ")
    lines = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip() if current else word
        w = draw.textbbox((0, 0), candidate, font=font)[2]
        if w <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            # If a single Thai token is wider than max_width, split safely between base clusters
            if draw.textbbox((0, 0), word, font=font)[2] > max_width:
                chunk = ""
                for ch in word:
                    test_chunk = chunk + ch
                    if ch in THAI_NON_BREAKING_MARKS:
                        chunk = test_chunk
                        continue
                    if draw.textbbox((0, 0), test_chunk, font=font)[2] <= max_width:
                        chunk = test_chunk
                    else:
                        if chunk:
                            lines.append(chunk)
                        chunk = ch
                current = chunk
            else:
                current = word

    if current:
        lines.append(current)
    return lines


def fit_cover_rounded(img_path, target_w, target_h, radius=24):
    """Load an image, resize with center-crop cover fit (zero gray bars), and apply rounded corners."""
    src = Image.open(img_path).convert("RGBA")
    src_ratio = src.width / src.height
    dst_ratio = target_w / target_h

    if src_ratio > dst_ratio:
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)

    resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    cropped = resized.crop((left, top, left + target_w, top + target_h))

    mask = Image.new("L", (target_w, target_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([(0, 0), (target_w, target_h)], radius=radius, fill=255)
    cropped.putalpha(mask)
    return cropped


def create_scene_frame(scene_data, infographic_path, theme_color, chapter_label, scene_idx, total_scenes):
    """Compose a 1920x1080 V2 luxury broadcast frame."""
    W, H = 1920, 1080
    im = Image.new("RGBA", (W, H), color=(10, 15, 28, 255))

    # 1. Ambient Radial Glows
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_layer)
    gdraw.ellipse([(-250, -250), (850, 850)], fill=(*theme_color, 32))
    gdraw.ellipse([(W - 750, H - 750), (W + 250, H + 250)], fill=(*theme_color, 26))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(90))
    im = Image.alpha_composite(im, glow_layer)

    draw = ImageDraw.Draw(im)

    # 2. Top Navigation Bar
    draw.rectangle([(0, 0), (W, 74)], fill=(15, 23, 42, 235))
    draw.line([(0, 74), (W, 74)], fill=(51, 65, 85, 180), width=1)

    # Diamond icon + Header
    draw.polygon([(76, 37), (86, 27), (96, 37), (86, 47)], fill=theme_color)
    draw.text(
        (110, 22),
        f"SENATE OF THAILAND  ×  ART FOR ALL 2569   |   {chapter_label}",
        font=FONTS["badge"],
        fill=(241, 245, 249),
    )

    # Scene indicator & progress pills
    draw.text((W - 310, 23), f"ฉากที่ {scene_idx + 1} / {total_scenes}", font=FONTS["micro"], fill=(148, 163, 184))
    for i in range(total_scenes):
        px = W - 210 + (i * 34)
        pcolor = (*theme_color, 255) if i == scene_idx else (51, 65, 85, 255)
        draw.rounded_rectangle([(px, 32), (px + 26, 40)], radius=4, fill=pcolor)

    # 3. Left Panel: Bespoke AI Cinematic Scene (Full Cover Fit - Zero Empty Bars!)
    lx, ly, lw, lh = 72, 108, 860, 892
    draw.rounded_rectangle(
        [(lx - 2, ly - 2), (lx + lw + 2, ly + lh + 2)],
        radius=26,
        outline=(*theme_color, 180),
        width=2,
    )

    ai_img_path = scene_data.get("ai_image")
    if ai_img_path and os.path.exists(ai_img_path):
        scene_art = fit_cover_rounded(ai_img_path, lw, lh, radius=24)
        im.alpha_composite(scene_art, (lx, ly))

    # Bottom gradient scrim over AI artwork for crisp PiP & caption legibility
    scrim = Image.new("RGBA", (lw, 220), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scrim)
    for row in range(220):
        alpha = int((row / 220) ** 1.4 * 215)
        sdraw.line([(0, row), (lw, row)], fill=(10, 15, 28, alpha))
    # Mask bottom corners of scrim
    smask = Image.new("L", (lw, 220), 255)
    smdraw = ImageDraw.Draw(smask)
    smdraw.rounded_rectangle([(0, -40), (lw, 220)], radius=24, fill=255)
    scrim.putalpha(Image.composite(scrim.split()[3], Image.new("L", (lw, 220), 0), smask))
    im.alpha_composite(scrim, (lx, ly + lh - 220))

    draw = ImageDraw.Draw(im)

    # Top-left AI Cinematic Badge inside Left Panel
    draw.rounded_rectangle([(lx + 24, ly + 22), (lx + 345, ly + 58)], radius=18, fill=(10, 15, 28), outline=theme_color, width=1)
    draw.text((lx + 42, ly + 27), "◆  AI CINEMATIC VISUALIZATION", font=FONTS["micro"], fill=(248, 250, 252))

    # Bottom-left Caption inside Left Panel
    draw.text((lx + 28, ly + lh - 68), "วุฒิสภาไทย  ×  มูลนิธิศิลปะเพื่อมวลมนุษย์ (Art for All)", font=FONTS["micro"], fill=(241, 245, 249))
    draw.text((lx + 28, ly + lh - 42), "สื่อประชาสัมพันธ์โครงการระดับชาติ ประจำปี 2569", font=FONTS["micro"], fill=(203, 213, 225))

    # Bottom-right Official Infographic PiP Card inside Left Panel
    if os.path.exists(infographic_path):
        info_src = Image.open(infographic_path).convert("RGBA")
        pip_w = 185
        pip_h = int(pip_w * (info_src.height / info_src.width))
        if pip_h > 175:
            pip_h = 175
            pip_w = int(pip_h * (info_src.width / info_src.height))
        pip_resized = info_src.resize((pip_w, pip_h), Image.Resampling.LANCZOS)

        px = lx + lw - pip_w - 24
        py = ly + lh - pip_h - 22
        draw.rounded_rectangle(
            [(px - 8, py - 30), (px + pip_w + 8, py + pip_h + 8)],
            radius=14,
            fill=(15, 23, 42),
            outline=theme_color,
            width=2,
        )
        draw.text((px + 4, py - 25), "▸ อินโฟกราฟิกโครงการ", font=FONTS["micro"], fill=(248, 250, 252))
        im.alpha_composite(pip_resized, (px, py))

    # 4. Right Panel: Executive Typography & Senate Governance Panel
    rx, ry, rw, rh = 964, 108, 884, 892
    draw = ImageDraw.Draw(im)
    tinted_bg = tuple(int(15 * 0.85 + c * 0.15) for c in theme_color)
    tinted_box = tuple(int(15 * 0.78 + c * 0.22) for c in theme_color)

    draw.rounded_rectangle(
        [(rx, ry), (rx + rw, ry + rh)],
        radius=26,
        fill=(15, 23, 42),
        outline=(51, 65, 85),
        width=1,
    )

    # Top Badge Pill
    badge_text = f"◆  {scene_data['badge']}"
    bw = draw.textbbox((0, 0), badge_text, font=FONTS["badge"])[2] + 40
    draw.rounded_rectangle(
        [(rx + 48, ry + 48), (rx + 48 + bw, ry + 90)],
        radius=21,
        fill=tinted_bg,
        outline=theme_color,
        width=2,
    )
    draw.text((rx + 68, ry + 55), badge_text, font=FONTS["badge"], fill=theme_color)

    # Main Scene Title
    ty = ry + 118
    title_lines = wrap_thai_text(scene_data["title"], FONTS["bold"], rw - 96, draw)
    for tline in title_lines:
        draw.text((rx + 48, ty), tline, font=FONTS["bold"], fill=(255, 255, 255))
        ty += 60

    # Accent Divider Bar
    ty += 12
    draw.rounded_rectangle([(rx + 48, ty), (rx + 210, ty + 5)], radius=2, fill=theme_color)
    ty += 32

    # Narrative Subtitle
    sub_lines = wrap_thai_text(scene_data["subtitle"], FONTS["semibold"], rw - 96, draw)
    for sline in sub_lines:
        draw.text((rx + 48, ty), sline, font=FONTS["semibold"], fill=(226, 232, 240))
        ty += 46

    # Senate Governance Highlight Card (Requirement 3 explicitly highlighted in every clip!)
    senate_y = ty + 26
    senate_lines = wrap_thai_text(scene_data["senate_pill"], FONTS["pill"], rw - 140, draw)
    senate_h = max(76, 28 + len(senate_lines) * 32)
    draw.rounded_rectangle(
        [(rx + 48, senate_y), (rx + rw - 48, senate_y + senate_h)],
        radius=16,
        fill=tinted_box,
        outline=theme_color,
        width=1,
    )
    # Vector gold/theme accent bar on left inside Senate card
    draw.rounded_rectangle(
        [(rx + 62, senate_y + 16), (rx + 68, senate_y + senate_h - 16)],
        radius=3,
        fill=theme_color,
    )
    sy_text = senate_y + 14
    for sline in senate_lines:
        draw.text((rx + 84, sy_text), sline, font=FONTS["pill"], fill=(255, 255, 255))
        sy_text += 32

    # Bottom Narration Box
    vlines = wrap_thai_text(f"“{scene_data['voice']}”", FONTS["body"], rw - 136, draw)
    box_h = max(135, 68 + len(vlines) * 38)
    box_y = ry + rh - box_h - 68
    draw.rounded_rectangle(
        [(rx + 48, box_y), (rx + rw - 48, box_y + box_h)],
        radius=18,
        fill=(24, 33, 49),
        outline=theme_color,
        width=1,
    )
    draw.text((rx + 70, box_y + 18), "▸ บทบรรยายประกอบภาพ (AI Voiceover):", font=FONTS["micro"], fill=(148, 163, 184))
    vy = box_y + 48
    quote_color = (254, 240, 138) if theme_color[0] > 200 else (241, 245, 249)
    for vl in vlines:
        draw.text((rx + 70, vy), vl, font=FONTS["body"], fill=quote_color)
        vy += 38

    # Footer Metadata
    foot_text = "◆ กำหนดการจัดงาน: 26 - 28 พฤศจิกายน 2569  |  ณ อาคารรัฐสภา (สัปปายะสภาสถาน)"
    draw.text((rx + 48, ry + rh - 44), foot_text, font=FONTS["footer"], fill=(148, 163, 184))

    return im.convert("RGB")


def build_single_clip(clip_data):
    """Build a single 1080p MP4 clip with 4 scenes, crossfades, narration, and music."""
    clip_id = clip_data["id"]
    print("\n=======================================================")
    print(f"🎬 กำลังผลิต V2 Master: {clip_data['title']}")
    print("=======================================================")

    clip_work = os.path.join(TEMP_WORK, clip_id)
    os.makedirs(clip_work, exist_ok=True)

    scene_videos = []
    scene_durations = []
    total_scenes = len(clip_data["scenes"])

    for s_idx, scene in enumerate(clip_data["scenes"]):
        scene_wav = os.path.join(clip_work, f"scene_{s_idx}_voice.wav")
        dur = synthesize_voice(scene["voice"], scene_wav, rate=155)
        pad_dur = max(dur + 1.2, 7.0)
        scene_durations.append(pad_dur)

        slide_img = create_scene_frame(
            scene,
            clip_data["infographic"],
            clip_data["theme_color"],
            clip_data["chapter"],
            s_idx,
            total_scenes,
        )
        slide_png = os.path.join(clip_work, f"scene_{s_idx}.png")
        slide_img.save(slide_png, "PNG")

        padded_wav = os.path.join(clip_work, f"scene_{s_idx}_padded.wav")
        subprocess.run(
            [
                FFMPEG_BIN,
                "-y",
                "-i",
                scene_wav,
                "-af",
                f"apad=whole_dur={pad_dur:.2f}",
                "-ar",
                "44100",
                "-ac",
                "2",
                padded_wav,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        scene_mp4 = os.path.join(clip_work, f"scene_{s_idx}.mp4")
        total_frames = int(pad_dur * 30)
        zoom_filter = (
            f"zoompan=z='min(zoom+0.00035,1.04)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={total_frames}:s=1920x1080:fps=30"
        )
        subprocess.run(
            [
                FFMPEG_BIN,
                "-y",
                "-loop",
                "1",
                "-i",
                slide_png,
                "-i",
                padded_wav,
                "-vf",
                zoom_filter,
                "-c:v",
                "libx264",
                "-tune",
                "stillimage",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-t",
                f"{pad_dur:.2f}",
                scene_mp4,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        scene_videos.append(scene_mp4)
        print(f"  ✓ ฉากที่ {s_idx + 1}/{total_scenes}: {scene['badge']} ({pad_dur:.1f} วินาที)")

    # Crossfade scenes smoothly (0.5s overlap)
    xfade_dur = 0.5
    raw_joined_mp4 = os.path.join(clip_work, "raw_joined.mp4")

    inputs = []
    for sv in scene_videos:
        inputs.extend(["-i", sv])

    filter_parts = []
    current_v = "[0:v]"
    current_a = "[0:a]"
    cumulative_offset = scene_durations[0] - xfade_dur

    for i in range(1, total_scenes):
        next_v = f"[{i}:v]"
        next_a = f"[{i}:a]"
        out_v = f"[v{i}]" if i < total_scenes - 1 else "[outv]"
        out_a = f"[a{i}]" if i < total_scenes - 1 else "[outa]"

        filter_parts.append(
            f"{current_v}{next_v}xfade=transition=fade:duration={xfade_dur}:offset={cumulative_offset:.2f}{out_v}"
        )
        filter_parts.append(f"{current_a}{next_a}acrossfade=d={xfade_dur}{out_a}")

        current_v = out_v
        current_a = out_a
        if i < total_scenes - 1:
            cumulative_offset += scene_durations[i] - xfade_dur

    total_clip_duration = sum(scene_durations) - xfade_dur * (total_scenes - 1)
    subprocess.run(
        [
            FFMPEG_BIN,
            "-y",
            *inputs,
            "-filter_complex",
            ";".join(filter_parts),
            "-map",
            "[outv]",
            "-map",
            "[outa]",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            raw_joined_mp4,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    # Generate ambient music & mix
    music_wav = os.path.join(clip_work, "ambient_bed.wav")
    generate_ambient_music(total_clip_duration + 0.5, music_wav)

    final_output = clip_data["output_file"]
    subprocess.run(
        [
            FFMPEG_BIN,
            "-y",
            "-i",
            raw_joined_mp4,
            "-i",
            music_wav,
            "-filter_complex",
            "[0:a]volume=1.0[voice];[1:a]volume=0.22[music];[voice][music]amix=inputs=2:duration=first[aout]",
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
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    fsize_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"  🎉 เรนเดอร์สำเร็จ: {os.path.basename(final_output)} ({fsize_mb:.2f} MB, ความยาว {total_clip_duration:.1f} วินาที)")


def build_master_full_presentation():
    """Concatenate all 3 V2 clips into the seamless Master Presentation."""
    print("\n=======================================================")
    print("🌟 กำลังประกอบร่าง: คลิปฉบับเต็มรวม 3 ตอน (V2 Master Presentation)")
    print("=======================================================")
    c1 = os.path.join(VIDEOS_DIR, "clip_1_art_for_all_expo.mp4")
    c2 = os.path.join(VIDEOS_DIR, "clip_2_five_in_one_genius.mp4")
    c3 = os.path.join(VIDEOS_DIR, "clip_3_senate_legislative_power.mp4")
    master_out = os.path.join(VIDEOS_DIR, "art_for_all_senate_full_presentation.mp4")

    subprocess.run(
        [
            FFMPEG_BIN,
            "-y",
            "-i",
            c1,
            "-i",
            c2,
            "-i",
            c3,
            "-filter_complex",
            "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]",
            "-map",
            "[outv]",
            "-map",
            "[outa]",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            master_out,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    fsize_mb = os.path.getsize(master_out) / (1024 * 1024)
    print(f"  🎉 ฉบับเต็มเสร็จสมบูรณ์: {os.path.basename(master_out)} ({fsize_mb:.2f} MB)")


def main():
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(TEMP_WORK, exist_ok=True)

    for clip in CLIPS_DATA:
        build_single_clip(clip)

    build_master_full_presentation()
    print("\n✨ อัปเกรดและผลิตชุดวิดีโอ V2 Master Edition ทั้งหมดเสร็จสมบูรณ์ 100% ✨")


if __name__ == "__main__":
    main()
