# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "torch",
#     "diffusers @ git+https://github.com/huggingface/diffusers",
#     "transformers",
#     "accelerate",
#     "safetensors",
#     "sentencepiece",
#     "huggingface_hub",
#     "imageio-ffmpeg",
#     "pillow",
#     "numpy",
# ]
# ///
#
#  استودیو ویدیو LTX 2.5 — برای اجرا روی molab (marimo)
#  ---------------------------------------------------
#  1) فایل را در molab.marimo.io باز کنید (New notebook → Upload)
#  2) از دکمه‌ی مشخصات نوت‌بوک در بالا، GPU را روشن کنید
#  3) دکمه‌ی Run all را بزنید و از تب‌ها استفاده کنید

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="full", app_title="LTX 2.5 Studio")


@app.cell
def _():
    import marimo as mo
    import os, gc, json, time, random, shutil, subprocess, wave, inspect, traceback
    from pathlib import Path
    import numpy as np
    from PIL import Image
    return (
        Image, Path, gc, inspect, json, mo, np, os, random, shutil,
        subprocess, time, traceback, wave,
    )


@app.cell
def _():
    # ───────────── ۱۰ سبک اصلی (دراپ‌داون بالای صفحه) ─────────────
    STYLES = {
        "🎬 فیلم سینمایی": (
            "Cinematic feature film, shot on 35mm anamorphic lens, dramatic motivated lighting, "
            "shallow depth of field, rich color grading, subtle film grain",
            "cartoon, anime, illustration, flat lighting, amateur footage",
        ),
        "📱 ویدیو طبیعی / واقعی": (
            "Natural realistic video, handheld modern camera, natural daylight, true-to-life colors, "
            "authentic everyday realism",
            "cartoon, anime, illustration, stylized, cgi look",
        ),
        "🎥 لایو اکشن": (
            "Live-action film footage, real actors, practical sets, professional cinema camera, "
            "realistic skin and fabric textures, natural motion",
            "cartoon, anime, 3d render, illustration, plastic skin",
        ),
        "🖍 کارتون": (
            "2D cartoon style, bold clean outlines, flat vibrant colors, expressive exaggerated "
            "characters, classic TV cartoon animation",
            "photorealistic, live action, 3d render, film grain",
        ),
        "🧸 انیمیشن سه‌بعدی": (
            "High-quality 3D animated feature film style, stylized characters, soft global "
            "illumination, detailed textures, family animated movie look",
            "photorealistic, live action, 2d flat, anime",
        ),
        "🌸 انیمه": (
            "Japanese anime style, cel-shaded characters, detailed hand-painted backgrounds, "
            "expressive eyes, dynamic anime cinematography",
            "photorealistic, live action, 3d render, western cartoon",
        ),
        "📽 مستند": (
            "Documentary footage, observational camera, natural available light, authentic "
            "details, slightly handheld framing",
            "cartoon, anime, stylized, fantasy, cgi",
        ),
        "🕯 ترسناک / تاریک": (
            "Dark horror film style, low-key lighting, deep shadows, desaturated cold tones, "
            "eerie atmosphere, drifting fog",
            "bright, cheerful, saturated colors, cartoon",
        ),
        "🐉 فانتزی حماسی": (
            "Epic fantasy film style, grand scale, volumetric god rays, magical atmosphere, "
            "rich saturated colors, sweeping cinematography",
            "modern city, mundane, flat lighting, low budget",
        ),
        "🧱 استاپ‌موشن خمیری": (
            "Stop-motion claymation style, handcrafted clay characters, miniature sets, tactile "
            "fingerprint textures, charming handmade look",
            "photorealistic, live action, smooth cgi, anime",
        ),
    }

    # ───────────── نحوه‌ی صحبت (دراپ‌داون کاراکتر و شات) ─────────────
    SPEECH = {
        "معمولی": "in a natural conversational tone",
        "آرام": "calmly and softly",
        "نجوا / زمزمه": "in a quiet whisper",
        "خشن / تهدیدآمیز": "harshly and aggressively, in a threatening low voice",
        "فریاد": "shouting loudly at the top of their lungs",
        "عصبانی": "angrily, through gritted teeth",
        "غمگین": "sadly, with a trembling voice",
        "گریان": "while crying, voice breaking",
        "شاد": "happily and cheerfully",
        "هیجان‌زده": "excitedly, speaking fast",
        "ترسیده": "fearfully, breathless and shaky",
        "مرموز": "mysteriously, slow and low",
        "طعنه‌آمیز": "sarcastically",
        "فرمان‌دهنده": "with a commanding, authoritative voice",
        "خسته": "wearily, tired and slow",
        "مهربان / عاشقانه": "tenderly, warm and gentle",
    }

    LANGS = {
        "انگلیسی (بهترین نتیجه)": "English",
        "فارسی": "Persian (Farsi)",
        "فرانسوی": "French",
        "عربی": "Arabic",
        "ترکی": "Turkish",
    }

    CAMERA = {
        "ثابت": "Static locked-off camera.",
        "زوم آرام به داخل": "The camera slowly pushes in.",
        "عقب‌کشیدن دوربین": "The camera slowly pulls back.",
        "پن به چپ": "The camera pans slowly to the left.",
        "پن به راست": "The camera pans slowly to the right.",
        "تعقیب سوژه (تراکینگ)": "The camera tracks alongside the subject.",
        "دوربین روی دست": "Handheld camera with subtle natural shake.",
        "چرخش دور سوژه": "The camera orbits slowly around the subject.",
        "کرین رو به بالا": "The camera cranes up to reveal the scene.",
        "نمای نزدیک صورت": "Close-up shot on the face.",
        "نمای باز": "Wide shot showing the whole environment.",
        "نمای اول‌شخص (POV)": "First-person point-of-view shot.",
        "پهپاد هوایی": "Aerial drone shot gliding over the scene.",
    }

    DURATIONS = {"۵ ثانیه": 121, "۷ ثانیه": 169, "۱۰ ثانیه": 241}  # 24fps, frames % 8 == 1
    FPS = 24

    # اندازه‌ی ساخت (ارتفاع، عرض) — باید بر ۳۲ بخش‌پذیر باشد
    GEN_720 = {"16:9 افقی": (736, 1280), "9:16 عمودی": (1280, 736), "1:1 مربع": (736, 736)}
    GEN_1080_STAGE1 = {"16:9 افقی": (544, 960), "9:16 عمودی": (960, 544), "1:1 مربع": (544, 544)}
    FINAL = {
        "1080p (1920×1080)": {"16:9 افقی": (1080, 1920), "9:16 عمودی": (1920, 1080), "1:1 مربع": (1080, 1080)},
        "720p (1280×720)": {"16:9 افقی": (720, 1280), "9:16 عمودی": (1280, 720), "1:1 مربع": (720, 720)},
    }
    IMG_SIZE = {"16:9 افقی": (1024, 1792), "9:16 عمودی": (1792, 1024), "1:1 مربع": (1280, 1280)}

    IMAGE_MODELS = {
        "Z-Image Turbo (سریع)": ("Tongyi-MAI/Z-Image-Turbo", 9, 0.0),
        "Qwen-Image (کیفیت بالا، کندتر)": ("Qwen/Qwen-Image", 40, 4.0),
    }
    LTX_ID = "Lightricks/LTX-2.5-Diffusers"

    CONTINUITY = (
        "The shot continues seamlessly from the opening frame: same characters, same faces, "
        "same outfits, same location, same lighting and color grade."
    )
    BASE_NEGATIVE = (
        "text, subtitles, watermark, logo, blurry, low quality, distorted face, deformed hands, "
        "extra limbs, flicker, jitter, scene cut, morphing"
    )
    return (
        BASE_NEGATIVE, CAMERA, CONTINUITY, DURATIONS, FINAL, FPS,
        GEN_1080_STAGE1, GEN_720, IMAGE_MODELS, IMG_SIZE, LANGS, LTX_ID,
        SPEECH, STYLES,
    )


