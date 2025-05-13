# compute/processor.py

from core.point import MPoint
from tropisms.field_finder import FieldFinder
from dataclasses import dataclass
from typing import List
from concurrent.futures import ThreadPoolExecutor

@dataclass
class Request:
    point: MPoint
    exclude_ids: List[int] = None  

@dataclass
class Response:
    field: float
    gradient: MPoint

class Processor:
    def __init__(self, field_sources: List[FieldFinder], threads: int = 4):
        self.sources = field_sources
        self.threads = threads

    def process_requests(self, requests: List[Request]) -> List[Response]:
        """Run field & gradient computations for each request point."""
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            results = list(executor.map(self._handle_request, requests))
        return results

    def _handle_request(self, req: Request) -> Response:
        total_field = 0.0
        total_grad = MPoint(0, 0, 0)

        for source in self.sources:
            if req.exclude_ids and source.get_id() in req.exclude_ids:
                continue
            total_field += source.find_field(req.point)
            grad = source.gradient(req.point)
            total_grad.add(grad)

        return Response(field=total_field, gradient=total_grad.normalise())
