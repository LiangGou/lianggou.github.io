"""A reproducible, asset-free CPU rendering experiment.

All geometry, materials, lights and camera are defined below.  The image is
computed by ray intersections, Monte Carlo light transport, reflection and
refraction.  There is no image-generation model or external image/texture.

Run: python coding_render_probe.py
Dependency: numpy. PNG serialization uses only the Python standard library.
This is a small simplified renderer, not a claim to solve arbitrary imagery.
"""
import math
import struct
import time
import zlib
from pathlib import Path

import numpy as np

WIDTH, HEIGHT, SAMPLES, BOUNCES = 640, 420, 144, 9
OUTPUT = Path(__file__).with_suffix('.png')
EPS = 1e-4
RNG = np.random.default_rng(20261002)
SPHERES = [
    (np.array([-1.35, 0.0, 0.0]), 1.0, 1),  # slightly rough chrome
    (np.array([1.10, 0.0, 0.15]), 1.0, 2),  # solid glass, IOR 1.5
    (np.array([0.15, -0.48, -2.0]), 0.52, 3),  # terracotta matte
]
LIGHT_Y, LIGHT_X0, LIGHT_X1, LIGHT_Z0, LIGHT_Z1 = 6.0, -3.5, 0.5, -1.0, 3.0
LIGHT_AREA = (LIGHT_X1 - LIGHT_X0) * (LIGHT_Z1 - LIGHT_Z0)
LIGHT_COLOR = np.array([15.0, 13.6, 11.6])


def normalize(x):
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)


def intersect(origins, directions):
    """Closest exact ray/sphere, ray/ground or ray/rectangular-light hit."""
    n = len(origins)
    distance = np.full(n, np.inf)
    material = np.full(n, -1, dtype=np.int8)
    normal = np.zeros((n, 3))
    for center, radius, mat in SPHERES:
        offset = origins - center
        b = np.sum(offset * directions, axis=1)
        c = np.sum(offset * offset, axis=1) - radius * radius
        disc = b * b - c
        root = np.sqrt(np.maximum(disc, 0.0))
        near, far = -b - root, -b + root
        t = np.where(near > EPS, near, far)
        valid = (disc >= 0) & (t > EPS) & (t < distance)
        distance[valid] = t[valid]
        material[valid] = mat
        normal[valid] = (origins[valid] + directions[valid] * t[valid, None] - center) / radius
    dy = directions[:, 1]
    safe_dy = np.where(np.abs(dy) > 1e-10, dy, 1e-10)
    t = (-1.0 - origins[:, 1]) / safe_dy
    valid = (np.abs(dy) > 1e-10) & (t > EPS) & (t < distance)
    distance[valid], material[valid] = t[valid], 0
    normal[valid] = [0.0, 1.0, 0.0]
    t = (LIGHT_Y - origins[:, 1]) / safe_dy
    p = origins + directions * t[:, None]
    valid = (np.abs(dy) > 1e-10) & (t > EPS) & (t < distance)
    valid &= (p[:, 0] > LIGHT_X0) & (p[:, 0] < LIGHT_X1)
    valid &= (p[:, 2] > LIGHT_Z0) & (p[:, 2] < LIGHT_Z1)
    distance[valid], material[valid] = t[valid], 4
    normal[valid] = [0.0, -1.0, 0.0]
    return distance, material, normal


def sky(directions):
    t = np.clip(0.5 * (directions[:, 1] + 1), 0, 1)[:, None]
    return (1-t) * np.array([0.25, 0.28, 0.32]) + t * np.array([0.54, 0.64, 0.78])


def cosine_hemisphere(normal):
    u, v = RNG.random((2, len(normal)))
    r = np.sqrt(u)
    angle = 2 * math.pi * v
    helper = np.zeros_like(normal)
    helper[:, 1] = 1.0
    helper[np.abs(normal[:, 1]) > 0.9] = [1.0, 0.0, 0.0]
    tangent = normalize(np.cross(helper, normal))
    bitangent = np.cross(normal, tangent)
    return (tangent * (r * np.cos(angle))[:, None]
            + bitangent * (r * np.sin(angle))[:, None]
            + normal * np.sqrt(1-u)[:, None])