@app.cell
def _(Path, json):
    OUT = Path("ltx_studio_output")
    for _d in ("images", "characters", "shots", "frames", "final"):
        (OUT / _d).mkdir(parents=True, exist_ok=True)
    PROJECT_FILE = OUT / "project.json"

    def load_project():
        try:
            _p = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
        except Exception:
            _p = {}
        _imgs = [i for i in _p.get("images", []) if Path(i["path"]).exists()]
        _chars = {k: v for k, v in _p.get("chars", {}).items() if Path(v["image"]).exists()}
        _shots = [s for s in _p.get("shots", []) if Path(s["video"]).exists()]
        return _imgs, _chars, _shots

    def save_project(images, chars, shots):
        PROJECT_FILE.write_text(
            json.dumps({"images": images, "chars": chars, "shots": shots}, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )

    def rtl(html):
        import marimo as _mo
        return _mo.Html(f'<div dir="rtl" style="text-align:right;line-height:1.9">{html}</div>')
    return OUT, load_project, rtl, save_project


@app.cell
def _(load_project, mo):
    _i, _c, _s = load_project()
    get_images, set_images = mo.state(_i)
    get_chars, set_chars = mo.state(_c)
    get_shots, set_shots = mo.state(_s)
    get_final, set_final = mo.state(None)
    get_log, set_log = mo.state("")
    return (
        get_chars, get_final, get_images, get_log, get_shots, set_chars,
        set_final, set_images, set_log, set_shots,
    )


@app.cell
def _(FPS, GEN_1080_STAGE1, GEN_720, Image, LTX_ID, gc, inspect, np, shutil, subprocess, wave):
    import torch

    def _ffmpeg():
        _f = shutil.which("ffmpeg")
        if _f:
            return _f
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()

    def fit_image(img, h, w):
        """برش وسط + تغییر اندازه به ابعاد دقیق ساخت"""
        img = img.convert("RGB")
        _sw, _sh = img.size
        _scale = max(w / _sw, h / _sh)
        img = img.resize((max(w, round(_sw * _scale)), max(h, round(_sh * _scale))), Image.LANCZOS)
        _l = (img.width - w) // 2
        _t = (img.height - h) // 2
        return img.crop((_l, _t, _l + w, _t + h))

    def _to_frames(v):
        if isinstance(v, (list, tuple)):
            v = v[0]
            if isinstance(v, (list, tuple)) and v and isinstance(v[0], Image.Image):
                return np.stack([np.asarray(f.convert("RGB")) for f in v])
        if isinstance(v, Image.Image):
            return np.asarray(v.convert("RGB"))[None]
        if hasattr(v, "detach"):
            v = v.detach().float().cpu().numpy()
        v = np.asarray(v)
        if v.ndim == 5:
            v = v[0]
        if v.ndim == 4 and v.shape[1] in (1, 3) and v.shape[-1] not in (1, 3):
            v = v.transpose(0, 2, 3, 1)
        if v.dtype != np.uint8:
            v = (np.clip(v, 0, 1) * 255).round().astype(np.uint8)
        return v

    def _to_audio(a):
        if a is None:
            return None
        if isinstance(a, (list, tuple)):
            a = a[0]
        if hasattr(a, "detach"):
            a = a.detach().float().cpu().numpy()
        a = np.asarray(a, dtype=np.float32)
        if a.ndim == 3:
            a = a[0]
        if a.ndim == 1:
            a = a[None]
        if a.shape[0] > a.shape[1]:
            a = a.T
        return a  # (channels, samples)

    def write_wav(path, audio, sr, n_seconds):
        if audio is None:
            audio = np.zeros((1, int(sr * n_seconds)), dtype=np.float32)
        _pcm = (np.clip(audio, -1, 1).T * 32767).astype(np.int16)
        with wave.open(str(path), "wb") as _w:
            _w.setnchannels(audio.shape[0])
            _w.setsampwidth(2)
            _w.setframerate(int(sr))
            _w.writeframes(_pcm.tobytes())

    def encode_mp4(frames, audio, sr, out_path, final_hw):
        _h, _w = frames.shape[1:3]
        _fh, _fw = final_hw
        _wav = str(out_path) + ".wav"
        write_wav(_wav, audio, sr, len(frames) / FPS)
        _cmd = [
            _ffmpeg(), "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{_w}x{_h}", "-r", str(FPS), "-i", "-",
            "-i", _wav,
            "-vf", f"scale={_fw}:{_fh}:force_original_aspect_ratio=increase:flags=lanczos,crop={_fw}:{_fh},setsar=1",
            "-af", "apad",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out_path),
        ]
        _r = subprocess.run(_cmd, input=frames.tobytes(), capture_output=True)
        if _r.returncode != 0:
            raise RuntimeError("ffmpeg: " + _r.stderr.decode(errors="ignore")[-800:])
        return out_path

    class Engine:
        """یک مدل در هر لحظه روی GPU نگه داشته می‌شود تا حافظه پر نشود"""

        def __init__(self):
            self.kind = None
            self.pipe = None
            self.t2v = None
            self.up = None
            self.image_id = None
            self.distilled = False
            self.notes = []

        def free(self):
            self.pipe = self.t2v = self.up = None
            self.kind = self.image_id = None
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        @staticmethod
        def _load(cls, mid, **kw):
            try:
                return cls.from_pretrained(mid, torch_dtype=torch.bfloat16, device_map="cuda", **kw)
            except Exception:
                gc.collect()
                return cls.from_pretrained(mid, torch_dtype=torch.bfloat16, **kw).to("cuda")

        # ─────────── مدل تصویر ───────────
        def image(self, model_id, steps, cfg, prompt, h, w, seed):
            if self.kind != "image" or self.image_id != model_id:
                self.free()
                from diffusers import DiffusionPipeline
                self.pipe = self._load(DiffusionPipeline, model_id)
                self.kind, self.image_id = "image", model_id
            _g = torch.Generator("cuda").manual_seed(seed)
            _kw = dict(prompt=prompt, height=h, width=w, num_inference_steps=steps, generator=_g)
            _params = inspect.signature(self.pipe.__call__).parameters
            if "true_cfg_scale" in _params and cfg > 1:
                _kw.update(true_cfg_scale=cfg, negative_prompt=" ")
            else:
                _kw.update(guidance_scale=cfg)
            return self.pipe(**_kw).images[0]

        # ─────────── LTX 2.5 ───────────
        def _load_ltx(self):
            if self.kind == "video":
                return
            self.free()
            from diffusers import LTX2ImageToVideoPipeline
            self.pipe = self._load(LTX2ImageToVideoPipeline, LTX_ID)
            try:
                self.pipe.vae.enable_tiling()
            except Exception:
                pass
            try:
                from diffusers.pipelines.ltx2.utils import DISTILLED_SIGMA_VALUES, STAGE_2_DISTILLED_SIGMA_VALUES
                self.s1, self.s2 = DISTILLED_SIGMA_VALUES, STAGE_2_DISTILLED_SIGMA_VALUES
                self.distilled = True
            except Exception:
                self.distilled = False
            try:
                from diffusers import LTX2Pipeline
                _ok = inspect.signature(LTX2Pipeline.__init__).parameters
                self.t2v = LTX2Pipeline(**{k: v for k, v in self.pipe.components.items() if k in _ok})
            except Exception:
                self.t2v = None
            self.kind = "video"

        def _load_upsampler(self):
            if self.up is not None:
                return
            from diffusers import LTX2LatentUpsamplePipeline
            from diffusers.pipelines.ltx2.latent_upsampler import LTX2LatentUpsamplerModel
            _m = LTX2LatentUpsamplerModel.from_pretrained(
                LTX_ID, subfolder="latent_upsampler", torch_dtype=torch.bfloat16
            ).to("cuda")
            self.up = LTX2LatentUpsamplePipeline(vae=self.pipe.vae, latent_upsampler=_m)

        def _steps(self, stage2=False):
            if self.distilled:
                return dict(sigmas=self.s2 if stage2 else self.s1, guidance_scale=1.0)
            return dict(num_inference_steps=12 if stage2 else 40, guidance_scale=4.0)

        def _call(self, img, prompt, negative, h, w, nf, seed, **extra):
            _g = torch.Generator("cuda").manual_seed(seed)
            _kw = dict(prompt=prompt, num_frames=nf, frame_rate=float(FPS), generator=_g, return_dict=False, **extra)
            if not self.distilled:
                _kw["negative_prompt"] = negative
            if "latents" not in extra:
                _kw.update(height=h, width=w)
            if img is not None:
                return self.pipe(image=img, **_kw)
            if self.t2v is None:
                raise RuntimeError("حالت «بدون تصویر» در این نسخه کار نکرد؛ یک تصویر شروع انتخاب کنید.")
            return self.t2v(**_kw)

        def video(self, start_img, prompt, negative, nf, quality, aspect, seed):
            """خروجی: (فریم‌ها uint8, صدا, نرخ نمونه‌برداری)"""
            self._load_ltx()
            self.notes = []
            _sr = 24000
            for _path in ("vocoder.config.output_sampling_rate", "vocoder.config.sampling_rate",
                          "audio_vae.config.sample_rate"):
                try:
                    _o = self.pipe
                    for _p in _path.split("."):
                        _o = getattr(_o, _p)
                    _sr = int(_o)
                    break
                except Exception:
                    pass

            if quality.startswith("1080") and self.distilled:
                try:
                    _h, _w = GEN_1080_STAGE1[aspect]
                    _img = fit_image(start_img, _h, _w) if start_img is not None else None
                    _vl, _al = self._call(_img, prompt, negative, _h, _w, nf, seed,
                                          output_type="latent", **self._steps())
                    self._load_upsampler()
                    _up = self.up(latents=_vl, output_type="latent", return_dict=False)[0]
                    _img2 = fit_image(start_img, _h * 2, _w * 2) if start_img is not None else None
                    _v, _a = self._call(_img2, prompt, negative, _h * 2, _w * 2, nf, seed,
                                        latents=_up, audio_latents=_al, output_type="np",
                                        **self._steps(stage2=True))
                    return _to_frames(_v), _to_audio(_a), _sr
                except Exception as _e:
                    self.notes.append(f"ساخت دومرحله‌ای 1080 انجام نشد ({type(_e).__name__})؛ "
                                      "با 720 ساخته و با ffmpeg به 1080 بزرگ شد.")
                    gc.collect()
                    torch.cuda.empty_cache()

            _h, _w = GEN_720[aspect]
            _img = fit_image(start_img, _h, _w) if start_img is not None else None
            _v, _a = self._call(_img, prompt, negative, _h, _w, nf, seed, output_type="np", **self._steps())
            return _to_frames(_v), _to_audio(_a), _sr

    engine = Engine()
    return encode_mp4, engine, torch


