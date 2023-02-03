from typing import Literal

import pyproj
from shapely import GeometryCollection, MultiPolygon, Polygon, ops


def _validate_geometry(geometry: Polygon | MultiPolygon | GeometryCollection, type: str) -> bool:
    if geometry.geom_type != type:
        raise TypeError(f'{type} expected, got {geometry.geom_type}')
    if not geometry.is_valid:
        raise ValueError('Invalid geometry')
    if geometry.is_empty:
        raise ValueError('Empty geometry')
    return True


def _convert_polygon_to_meters(polygon: Polygon) -> Polygon:
    _validate_geometry(polygon, 'Polygon')
    transformer = pyproj.Transformer.from_proj(
        pyproj.Proj('EPSG:4326'),
        pyproj.Proj('EPSG:5880'),
        always_xy=True
    )
    return ops.transform(transformer.transform, polygon)


def _polygon_calc(polygon: Polygon | MultiPolygon, func: Literal['area', 'perimeter']) -> float:
    if polygon.geom_type == 'Polygon':
        if func == 'area':
            return _convert_polygon_to_meters(polygon).area
        elif func == 'perimeter':
            return _convert_polygon_to_meters(polygon).boundary.length
    elif polygon.geom_type == 'MultiPolygon':
        _validate_geometry(polygon, 'MultiPolygon')
        if func == 'area':
            return sum(_convert_polygon_to_meters(i).area for i in polygon.geoms)
        elif func == 'perimeter':
            return sum(_convert_polygon_to_meters(i).boundary.length for i in polygon.geoms)
    else:
        raise TypeError(f'Polygon or MultiPolygon expected, got {polygon.geom_type}')


def _geometry_calc(geometry: Polygon | MultiPolygon | GeometryCollection, func: Literal['area', 'perimeter']) -> float:
    if geometry.geom_type in ['Polygon', 'MultiPolygon']:
        return _polygon_calc(geometry, func)
    elif geometry.geom_type == 'GeometryCollection':
        _validate_geometry(geometry, 'GeometryCollection')
        value = sum(_polygon_calc(i, func) for i in geometry.geoms if i.geom_type in ['Polygon', 'MultiPolygon'])
        if value > 0:
            return value
        else:
            raise ValueError('No polygons found in GeometryCollection')
    else:
        raise TypeError(f'Polygon, MultiPolygon or GeometryCollection expected, got {geometry.geom_type}')


def area(geometry: Polygon | MultiPolygon | GeometryCollection) -> float:
    return _geometry_calc(geometry, 'area')


def perimeter(geometry: Polygon | MultiPolygon | GeometryCollection) -> float:
    return _geometry_calc(geometry, 'perimeter')
