from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from . import coercions as coercions
from . import elements as elements
from . import operators as operators
from . import roles as roles
from . import type_api as type_api
from .base import NO_ARG as NO_ARG
from .base import SchemaEventTarget as SchemaEventTarget
from .elements import quoted_name as quoted_name
from .elements import Slice as Slice
from .traversals import HasCacheKey as HasCacheKey
from .traversals import InternalTraversal as InternalTraversal
from .type_api import Emulated as Emulated
from .type_api import NativeForEmulated as NativeForEmulated
from .type_api import to_instance as to_instance
from .type_api import TypeDecorator as TypeDecorator
from .type_api import TypeEngine as TypeEngine
from .type_api import Variant as Variant
from .. import event as event
from .. import exc as exc
from .. import inspection as inspection
from .. import processors as processors
from .. import util as util
from ..util import compat as compat
from ..util import langhelpers as langhelpers
from ..util import pickle as pickle

_U = TypeVar("_U")

class _LookupExpressionAdapter:
    class Comparator(TypeEngine.Comparator): ...
    comparator_factory: Any = ...

class Concatenable:
    class Comparator(TypeEngine.Comparator): ...
    comparator_factory: Any = ...

class Indexable:
    class Comparator(TypeEngine.Comparator):
        def __getitem__(self, index: Any): ...
    comparator_factory: Any = ...

class String(Concatenable, TypeEngine[str]):
    __visit_name__: str = ...
    RETURNS_UNICODE: Any = ...
    RETURNS_BYTES: Any = ...
    RETURNS_CONDITIONAL: Any = ...
    RETURNS_UNKNOWN: Any = ...
    length: Any = ...
    collation: Any = ...
    def __init__(
        self,
        length: Optional[Any] = ...,
        collation: Optional[Any] = ...,
        convert_unicode: bool = ...,
        unicode_error: Optional[Any] = ...,
        _warn_on_bytestring: bool = ...,
        _expect_unicode: bool = ...,
    ) -> None: ...
    def literal_processor(self, dialect: Any): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...
    @property
    def python_type(self): ...
    def get_dbapi_type(self, dbapi: Any): ...

class Text(String):
    __visit_name__: str = ...

class Unicode(String):
    __visit_name__: str = ...
    def __init__(self, length: Optional[Any] = ..., **kwargs: Any) -> None: ...

class UnicodeText(Text):
    __visit_name__: str = ...
    def __init__(self, length: Optional[Any] = ..., **kwargs: Any) -> None: ...

class Integer(_LookupExpressionAdapter, TypeEngine[int]):
    __visit_name__: str = ...
    def get_dbapi_type(self, dbapi: Any): ...
    @property
    def python_type(self): ...
    def literal_processor(self, dialect: Any): ...

class SmallInteger(Integer):
    __visit_name__: str = ...

class BigInteger(Integer):
    __visit_name__: str = ...

class Numeric(_LookupExpressionAdapter, TypeEngine[Union[float, Decimal]]):
    __visit_name__: str = ...
    precision: Any = ...
    scale: Any = ...
    decimal_return_scale: Any = ...
    asdecimal: Any = ...
    def __init__(
        self,
        precision: Optional[Any] = ...,
        scale: Optional[Any] = ...,
        decimal_return_scale: Optional[Any] = ...,
        asdecimal: bool = ...,
    ) -> None: ...
    def get_dbapi_type(self, dbapi: Any): ...
    def literal_processor(self, dialect: Any): ...
    @property
    def python_type(self): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...

class Float(Numeric):
    __visit_name__: str = ...
    scale: Any = ...
    precision: Any = ...
    asdecimal: Any = ...
    decimal_return_scale: Any = ...
    def __init__(
        self,
        precision: Optional[Any] = ...,
        asdecimal: bool = ...,
        decimal_return_scale: Optional[Any] = ...,
    ) -> None: ...
    def result_processor(self, dialect: Any, coltype: Any): ...

class DateTime(_LookupExpressionAdapter, TypeEngine[datetime]):
    __visit_name__: str = ...
    timezone: Any = ...
    def __init__(self, timezone: bool = ...) -> None: ...
    def get_dbapi_type(self, dbapi: Any): ...
    @property
    def python_type(self): ...