@app.cell
def _(rtl, torch):
    _gpu = (
        f"✅ GPU: {torch.cuda.get_device_name(0)} — "
        f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.0f} GB"
        if torch.cuda.is_available()
        else "⚠️ GPU روشن نیست! از دکمه‌ی مشخصات نوت‌بوک در بالای molab، GPU را فعال کنید و نوت‌بوک را دوباره اجرا کنید."
    )
    rtl(f"<h1>🎬 استودیو ویدیو LTX 2.5</h1><p>{_gpu}</p>")
    return


@app.cell
def _(FINAL, STYLES, mo):
    style_dd = mo.ui.dropdown(options=list(STYLES), value="🎬 فیلم سینمایی", label="سبک ویدیو")
    aspect_dd = mo.ui.dropdown(options=["16:9 افقی", "9:16 عمودی", "1:1 مربع"], value="16:9 افقی", label="نسبت تصویر")
    quality_dd = mo.ui.dropdown(options=list(FINAL), value="1080p (1920×1080)", label="کیفیت")
    seed_in = mo.ui.number(start=-1, stop=2**31 - 1, value=-1, label="Seed (‎-1 = تصادفی)")
    hf_token = mo.ui.text(kind="password", label="توکن Hugging Face (اختیاری)", full_width=False)
    return aspect_dd, hf_token, quality_dd, seed_in, style_dd


