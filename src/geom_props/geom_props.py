import pyproj
from shapely import Polygon, ops


def _validate_polygon(polygon: Polygon) -> bool:
    if polygon.geom_type != 'Polygon':
        raise TypeError(f'Polygon expected, got {polygon.geom_type}')
    if not polygon.is_valid:
        raise ValueError('Invalid polygon')
    if polygon.is_empty:
        raise ValueError('Empty polygon')
    return True


def _convert_polygon_to_meters(polygon: Polygon) -> Polygon:
    _validate_polygon(polygon)
    transformer = pyproj.Transformer.from_proj(
        pyproj.Proj('EPSG:4326'),
        pyproj.Proj('EPSG:5880'),
        always_xy=True
    )
    return ops.transform(transformer.transform, polygon)


def _polygon_area(polygon: Polygon) -> float:
    return _convert_polygon_to_meters(polygon).area


def _polygon_perimeter(polygon: Polygon) -> float:
    return _convert_polygon_to_meters(polygon).boundary.length


def area(polygon: Polygon) -> float:
    return _polygon_area(polygon)


def perimeter(polygon: Polygon) -> float:
    return _polygon_perimeter(polygon)
