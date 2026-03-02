#!/usr/bin/env python3
"""
OpenRouter API client for frontend-agent skill.
Supports Gemini 3.1 Pro (code generation) and Nano Banana 2 (image generation).

Usage:
    # Code generation with Gemini 3.1 Pro
    python3 openrouter_client.py code --prompt "Create a responsive hero section" --output result.html

    # Code generation with screenshot analysis
    python3 openrouter_client.py code --prompt "Recreate this design" --image screenshot.png --output result.html

    # Image generation with Nano Banana 2
    python3 openrouter_client.py image --prompt "Flat icon of a rocket, blue, 512x512" --output icon.png

    # Image generation with reference image
    python3 openrouter_client.py image --prompt "Similar style icon but for settings" --image reference.png --output icon.png

    # Code generation with content manifest (anti-hallucination)
    python3 openrouter_client.py code --prompt "Layout instructions" --content content.json --output result.html

    # Patch existing file with targeted changes
    python3 openrouter_client.py patch --file index.html --prompt "Change hero layout to centered" --output index.html
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env from workspace
ENV_PATHS = [
    Path.home() / ".env",
    Path(".env"),
]

for env_path in ENV_PATHS:
    if env_path.exists():
        load_dotenv(env_path)
        break

API_URL = "https://openrouter.ai/api/v1/chat/completions"
GEMINI_PRO = "google/gemini-3.1-pro-preview"
NANO_BANANA = "google/gemini-3.1-flash-image-preview"


def get_api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("ERROR: OPENROUTER_API_KEY not found.", file=sys.stderr)
        print("Set it in .env or as environment variable.", file=sys.stderr)
        sys.exit(1)
    return key


def encode_image(image_path):
    path = Path(image_path)
    if not path.exists():
        print(f"ERROR: Image not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    suffix = path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
    }
    mime = mime_types.get(suffix, "image/png")

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def build_messages(prompt, image_path=None, system_prompt=None):
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    if image_path:
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": encode_image(image_path)}},
        ]
        messages.append({"role": "user", "content": content})
    else:
        messages.append({"role": "user", "content": prompt})

    return messages


def call_gemini_pro(prompt, image_path=None, system_prompt=None):
    """Call Gemini 3.1 Pro for code generation and analysis."""
    api_key = get_api_key()

    default_system = (
        "You are an expert frontend developer. Generate clean, production-ready code.\n"
        "Use semantic HTML, CSS custom properties, mobile-first responsive design.\n"
        "Use BEM naming for CSS classes. Include Google Fonts links when using custom fonts.\n"
        "Return ONLY code without explanations unless asked.\n\n"
        "CRITICAL CONTENT RULES:\n"
        "1. Content text is SACRED - reproduce ALL text from the content manifest EXACTLY as provided.\n"
        "2. NEVER invent, rephrase, summarize, or replace any text content.\n"
        "3. NEVER add placeholder text like 'Lorem ipsum' or generic descriptions.\n"
        "4. If content manifest is provided, use ONLY data from it.\n"
        "5. Keep all numbers, names, titles, descriptions EXACTLY as given.\n"
        "6. If something is unclear, keep original text - do NOT guess or improvise.\n"
        "7. Your job is LAYOUT and STYLING only. Content comes from the manifest."
    )

    payload = {
        "model": GEMINI_PRO,
        "messages": build_messages(
            prompt, image_path, system_prompt or default_system
        ),
        "max_tokens": 32000,
        "temperature": 0.3,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/vibe-frontend-agent",
        "X-Title": "Frontend Agent",
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        print(f"API Error: {data['error']}", file=sys.stderr)
        sys.exit(1)

    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})

    return {
        "text": text,
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
        "model": data.get("model", GEMINI_PRO),
    }


def call_nano_banana(prompt, image_path=None, aspect_ratio="1:1", quality="2k"):
    """Call Nano Banana 2 for image generation.

    quality: "1k" (1024), "2k" (2048), "4k" (4096)
    """
    api_key = get_api_key()

    # Map quality to resolution hint in prompt
    quality_map = {
        "1k": "1024x1024",
        "2k": "2048x2048",
        "4k": "4096x4096",
    }
    resolution = quality_map.get(quality, "2048x2048")

    # Append resolution to prompt if not already specified
    if "resolution" not in prompt.lower() and "x" not in prompt[-10:]:
        prompt = f"{prompt}, high quality, resolution {resolution}"

    messages = build_messages(prompt, image_path)

    image_config = {
        "aspect_ratio": aspect_ratio,
    }
    # Nano Banana 2 supports image_size parameter
    size_map = {"1k": "1K", "2k": "2K", "4k": "4K"}
    if quality in size_map:
        image_config["image_size"] = size_map[quality]

    payload = {
        "model": NANO_BANANA,
        "messages": messages,
        "modalities": ["image", "text"],
        "image_config": image_config,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/vibe-frontend-agent",
        "X-Title": "Frontend Agent",
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        print(f"API Error: {data['error']}", file=sys.stderr)
        sys.exit(1)

    message = data["choices"][0]["message"]
    usage = data.get("usage", {})

    # Extract images from response
    # OpenRouter returns images in message["images"] array
    images = []
    for img in message.get("images", []):
        if isinstance(img, dict) and "image_url" in img:
            images.append(img["image_url"]["url"])
        elif isinstance(img, str):
            images.append(img)

    # Fallback: check content array
    if not images and isinstance(message.get("content"), list):
        for part in message["content"]:
            if isinstance(part, dict) and part.get("type") == "image_url":
                images.append(part["image_url"]["url"])

    return {
        "images": images,
        "text": extract_text(message),
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
        "model": data.get("model", NANO_BANANA),
    }


def extract_text(message):
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
        return "\n".join(texts)
    return ""


def save_base64_image(data_url, output_path):
    """Save a base64 data URL to file."""
    if data_url.startswith("data:"):
        # data:image/png;base64,<data>
        header, data = data_url.split(",", 1)
    else:
        data = data_url

    img_bytes = base64.b64decode(data)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_bytes)
    print(f"Image saved: {output_path}")


def cmd_code(args):
    """Handle 'code' subcommand."""
    prompt = args.prompt
    if args.content:
        content_path = Path(args.content)
        if not content_path.exists():
            print(f"ERROR: Content manifest not found: {args.content}", file=sys.stderr)
            sys.exit(1)
        content_data = content_path.read_text()
        prompt = (
            f"CONTENT MANIFEST (use EXACTLY as provided, do NOT modify any text):\n"
            f"```json\n{content_data}\n```\n\n"
            f"LAYOUT INSTRUCTIONS:\n{args.prompt}"
        )

    result = call_gemini_pro(
        prompt=prompt,
        image_path=args.image,
        system_prompt=args.system,
    )

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(result["text"])
        print(f"Code saved: {args.output}", file=sys.stderr)
    else:
        print(result["text"])

    print(
        f"\n[Gemini 3.1 Pro] Tokens: {result['input_tokens']} in / {result['output_tokens']} out",
        file=sys.stderr,
    )


def cmd_image(args):
    """Handle 'image' subcommand."""
    result = call_nano_banana(
        prompt=args.prompt,
        image_path=args.image,
        aspect_ratio=args.aspect_ratio,
        quality=args.quality,
    )

    if result["images"]:
        for i, img_url in enumerate(result["images"]):
            if args.output:
                out_path = args.output if len(result["images"]) == 1 else f"{Path(args.output).stem}_{i}{Path(args.output).suffix}"
                save_base64_image(img_url, out_path)
            else:
                print(f"Image {i}: {img_url[:80]}...")
    else:
        print("No images generated.", file=sys.stderr)
        if result["text"]:
            print(f"Response: {result['text']}", file=sys.stderr)

    print(
        f"\n[Nano Banana 2] Tokens: {result['input_tokens']} in / {result['output_tokens']} out",
        file=sys.stderr,
    )


def cmd_analyze(args):
    """Handle 'analyze' subcommand - analyze a screenshot with Gemini Pro."""
    system = (
        "You are an expert UI/UX analyst. Analyze the provided design screenshot and extract:\n"
        "1. Layout structure (grid, sections, columns)\n"
        "2. Color palette (hex codes for primary, accent, background, text)\n"
        "3. Typography (font families, sizes, weights)\n"
        "4. Components (buttons, cards, navigation, forms)\n"
        "5. Special effects (gradients, shadows, animations hints)\n"
        "Format as structured markdown."
    )

    result = call_gemini_pro(
        prompt=args.prompt or "Analyze this design in detail. Extract colors, fonts, layout, and components.",
        image_path=args.image,
        system_prompt=system,
    )

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(result["text"])
        print(f"Analysis saved: {args.output}", file=sys.stderr)
    else:
        print(result["text"])

    print(
        f"\n[Gemini 3.1 Pro] Tokens: {result['input_tokens']} in / {result['output_tokens']} out",
        file=sys.stderr,
    )


def cmd_patch(args):
    """Handle 'patch' subcommand - patch existing code with targeted changes."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    existing_code = file_path.read_text()

    system = (
        "You are patching existing HTML/CSS/JS code. Your task:\n"
        "1. Read the existing code provided below.\n"
        "2. Apply ONLY the requested changes.\n"
        "3. Return the COMPLETE updated file (not just changed sections).\n"
        "4. PRESERVE all existing content text exactly as-is unless explicitly told to change it.\n"
        "5. Do NOT rewrite, rephrase, or reorganize unchanged sections.\n"
        "6. Do NOT add new content that wasn't requested.\n"
        "7. If a content manifest is provided, any NEW text must come from it exactly."
    )

    prompt = f"EXISTING CODE:\n```html\n{existing_code}\n```\n\n"

    if args.content:
        content_path = Path(args.content)
        if not content_path.exists():
            print(f"ERROR: Content manifest not found: {args.content}", file=sys.stderr)
            sys.exit(1)
        content_data = content_path.read_text()
        prompt += (
            f"CONTENT MANIFEST (use EXACTLY as provided):\n"
            f"```json\n{content_data}\n```\n\n"
        )

    prompt += f"CHANGES REQUESTED:\n{args.prompt}"

    result = call_gemini_pro(
        prompt=prompt,
        image_path=None,
        system_prompt=system,
    )

    output_path = args.output or args.file
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(result["text"])
    print(f"Patched code saved: {output_path}", file=sys.stderr)

    print(
        f"\n[Gemini 3.1 Pro] Tokens: {result['input_tokens']} in / {result['output_tokens']} out",
        file=sys.stderr,
    )