@app.cell
def _(aspect_dd, hf_token, mo, os, quality_dd, seed_in, style_dd):
    if hf_token.value:
        os.environ["HF_TOKEN"] = hf_token.value.strip()
    mo.hstack([style_dd, aspect_dd, quality_dd, seed_in, hf_token], justify="start", gap=1.5, wrap=True)
    return


@app.cell
def _(random, seed_in):
    def pick_seed():
        return random.randint(0, 2**31 - 1) if seed_in.value is None or seed_in.value < 0 else int(seed_in.value)
    return (pick_seed,)


# ═══════════════════════ تب ۱: تصویرسازی ═══════════════════════
@app.cell
def _(IMAGE_MODELS, mo):
    img_prompt = mo.ui.text_area(
        label="پرامپت تصویر (پرامپت آماده‌ی فایل PDF را اینجا بگذارید)",
        placeholder="Wide establishing shot of ...", rows=7, full_width=True,
    )
    img_model = mo.ui.dropdown(options=list(IMAGE_MODELS), value="Z-Image Turbo (سریع)", label="مدل تصویر")
    img_count = mo.ui.slider(1, 4, value=1, label="تعداد")
    img_use_style = mo.ui.checkbox(value=True, label="سبک بالای صفحه را اضافه کن")
    img_name = mo.ui.text(label="نام تصویر (مثلاً: کوچه شب)")
    img_btn = mo.ui.run_button(label="🎨 ساخت تصویر", kind="success")
    img_upload = mo.ui.file(filetypes=[".png", ".jpg", ".jpeg", ".webp"], multiple=True, kind="area",
                            label="یا تصویر آماده آپلود کنید")
    img_upload_btn = mo.ui.run_button(label="⬆️ افزودن تصاویر آپلودشده")
    return img_btn, img_count, img_model, img_name, img_prompt, img_upload, img_upload_btn, img_use_style


