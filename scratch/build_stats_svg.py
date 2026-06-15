import urllib.request
import re
import base64
import os

def fetch_content(url, headers=None):
    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def embed_svg(svg_content, x, y, width, height, default_viewbox, custom_class=None):
    # Find viewBox in the original svg_content
    vb_match = re.search(r'viewBox=["\']([^"\']+)["\']', svg_content)
    viewbox = vb_match.group(1) if vb_match else default_viewbox
    
    # Remove XML declaration and any DOCTYPE if present
    svg_content = re.sub(r'<\?xml[^>]*\?>', '', svg_content)
    svg_content = re.sub(r'<!DOCTYPE[^>]*>', '', svg_content)
    
    # Find the actual <svg ...> tag using regex (ignoring XML declarations or comments preceding it)
    pattern = r'<svg[^>]*>'
    match = re.search(pattern, svg_content)
    if match:
        end_idx = match.end()
        content_body = svg_content[end_idx:]
    else:
        # Fallback if no <svg> tag is found
        content_body = svg_content
    
    # Create the new nested svg tag preserving viewBox
    class_attr = f' class="{custom_class}"' if custom_class else ''
    nested_svg = f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{viewbox}" fill="none"{class_attr} xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    return nested_svg + content_body

def get_pixel_path(x, y, w, h, p=3):
    return (
        f"M {x+3*p} {y} "
        f"H {x+w-3*p} "
        f"H {x+w-2*p} V {y+p} "
        f"H {x+w-p} V {y+2*p} "
        f"H {x+w} V {y+3*p} "
        f"V {y+h-3*p} "
        f"V {y+h-2*p} H {x+w-p} "
        f"V {y+h-p} H {x+w-2*p} "
        f"V {y+h} H {x+3*p} "
        f"H {x+3*p} "
        f"H {x+2*p} V {y+h-p} "
        f"H {x+p} V {y+h-2*p} "
        f"H {x} V {y+h-3*p} "
        f"V {y+3*p} "
        f"V {y+2*p} H {x+p} "
        f"V {y+p} H {x+2*p} "
        f"V {y} H {x+3*p} Z"
    )

