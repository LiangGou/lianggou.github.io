"""Model-authored, asset-free rendering arm of a paired generation experiment.

The full coding brief was recorded before authoring in
coding_image_comparison_prompts.json. No image model is used in this program.
Run the base image, the blue-material edit, and the opposite-camera edit:
    python coding_image_comparison.py --variant all
Dependencies: NumPy; all other imports are Python standard library.
"""
import argparse
import json
import math
import struct
import time
import zlib
from pathlib import Path

import numpy as np

WIDTH, HEIGHT = 640, 420
SAMPLES, BOUNCES, SEED = 144, 9, 20261003
EPSILON = 1e-4
SPHERES = [
    (np.array([-1.35, 0.0, 0.0]), 1.0, 1),
    (np.array([1.10, 0.0, 0.15]), 1.0, 2),
    (np.array([0.15, -0.48, -2.0]), 0.52, 3),
]
LIGHT_MIN = np.array([-3.5, 6.0, -1.0])
LIGHT_MAX = np.array([0.5, 6.0, 3.0])
LIGHT_AREA = 16.0
LIGHT_RADIANCE = np.array([15.0, 13.6, 11.6])
TARGET = np.array([0.0, -0.03, -0.25])
VARIANTS = {
    'base': {'camera': [6.0, 3.0, 8.0], 'small_albedo': [0.56, 0.13, 0.055]},
    'blue': {'camera': [6.0, 3.0, 8.0], 'small_albedo': [0.035, 0.15, 0.65]},
    'camera': {'camera': [-6.0, 3.0, 8.0], 'small_albedo': [0.035, 0.15, 0.65]},
}


def unit(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-12)


def hit(origin, direction):
    count = len(origin)
    distance = np.full(count, np.inf)
    material = np.full(count, -1, dtype=np.int8)
    normal = np.zeros((count, 3))
    for center, radius, identifier in SPHERES:
        offset = origin - center
        projection = np.sum(offset * direction, axis=1)
        discriminant = projection**2 - np.sum(offset**2, axis=1) + radius**2
        root = np.sqrt(np.maximum(discriminant, 0))
        near, far = -projection-root, -projection+root
        candidate = np.where(near > EPSILON, near, far)
        select = (discriminant >= 0) & (candidate > EPSILON) & (candidate < distance)
        distance[select] = candidate[select]
        material[select] = identifier
        normal[select] = (origin[select] + candidate[select, None]*direction[select] - center)/radius
    vertical = direction[:, 1]
    divisor = np.where(np.abs(vertical) > 1e-10, vertical, 1e-10)
    candidate = (-1-origin[:, 1])/divisor
    select = (np.abs(vertical) > 1e-10) & (candidate > EPSILON) & (candidate < distance)
    distance[select], material[select], normal[select] = candidate[select], 0, [0, 1, 0]
    candidate = (6-origin[:, 1])/divisor
    point = origin + candidate[:, None]*direction
    select = (np.abs(vertical) > 1e-10) & (candidate > EPSILON) & (candidate < distance)
    select &= (point[:, 0] > LIGHT_MIN[0]) & (point[:, 0] < LIGHT_MAX[0])
    select &= (point[:, 2] > LIGHT_MIN[2]) & (point[:, 2] < LIGHT_MAX[2])
    distance[select], material[select], normal[select] = candidate[select], 4, [0, -1, 0]
    return distance, material, normal


def environment(direction):
    blend = np.clip((direction[:, 1]+1)/2, 0, 1)[:, None]
    return (1-blend)*[0.25, 0.28, 0.32] + blend*[0.54, 0.64, 0.78]


def diffuse_direction(normal, rng):
    u, v = rng.random((2, len(normal)))
    helper = np.tile([0.0, 1.0, 0.0], (len(normal), 1))
    helper[np.abs(normal[:, 1]) > 0.9] = [1, 0, 0]
    tangent = unit(np.cross(helper, normal))
    bitangent = np.cross(normal, tangent)
    return (tangent*(np.sqrt(u)*np.cos(2*math.pi*v))[:, None]
            + bitangent*(np.sqrt(u)*np.sin(2*math.pi*v))[:, None]
            + normal*np.sqrt(1-u)[:, None])