@app.cell
def _(
    IMAGE_MODELS, IMG_SIZE, OUT, STYLES, aspect_dd, engine, get_chars, get_images, get_shots,
    img_btn, img_count, img_model, img_name, img_prompt, img_use_style, mo, pick_seed,
    save_project, set_images, set_log, style_dd, time, traceback,
):
    mo.stop(not img_btn.value)
    if not img_prompt.value.strip():
        set_log("⚠️ پرامپت تصویر خالی است.")
    else:
        _mid, _steps, _cfg = IMAGE_MODELS[img_model.value]
        _prompt = img_prompt.value.strip()
        if img_use_style.value:
            _prompt = STYLES[style_dd.value][0] + ". " + _prompt
        _h, _w = IMG_SIZE[aspect_dd.value]
        _new = []
        try:
            for _i in mo.status.progress_bar(range(img_count.value), title="در حال ساخت تصویر…",
                                             subtitle="بار اول مدل دانلود می‌شود (چند دقیقه)"):
                _seed = pick_seed()
                _im = engine.image(_mid, _steps, _cfg, _prompt, _h, _w, _seed)
                _p = OUT / "images" / f"img_{int(time.time() * 1000)}.png"
                _im.save(_p)
                _label = (img_name.value.strip() or "تصویر") + (f" {_i + 1}" if img_count.value > 1 else "")
                _new.append({"path": str(_p), "label": _label, "prompt": _prompt, "seed": _seed})
            _all = get_images() + _new
            set_images(_all)
            save_project(_all, get_chars(), get_shots())
            set_log(f"✅ {len(_new)} تصویر ساخته شد.")
        except Exception as _e:
            set_log(f"❌ خطا در ساخت تصویر: {_e}\n\n{traceback.format_exc()[-1500:]}")
    return


@app.cell
def _(OUT, get_chars, get_images, get_shots, img_upload, img_upload_btn, mo, save_project, set_images, set_log, time):
    mo.stop(not img_upload_btn.value)
    _new = []
    for _i in range(len(img_upload.value)):
        _p = OUT / "images" / f"up_{int(time.time() * 1000)}_{_i}_{img_upload.name(_i)}"
        _p.write_bytes(img_upload.contents(_i))
        _new.append({"path": str(_p), "label": img_upload.name(_i).rsplit(".", 1)[0], "prompt": "", "seed": None})
    if _new:
        _all = get_images() + _new
        set_images(_all)
        save_project(_all, get_chars(), get_shots())
        set_log(f"✅ {len(_new)} تصویر اضافه شد.")
    else:
        set_log("⚠️ اول فایلی انتخاب کنید.")
    return


# ═══════════════════════ تب ۲: کاراکترها ═══════════════════════
@app.cell
def _(SPEECH, get_images, mo):
    _imgs = get_images()
    char_name = mo.ui.text(label="نام کاراکتر", placeholder="مثلاً: Arash")
    char_upload = mo.ui.file(filetypes=[".png", ".jpg", ".jpeg", ".webp"], kind="area", label="عکس کاراکتر")
    char_from_gallery = mo.ui.dropdown(
        options={"— از گالری انتخاب نشده —": ""} | {f"{i + 1}. {im['label']}": im["path"] for i, im in enumerate(_imgs)},
        value="— از گالری انتخاب نشده —", label="یا عکس از گالری تصاویر",
    )
    char_look = mo.ui.text_area(
        label="ظاهر کاراکتر (به انگلیسی — همان «Character DNA» فایل PDF)",
        placeholder="a 35-year-old man with short black hair, thick beard, scar on left cheek, wearing a worn brown leather jacket",
        rows=3, full_width=True,
    )
    char_voice = mo.ui.text_area(
        label="تُن صدا (به انگلیسی)",
        placeholder="deep, raspy male voice with a slight echo",
        rows=2, full_width=True,
    )
    char_style = mo.ui.dropdown(options=list(SPEECH), value="معمولی", label="حالت پیش‌فرض صحبت")
    char_add = mo.ui.run_button(label="➕ ذخیره کاراکتر", kind="success")
    return char_add, char_from_gallery, char_look, char_name, char_style, char_upload, char_voice


@app.cell
def _(
    OUT, char_add, char_from_gallery, char_look, char_name, char_style, char_upload, char_voice,
    get_chars, get_images, get_shots, mo, save_project, set_chars, set_log, shutil, time,
):
    mo.stop(not char_add.value)
    _name = char_name.value.strip()
    if not _name:
        set_log("⚠️ نام کاراکتر را بنویسید.")
    elif not char_upload.value and not char_from_gallery.value:
        set_log("⚠️ یک عکس برای کاراکتر انتخاب کنید.")
    else:
        _dst = OUT / "characters" / f"{int(time.time())}_{_name}.png"
        if char_upload.value:
            _dst.write_bytes(char_upload.contents(0))
        else:
            shutil.copy(char_from_gallery.value, _dst)
        _c = dict(get_chars())
        _c[_name] = {
            "image": str(_dst), "look": char_look.value.strip(),
            "voice": char_voice.value.strip(), "style": char_style.value,
        }
        set_chars(_c)
        save_project(get_images(), _c, get_shots())
        set_log(f"✅ کاراکتر «{_name}» ذخیره شد.")
    return