class Date(_LookupExpressionAdapter, TypeEngine[date]):
    __visit_name__: str = ...
    def get_dbapi_type(self, dbapi: Any): ...
    @property
    def python_type(self): ...

class Time(_LookupExpressionAdapter, TypeEngine[time]):
    __visit_name__: str = ...
    timezone: Any = ...
    def __init__(self, timezone: bool = ...) -> None: ...
    def get_dbapi_type(self, dbapi: Any): ...
    @property
    def python_type(self): ...

class _Binary(TypeEngine[bytes]):
    length: Any = ...
    def __init__(self, length: Optional[Any] = ...) -> None: ...
    def literal_processor(self, dialect: Any): ...
    @property
    def python_type(self): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...
    def coerce_compared_value(self, op: Any, value: Any): ...
    def get_dbapi_type(self, dbapi: Any): ...

class LargeBinary(_Binary):
    __visit_name__: str = ...
    def __init__(self, length: Optional[Any] = ...) -> None: ...

class SchemaType(SchemaEventTarget):
    name: Any = ...
    schema: Any = ...
    metadata: Any = ...
    inherit_schema: Any = ...
    def __init__(
        self,
        name: Optional[Any] = ...,
        schema: Optional[Any] = ...,
        metadata: Optional[Any] = ...,
        inherit_schema: bool = ...,
        quote: Optional[Any] = ...,
        _create_events: bool = ...,
    ) -> None: ...
    def copy(self, **kw: Any): ...
    def adapt(self, __impltype: Type[_U], **kw: Any) -> _U: ...
    @property
    def bind(self): ...
    def create(
        self, bind: Optional[Any] = ..., checkfirst: bool = ...
    ) -> None: ...
    def drop(
        self, bind: Optional[Any] = ..., checkfirst: bool = ...
    ) -> None: ...

class Enum(Emulated, String, SchemaType):
    __visit_name__: str = ...
    def __init__(self, *enums: Any, **kw: Any) -> None: ...
    @property
    def sort_key_function(self): ...
    @property
    def native(self): ...
    class Comparator(String.Comparator): ...
    comparator_factory: Any = ...
    def as_generic(self, allow_nulltype: bool = ...): ...
    def adapt_to_emulated(self, impltype: Any, **kw: Any): ...
    def adapt(self, __impltype: Type[_U], **kw: Any) -> _U: ...
    def literal_processor(self, dialect: Any): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...
    def copy(self, **kw: Any): ...
    @property
    def python_type(self): ...

class PickleType(TypeDecorator[Any]):
    impl: Any = ...
    protocol: Any = ...
    pickler: Any = ...
    comparator: Any = ...
    def __init__(
        self,
        protocol: Any = ...,
        pickler: Optional[Any] = ...,
        comparator: Optional[Any] = ...,
    ) -> None: ...
    def __reduce__(self): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...
    def compare_values(self, x: Any, y: Any): ...

class Boolean(Emulated, TypeEngine[bool], SchemaType):
    __visit_name__: str = ...
    native: bool = ...
    create_constraint: Any = ...
    name: Any = ...
    def __init__(
        self,
        create_constraint: bool = ...,
        name: Optional[Any] = ...,
        _create_events: bool = ...,
    ) -> None: ...
    @property
    def python_type(self): ...
    def literal_processor(self, dialect: Any): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...

class _AbstractInterval(_LookupExpressionAdapter, TypeEngine[Any]):
    def coerce_compared_value(self, op: Any, value: Any): ...

# "comparator_factory" of "_LookupExpressionAdapter" and "TypeDecorator" are incompatible
class Interval(Emulated, _AbstractInterval, TypeDecorator[timedelta]):  # type: ignore[misc]
    impl: Any = ...
    epoch: datetime = ...
    native: bool = ...
    second_precision: Optional[float] = ...
    day_precision: Optional[float] = ...
    def __init__(
        self,
        native: bool = ...,
        second_precision: Optional[float] = ...,
        day_precision: Optional[float] = ...,
    ) -> None: ...
    @property
    def python_type(self) -> Type[timedelta]: ...
    def adapt_to_emulated(self, impltype: Any, **kw: Any): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...