def trace(origin, direction, rng, small_albedo):
    accumulated = np.zeros_like(origin)
    indices = np.arange(len(origin))
    weight = np.ones_like(origin)
    specular_previous = np.ones(len(origin), dtype=bool)
    for bounce in range(BOUNCES):
        distance, material, outward = hit(origin, direction)
        escaped = material == -1
        accumulated[indices[escaped]] += weight[escaped]*environment(direction[escaped])
        on_light = material == 4
        emission = on_light & specular_previous & (direction[:, 1] > 0)
        accumulated[indices[emission]] += weight[emission]*LIGHT_RADIANCE
        keep = ~(escaped | on_light)
        if not np.any(keep):
            break
        indices, weight, origin, direction = indices[keep], weight[keep], origin[keep], direction[keep]
        distance, material, outward = distance[keep], material[keep], outward[keep]
        point = origin + distance[:, None]*direction
        entering = np.sum(direction*outward, axis=1) < 0
        normal = np.where(entering[:, None], outward, -outward)
        outgoing = np.zeros_like(direction)
        specular_previous = np.ones(len(point), dtype=bool)
        matte = (material == 0) | (material == 3)
        if np.any(matte):
            p, n = point[matte], normal[matte]
            albedo = np.tile(small_albedo, (len(p), 1))
            floor = material[matte] == 0
            checker = ((np.floor(p[:, 0]/1.1)+np.floor(p[:, 2]/1.1)) % 2) == 0
            albedo[floor] = np.where(checker[floor, None], [0.57, 0.55, 0.50], [0.26, 0.29, 0.31])
            light_point = np.column_stack((rng.uniform(-3.5, 0.5, len(p)), np.full(len(p), 6), rng.uniform(-1, 3, len(p))))
            displacement = light_point-p
            length = np.linalg.norm(displacement, axis=1)
            light_direction = displacement/length[:, None]
            blocker, _, _ = hit(p+EPSILON*n, light_direction)
            visible = blocker >= length-0.002
            cosine = np.maximum(np.sum(n*light_direction, axis=1), 0)
            geometry = cosine*np.maximum(light_direction[:, 1], 0)*LIGHT_AREA/(math.pi*length**2)
            accumulated[indices[matte]] += weight[matte]*albedo*LIGHT_RADIANCE*(geometry*visible)[:, None]
            weight[matte] *= albedo
            outgoing[matte] = diffuse_direction(n, rng)
            specular_previous[matte] = False
        metal = material == 1
        if np.any(metal):
            d, n = direction[metal], normal[metal]
            reflection = d-2*np.sum(d*n, axis=1)[:, None]*n
            candidate = unit(reflection+0.025*unit(rng.normal(size=reflection.shape)))
            invalid = np.sum(candidate*n, axis=1) <= 0
            candidate[invalid] = reflection[invalid]
            outgoing[metal] = candidate
            weight[metal] *= [0.93, 0.94, 0.96]
        glass = material == 2
        if np.any(glass):
            d, n, entry = direction[glass], normal[glass], entering[glass]
            eta = np.where(entry, 1/1.5, 1.5)
            cosine = np.clip(-np.sum(d*n, axis=1), 0, 1)
            transmitted_squared = 1-eta**2*(1-cosine**2)
            fresnel = 0.04+0.96*(1-cosine)**5
            reflected = (transmitted_squared < 0) | (rng.random(len(d)) < fresnel)
            reflection = d+2*cosine[:, None]*n
            refraction = eta[:, None]*d+(eta*cosine-np.sqrt(np.maximum(transmitted_squared, 0)))[:, None]*n
            outgoing[glass] = np.where(reflected[:, None], reflection, refraction)
            absorption = np.exp(-distance[glass, None]*np.array([0.09, 0.025, 0.014]))
            weight[glass] *= np.where(entry[:, None], 1.0, absorption)
        direction = unit(outgoing)
        origin = point+EPSILON*direction
        if bounce >= 3:
            probability = np.clip(np.max(weight, axis=1), 0.08, 0.95)
            survive = rng.random(len(indices)) < probability
            indices = indices[survive]
            weight = weight[survive]/probability[survive, None]
            origin, direction, specular_previous = origin[survive], direction[survive], specular_previous[survive]
            if len(indices) == 0:
                break
    return accumulated


def write_png(path, pixels):
    height, width, _ = pixels.shape
    def chunk(kind, data):
        return struct.pack('!I', len(data))+kind+data+struct.pack('!I', zlib.crc32(kind+data)&0xffffffff)
    filtered = b''.join(b'\x00'+row.tobytes() for row in pixels)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('!2I5B', width, height, 8, 2, 0, 0, 0))
                     +chunk(b'IDAT', zlib.compress(filtered, 7))+chunk(b'IEND', b''))


def render(name):
    start = time.perf_counter()
    settings = VARIANTS[name]
    rng = np.random.default_rng(SEED)
    camera = np.array(settings['camera'])
    forward = unit(TARGET-camera)
    right = unit(np.cross(forward, [0, 1, 0]))
    up = np.cross(right, forward)
    x, y = np.meshgrid(np.arange(WIDTH), np.arange(HEIGHT))
    origins = np.tile(camera, (WIDTH*HEIGHT, 1))
    radiance = np.zeros_like(origins)
    scale = math.tan(math.radians(37)/2)
    for sample in range(SAMPLES):
        sx = (2*(x.ravel()+rng.random(WIDTH*HEIGHT))/WIDTH-1)*WIDTH/HEIGHT*scale
        sy = (1-2*(y.ravel()+rng.random(WIDTH*HEIGHT))/HEIGHT)*scale
        ray = unit(forward+sx[:, None]*right+sy[:, None]*up)
        radiance += trace(origins.copy(), ray, rng, np.array(settings['small_albedo']))
    radiance = radiance.reshape(HEIGHT, WIDTH, 3)/SAMPLES*0.95
    display = np.clip((radiance*(2.51*radiance+0.03))/(radiance*(2.43*radiance+0.59)+0.14), 0, 1)
    display = np.where(display <= 0.0031308, 12.92*display, 1.055*display**(1/2.4)-0.055)
    path = Path(__file__).with_name('comparison_code_'+name+'.png')
    write_png(path, np.rint(display*255).astype(np.uint8))
    seconds = time.perf_counter()-start
    record = {'variant': name, 'output': str(path), 'width': WIDTH, 'height': HEIGHT,
              'samples_per_pixel': SAMPLES, 'max_bounces': BOUNCES, 'seed': SEED,
              'render_seconds': seconds, **settings}
    print(json.dumps(record), flush=True)
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', choices=['all', *VARIANTS], default='all')
    args = parser.parse_args()
    names = list(VARIANTS) if args.variant == 'all' else [args.variant]
    records = [render(name) for name in names]
    Path(__file__).with_name('coding_image_comparison_render_log.json').write_text(json.dumps(records, indent=2)+'\n')
