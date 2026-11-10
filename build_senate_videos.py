#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Senate & Art for All Video Production Pipeline
Produces 3 high-class, broadcast-ready 1080p MP4 videos with:
1. Native Apple Thai Speech Narration (say -v Kanya)
2. Ambient cinematic harmonic soundtrack (synthesized via numpy/wave)
3. Luxury typography & glassmorphic graphics (PIL with SukhumvitSet)
4. Smooth Ken Burns motion and H.264 MP4 encoding (ffmpeg)
"""

import os
import sys
import math
import wave
import shutil
import tempfile
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = "/Users/jake/Desktop/สว"
ASSETS_IMG = os.path.join(BASE_DIR, "assets", "images")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
TEMP_WORK = "/tmp/senate_video_work"

FONTS = {
    "bold": ImageFont.truetype("/System/Library/Fonts/Supplemental/SukhumvitSet.ttc", 46, index=5),
    "semibold": ImageFont.truetype("/System/Library/Fonts/Supplemental/SukhumvitSet.ttc", 36, index=4),
    "badge": ImageFont.truetype("/System/Library/Fonts/Supplemental/SukhumvitSet.ttc", 22, index=4),
    "body": ImageFont.truetype("/System/Library/Fonts/Supplemental/SukhumvitSet.ttc", 28, index=3),
    "footer": ImageFont.truetype("/System/Library/Fonts/Supplemental/SukhumvitSet.ttc", 20, index=2),
}

CLIPS_DATA = [
    {
        "id": "clip_1_art_for_all_expo",
        "title": "คลิปที่ 1: Art for All 2569: สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ",
        "output_file": os.path.join(VIDEOS_DIR, "clip_1_art_for_all_expo.mp4"),
        "infographic": os.path.join(ASSETS_IMG, "art-for-all-opportunity.png"),
        "theme_color": (245, 158, 11),  # Amber
        "scenes": [
            {
                "badge": "โครงการระดับชาติ • วุฒิสภาไทย",
                "title": "Art for All: สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ",
                "subtitle": "ขอเชิญร่วมสัมผัสพลังแห่งการสร้างสรรค์ ก้าวข้ามขีดจำกัดด้วยศิลปะ เพื่อพัฒนาศักยภาพคนพิการสู่ระดับสากล",
                "voice": "ขอเชิญร่วมสัมผัสพลังแห่งการสร้างสรรค์ ในโครงการ Art for All: สร้างศิลป์ สร้างสรรค์ สร้างอาชีพ",
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
        "title": "คลิปที่ 2: มหัศจรรย์ 5 รวมเป็น 1 อัจฉริยะ: พลังแห่งการก้าวข้ามข้อจำกัด",
        "output_file": os.path.join(VIDEOS_DIR, "clip_2_five_in_one_genius.mp4"),
        "infographic": os.path.join(ASSETS_IMG, "channarong-art-for-all.png"),
        "theme_color": (168, 85, 247),  # Purple
        "scenes": [
            {
                "badge": "ปรัชญาโครงการ • ศ.ดร.ชาญณรงค์ พรรุ่งโรจน์",
                "title": "ความพิการไม่ใช่ข้อจำกัด",
                "subtitle": "\"ความพิการอาจสร้างข้อจำกัดทางกายภาพ แต่โอกาสต่างหาก คือสิ่งที่กำหนดขีดความสามารถของมนุษย์\"",
                "voice": "ความพิการไม่ใช่ข้อจำกัด แต่โอกาสต่างหาก คือสิ่งที่กำหนดขีดความสามารถ",
            },
            {
                "badge": "โมเดลนวัตกรรมสังคม • 5 In 1 Genius",
                "title": "โมเดล '5 รวมเป็น 1 อัจฉริยะ'",
                "subtitle": "ริเริ่มตั้งแต่ พ.ศ. 2540 และได้รับรางวัลเกียรติยศระดับชาติ 'ค่าของแผ่นดิน' จากสำนักนายกรัฐมนตรี",
                "voice": "โมเดล '5 รวมเป็น 1 อัจฉริยะ' ริเริ่มโดย ศาสตราจารย์ ดร.ชาญณรงค์ พรรุ่งโรจน์ สมาชิกวุฒิสภา",
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

def synthesize_voice(text, output_wav, rate=155):
    """Synthesize voice using Mac's native Kanya voice."""
    temp_aiff = output_wav.replace(".wav", ".aiff")
    cmd = ["say", "-v", "Kanya", "-r", str(rate), text, "-o", temp_aiff]
    subprocess.run(cmd, check=True)
    conv_cmd = ["/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_aiff, "-ar", "44100", "-ac", "2", output_wav]
    subprocess.run(conv_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(temp_aiff):
        os.remove(temp_aiff)
    # Get duration
    ffprobe_cmd = [
        "/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", output_wav
    ]
    dur = float(subprocess.check_output(ffprobe_cmd).decode().strip())
    return dur

def generate_ambient_music(duration, output_wav):
    """Synthesize a warm cinematic ambient chord progression."""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Chord chords progression: Cmaj7 -> Am9 -> Fmaj7 -> Gsus4
    # Frequencies
    chords = [
        [261.63, 329.63, 392.00, 493.88],       # Cmaj7
        [220.00, 261.63, 329.63, 392.00, 493.88],# Am9
        [174.61, 261.63, 329.63, 392.00],       # Fmaj7
        [196.00, 261.63, 293.66, 392.00],       # Gsus4
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
            # Fundamental + soft octave
            segment_sig += 0.15 * np.sin(2 * np.pi * f * t_segment)
            segment_sig += 0.05 * np.sin(2 * np.pi * (f * 2) * t_segment)
            
        # Smooth envelope
        attack = int(sample_rate * 0.8)
        decay = int(sample_rate * 0.8)
        env = np.ones(segment_len)
        if segment_len > attack:
            env[:attack] = np.linspace(0.1, 1.0, attack)
        if segment_len > decay:
            env[-decay:] = np.linspace(1.0, 0.2, decay)
        segment_sig = segment_sig * env
        signal[idx_mask] += segment_sig
        
    # Master gentle fade in / fade out
    total_len = len(signal)
    master_fade = min(int(sample_rate * 1.5), total_len // 4)
    signal[:master_fade] *= np.linspace(0.0, 1.0, master_fade)
    signal[-master_fade:] *= np.linspace(1.0, 0.0, master_fade)
    
    # Volume scaling (subtle bed)
    signal = signal * 0.22
    audio = (signal * 32767).astype(np.int16)
    
    with wave.open(output_wav, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

def wrap_text(text, font, max_width, draw):
    """Helper to wrap Thai text into multiple lines."""
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip() if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def create_scene_frame(scene_data, infographic_path, theme_color, scene_idx, total_scenes):
    """Draw a 1920x1080 luxury presentation slide."""
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)
    
    # 1. Subtle Background Radial Glow
    glow_color = (*theme_color, 45)
    glow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_overlay)
    gdraw.ellipse([(-200, -200), (800, 800)], fill=(*theme_color, 25))
    gdraw.ellipse([(W - 700, H - 700), (W + 200, H + 200)], fill=(*theme_color, 20))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(80))
    im.paste(glow_overlay, (0, 0), glow_overlay)
    
    # 2. Top Header Navigation Bar
    draw.rectangle([(0, 0), (W, 72)], fill=(15, 23, 42, 220))
    draw.line([(0, 72), (W, 72)], fill=(30, 41, 59), width=1)
    
    # Top badge
    draw.text((80, 24), "🏛️  SENATE OF THAILAND  ×  ART FOR ALL 2569", font=FONTS["badge"], fill=(226, 232, 240))
    
    # Progress pills
    for i in range(total_scenes):
        px = W - 220 + (i * 32)
        pcolor = theme_color if i == scene_idx else (51, 65, 85)
        draw.rounded_rectangle([(px, 32), (px + 24, 38)], radius=3, fill=pcolor)
        
    # 3. Left Panel: High-Res Infographic in Luxury Glass Frame
    card_x, card_y, card_w, card_h = 80, 120, 780, 860
    # Outer Card glow
    draw.rounded_rectangle([(card_x - 2, card_y - 2), (card_x + card_w + 2, card_y + card_h + 2)], radius=24, outline=(*theme_color, 120), width=2)
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=22, fill=(15, 23, 42))
    
    # Load and fit infographic image
    if os.path.exists(infographic_path):
        info_img = Image.open(infographic_path).convert("RGB")
        info_ratio = info_img.width / info_img.height
        target_w = card_w - 24
        target_h = card_h - 24
        target_ratio = target_w / target_h
        
        if info_ratio > target_ratio:
            nw = target_w
            nh = int(nw / info_ratio)
        else:
            nh = target_h
            nw = int(nh * info_ratio)
            
        resized_info = info_img.resize((nw, nh), Image.Resampling.LANCZOS)
        px = card_x + 12 + (target_w - nw) // 2
        py = card_y + 12 + (target_h - nh) // 2
        im.paste(resized_info, (px, py))
        
    # 4. Right Panel: Content Card & Typography
    rx, ry, rw, rh = 900, 120, 940, 860
    
    # Right Glass Card
    draw.rounded_rectangle([(rx, ry), (rx + rw, ry + rh)], radius=24, fill=(17, 24, 39, 230), outline=(51, 65, 85), width=1)
    
    # Badge Pill inside right card
    badge_text = f"✦ {scene_data['badge']}"
    bbox = draw.textbbox((0, 0), badge_text, font=FONTS["badge"])
    bw = bbox[2] - bbox[0] + 32
    draw.rounded_rectangle([(rx + 50, ry + 60), (rx + 50 + bw, ry + 102)], radius=20, fill=(*theme_color, 35), outline=theme_color, width=1)
    draw.text((rx + 66, ry + 70), badge_text, font=FONTS["badge"], fill=theme_color)
    
    # Title
    title_lines = wrap_text(scene_data["title"], FONTS["bold"], rw - 100, draw)
    ty = ry + 130
    for tline in title_lines:
        draw.text((rx + 50, ty), tline, font=FONTS["bold"], fill=(255, 255, 255))
        ty += 64
        
    # Elegant Accent Line
    ty += 15
    draw.line([(rx + 50, ty), (rx + 250, ty)], fill=theme_color, width=3)
    ty += 35
    
    # Subtitle / Narrative
    sub_lines = wrap_text(scene_data["subtitle"], FONTS["semibold"], rw - 110, draw)
    for sline in sub_lines:
        draw.text((rx + 50, ty), sline, font=FONTS["semibold"], fill=(226, 232, 240))
        ty += 52
        
    # Spoken Highlight Box (The actual narration being delivered)
    box_y = ry + rh - 220
    draw.rounded_rectangle([(rx + 40, box_y), (rx + rw - 40, box_y + 150)], radius=18, fill=(30, 41, 59, 180), outline=(*theme_color, 80), width=1)
    draw.text((rx + 65, box_y + 20), "🎙️ สาระสำคัญจากบทบรรยาย:", font=FONTS["badge"], fill=(148, 163, 184))
    
    vlines = wrap_text(f"\"{scene_data['voice']}\"", FONTS["body"], rw - 130, draw)
    vy = box_y + 55
    for vl in vlines:
        draw.text((rx + 65, vy), vl, font=FONTS["body"], fill=(254, 240, 138) if theme_color[0] > 200 else (241, 245, 249))
        vy += 40
        
    # Bottom Card Footer
    foot_text = "📅 26 - 28 พฤศจิกายน 2569  |  ณ อาคารรัฐสภา (สัปปายะสภาสถาน)"
    draw.text((rx + 50, ry + rh - 45), foot_text, font=FONTS["footer"], fill=(100, 116, 139))
    
    return im

def build_single_clip(clip_data):
    """Build an entire video clip with 4 scenes, synchronized voice, ambient music and Ken Burns pan."""
    clip_id = clip_data["id"]
    print(f"\n=======================================================")
    print(f"🎬 กำลังผลิต: {clip_data['title']}")
    print(f"=======================================================")
    
    clip_work = os.path.join(TEMP_WORK, clip_id)
    os.makedirs(clip_work, exist_ok=True)
    
    scene_videos = []
    total_scenes = len(clip_data["scenes"])
    
    total_clip_duration = 0.0
    scene_durations = []
    
    # Step 1: Generate voice audio and frames for each scene
    for s_idx, scene in enumerate(clip_data["scenes"]):
        scene_wav = os.path.join(clip_work, f"scene_{s_idx}_voice.wav")
        dur = synthesize_voice(scene["voice"], scene_wav, rate=155)
        # Pad duration slightly for natural breathing pause (min 6.5s)
        pad_dur = max(dur + 1.2, 6.5)
        scene_durations.append(pad_dur)
        total_clip_duration += pad_dur
        
        # Create slide image
        slide_img = create_scene_frame(scene, clip_data["infographic"], clip_data["theme_color"], s_idx, total_scenes)
        slide_png = os.path.join(clip_work, f"scene_{s_idx}.png")
        slide_img.save(slide_png, "PNG")
        
        # Padded voice audio
        padded_wav = os.path.join(clip_work, f"scene_{s_idx}_padded.wav")
        pad_cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y", "-i", scene_wav,
            "-af", f"apad=whole_dur={pad_dur:.2f}",
            "-ar", "44100", "-ac", "2", padded_wav
        ]
        subprocess.run(pad_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Create smooth video with Ken Burns zoom effect
        scene_mp4 = os.path.join(clip_work, f"scene_{s_idx}.mp4")
        # zoompan slowly from 1.0 to 1.03 over pad_dur seconds at 30 fps
        total_frames = int(pad_dur * 30)
        zoom_filter = f"zoompan=z='min(zoom+0.0003,1.03)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1920x1080:fps=30"
        
        vid_cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y",
            "-loop", "1", "-i", slide_png,
            "-i", padded_wav,
            "-vf", zoom_filter,
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{pad_dur:.2f}",
            scene_mp4
        ]
        subprocess.run(vid_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        scene_videos.append(scene_mp4)
        print(f"  ✓ ฉากที่ {s_idx + 1}/{total_scenes}: {scene['badge']} ({pad_dur:.1f} วินาที)")
        
    # Step 2: Generate Ambient Music for entire duration
    music_wav = os.path.join(clip_work, "ambient_bed.wav")
    generate_ambient_music(total_clip_duration, music_wav)
    
    # Step 3: Concatenate scenes
    concat_txt = os.path.join(clip_work, "concat_list.txt")
    with open(concat_txt, "w") as f:
        for sv in scene_videos:
            f.write(f"file '{sv}'\n")
            
    raw_joined_mp4 = os.path.join(clip_work, "raw_joined.mp4")
    concat_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", raw_joined_mp4
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Step 4: Mix Narration Audio with Ambient Music
    final_output = clip_data["output_file"]
    mix_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", raw_joined_mp4,
        "-i", music_wav,
        "-filter_complex",
        "[0:a]volume=1.0[voice];[1:a]volume=0.25[music];[voice][music]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        final_output
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Measure file size
    fsize_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"  🎉 เรนเดอร์สำเร็จ: {os.path.basename(final_output)} ({fsize_mb:.2f} MB, ความยาว {total_clip_duration:.1f} วินาที)")

def main():
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(TEMP_WORK, exist_ok=True)
    
    for clip in CLIPS_DATA:
        build_single_clip(clip)
        
    print("\n✨ ผลิตคลิปวิดีโอระดับผู้บริหารทั้ง 3 คลิปเสร็จสมบูรณ์ 100% ✨")

if __name__ == "__main__":
    main()
