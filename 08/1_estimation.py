from typing import List
import weakref
import random
import time
from memory_profiler import profile


class Coordinates:
    def __init__(
            self,
            x: float, y: float, z: float
    ):
        self.x = x
        self.y = y
        self.z = z


class Voxels:
    def __init__(self,
                 coordinates,
                 transparency: float = 1.0
                 ):
        self.coordinates = coordinates
        self.transparency = transparency


class VoxelsSlots:
    __slots__ = ("coordinates", "transparency")

    def __init__(self,
                 coordinates,
                 transparency: float = 1.0
                 ):
        self.coordinates = coordinates
        self.transparency = transparency


class VoxelsWeakRef:
    def __init__(self,
                 coordinates,
                 transparency: float = 1.0
                 ):
        self.coordinates = coordinates
        self.transparency = transparency


@profile()
def create_voxels_sample(cls, params_list: List):
    start = time.time()
    voxels_list = [
        cls(**params_list[i]) for i in range(len(params_list))
    ]
    end = time.time()
    print(
        f"Time for creating {n}-sample of {cls.__name__}: {end-start: .5f}"
    )
    return voxels_list


@profile()
def update_voxels_sample(voxels_list: List):
    start = time.time()
    for voxel in voxels_list:
        voxel.coordinates.x = \
            voxel.coordinates.x ** 2
        voxel.coordinates.y = \
            voxel.coordinates.y ** 2
        voxel.coordinates.z = \
            voxel.coordinates.x + voxel.coordinates.y
        voxel.transparency /= 2
    end = time.time()
    print(
        f"{voxels_list[0].__class__.__name__} "
        f"time for updating {len(voxels_list)}-sample: {end - start: .5f}"
    )


if __name__ == "__main__":
    n = 1_000_000
    params = [{
            "coordinates":
            Coordinates(
                x=random.random(),
                y=random.random(),
                z=random.random()
            )
        } for _ in range(n)
    ]

    weak_params = []
    for param in params:
        weak_params.append(weakref.WeakValueDictionary(param))

    print("Creating:")
    voxels = create_voxels_sample(Voxels, params)
    voxels_slots = create_voxels_sample(VoxelsSlots, params)
    voxels_weakref = create_voxels_sample(VoxelsWeakRef, weak_params)

    print("\nChanging:")
    update_voxels_sample(voxels)
    update_voxels_sample(voxels_slots)
    update_voxels_sample(voxels_weakref)