@app.cell
def _(get_chars, mo):
    char_del_dd = mo.ui.dropdown(options=list(get_chars()) or ["—"], label="حذف کاراکتر")
    char_del_btn = mo.ui.run_button(label="🗑 حذف")
    return char_del_btn, char_del_dd


@app.cell
def _(char_del_btn, char_del_dd, get_chars, get_images, get_shots, mo, save_project, set_chars, set_log):
    mo.stop(not char_del_btn.value)
    _c = dict(get_chars())
    if char_del_dd.value in _c:
        _c.pop(char_del_dd.value)
        set_chars(_c)
        save_project(get_images(), _c, get_shots())
        set_log(f"🗑 کاراکتر «{char_del_dd.value}» حذف شد.")
    return


# ═══════════════════════ تب ۳: استودیو ═══════════════════════
@app.cell
def _(CAMERA, DURATIONS, LANGS, SPEECH, mo):
    story = mo.ui.text_area(
        label="دنیای داستان (ثابت برای همه‌ی شات‌ها — به انگلیسی)",
        placeholder="A rainy night in an old Middle-Eastern city, 1970s, neon signs reflecting on wet stone streets.",
        rows=2, full_width=True,
    )
    scene = mo.ui.text_area(
        label="اتفاق این شات (به انگلیسی — چه کسی چه کاری می‌کند)",
        placeholder="Arash walks slowly toward the door, stops, and turns his head toward the camera.",
        rows=4, full_width=True,
    )
    dialogue = mo.ui.text_area(label="دیالوگ (خالی = بدون حرف)", rows=2, full_width=True)
    dlg_lang = mo.ui.dropdown(options=list(LANGS), value="انگلیسی (بهترین نتیجه)", label="زبان دیالوگ")
    speech_dd = mo.ui.dropdown(options=["پیش‌فرض کاراکتر"] + list(SPEECH), value="پیش‌فرض کاراکتر",
                               label="حالت صحبت در این شات")
    camera_dd = mo.ui.dropdown(options=list(CAMERA), value="ثابت", label="حرکت دوربین")
    dur_dd = mo.ui.dropdown(options=list(DURATIONS), value="۵ ثانیه", label="مدت شات")
    sfx = mo.ui.text(label="صدای محیط / موسیقی (انگلیسی)", placeholder="rain, distant thunder, low cello music",
                     full_width=True)
    manual = mo.ui.text_area(label="پرامپت دستی (اختیاری — اگر پر شود جای پرامپت خودکار استفاده می‌شود)",
                             rows=3, full_width=True)
    gen_btn = mo.ui.run_button(label="🎬 ساخت شات بعدی", kind="success")
    undo_btn = mo.ui.run_button(label="↩️ حذف آخرین شات", kind="warn")
    merge_btn = mo.ui.run_button(label="🎞 چسباندن همه‌ی شات‌ها (فیلم نهایی)")
    return camera_dd, dialogue, dlg_lang, dur_dd, gen_btn, manual, merge_btn, scene, sfx, speech_dd, story, undo_btn


@app.cell
def _(get_chars, get_images, get_shots, mo):
    _opts = {}
    if get_shots():
        _opts["▶ ادامه از آخرین فریم شات قبلی"] = "continue"
    for _i, _im in enumerate(get_images()):
        _opts[f"🖼 {_i + 1}. {_im['label']}"] = "img:" + _im["path"]
    for _n, _c in get_chars().items():
        _opts[f"👤 {_n}"] = "img:" + _c["image"]
    _opts["⛔ بدون تصویر (فقط متن)"] = "none"
    start_dd = mo.ui.dropdown(options=_opts, value=list(_opts)[0], label="فریم شروع")
    _names = list(get_chars())
    speaker_dd = mo.ui.dropdown(options=["— هیچ‌کس —"] + _names, value="— هیچ‌کس —", label="گوینده")
    others_ms = mo.ui.multiselect(options=_names, label="کاراکترهای دیگر در صحنه")
    return others_ms, speaker_dd, start_dd


@app.cell
def _(
    BASE_NEGATIVE, CAMERA, CONTINUITY, LANGS, SPEECH, STYLES, camera_dd, dialogue, dlg_lang,
    get_chars, manual, others_ms, scene, sfx, speaker_dd, speech_dd, start_dd, story, style_dd,
):
    def build_prompt():
        if manual.value.strip():
            return manual.value.strip(), STYLES[style_dd.value][1] + ", " + BASE_NEGATIVE
        _chars = get_chars()
        _parts = [STYLES[style_dd.value][0] + "."]
        if story.value.strip():
            _parts.append(story.value.strip().rstrip(".") + ".")
        if start_dd.value == "continue":
            _parts.append(CONTINUITY)
        for _n in others_ms.value:
            if _n in _chars and _chars[_n]["look"] and _n != speaker_dd.value:
                _parts.append(f"{_n} is {_chars[_n]['look'].rstrip('.')}.")
        if scene.value.strip():
            _parts.append(scene.value.strip().rstrip(".") + ".")
        _sp = speaker_dd.value
        if _sp in _chars:
            _c = _chars[_sp]
            if _c["look"]:
                _parts.append(f"{_sp} is {_c['look'].rstrip('.')}.")
            if dialogue.value.strip():
                _mode = _c["style"] if speech_dd.value == "پیش‌فرض کاراکتر" else speech_dd.value
                _voice = f" in a {_c['voice'].rstrip('.')}" if _c["voice"] else ""
                _parts.append(
                    f"{_sp} looks toward the listener and speaks {SPEECH[_mode]}{_voice}, "
                    f"in {LANGS[dlg_lang.value]}, with clear lip movement, saying: \"{dialogue.value.strip()}\""
                )
        elif dialogue.value.strip():
            _mode = "معمولی" if speech_dd.value == "پیش‌فرض کاراکتر" else speech_dd.value
            _parts.append(f"A voice says {SPEECH[_mode]} in {LANGS[dlg_lang.value]}: \"{dialogue.value.strip()}\"")
        _parts.append(CAMERA[camera_dd.value])
        if sfx.value.strip():
            _parts.append(f"Audio: {sfx.value.strip()}.")
        return " ".join(_parts), STYLES[style_dd.value][1] + ", " + BASE_NEGATIVE
    return (build_prompt,)


