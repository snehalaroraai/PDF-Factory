from pathlib import Path
import struct
import zlib

out_dir = Path('icons')
out_dir.mkdir(exist_ok=True)


def write_png(path, size):
    pixels = bytearray()
    for y in range(size):
        pixels.append(0)
        for x in range(size):
            # background
            if x < size // 3 or x > size * 2 // 3:
                r, g, b = 15, 17, 23
            else:
                r, g, b = 108, 99, 255
            # central white panel
            if size // 4 < x < size * 3 // 4 and size // 4 < y < size * 3 // 4:
                r, g, b = 255, 255, 255
            # accent bar for PDF-like shape
            if size // 3 <= x <= size * 2 // 3 and size // 3 <= y <= size * 2 // 3:
                r, g, b = 108, 99, 255
            pixels.extend((r, g, b, 255))

    raw = zlib.compress(bytes(pixels), 9)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')

        def chunk(chunk_type, data):
            f.write(struct.pack('!I', len(data)))
            f.write(chunk_type)
            f.write(data)
            f.write(struct.pack('!I', zlib.crc32(chunk_type + data) & 0xFFFFFFFF))

        chunk(b'IHDR', struct.pack('!IIBBBBB', size, size, 8, 6, 0, 0, 0))
        chunk(b'IDAT', raw)
        chunk(b'IEND', b'')


for size in [180, 192, 512]:
    write_png(out_dir / f'icon-{size}.png', size)
for size in [192, 512]:
    write_png(out_dir / f'icon-{size}-maskable.png', size)

print('generated icons')