def trace(origins, directions):
    count = len(origins)
    result = np.zeros((count, 3))
    active = np.arange(count)
    throughput = np.ones((count, 3))
    previous_specular = np.ones(count, dtype=bool)
    for bounce in range(BOUNCES):
        distance, material, outward = intersect(origins, directions)
        miss = material == -1
        result[active[miss]] += throughput[miss] * sky(directions[miss])
        emissive = material == 4
        emission = emissive & previous_specular & (directions[:, 1] > 0)
        result[active[emission]] += throughput[emission] * LIGHT_COLOR
        keep = ~(miss | emissive)
        if not np.any(keep):
            break
        active, throughput = active[keep], throughput[keep]
        directions, origins = directions[keep], origins[keep]
        outward, distance, material = outward[keep], distance[keep], material[keep]
        point = origins + directions * distance[:, None]
        front = np.sum(directions * outward, axis=1) < 0
        normal = np.where(front[:, None], outward, -outward)
        next_directions = np.zeros_like(directions)
        next_specular = np.ones(len(point), dtype=bool)

        diffuse = (material == 0) | (material == 3)
        if np.any(diffuse):
            p, norm = point[diffuse], normal[diffuse]
            albedo = np.tile([0.56, 0.13, 0.055], (len(p), 1))
            ground = material[diffuse] == 0
            # A mathematical checker, not an image texture.
            check = ((np.floor(p[:, 0] / 1.1) + np.floor(p[:, 2] / 1.1)) % 2) == 0
            light_tile, dark_tile = np.array([0.57, 0.55, 0.50]), np.array([0.26, 0.29, 0.31])
            albedo[ground] = np.where(check[ground, None], light_tile, dark_tile)
            target = np.column_stack((RNG.uniform(LIGHT_X0, LIGHT_X1, len(p)),
                                      np.full(len(p), LIGHT_Y),
                                      RNG.uniform(LIGHT_Z0, LIGHT_Z1, len(p))))
            offset = target - p
            distance_light = np.linalg.norm(offset, axis=1)
            toward_light = offset / distance_light[:, None]
            cos_surface = np.maximum(np.sum(norm * toward_light, axis=1), 0)
            cos_light = np.maximum(toward_light[:, 1], 0)
            blocker_distance, _, _ = intersect(p + EPS * norm, toward_light)
            visible = blocker_distance >= distance_light - 0.002
            factor = cos_surface * cos_light * LIGHT_AREA / (math.pi * distance_light**2)
            direct = albedo * LIGHT_COLOR * (factor * visible)[:, None]
            result[active[diffuse]] += throughput[diffuse] * direct
            throughput[diffuse] *= albedo
            next_directions[diffuse] = cosine_hemisphere(norm)
            next_specular[diffuse] = False

        metal = material == 1
        if np.any(metal):
            d, nrm = directions[metal], normal[metal]
            reflected = d - 2 * np.sum(d*nrm, axis=1)[:, None] * nrm
            perturbation = normalize(RNG.normal(size=reflected.shape))
            candidate = normalize(reflected + 0.025 * perturbation)
            bad = np.sum(candidate*nrm, axis=1) <= 0
            candidate[bad] = reflected[bad]
            next_directions[metal] = candidate
            throughput[metal] *= [0.93, 0.94, 0.96]

        glass = material == 2
        if np.any(glass):
            d, nrm, entry = directions[glass], normal[glass], front[glass]
            eta = np.where(entry, 1/1.5, 1.5)
            cosine = np.clip(-np.sum(d * nrm, axis=1), 0, 1)
            k = 1 - eta**2 * (1-cosine**2)
            fresnel = 0.04 + 0.96 * (1-cosine)**5
            reflect = (k < 0) | (RNG.random(len(d)) < fresnel)
            reflected = d + 2 * cosine[:, None] * nrm
            refracted = eta[:, None]*d + (eta*cosine-np.sqrt(np.maximum(k, 0)))[:, None]*nrm
            next_directions[glass] = np.where(reflect[:, None], reflected, refracted)
            # Beer-Lambert absorption only for the segment traveled inside glass.
            attenuation = np.exp(-distance[glass, None] * np.array([0.09, 0.025, 0.014]))
            throughput[glass] *= np.where(entry[:, None], 1.0, attenuation)

        directions = normalize(next_directions)
        origins = point + directions * EPS
        previous_specular = next_specular
        if bounce >= 3:
            probability = np.clip(np.max(throughput, axis=1), 0.08, 0.95)
            survive = RNG.random(len(active)) < probability
            active, throughput = active[survive], throughput[survive] / probability[survive, None]
            directions, origins = directions[survive], origins[survive]
            previous_specular = previous_specular[survive]
            if len(active) == 0:
                break
    return result


def png_write(path, image):
    height, width, _ = image.shape
    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind+data)&0xffffffff)
    raw = b''.join(b'\x00' + image[y].tobytes() for y in range(height))
    data = b'\x89PNG\r\n\x1a\n'
    data += chunk(b'IHDR', struct.pack('!2I5B', width, height, 8, 2, 0, 0, 0))
    data += chunk(b'IDAT', zlib.compress(raw, 7)) + chunk(b'IEND', b'')
    path.write_bytes(data)


def main():
    start = time.perf_counter()
    camera = np.array([6.0, 3.0, 8.0])
    target = np.array([0.0, -0.03, -0.25])
    forward = normalize(target-camera)
    right = normalize(np.cross(forward, [0, 1, 0]))
    up = np.cross(right, forward)
    x, y = np.meshgrid(np.arange(WIDTH), np.arange(HEIGHT))
    origins = np.tile(camera, (WIDTH*HEIGHT, 1))
    film = np.zeros((WIDTH*HEIGHT, 3))
    tan_half_fov = math.tan(math.radians(37) / 2)
    for sample in range(SAMPLES):
        sx = (2*(x.ravel()+RNG.random(WIDTH*HEIGHT))/WIDTH-1) * WIDTH/HEIGHT * tan_half_fov
        sy = (1-2*(y.ravel()+RNG.random(WIDTH*HEIGHT))/HEIGHT) * tan_half_fov
        direction = normalize(forward + sx[:, None]*right + sy[:, None]*up)
        film += trace(origins.copy(), direction)
        if (sample+1) % 8 == 0:
            print(f'{sample+1}/{SAMPLES} samples, {time.perf_counter()-start:.1f}s', flush=True)
    film = film.reshape(HEIGHT, WIDTH, 3) / SAMPLES
    # Standard ACES-style display tone mapping, followed by sRGB transfer.
    film *= 0.95
    film = np.clip((film*(2.51*film+0.03))/(film*(2.43*film+0.59)+0.14), 0, 1)
    film = np.where(film <= 0.0031308, 12.92*film, 1.055*film**(1/2.4)-0.055)
    png_write(OUTPUT, np.rint(np.clip(film, 0, 1)*255).astype(np.uint8))
    print(f'Wrote {OUTPUT} ({WIDTH} x {HEIGHT}); elapsed {time.perf_counter()-start:.1f}s')


if __name__ == '__main__':
    main()