@app.cell
def _(
    DURATIONS, FINAL, Image, OUT, aspect_dd, build_prompt, dur_dd, encode_mp4, engine, gen_btn,
    get_chars, get_images, get_shots, mo, pick_seed, quality_dd, save_project, set_log, set_shots,
    start_dd, time, traceback,
):
    mo.stop(not gen_btn.value)
    _shots = get_shots()
    _src = start_dd.value
    _continued = _src == "continue"
    _img = None
    try:
        if _continued:
            _img = Image.open(_shots[-1]["last_frame"])
        elif _src.startswith("img:"):
            _img = Image.open(_src[4:])
        _prompt, _neg = build_prompt()
        _nf = DURATIONS[dur_dd.value]
        _seed = pick_seed()
        _t0 = time.time()
        with mo.status.spinner(title=f"ساخت شات {len(_shots) + 1}…",
                               subtitle="بار اول LTX 2.5 دانلود و بارگذاری می‌شود (ممکن است ۱۰–۲۰ دقیقه طول بکشد)"):
            _frames, _audio, _sr = engine.video(_img, _prompt, _neg, _nf, quality_dd.value, aspect_dd.value, _seed)
            _stamp = int(time.time())
            _lf = OUT / "frames" / f"shot_{len(_shots) + 1:03d}_{_stamp}_last.png"
            Image.fromarray(_frames[-1]).save(_lf)
            _vp = OUT / "shots" / f"shot_{len(_shots) + 1:03d}_{_stamp}.mp4"
            encode_mp4(_frames, _audio, _sr, _vp, FINAL[quality_dd.value][aspect_dd.value])
        _new = _shots + [{
            "video": str(_vp), "last_frame": str(_lf), "prompt": _prompt, "seed": _seed,
            "continued": _continued, "duration": dur_dd.value, "quality": quality_dd.value,
        }]
        set_shots(_new)
        save_project(get_images(), get_chars(), _new)
        _note = ("\n\n" + "\n".join(engine.notes)) if engine.notes else ""
        set_log(f"✅ شات {len(_new)} در {time.time() - _t0:.0f} ثانیه ساخته شد. "
                f"برای ادامه‌ی داستان، «ادامه از آخرین فریم» انتخاب شده است.{_note}")
    except Exception as _e:
        set_log(f"❌ خطا در ساخت شات: {_e}\n\n{traceback.format_exc()[-2000:]}")
    return


@app.cell
def _(get_chars, get_images, get_shots, mo, save_project, set_log, set_shots, undo_btn):
    mo.stop(not undo_btn.value)
    _s = get_shots()
    if _s:
        set_shots(_s[:-1])
        save_project(get_images(), get_chars(), _s[:-1])
        set_log(f"↩️ شات {len(_s)} حذف شد. حالا می‌توانید دوباره از آخرین فریم شات قبلی بسازید.")
    return


@app.cell
def _(FPS, OUT, get_shots, merge_btn, mo, set_final, set_log, subprocess, time, traceback):
    mo.stop(not merge_btn.value)
    _s = get_shots()
    if len(_s) < 1:
        set_log("⚠️ هنوز شاتی ساخته نشده.")
    else:
        try:
            import shutil as _sh
            try:
                import imageio_ffmpeg as _iff
                _ff = _sh.which("ffmpeg") or _iff.get_ffmpeg_exe()
            except Exception:
                _ff = "ffmpeg"
            _probe = subprocess.run([_ff, "-i", _s[0]["video"]], capture_output=True).stderr.decode(errors="ignore")
            import re as _re
            _m = _re.search(r"Video:.*?(\d{3,4})x(\d{3,4})", _probe)
            _W, _H = (int(_m.group(1)), int(_m.group(2))) if _m else (1920, 1080)
            _cmd = [_ff, "-y", "-loglevel", "error"]
            for _x in _s:
                _cmd += ["-i", _x["video"]]
            _f = []
            for _i, _x in enumerate(_s):
                _skip = 1 if (_x.get("continued") and _i > 0) else 0  # فریم تکراری اتصال حذف می‌شود
                _f.append(f"[{_i}:v]trim=start_frame={_skip},setpts=PTS-STARTPTS,"
                          f"scale={_W}:{_H}:force_original_aspect_ratio=increase,crop={_W}:{_H},setsar=1,fps={FPS}[v{_i}]")
                _f.append(f"[{_i}:a]atrim=start={_skip / FPS:.5f},asetpts=PTS-STARTPTS,aresample=48000,"
                          f"aformat=channel_layouts=stereo[a{_i}]")
            _f.append("".join(f"[v{_i}][a{_i}]" for _i in range(len(_s))) + f"concat=n={len(_s)}:v=1:a=1[v][a]")
            _out = OUT / "final" / f"movie_{int(time.time())}.mp4"
            _cmd += ["-filter_complex", ";".join(_f), "-map", "[v]", "-map", "[a]",
                     "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
                     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(_out)]
            with mo.status.spinner(title="در حال چسباندن شات‌ها…"):
                _r = subprocess.run(_cmd, capture_output=True)
            if _r.returncode != 0:
                raise RuntimeError(_r.stderr.decode(errors="ignore")[-1500:])
            set_final(str(_out))
            set_log(f"✅ فیلم نهایی آماده شد ({len(_s)} شات).")
        except Exception as _e:
            set_log(f"❌ خطا در چسباندن: {_e}\n\n{traceback.format_exc()[-1500:]}")
    return


