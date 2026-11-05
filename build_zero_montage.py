"""Compose a regular task wall, revealing it by zooming out from one task."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'open-humanscale'
ASSETS = ROOT / 'dist' / 'assets'
clips = json.loads((SOURCE / 'assets/zero-shot-gallery.json').read_text())['clips']
assert len(clips) == 21
# The two-drinks examples repeat the same task. Retain example 1 only.
excluded = 'zero-two-drinks-2'
hero = next(c for c in clips if c['id'] == 'zero-two-drinks-1')
ordered = [c for c in clips if c['id'] != excluded and c != hero]
ordered.insert(7, hero)  # Near the centre: column 3, row 2.
assert len(ordered) == 20
positions = [(x * 640, y * 360) for y in range(4) for x in range(5)]
duration = 56
command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y']
filters = []
for i, clip in enumerate(ordered):
    source = SOURCE / clip['src']
    assert source.is_file(), source
    command += ['-stream_loop', '-1', '-threads', '1', '-i', str(source)]
    width, height = 640, 360
    filters.append(
        f'[{i}:v]setpts=PTS-STARTPTS,fps=24,'
        f'scale={width-6}:{height-6}:force_original_aspect_ratio=decrease,'
        f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x14251f,'
        f'setsar=1,trim=duration={duration}[v{i}]'
    )
filters.append(''.join(f'[v{i}]' for i in range(20)) +
               'xstack=inputs=20:layout=' + '|'.join(f'{x}_{y}' for x,y in positions) +
               ',pad=3200:1800:0:180:color=0x14251f[wall]')
# Hold one task for 4 seconds, then smoothly reveal the wall over 6 seconds.
# x/y keep the opening panel in view, moving continuously to the full canvas.
progress = '((on-96)/144)'
zoom = f'if(lt(on,96),5,if(lt(on,240),5-4*{progress}*{progress}*(3-2*{progress}),1))'
filters.append(f"[wall]zoompan=z='{zoom}':x='(iw-iw/zoom)*0.5':"
               "y='(ih-ih/zoom)*0.375':d=1:s=1920x1080:fps=24[out]")
output = ASSETS / 'zero-shot-tasks-zoom.mp4'
command += ['-filter_complex_threads', '2', '-filter_complex', ';'.join(filters),
            '-map', '[out]', '-an', '-t', str(duration), '-c:v', 'libx264',
            '-threads', '4', '-preset', 'fast', '-crf', '24', '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart', str(output)]
subprocess.run(command, check=True)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                '-ss', '0', '-i', str(output), '-frames:v', '1', '-q:v', '2',
                str(ASSETS / 'zero-shot-tasks-zoom.jpg')], check=True)
manifest = {
    'source_project': 'https://jiankai-ss.github.io/open-humanscale/',
    'description': '20 source recordings in a 5 by 4 grid. Starts on a single task; smooth zoom-out from 4s to 10s reveals the full grid. Independent loops at source playback speed. No audio.',
    'excluded_duplicate': excluded,
    'duration_seconds': duration, 'dimensions': [1920, 1080],
    'output': output.name, 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
    'panels': [{'id': c['id'], 'source': c['src'], 'position': positions[i],
                'source_sha256': hashlib.sha256((SOURCE / c['src']).read_bytes()).hexdigest()}
               for i,c in enumerate(ordered)]
}
(ROOT / 'zero-montage-sources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
print(f'Created {output.name}: {output.stat().st_size/1024/1024:.1f} MB, 20 panels, {duration}s')