class JSON(Indexable, TypeEngine[Union[str, Mapping, List]]):
    __visit_name__: str = ...
    hashable: bool = ...
    NULL: Any = ...
    none_as_null: bool = ...
    should_evaluate_none: bool = ...
    def __init__(self, none_as_null: bool = ...) -> None: ...
    class JSONElementType(TypeEngine):
        def string_bind_processor(self, dialect: Any): ...
        def string_literal_processor(self, dialect: Any): ...
        def bind_processor(self, dialect: Any): ...
        def literal_processor(self, dialect: Any): ...
    class JSONIndexType(JSONElementType): ...
    class JSONIntIndexType(JSONIndexType): ...
    class JSONStrIndexType(JSONIndexType): ...
    class JSONPathType(JSONElementType): ...
    class Comparator(Indexable.Comparator, Concatenable.Comparator):
        def as_boolean(self): ...
        def as_string(self): ...
        def as_integer(self): ...
        def as_float(self): ...
        def as_numeric(
            self, precision: Any, scale: Any, asdecimal: bool = ...
        ): ...
        def as_json(self): ...
    comparator_factory: Any = ...
    @property
    def python_type(self): ...
    def bind_processor(self, dialect: Any): ...
    def result_processor(self, dialect: Any, coltype: Any): ...

class ARRAY(SchemaEventTarget, Indexable, Concatenable, TypeEngine[List]):
    __visit_name__: str = ...
    zero_indexes: bool = ...
    class Comparator(Indexable.Comparator, Concatenable.Comparator):
        def contains(self, *arg: Any, **kw: Any) -> None: ...
        def any(self, other: Any, operator: Optional[Any] = ...): ...
        def all(self, other: Any, operator: Optional[Any] = ...): ...
    comparator_factory: Any = ...
    item_type: Any = ...
    as_tuple: Any = ...
    dimensions: Any = ...
    def __init__(
        self,
        item_type: Any,
        as_tuple: bool = ...,
        dimensions: Optional[Any] = ...,
        zero_indexes: bool = ...,
    ) -> None: ...
    @property
    def hashable(self): ...
    @property
    def python_type(self): ...
    def compare_values(self, x: Any, y: Any): ...

class TupleType(TypeEngine[TupleType]):
    types: Any = ...
    def __init__(self, *types: Any) -> None: ...
    def result_processor(self, dialect: Any, coltype: Any) -> None: ...

class REAL(Float):
    __visit_name__: str = ...

class FLOAT(Float):
    __visit_name__: str = ...

class NUMERIC(Numeric):
    __visit_name__: str = ...

class DECIMAL(Numeric):
    __visit_name__: str = ...

class INTEGER(Integer):
    __visit_name__: str = ...

INT = INTEGER

class SMALLINT(SmallInteger):
    __visit_name__: str = ...

class BIGINT(BigInteger):
    __visit_name__: str = ...

class TIMESTAMP(DateTime):
    __visit_name__: str = ...
    def __init__(self, timezone: bool = ...) -> None: ...
    def get_dbapi_type(self, dbapi: Any): ...

class DATETIME(DateTime):
    __visit_name__: str = ...

class DATE(Date):
    __visit_name__: str = ...

class TIME(Time):
    __visit_name__: str = ...

class TEXT(Text):
    __visit_name__: str = ...

class CLOB(Text):
    __visit_name__: str = ...

class VARCHAR(String):
    __visit_name__: str = ...

class NVARCHAR(Unicode):
    __visit_name__: str = ...

class CHAR(String):
    __visit_name__: str = ...

class NCHAR(Unicode):
    __visit_name__: str = ...

class BLOB(LargeBinary):
    __visit_name__: str = ...

class BINARY(_Binary):
    __visit_name__: str = ...

class VARBINARY(_Binary):
    __visit_name__: str = ...

class BOOLEAN(Boolean):
    __visit_name__: str = ...

class NullType(TypeEngine[None]):
    __visit_name__: str = ...
    hashable: bool = ...
    def literal_processor(self, dialect: Any): ...
    class Comparator(TypeEngine.Comparator): ...
    comparator_factory: Any = ...

class TableValueType(HasCacheKey, TypeEngine[Any]):
    def __init__(self, *elements: Any) -> None: ...

class MatchType(Boolean): ...

NULLTYPE: Any
BOOLEANTYPE: Any
STRINGTYPE: Any
INTEGERTYPE: Any
MATCHTYPE: Any
TABLEVALUE: Any