def main():
    username = "NITHEESH-14"
    streak_y = 65
    left_pixel_path = get_pixel_path(15, 20, 327, 144, p=3)
    right_pixel_path = get_pixel_path(492, streak_y, 347, 144, p=3)
    left_inset_path = get_pixel_path(15 + 6, 20 + 6, 327 - 12, 144 - 12, p=3)
    right_inset_path = get_pixel_path(492 + 6, streak_y + 6, 347 - 12, 144 - 12, p=3)
    gif_path = r"c:\Users\R Nitheesh\Desktop\NITHEESH-14\assests\gifs\225813708-98b745f2-7d22-48cf-9150-083f1b00d6c9.gif"
    output_path_standard = r"c:\Users\R Nitheesh\Desktop\NITHEESH-14\assests\images\stats_banner.svg"
    output_path_counter = r"c:\Users\R Nitheesh\Desktop\NITHEESH-14\assests\images\stats_banner_with_counter.svg"

    # 1. Fetch Main Stats SVG
    url_stats = f"https://github-readme-stats.vercel.app/api?username={username}&rank_icon=github&theme=dracula&text_bold=false&hide_border=true&bg_color=00000000&show_icons=true&hide=issues&count_private=true&include_all_commits=true"
    stats_svg = fetch_content(url_stats)

    # 2. Fetch Streak Stats SVG
    url_streak = f"https://github-readme-streak-stats-eight.vercel.app/?user={username}&theme=dracula&border_radius=0&background=FFFFFF00&hide_border=true"
    streak_svg = fetch_content(url_streak)

    # 3. Live Profile Counter URL (embedded as live image to update counter on every view)
    url_counter = f"https://count.getloli.com/@ZennitS?name=ZennitS&theme=booru-lewd&padding=7&offset=0&align=top&scale=1&pixelated=1&darkmode=auto"

    if not stats_svg or not streak_svg:
        print("Error: Could not fetch stats or streak SVGs from the APIs.")
        return

    # Base64 Encode Profile Views PNG
    profileviews_path = r"c:\Users\R Nitheesh\Desktop\NITHEESH-14\assests\images\Profileviews.png"
    if not os.path.exists(profileviews_path):
        print(f"Error: Profileviews PNG not found at {profileviews_path}")
        return

    with open(profileviews_path, "rb") as image_file:
        encoded_profileviews = base64.b64encode(image_file.read()).decode('utf-8')

    # Clean the streak SVG background rect to make it transparent
    streak_svg = streak_svg.replace("<rect width='495' height='195' rx='0'/>", "<rect width='495' height='195' rx='0' fill='none'/>")

    # Modify font sizes in SVGs for better readability
    stats_svg = re.sub(r'font:\s*600\s+14px', 'font: 600 16px', stats_svg)
    stats_svg = re.sub(r'font:\s*600\s+18px', 'font: 600 20px', stats_svg)

    # Increase font size inside elements of the streak SVG
    streak_svg = re.sub(r"font-size=['\"]28px['\"]", "font-size='34px'", streak_svg)
    streak_svg = re.sub(r"font-size=['\"]14px['\"]", "font-size='16.5px'", streak_svg)
    streak_svg = re.sub(r"font-size=['\"]12px['\"]", "font-size='13.5px'", streak_svg)
    streak_svg = re.sub(r"font-size:\s*34px;", "font-size: 40px;", streak_svg)
    streak_svg = re.sub(r"font-size:\s*28px;", "font-size: 34px;", streak_svg)

    # Add solid black outlines to all text elements in the streak SVG for 100% readability on the GIF
    streak_svg = streak_svg.replace("stroke-width='0'", "stroke-width='3.5px' paint-order='stroke fill' stroke-linejoin='round'")
    streak_svg = streak_svg.replace("stroke='none'", "stroke='#000000'")

    # Add solid black outlines to all text elements in the GitHub stats SVG for 100% readability on the GIF
    stats_svg = stats_svg.replace("fill: #f8f8f2;", "fill: #f8f8f2; stroke: #000000; stroke-width: 3px; paint-order: stroke fill; stroke-linejoin: round;")
    stats_svg = stats_svg.replace("fill: #ff6e96;", "fill: #ff6e96; stroke: #000000; stroke-width: 3.5px; paint-order: stroke fill; stroke-linejoin: round;")

    # Scale stats and streaks to 70%
    nested_stats = embed_svg(stats_svg, x=15, y=22, width=327, height=136.5, default_viewbox="0 0 467 195")
    nested_streak = embed_svg(streak_svg, x=492, y=streak_y + 2, width=346.5, height=136.5, default_viewbox="0 0 495 195")

    # Base64 Encode GIF
    if not os.path.exists(gif_path):
        print(f"Error: GIF not found at {gif_path}")
        return

    with open(gif_path, "rb") as image_file:
        encoded_gif = base64.b64encode(image_file.read()).decode('utf-8')

    # SVG Template Shared Parts
    defs_and_styles = f"""  <defs>
    <!-- Rounded clipping path for the entire banner -->
    <clipPath id="bannerClip">
      <rect width="854" height="480" rx="12" />
    </clipPath>
    <!-- Clipping paths for diagonal glare sweeps on cards (using pixelated boundaries) -->
    <clipPath id="leftCardClip">
      <path d="{left_inset_path}" />
    </clipPath>
    <clipPath id="rightCardClip">
      <path d="{right_inset_path}" />
    </clipPath>
    <!-- Soft Vertical Gradient Overlay for stats readability -->
    <linearGradient id="overlayGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d1117" stop-opacity="0.8" />
      <stop offset="55%" stop-color="#0d1117" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0.0" />
    </linearGradient>
    <!-- Liquid Glass Card Background Gradient (Frosted & Translucent) -->
    <linearGradient id="liquidGlassBg" x1="0" y1="0" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08" />
      <stop offset="30%" stop-color="#ffffff" stop-opacity="0.02" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.2" />
    </linearGradient>
    <!-- Stats Card Pixel Highlight: sky blue top-left, dark pixels bottom-right -->
    <linearGradient id="pixelHighlightStats" x1="0" y1="0" x2="1" y2="1">
      <!-- Sky Blue Block 1 (top-left corner) -->
      <stop offset="0%" stop-color="#5fa0fe" />
      <stop offset="5%" stop-color="#5fa0fe" />
      <!-- Gap -->
      <stop offset="5%" stop-color="#5fa0fe" stop-opacity="0" />
      <stop offset="7%" stop-color="#5fa0fe" stop-opacity="0" />
      <!-- Sky Blue Block 2 -->
      <stop offset="7%" stop-color="#5fa0fe" />
      <stop offset="12%" stop-color="#5fa0fe" />
      <!-- Gap -->
      <stop offset="12%" stop-color="#5fa0fe" stop-opacity="0" />
      <stop offset="14%" stop-color="#5fa0fe" stop-opacity="0" />
      <!-- Pink accent pixel -->
      <stop offset="14%" stop-color="#ff34e7" />
      <stop offset="18%" stop-color="#ff34e7" />

      <!-- Long transparent gap (middle of border) -->
      <stop offset="18%" stop-color="#000000" stop-opacity="0" />
      <stop offset="70%" stop-color="#000000" stop-opacity="0" />

      <!-- Dark blue block 1 (bottom-right area) -->
      <stop offset="70%" stop-color="#1e3a5f" />
      <stop offset="76%" stop-color="#1e3a5f" />
      <!-- Gap -->
      <stop offset="76%" stop-color="#1e3a5f" stop-opacity="0" />
      <stop offset="78%" stop-color="#1e3a5f" stop-opacity="0" />
      <!-- Dark navy block 2 -->
      <stop offset="78%" stop-color="#0d1b2a" />
      <stop offset="84%" stop-color="#0d1b2a" />
      <!-- Gap -->
      <stop offset="84%" stop-color="#0d1b2a" stop-opacity="0" />
      <stop offset="86%" stop-color="#0d1b2a" stop-opacity="0" />
      <!-- Dark block 3 -->
      <stop offset="86%" stop-color="#1e3a5f" />
      <stop offset="92%" stop-color="#1e3a5f" />
      <!-- End -->
      <stop offset="92%" stop-color="#000000" stop-opacity="0" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0" />
    </linearGradient>

    <!-- Streak Card Pixel Highlight: similar colors, shifted placement for variety -->
    <linearGradient id="pixelHighlightStreak" x1="0" y1="0" x2="1" y2="1">
      <!-- Pink accent pixel (top-left corner) -->
      <stop offset="0%" stop-color="#ff34e7" />
      <stop offset="4%" stop-color="#ff34e7" />
      <!-- Gap -->
      <stop offset="4%" stop-color="#ff34e7" stop-opacity="0" />
      <stop offset="6%" stop-color="#ff34e7" stop-opacity="0" />
      <!-- Sky Blue Block 1 -->
      <stop offset="6%" stop-color="#5fa0fe" />
      <stop offset="11%" stop-color="#5fa0fe" />
      <!-- Gap -->
      <stop offset="11%" stop-color="#5fa0fe" stop-opacity="0" />
      <stop offset="13%" stop-color="#5fa0fe" stop-opacity="0" />
      <!-- Sky Blue Block 2 -->
      <stop offset="13%" stop-color="#5fa0fe" />
      <stop offset="19%" stop-color="#5fa0fe" />

      <!-- Long transparent gap (middle of border) -->
      <stop offset="19%" stop-color="#000000" stop-opacity="0" />
      <stop offset="68%" stop-color="#000000" stop-opacity="0" />

      <!-- Dark navy block 1 (bottom-right area) -->
      <stop offset="68%" stop-color="#0d1b2a" />
      <stop offset="74%" stop-color="#0d1b2a" />
      <!-- Gap -->
      <stop offset="74%" stop-color="#0d1b2a" stop-opacity="0" />
      <stop offset="76%" stop-color="#0d1b2a" stop-opacity="0" />
      <!-- Dark blue block 2 -->
      <stop offset="76%" stop-color="#1e3a5f" />
      <stop offset="83%" stop-color="#1e3a5f" />
      <!-- Gap -->
      <stop offset="83%" stop-color="#1e3a5f" stop-opacity="0" />
      <stop offset="85%" stop-color="#1e3a5f" stop-opacity="0" />
      <!-- Dark navy block 3 -->
      <stop offset="85%" stop-color="#0d1b2a" />
      <stop offset="90%" stop-color="#0d1b2a" />
      <!-- Gap -->
      <stop offset="90%" stop-color="#0d1b2a" stop-opacity="0" />
      <stop offset="92%" stop-color="#0d1b2a" stop-opacity="0" />
      <!-- Dark block 4 -->
      <stop offset="92%" stop-color="#1e3a5f" />
      <stop offset="96%" stop-color="#1e3a5f" />
      <!-- End -->
      <stop offset="96%" stop-color="#000000" stop-opacity="0" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0" />
    </linearGradient>
    <!-- Left Card Glare Gradient -->
    <linearGradient id="glareGradLeft" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.12" />
      <stop offset="35%" stop-color="#ffffff" stop-opacity="0.03" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0" />
    </linearGradient>
    <!-- Right Card Glare Gradient -->
    <linearGradient id="glareGradRight" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.12" />
      <stop offset="35%" stop-color="#ffffff" stop-opacity="0.03" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0" />
    </linearGradient>
    <!-- Relative bounding box filter for drop shadow -->
    <filter id="glassShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4" />
      <feOffset dx="0" dy="3" />
      <feComponentTransfer><feFuncA type="linear" slope="0.18" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .glass-card-left {{
      fill: url(#liquidGlassBg);
      stroke: #004498;
      stroke-width: 3;
    }}
    .glass-card-right {{
      fill: url(#liquidGlassBg);
      stroke: #004498;
      stroke-width: 3;
    }}
  </style>"""

    # Generate Standard SVG Content (Without Counter)
    svg_standard = f"""<svg width="854" height="480" viewBox="0 0 854 480" fill="none" xmlns="http://www.w3.org/2000/svg">
{defs_and_styles}
  <g clip-path="url(#bannerClip)">
    <!-- 1. Background GIF -->
    <image href="data:image/gif;base64,{encoded_gif}" width="854" height="480" preserveAspectRatio="xMidYMid slice" />
    
    <!-- 2. Dark Overlay Gradient only on the top portion of the GIF -->
    <rect width="854" height="200" fill="url(#overlayGrad)" />

    <!-- 3. Left Card (Actual Github Stats) -->
    <g filter="url(#glassShadow)">
      <!-- Outer dark blue border + glass background -->
      <path d="{left_pixel_path}" class="glass-card-left" />
      <!-- Solid black bezel/frame inside -->
      <path d="{left_pixel_path} {left_inset_path}" fill="#000000" fill-rule="evenodd" />
      <!-- Inner pixelated highlight -->
      <path d="{left_pixel_path}" fill="none" stroke="url(#pixelHighlightStats)" stroke-width="1.5" stroke-linejoin="miter" />
      <!-- Glare sweep -->
      <path d="M15 20 L130 20 L70 164 L15 164 Z" fill="url(#glareGradLeft)" clip-path="url(#leftCardClip)" />
    </g>
    {nested_stats}

    <!-- 4. Right Card (Actual Streak Stats) -->
    <g filter="url(#glassShadow)">
      <!-- Outer dark blue border + glass background -->
      <path d="{right_pixel_path}" class="glass-card-right" />
      <!-- Solid black bezel/frame inside -->
      <path d="{right_pixel_path} {right_inset_path}" fill="#000000" fill-rule="evenodd" />
      <!-- Inner pixelated highlight -->
      <path d="{right_pixel_path}" fill="none" stroke="url(#pixelHighlightStreak)" stroke-width="1.5" stroke-linejoin="miter" />
      <!-- Glare sweep -->
      <path d="M839 {streak_y} L724 {streak_y} L784 {streak_y+144} L839 {streak_y+144} Z" fill="url(#glareGradRight)" clip-path="url(#rightCardClip)" />
    </g>
    {nested_streak}
  </g>
</svg>"""

    # Generate Duplicate SVG Content (With Counter)
    svg_counter = f"""<svg width="854" height="480" viewBox="0 0 854 480" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
{defs_and_styles}
  <g clip-path="url(#bannerClip)">
    <!-- 1. Background GIF -->
    <image href="data:image/gif;base64,{encoded_gif}" width="854" height="480" preserveAspectRatio="xMidYMid slice" />
    
    <!-- 2. Dark Overlay Gradient only on the top portion of the GIF -->
    <rect width="854" height="200" fill="url(#overlayGrad)" />

    <!-- 3. Left Card (Actual Github Stats) -->
    <g filter="url(#glassShadow)">
      <!-- Outer dark blue border + glass background -->
      <path d="{left_pixel_path}" class="glass-card-left" />
      <!-- Solid black bezel/frame inside -->
      <path d="{left_pixel_path} {left_inset_path}" fill="#000000" fill-rule="evenodd" />
      <!-- Inner pixelated highlight -->
      <path d="{left_pixel_path}" fill="none" stroke="url(#pixelHighlightStats)" stroke-width="1.5" stroke-linejoin="miter" />
      <!-- Glare sweep -->
      <path d="M15 20 L130 20 L70 164 L15 164 Z" fill="url(#glareGradLeft)" clip-path="url(#leftCardClip)" />
    </g>
    {nested_stats}

    <!-- 4. Right Card (Actual Streak Stats) -->
    <g filter="url(#glassShadow)">
      <!-- Outer dark blue border + glass background -->
      <path d="{right_pixel_path}" class="glass-card-right" />
      <!-- Solid black bezel/frame inside -->
      <path d="{right_pixel_path} {right_inset_path}" fill="#000000" fill-rule="evenodd" />
      <!-- Inner pixelated highlight -->
      <path d="{right_pixel_path}" fill="none" stroke="url(#pixelHighlightStreak)" stroke-width="1.5" stroke-linejoin="miter" />
      <!-- Glare sweep -->
      <path d="M839 {streak_y} L724 {streak_y} L784 {streak_y+144} L839 {streak_y+144} Z" fill="url(#glareGradRight)" clip-path="url(#rightCardClip)" />
    </g>
    {nested_streak}

    <!-- Profile Views Image (Start-aligned with 2nd character of counter, y=293) -->
    <image href="data:image/png;base64,{encoded_profileviews}" x="591.8" y="274.5" width="150" style="image-rendering: pixelated;" />
    <!-- 5. Profile Visitor Counter (Live image link to update counter on every profile view) -->
    <image href="{url_counter}" x="555" y="312" width="283.5" height="90" />
  </g>
</svg>"""

    # Write output SVG files
    with open(output_path_standard, "w", encoding="utf-8") as f:
        f.write(svg_standard)
    print(f"Successfully compiled standard SVG banner to {output_path_standard}!")

    with open(output_path_counter, "w", encoding="utf-8") as f:
        f.write(svg_counter)
    print(f"Successfully compiled SVG banner with counter to {output_path_counter}!")

if __name__ == "__main__":
    main()