def main():
    parser = argparse.ArgumentParser(description="OpenRouter API client for frontend-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Code generation
    code_parser = subparsers.add_parser("code", help="Generate code with Gemini 3.1 Pro")
    code_parser.add_argument("--prompt", "-p", required=True, help="Prompt for code generation")
    code_parser.add_argument("--image", "-i", help="Path to screenshot/design image")
    code_parser.add_argument("--output", "-o", help="Output file path")
    code_parser.add_argument("--system", "-s", help="Custom system prompt")
    code_parser.add_argument("--content", "-c", help="Path to JSON content manifest")

    # Image generation
    img_parser = subparsers.add_parser("image", help="Generate images with Nano Banana 2")
    img_parser.add_argument("--prompt", "-p", required=True, help="Image generation prompt")
    img_parser.add_argument("--image", "-i", help="Reference image path")
    img_parser.add_argument("--output", "-o", help="Output image path")
    img_parser.add_argument("--aspect-ratio", "-a", default="1:1",
                           help="Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4)")
    img_parser.add_argument("--quality", "-q", default="2k", choices=["1k", "2k", "4k"],
                           help="Image quality/resolution (1k, 2k, 4k). Default: 2k")

    # Patch existing code
    patch_parser = subparsers.add_parser("patch", help="Patch existing code with targeted changes")
    patch_parser.add_argument("--file", "-f", required=True, help="Existing HTML file to patch")
    patch_parser.add_argument("--prompt", "-p", required=True, help="What to change")
    patch_parser.add_argument("--content", "-c", help="Path to JSON content manifest")
    patch_parser.add_argument("--output", "-o", help="Output file path (default: overwrite input)")

    # Design analysis
    analyze_parser = subparsers.add_parser("analyze", help="Analyze design with Gemini 3.1 Pro")
    analyze_parser.add_argument("--image", "-i", required=True, help="Screenshot to analyze")
    analyze_parser.add_argument("--prompt", "-p", help="Custom analysis prompt")
    analyze_parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if args.command == "code":
        cmd_code(args)
    elif args.command == "image":
        cmd_image(args)
    elif args.command == "patch":
        cmd_patch(args)
    elif args.command == "analyze":
        cmd_analyze(args)


if __name__ == "__main__":
    main()