# ═══════════════════════ نمایش ═══════════════════════
@app.cell
def _(Path, build_prompt, mo):
    def show_video(path, label="⬇️ دانلود"):
        _b = Path(path).read_bytes()
        return mo.vstack([
            mo.video(src=_b, controls=True, width="100%"),
            mo.download(data=_b, filename=Path(path).name, mimetype="video/mp4", label=label),
        ])

    def prompt_preview():
        _p, _n = build_prompt()
        return mo.accordion({"👁 پیش‌نمایش پرامپت این شات": mo.md(f"```text\n{_p}\n```")})
    return prompt_preview, show_video


@app.cell
def _(
    camera_dd, char_add, char_del_btn, char_del_dd, char_from_gallery, char_look, char_name,
    char_style, char_upload, char_voice, dialogue, dlg_lang, dur_dd, gen_btn, get_chars,
    get_final, get_images, get_log, get_shots, img_btn, img_count, img_model, img_name,
    img_prompt, img_upload, img_upload_btn, img_use_style, manual, merge_btn, mo, others_ms,
    prompt_preview, rtl, scene, sfx, show_video, speaker_dd, speech_dd, start_dd, story, undo_btn,
):
    # ── گالری تصاویر
    _imgs = get_images()
    _gallery = mo.hstack(
        [mo.vstack([mo.image(src=_im["path"], width=240, rounded=True), mo.md(f"**{_i + 1}.** {_im['label']}")])
         for _i, _im in enumerate(_imgs)],
        wrap=True, justify="start", gap=1,
    ) if _imgs else rtl("<i>هنوز تصویری نیست.</i>")
    _tab_img = mo.vstack([
        img_prompt,
        mo.hstack([img_model, img_count, img_name, img_use_style, img_btn], justify="start", gap=1.5, wrap=True),
        mo.hstack([img_upload, img_upload_btn], justify="start", gap=1),
        rtl("<h3>🖼 گالری</h3>"), _gallery,
    ], gap=1)

    # ── کاراکترها
    _chars = get_chars()
    _cards = mo.hstack([
        mo.vstack([
            mo.image(src=_c["image"], width=200, rounded=True),
            rtl(f"<b>{_n}</b><br>🗣 حالت: {_c['style']}<br><small>صدا: {_c['voice'] or '—'}</small>"),
        ]) for _n, _c in _chars.items()
    ], wrap=True, justify="start", gap=1) if _chars else rtl("<i>هنوز کاراکتری نیست.</i>")
    _tab_char = mo.hstack([
        mo.vstack([char_name, char_upload, char_from_gallery, char_look, char_voice, char_style, char_add,
                   mo.hstack([char_del_dd, char_del_btn], justify="start")], gap=0.8),
        mo.vstack([rtl("<h3>👥 کاراکترهای پروژه</h3>"), _cards]),
    ], widths=[1, 1.4], gap=2, align="start")

    # ── استودیو
    _shots = get_shots()
    _timeline = mo.vstack([
        mo.hstack([
            mo.vstack([rtl(f"<b>شات {_i + 1}</b> — {_x['duration']} — {_x['quality'].split()[0]}"
                           + (" — 🔗 ادامه‌ی شات قبل" if _x.get("continued") else "")),
                       show_video(_x["video"])]),
        ]) for _i, _x in enumerate(_shots)
    ], gap=1.5) if _shots else rtl("<i>هنوز شاتی ساخته نشده. یک فریم شروع انتخاب کنید و «ساخت شات بعدی» را بزنید.</i>")
    _final = get_final()
    _tab_studio = mo.hstack([
        mo.vstack([
            story, start_dd,
            mo.hstack([dur_dd, camera_dd], justify="start", gap=1),
            scene,
            mo.hstack([speaker_dd, others_ms], justify="start", gap=1),
            dialogue,
            mo.hstack([speech_dd, dlg_lang], justify="start", gap=1),
            sfx, manual, prompt_preview(),
            mo.hstack([gen_btn, undo_btn, merge_btn], justify="start", gap=1),
        ], gap=0.8),
        mo.vstack([
            rtl("<h3>🎞 تایم‌لاین</h3>"), _timeline,
            *( [rtl("<h3>🏁 فیلم نهایی</h3>"), show_video(_final, "⬇️ دانلود فیلم نهایی")] if _final else [] ),
        ]),
    ], widths=[1, 1.3], gap=2, align="start")

    _log = get_log()
    mo.vstack([
        mo.callout(mo.md(_log), kind="danger" if _log.startswith("❌") else "info") if _log else mo.md(""),
        mo.ui.tabs({"🎬 استودیو": _tab_studio, "🎨 تصویرسازی": _tab_img, "👤 کاراکترها": _tab_char}),
    ])
    return


if __name__ == "__main__":
    app.run()
