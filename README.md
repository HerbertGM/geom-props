# geom-props

## Installation

```console
pip install geom-props
```

## Usage

```python
from shapely import Polygon
from geom_props import area, perimeter

polygon = Polygon([
    [-51.73378826916447, -19.82529005404656],
    [-51.733842668569835, -19.821453938187894],
    [-51.73789902019809, -19.821505344064033],
    [-51.7378447179625, -19.82534147068279],
    [-51.73378826916447, -19.82529005404656]
])

print(f'Area: {area(polygon)} m²')
print(f'Perimeter: {perimeter(polygon)} m')
```